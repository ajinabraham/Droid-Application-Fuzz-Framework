"""
Fuzz Server
"""
import os
import re
import sys

from flask import (
    Flask,
    abort,
    send_file,
    request,
    jsonify
)
from browser_fuzz import (
    generate_html,
    start_browser_fuzz
)
from pdf_fuzz import (
    start_pdf_fuzz
)

import settings
import utils

sys.tracebacklimit = 0
APP = Flask(__name__)
FILENAME_REGEX = re.compile(r"^[^\\\/]*\.(\w{3,4})$")


@APP.route('/html/<filename>')
def serve_html_pregenerated_files(filename):
    """Pre Generated HTML Files"""
    if filename.endswith(".html") and re.match(FILENAME_REGEX, filename):
        pregen_pdf_dir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "generators/html/htmls/")
        fuzz_file = os.path.join(pregen_pdf_dir, filename)
        if os.path.exists(fuzz_file):
            return send_file(fuzz_file)
        return "File Not Found!"
    abort(404)


@APP.route('/pdf/<filename>')
def serve_pdf_pregenerated_files(filename):
    """Pre Generated Files"""
    if filename.endswith(".pdf") and re.match(FILENAME_REGEX, filename):
        pregen_pdf_dir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "generators/pdf/pdfs")
        fuzz_file = os.path.join(pregen_pdf_dir, filename)
        if os.path.exists(fuzz_file):
            return send_file(fuzz_file)
        return "File Not Found!"
    abort(404)


@APP.route('/fuzz_html/<req_id>', methods=['GET', 'POST'])
def gen_fuzz_html(req_id):
    """Generate Fuzz HTML"""
    if req_id.isdigit():
        return generate_html(req_id)
    abort(404)


@APP.route('/fuzz_pdf/<filename>')
def serve_pdf_fuzz_files(filename):
    """Fuzzer Generated Files"""
    if filename.endswith(".pdf") and re.match(FILENAME_REGEX, filename):
        fuzz_output_dir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "fuzz_files")
        fuzz_file = os.path.join(fuzz_output_dir, filename)
        if os.path.exists(fuzz_file):
            return send_file(fuzz_file)
        return "File Not Found!"
    abort(404)


@APP.route('/browser_fuzz', methods=['POST'])
def browser_fuzz():
    """Start Browser Fuzzer"""
    browser = request.form.get('browser')
    fuzzer = request.form.get('fuzzer')
    iteration = request.form.get('iteration')
    start_browser_fuzz(browser, fuzzer, int(iteration))
    return "Browser Fuzzing Started"


@APP.route('/pdf_fuzz', methods=['POST'])
def pdf_fuzz():
    """Start PDF Fuzzer"""
    pdf_reader = request.form.get('pdf_reader')
    fuzzer = request.form.get('fuzzer')
    iteration = request.form.get('iteration')
    start_pdf_fuzz(pdf_reader, fuzzer, int(iteration))
    return "PDF Reader Fuzzing Started"


@APP.route('/crashes', methods=['POST'])
def get_crashes():
    """Get Crashes if any"""
    crash_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "crash")
    if os.path.exists(crash_dir):
        allfiles = os.listdir(crash_dir)
        file_list = [filename for filename in allfiles if filename.endswith(
            ".html") or filename.endswith(".pdf")]
        if len(file_list) > 0:
            return jsonify({"crash": len(file_list), "files": file_list})
    return jsonify({"crash": 0, "files": []})


@APP.route('/stop', methods=['POST'])
def shutdown():
    """Shut down the server"""
    utils.adb_kill()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


@APP.route('/', methods=['GET'])
def main():
    """UI"""
    with open('static/index.html', 'r') as filep:
        return filep.read()

if __name__ == '__main__':
    APP.run(threaded=True, host=settings.SERVER_IP,
            port=settings.SERVER_PORT, debug=settings.DEBUG)
