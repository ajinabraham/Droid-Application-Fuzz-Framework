"""PDF Fuzzer"""
import os
import time
import subprocess
import urlparse
from shutil import copyfile

from generators.pdf.exports import (
    get_pdfs,
    generate_pdf_domato,
    generate_dumb_pdf_sample
)
import settings
import utils


def start_pdf_fuzz(pdf_reader, fuzz_type, limit=-1):
    """
    Start PDF Fuzzing
    Limit: -1 (Infinite fuzz)
    """
    print "[INFO] Running PDF Fuzzer"
    print "\n[DETAILS]"
    print "PDF Reader: " + pdf_reader
    print "Fuzzer Type: " + fuzz_type
    print "Fuzz Iteration: " + str(limit)
    utils.make_dirs()
    utils.adb_connection_int(settings.PDF_READERS)
    iteration = 1
    fuzz_server_url = "http://" + settings.FUZZ_IP + ":" + str(settings.SERVER_PORT)
    if fuzz_type == "pregenerated":
        for pdf in get_pdfs():
            pdf_file_name = os.path.basename(pdf)
            url = fuzz_server_url + "/pdf/" + pdf_file_name
            pdf_fuzz(pdf_reader, url, fuzz_type, iteration)
            if iteration == limit:
                break
            iteration += 1
    elif fuzz_type == "domato":
        fuzz_out_dir = os.path.join(os.path.dirname(__file__), "fuzz_files")
        while True:
            pdf_file_name = "pdf-smart-" + str(iteration) + ".pdf"
            fuzz_file = os.path.join(fuzz_out_dir, pdf_file_name)
            generate_pdf_domato(fuzz_file)
            url = fuzz_server_url + "/fuzz_pdf/" + pdf_file_name
            pdf_fuzz(pdf_reader, url, fuzz_type, iteration)
            if iteration == limit:
                break
            iteration += 1
    elif fuzz_type == "dumb":
        fuzz_factor = 250
        fuzz_out_dir = os.path.join(os.path.dirname(__file__), "fuzz_files")
        while True:
            pdf_file_name = "pdf-dump-" + str(iteration) + ".pdf"
            fuzz_file = os.path.join(fuzz_out_dir, pdf_file_name)
            generate_dumb_pdf_sample(fuzz_factor, fuzz_file)
            url = fuzz_server_url + "/fuzz_pdf/" + pdf_file_name
            pdf_fuzz(pdf_reader, url, fuzz_type, iteration)
            if limit > 0 and iteration == limit:
                break
            iteration += 1
    print "[INFO] PDF Reader Fuzzing Completed!"
    print "\n[Status]"
    print "PDF Reader: " + pdf_reader
    print "Fuzzer Type: " + fuzz_type
    print "Fuzz Iteration: " + str(limit)

def pdf_fuzz(pdf_reader, url, fuzz_type, iteration):
    """PDF Fuzzing"""
    adb = settings.ADB_BINARY
    pdf_reader_args = settings.PDF_READER_ARGS
    wait = settings.FUZZ_WAIT
    valid_crash_dir = os.path.join(os.path.dirname(__file__), "crash")
    fuzz_out_dir = os.path.join(os.path.dirname(__file__), "fuzz_files")
    subprocess.call([adb, "shell", "input", "keyevent", "82"])
    identifier = ""

    print "[INFO] Sending Fuzz URL: " + url
    if pdf_reader == "adobe":
        identifier = "adobe"
        args = [adb, "shell"] + pdf_reader_args["adobe"] + [url]
        subprocess.call(
            [adb, "shell", "am", "force-stop", "com.adobe.reader"])
    elif pdf_reader == "foxit":
        identifier = "foxit"
        args = [adb, "shell"] + pdf_reader_args["foxit"] + [url]
        subprocess.call(
            [adb, "shell", "pm", "clear", "com.foxit.mobile.pdf.lite"])
    elif pdf_reader == "google":
        identifier = "google"
        args = [adb, "shell"] + pdf_reader_args["google"] + [url]
        subprocess.call(
            [adb, "shell", "am", "force-stop", "com.google.android.apps.pdfviewer"])
    elif pdf_reader == "polaris":
        identifier = "polaris"
        args = [adb, "shell"] + pdf_reader_args["polaris"] + [url]
        subprocess.call(
            [adb, "shell", "am", "force-stop", "com.infraware.office.link"])
    elif pdf_reader == "wpsoffice":
        identifier = "wpsoffice"
        args = [adb, "shell"] + pdf_reader_args["wpsoffice"] + [url]
        subprocess.call(
            [adb, "shell", "am", "force-stop", "cn.wps.moffice_eng"])
    out = subprocess.Popen(args, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT).communicate()[0]
    print "[INFO] Waiting for " + str(wait) + " seconds"
    time.sleep(wait)
    # Debug
    print out
    logcat_args = [adb, 'logcat', '-d']
    logcat = subprocess.Popen(
        logcat_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    # clear logs
    logcat_args = [adb, 'logcat', '-c']
    subprocess.call(logcat_args)
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
            pregen_pdf_dir = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "generators/pdf/pdfs/")
            parsed_url = urlparse.urlparse(url)
            fname = os.path.basename(parsed_url.path)
            crash_file = os.path.join(pregen_pdf_dir, fname)
        else:
            crash_file = os.path.join(
                fuzz_out_dir, "pdf-" + fuzz_type + "-" + str(iteration) + ".pdf")
        save_file = os.path.join(
            valid_crash_dir, "pdf-" + fuzz_type + "-" + identifier + "-" + str(iteration) + ".pdf")
        log_file = os.path.join(
            valid_crash_dir, "pdf-" + fuzz_type + "-" + identifier + "-" + str(iteration) + ".log")
        copyfile(crash_file, save_file)
        with open(log_file, "w") as flip:
            flip.write(logcat)
