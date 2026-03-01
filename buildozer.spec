[app]

title = AI Dubbing Pro
package.name = dubbingpro
package.domain = org.ai.dubbing
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 2.0.0
requirements = python3,kivy==2.2.1,pillow
orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

[buildozer]

log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin
