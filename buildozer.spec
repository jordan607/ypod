
[app]
title = ypod
package.name = musicplayer
package.domain = org.vishal

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

# Explicitly specify the main entry point
# If your main file is main.py
source.main = main.py

# Requirements: remove python-vlc; add ffpyplayer or SDL2 audio
requirements = python3,kivy,yt-dlp,ffpyplayer

version = 0.1

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a

p4a.bootstrap = sdl2

android.allow_backup = True

log_level = 2
warn_on_root = 0

# bin_dir is optional; uncomment if your APK appears elsewhere
# bin_dir = ./bin
