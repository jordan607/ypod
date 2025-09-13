# ypod - Music Player App

A simple, modern music player built with Kivy. Search, download, and play songs from YouTube, manage playlists, and mark favorites—all in one app!

---

## Features

- **Search & Download:** Search for songs (YouTube) and download audio with a single click.
- **Play Local Files:** Play downloaded `.mp3` and `.m4a` files from the built-in cache.
- **Playlist Management:** View and scroll through your playlist. Tap to play any song.
- **Playback Controls:** Play, pause, resume, skip next/previous, and seek within songs.
- **Volume Control:** Adjust playback volume with a slider.
- **Favorites:** Mark/unmark songs as favorites (future feature).
- **Remove Songs:** Remove songs from your playlist (future feature).
- **Shuffle & Repeat:** Shuffle and repeat modes (future feature).
- **Progress Display:** See current and total song time, and seek using the progress bar.
- **Android Support:** Ready for packaging with Buildozer for Android devices.

---

## Requirements

- **Python 3.7+**
- [Kivy](https://kivy.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [python-vlc](https://pypi.org/project/python-vlc/)
- [ffmpeg](https://ffmpeg.org/) (must be installed and in your PATH)
- (Optional) [Tkinter](https://wiki.python.org/moin/TkInter) for error dialogs

---

## Installation

1. **Clone this repository:**
    ```sh
    git clone <your-repo-url>
    cd <your-project-folder>
    ```

2. **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install kivy yt-dlp python-vlc
    ```

    - Make sure `ffmpeg` is installed and available in your system PATH.

4. **Run the app:**
    ```sh
    python main.py
    ```

---

## File Structure

- [main.py](http://_vscodecontentref_/0) — Main application logic
- [musicplayer.kv](http://_vscodecontentref_/1) — Kivy UI layout
- [buildozer.spec](http://_vscodecontentref_/2) — Buildozer config for Android packaging
- [cache](http://_vscodecontentref_/3) — Downloaded audio files
- [favorites.txt](http://_vscodecontentref_/4) — List of favorite songs

---



## Notes

- The app uses `yt-dlp` to download audio from YouTube. Please respect YouTube's Terms of Service.
- On first run, a [cache](http://_vscodecontentref_/5) directory will be created for downloaded songs.
- Favorites and remove song features are placeholders and will be implemented soon.

---

## License

MIT License

---

**Enjoy your music!**
