[app]

# Title of your application
title = AI Dubbing Pro

# Package name
package.name = dubbingpro

# Package domain (needed for android/ios packaging)
package.domain = org.ai.dubbing

# Source code where the main.py live
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3,json,txt

# Version of your application
version = 2.0.0

# Requirements for the application
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,numpy

# Orientation (landscape, portrait, or all)
orientation = portrait

# Android specific
fullscreen = 0
android.presplash_color = #667eea
android.icon = icon.png

# Android API settings
android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,RECORD_AUDIO

# Android app settings
android.allow_backup = True
android.theme = "@android:style/Theme.NoTitleBar"

# Build options
android.build_tools_version = 33.0.0

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Warn on root
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Binaries output directory
bin_dir = ./bin
