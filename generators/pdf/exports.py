"""PDF Fuzz Grammer"""
import os
import math
import random

import generators.pdf.mPDF as mPDF
from generators.html.domato.exports import (
    gen_new_jscript_js
)


def get_pdfs():
    """Return PDF Paths"""
    pdf_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs")
    pdfs = os.listdir(pdf_dir)
    full_path = [os.path.join(pdf_dir, filename)
                 for filename in pdfs if filename.endswith(".pdf")]
    return full_path


def generate_pdf_domato(outfile):
    """Create PDF fuzz sample"""
    pdf_writer = mPDF.cPDF(outfile)
    pdf_writer.header()
    pdf_writer.indirectobject(
        1, 0, '<<\n /Type /Catalog\n /Outlines 2 0 R\n /Pages 3 0 R\n /OpenAction 7 0 R\n>>')
    pdf_writer.indirectobject(2, 0, '<<\n /Type /Outlines\n /Count 0\n>>')
    pdf_writer.indirectobject(
        3, 0, '<<\n /Type /Pages\n /Kids [4 0 R]\n /Count 1\n>>')
    pdf_writer.indirectobject(
        4, 0, '<<\n /Type /Page\n /Parent 3 0 R\n /MediaBox [0 0 612 792]\n /Contents 5 0 R\n /Resources <<\n             /ProcSet [/PDF /Text]\n             /Font << /F1 6 0 R >>\n            >>\n>>')
    pdf_writer.stream(5, 0, 'BT /F1 12 Tf 100 700 Td 15 TL (Fuzz File) Tj ET')
    pdf_writer.indirectobject(
        6, 0, '<<\n /Type /Font\n /Subtype /Type1\n /Name /F1\n /BaseFont /Helvetica\n /Encoding /MacRomanEncoding\n>>')
    javascript = gen_new_jscript_js()#"app.alert({cMsg: 'PDF JavaScript'});"
    pdf_writer.indirectobject(
        7, 0, '<<\n /Type /Action\n /S /JavaScript\n /JS (%s)\n>>' % javascript)
    pdf_writer.xrefAndTrailer('1 0 R')


def generate_dumb_pdf_sample(fuzz_factor, outfile):
    """ Generate PDF Sample
        Charlie Miller code (modified)
    """
    file_choice = random.choice(get_pdfs())
    buf = bytearray(open(file_choice, 'rb').read())
    numwrites = random.randrange(
        math.ceil(((float(len(buf))) / fuzz_factor))) + 1
    fuzz_choice = random.choice(['start', 'end', 'middle', 'random'])
    begin = None
    if fuzz_choice == 'start':
        begin = 0
    if fuzz_choice == 'end':
        begin = len(buf) - numwrites - 1
    if fuzz_choice == 'middle':
        begin = random.randrange(len(buf) - numwrites)
    for ___ in xrange(numwrites):
        rbyte = random.randrange(256)
        if begin is None:
            rnge = random.randrange(len(buf))
        else:
            rnge = begin
            begin += 1
        buf[rnge] = "%c" % (rbyte)
    with open(outfile, 'wb') as flip:
        flip.write(buf)
