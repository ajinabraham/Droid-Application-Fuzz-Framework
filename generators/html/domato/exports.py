import os
from generators.html.domato.grammar import Grammar
from generators.html.domato.generator import GenerateNewSample


def generate_fuzz_grammer():
    """Generate HTML Fuzz Sample"""
    grammar_dir = os.path.dirname(__file__)
    with open(os.path.join(grammar_dir, 'template.html'), "r") as flip:
        template = flip.read()

    htmlgrammar = Grammar()
    err = htmlgrammar.ParseFromFile(os.path.join(grammar_dir, 'html.txt'))
    # CheckGrammar(htmlgrammar)
    if err > 0:
        print 'There were errors parsing grammar'
        return

    cssgrammar = Grammar()
    err = cssgrammar.ParseFromFile(os.path.join(grammar_dir, 'css.txt'))
    # CheckGrammar(cssgrammar)
    if err > 0:
        print 'There were errors parsing grammar'
        return

    jsgrammar = Grammar()
    err = jsgrammar.ParseFromFile(os.path.join(grammar_dir, 'js.txt'))
    # CheckGrammar(jsgrammar)
    if err > 0:
        print 'There were errors parsing grammar'
        return

    # JS and HTML grammar need access to CSS grammar.
    # Add it as import
    htmlgrammar.AddImport('cssgrammar', cssgrammar)
    jsgrammar.AddImport('cssgrammar', cssgrammar)
    syntax = {}
    syntax["template"] = template
    syntax["htmlgrammar"] = htmlgrammar
    syntax["cssgrammar"] = cssgrammar
    syntax["jsgrammar"] = jsgrammar
    return syntax

FUZZ_SYNTAX = generate_fuzz_grammer()


def gen_new_html():
    """Generate New Sample"""
    template = FUZZ_SYNTAX["template"]
    htmlgrammar = FUZZ_SYNTAX["htmlgrammar"]
    cssgrammar = FUZZ_SYNTAX["cssgrammar"]
    jsgrammar = FUZZ_SYNTAX["jsgrammar"]
    return GenerateNewSample(template, htmlgrammar, cssgrammar, jsgrammar)


def gen_new_jscript_js():
    """Generate Js to be injected in PDF"""
    grammar_dir = os.path.dirname(__file__)
    jsgrammar = Grammar()
    err = jsgrammar.ParseFromFile(os.path.join(grammar_dir, 'jscript.txt'))
    if err > 0:
        print 'There were errors parsing grammar'
        return
    js_tmpl = "var vars = new Array(100);for(var i=0;i<20;i++) {vars[i] = new Array(10);}for(var i=20;i<40;i++) {vars[i] = 'aaaaaaaaaa';}"
    return js_tmpl + jsgrammar._GenerateCode(1)
