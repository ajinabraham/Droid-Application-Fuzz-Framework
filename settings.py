# Fuzz Server Settings
SERVER_IP = "0.0.0.0"
SERVER_PORT = 1337
FUZZ_IP = "192.168.0.103"
FUZZ_WAIT = 13
DEBUG = True
ADB_BINARY = "adb"
CRASH_IDENTIFIERS = ['SIGSEGV', 'SIGFPE', 'SIGILL']

# Device Settings
DEVICE_ID = "ZY222VQZWD"

# Fuzz Targets
BROWSERS = ["com.android.chrome", "org.mozilla.firefox",
            "com.opera.browser", "com.UCMobile.intl"]
BROWSER_ARGS = {
    "chrome": ["am", "start", "-n",
               "com.android.chrome/com.google.android.apps.chrome.Main",
               "-a", "android.intent.action.VIEW", "--es",
               "com.android.browser.application_id",
               "com.opensecurity.chrome_fuzz", "-d"],
    "firefox": ["am", "start", "-n",
                "org.mozilla.firefox/.App",
                "-a", "android.intent.action.VIEW", "--es",
                "com.android.browser.application_id",
                "com.opensecurity.firefox_fuzz""-d"],
    "opera": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
              "com.opera.browser/com.opera.Opera", "--es",
              "com.android.browser.application_id", "com.android.browser",
              "--ez", "create_new_tab false", "-d"],
    "ucweb": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
              "com.UCMobile.intl/com.UCMobile.main.UCMobile", "-d"],
}
PDF_READERS = ["com.adobe.reader",
               "com.foxit.mobile.pdf.lite",
               "com.google.android.apps.pdfviewer",
               "com.infraware.office.link",
               "cn.wps.moffice_eng"]
PDF_READER_ARGS = {
    "adobe": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
              "com.adobe.reader/.AdobeReader", "-t", "application/pdf", "-d"],
    "foxit": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
              "com.foxit.mobile.pdf.lite/com.fuxin.read.imp.RD_ReadActivity",
              "-t", "application/pdf", "-d"],
    "google": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
               "com.google.android.apps.pdfviewer/com.google.android.apps.viewer.PdfViewerActivity",
               "-t", "application/pdf", "-d"],
    "polaris": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
                "com.infraware.office.link/com.infraware.filemanager.FmLauncherActivity", "-t",
                "application/pdf", "-d"],
    "wpsoffice": ["am", "start", "-a", "android.intent.action.VIEW", "-n",
                  "cn.wps.moffice_eng/cn.wps.moffice.documentmanager.PreStartActivity2", "-t",
                  "application/pdf", "-d"],
}
