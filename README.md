# Droid Application Fuzz Framework

Droid Application Fuzz Framework (DAFF) helps you to fuzz Android Browsers and PDF Readers for memory corruption bugs in real android devices. You can use the inbuilt fuzzers or import fuzz files from your own custom fuzzers. DAFF consist of inbuilt fuzzers and crash monitor. It currently supports fuzzing the following applications:

#### Browsers

* [Google Chrome - com.android.chrome](https://play.google.com/store/apps/details?id=com.android.chrome)
* [Mozilla Firefox - org.mozilla.firefox](https://play.google.com/store/apps/details?id=org.mozilla.firefox)
* [Opera - com.opera.browser](https://play.google.com/store/apps/details?id=com.opera.browser)
* [UCWeb - com.UCMobile.intl](https://play.google.com/store/apps/details?id=com.UCMobile.intl)

#### PDF Viewers/Readers

* [Adobe Acrobat Reader - com.adobe.reader](https://play.google.com/store/apps/details?id=com.adobe.reader)
* [Foxit PDF Reader - com.foxit.mobile.pdf.lite](https://play.google.com/store/apps/details?id=com.foxit.mobile.pdf.lite)
* [Google PDF Viewer - com.google.android.apps.pdfviewer](https://play.google.com/store/apps/details?id=com.google.android.apps.pdfviewer)
* [Polaris Office - com.infraware.office.link](https://play.google.com/store/apps/details?id=com.infraware.office.link)
* [WPS Office + PDF - cn.wps.moffice_eng(WIP)](https://play.google.com/store/apps/details?id=cn.wps.moffice_eng)

### Fuzzer Generators

DAFF has three fuzzer modes:

1. **Google Domato** - Uses slightly modified version of [Google Domato](https://github.com/google/domato) for generating fuzz files.
2. **Dumb Fuzzer** - As the the name suggests, a dumb fuzzer. (Only for PDF)
3. **Pregenerated Files (3rd Party Fuzzer)** - To use your private or custom fuzzer generated files.

### Usage for Dummies

#### Android Device

* Install the supported Browsers and PDF readers in Android Device.
* Enable USB Debugging in the Android Device.
* Connect the Android Device to the same WiFi Network where the Computer is connected.
* Connect the Android Device to Computer using USB cable and Always allow the Computer for USB Debuging.

#### Computer

* Install Python 2.7
* `git clone https://github.com/ajinabraham/Droid-Application-Fuzz-Framework.git`
* `pip install -r requirements.txt`
* In `settings.py` set the `DEVICE_ID` as the Android Device ID. You can find this with `adb devices` command.
* Also set `FUZZ_IP` as the local IP of the computer. Use `ifconfig/ipconfig` command.
* Set the path to adb binary in `ADB_BINARY` if `adb` is not in your `PATH`.
* Run the Web GUI `python python daff_server.py`
* Access the Fuzzer Web Interface at `http://0.0.0.0:1337`
* Select the Application, Select the Fuzz Generator and Start Fuzzing!

### PS

I am just open sourcing a private project for the benefit of community. I don't have time to actively maintain this project. If you have found bugs, fix them and send pull requests. That's how opensource should work! I have done my best to make the documentation clear and simple for all types of users. Please ask Google or Stack Overflow if you are stuck. Spare me!


