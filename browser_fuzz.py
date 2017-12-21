"""browser_fuzz"""

import os
import time
import urlparse
import subprocess
from shutil import copyfile
import settings
import utils

from generators.html.domato.exports import gen_new_html


def start_browser_fuzz(browser, fuzz_type, limit=-1):
    """Start Fuzzing
    Limit: -1 (Infinite fuzz)
    """

    print "[INFO] Running Browser Fuzzer"
    print "\n[DETAILS]"
    print "Browser: " + browser
    print "Fuzzer Type: " + fuzz_type
    print "Fuzz Iteration: " + str(limit)
    utils.adb_connection_int(settings.BROWSERS)
    iteration = 1
    fuzz_server_url = "http://" + settings.FUZZ_IP + ":" + str(settings.SERVER_PORT)
    if fuzz_type == "domato":
        while True:
            url = fuzz_server_url + "/fuzz_html/" + str(iteration)
            browser_fuzz(browser, fuzz_type, iteration, url)
            if iteration == limit:
                break
            iteration += 1
    elif fuzz_type == "pregenerated":
        for html in get_htmls():
            html_file_name = os.path.basename(html)
            url = fuzz_server_url + "/html/" + html_file_name
            browser_fuzz(browser, fuzz_type, iteration, url)
            if iteration == limit:
                break
            iteration += 1
    print "[INFO] Browser Fuzzing Completed!"
    print "\n[Status]"
    print "Browser: " + browser
    print "Fuzzer Type: " + fuzz_type
    print "Fuzz Iteration: " + str(limit)

def browser_fuzz(browser, fuzz_type, iteration, url):
    """Fuzz Browser and Collect Crashes"""
    adb = settings.ADB_BINARY
    browser_args = settings.BROWSER_ARGS
    wait = settings.FUZZ_WAIT
    valid_crash_dir = os.path.join(os.path.dirname(__file__), "crash")
    fuzz_out_dir = os.path.join(os.path.dirname(__file__), "fuzz_files")
    subprocess.call([adb, "shell", "input", "keyevent", "82"])
    identifier = ""

    print "[INFO] Sending Fuzz URL: " + url
    if browser == "chrome":
        identifier = "gc"
        args = [adb, "shell"] + browser_args["chrome"] + [url]
    elif browser == "firefox":
        identifier = "ff"
        args = [adb, "shell"] + browser_args["firefox"] + [url]
    elif browser == "opera":
        identifier = "op"
        args = [adb, "shell"] + browser_args["opera"] + [url]
        # Remove this if we get proper flag to prevent new tab creation
        subprocess.call([adb, "shell", "pm", "clear", "com.opera.browser"])
    elif browser == "ucweb":
        identifier = "uc"
        args = [adb, "shell"] + browser_args["ucweb"] + [url]
        # Remove this if we get proper flag to prevent new tab creation
        subprocess.call(
            [adb, "shell", "am", "force-stop", "com.UCMobile.intl"])
    out = subprocess.Popen(args, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT).communicate()[0]
    print "[INFO] Waiting for " + str(wait) + " seconds"
    time.sleep(wait)
    # Debug
    print out
    logcat_args = [adb, 'logcat', '-d']
    logcat = subprocess.Popen(
        logcat_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    crash_identifiers = settings.CRASH_IDENTIFIERS
    if any(id_string in logcat for id_string in crash_identifiers):
        print "[VALID CRASH] - " + url
        print "\n[DETAILS]"
        print "Fuzz Type: " + fuzz_type
        print "Iteration: " + str(iteration)
        print "identifier: " + identifier
        if not os.path.exists(valid_crash_dir):
            os.makedirs(valid_crash_dir)
        if fuzz_type == "pregenerated":
            pregen_html_dir = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "generators/html/htmls/")
            parsed_url = urlparse.urlparse(url)
            fname = os.path.basename(parsed_url.path)
            crash_file = os.path.join(pregen_html_dir, fname)
        else:
            crash_file = os.path.join(
                fuzz_out_dir, "fuzz-" + str(iteration) + ".html")
        save_file = os.path.join(
            valid_crash_dir, "fuzz-" + identifier + "-" + str(iteration) + ".html")
        log_file = os.path.join(
            valid_crash_dir, "fuzz-" + identifier + "-" + str(iteration) + ".log")
        copyfile(crash_file, save_file)
        with open(log_file, "w") as flip:
            flip.write(logcat)


def generate_html(iteration):
    """Generate HTML"""
    fuzz_out_dir = os.path.join(os.path.dirname(__file__), "fuzz_files")
    if not os.path.exists(fuzz_out_dir):
        os.makedirs(fuzz_out_dir)
    fuzz_html = gen_new_html()
    with open(os.path.join(fuzz_out_dir, "fuzz-" + str(iteration) + ".html"), "w") as flip:
        flip.write(fuzz_html)
    return fuzz_html


def get_htmls():
    """Get Pregenerated HTMLS"""
    html_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "generators/html/htmls")
    htmls = os.listdir(html_dir)
    full_path = [os.path.join(html_dir, filename)
                 for filename in htmls if filename.endswith(".html")]
    return full_path
