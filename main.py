import os
import threading
import yt_dlp
import vlc
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
import queue
from tkinter import messagebox
from kivy.lang import Builder

# === Globals ===
cache_dir = "cache"
favorites_file = "favorites.txt"

# === Ensure cache directory exists ===
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

class MusicPlayerApp(App):
    # Kivy Properties for UI state
    is_playing = BooleanProperty(False)
    current_index = NumericProperty(-1)
    song_title = StringProperty("No song playing")
    time_progress = NumericProperty(0)
    time_label = StringProperty("0:00 / 0:00")
    
    # Store other data
    playlist = []
    favorites = set()
    player = None
    shuffle_mode = False
    repeat_mode = False
    song_end_queue = queue.Queue()

    def build(self):
        # The KV file will be loaded automatically if named correctly
        # The root widget is returned here, and `self.root` is assigned.
        # Do not call load_cached_songs() here.
        return MusicPlayerRoot()

    def on_start(self):
        # This method is called after the main UI has been built.
        self.load_favorites()
        self.load_cached_songs()
        Clock.schedule_interval(self.check_queue, 0.5)
        Clock.schedule_interval(self.update_progress, 1)

    def load_favorites(self):
        if os.path.exists(favorites_file):
            with open(favorites_file, "r", encoding="utf-8") as f:
                for line in f:
                    self.favorites.add(line.strip())
                    
    # ... (the rest of your methods like load_favorites, load_cached_songs, etc. are correct) ...
    def load_cached_songs(self):
        self.playlist.clear()

        view_data = []
        for i, file in enumerate(os.listdir(cache_dir)):
            if file.endswith((".m4a", ".mp3")):
                path = os.path.join(cache_dir, file)
                title = os.path.splitext(file)[0]
                self.playlist.append((path, title))
                view_data.append({'text': title, 'index': i}) # Add the index here

        self.root.ids.playlist_view.data = view_data
                
    def download_audio(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
            'outtmpl': f'{cache_dir}/%(title).80s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                original_path = ydl.prepare_filename(info)
                filepath = os.path.splitext(original_path)[0] + '.mp3'
                title = info.get('title', 'Unknown Title')
                return filepath, title
        except Exception as e:
            messagebox.showerror("Download Error", f"An error occurred during download: {e}")
            return None, None

    def on_download(self, query):
        if not query:
            return

        self.song_title = "Downloading..."

        def worker():
            filepath, title = self.download_audio(query)
            if filepath and title:
                self.load_cached_songs()
                self.song_title = "✅ Download complete. Reloaded playlist."
            else:
                self.song_title = "❌ Download failed."
        
        threading.Thread(target=worker).start()

    def on_media_end(self, event):
        self.song_end_queue.put("Song ended")
        
    def check_queue(self, dt):
        try:
            if self.song_end_queue.get(block=False) == "Song ended":
                self.next_song()
        except queue.Empty:
            pass
            
    def on_song_press(self, index):
        self.play_song(index)

    def play_song(self, index):
        if not self.playlist or not 0 <= index < len(self.playlist):
            self.song_title = "Select a song to play"
            return

        self.current_index = index
        filepath, title = self.playlist[int(self.current_index)]
        self.song_title = f"🎵 Now Playing: {title}"

        if self.player:
            self.player.stop()

        filepath = os.path.abspath(filepath)
        if os.name == 'nt':
            filepath = filepath.replace('\\', '/')
            filepath = f"file:///{filepath}"

        instance = vlc.Instance('--no-video')
        self.player = instance.media_player_new()
        media = instance.media_new(filepath)
        self.player.set_media(media)
        self.player.play()

        self.is_playing = True
        
        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_media_end)

    def pause_song(self):
        if self.player:
            self.player.pause()
            self.is_playing = False

    def resume_song(self):
        if self.player:
            self.player.play()
            self.is_playing = True

    def next_song(self):
        if not self.playlist:
            return
        
        if self.shuffle_mode and len(self.playlist) > 1:
            next_index = random.choice([i for i in range(len(self.playlist)) if i != self.current_index])
        else:
            next_index = (self.current_index + 1) % len(self.playlist)
        
        self.play_song(next_index)

    def previous_song(self):
        if not self.playlist:
            return
        
        if self.shuffle_mode and len(self.playlist) > 1:
            prev_index = random.choice([i for i in range(len(self.playlist)) if i != self.current_index])
        else:
            prev_index = (self.current_index - 1 + len(self.playlist)) % len(self.playlist)
        
        self.play_song(prev_index)

    def change_volume(self, value):
        if self.player:
            self.player.audio_set_volume(int(value))

    def seek_song(self, value):
        if self.player:
            length = self.player.get_length()
            new_time = (value / 100) * length
            self.player.set_time(int(new_time))
    
    def update_progress(self, dt):
        if self.player and self.player.get_media() and self.player.is_playing():
            try:
                length = self.player.get_length()
                pos = self.player.get_time()
                if length > 0:
                    self.time_progress = (pos / length) * 100
                    mins_total, secs_total = divmod(length // 1000, 60)
                    mins_pos, secs_pos = divmod(pos // 1000, 60)
                    self.time_label = f"{mins_pos:02}:{secs_pos:02} / {mins_total:02}:{secs_total:02}"
            except Exception:
                self.time_progress = 0
                self.time_label = "00:00 / 00:00"

    def remove_song(self):
        pass

    def toggle_favorite(self):
        pass
    
class MusicPlayerRoot(FloatLayout):
    pass

if __name__ == '__main__':
    MusicPlayerApp().run()