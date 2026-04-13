[app]

# (str) Title of your application
title = BubbleTech

# (str) Package name
package.name = bubbletech

# (str) Package domain (needed for android/ios packaging)
package.domain = org.bubbletech

# (str) Source code where the main.py live
source.dir = .

# (str) Source code file to run
source.main = main.py

# (list) Source files to include (separated by spaces)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,pygame,android

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 27

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Android app theme, default is Theme.MaterialComponents.Light.NoActionBar
android.apptheme = "@android:style/Theme.NoTitleBar.Fullscreen"

# (list) Pattern to whitelist for the android project
android.gradle_dependencies =

# (list) Extra packages to include in the apk
android.add_src =

# (list) Additional directories to include in the apk
android.add_assets =

# (list) List of Java .jar files to add to the libs
android.add_jars =

# (str) python-for-android branch to use
p4a.branch = master

# (str) Specific p4a commit to use (before build isolation bug)
# p4a.commit = abc123

# (bool) Use local p4a instead of downloading
# p4a.source_dir =

# (str) bootstrap to use (sdl2 for pygame)
p4a.bootstrap = sdl2

# (list) SDL2 image formats to include
image.formats = png,jpg

# (list) SDL2 mixer formats to include
audio.formats = ogg,wav

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. the apk/bin folder), absolute or relative to spec file
bin_dir = ./bin
