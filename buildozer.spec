[app]

# (str) Title of your application
title = ypod

# (str) Package name
package.name = musicplayer

# (str) Package domain (needed for android/ios packaging)
package.domain = org.vishal

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,yt-dlp,python-vlc

# (str) Application versioning
version = 0.1

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions - corrected for modern Android
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
# Setting to a modern API level like 33 is recommended.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Bootstrap to use for android builds
# Set to sdl2, which is the standard for Kivy apps.
p4a.bootstrap = sdl2

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

#
# buildozer specific
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin