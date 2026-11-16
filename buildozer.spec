[app]
title = NUEL AI
package.name = nuelai
package.domain = org.nuel
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy,plyer,jnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, CALL_PHONE, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Explicitly target stable Android SDK versions to prevent missing build-tools errors
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
