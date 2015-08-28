import logging
logging.basicConfig(filename='cssedit.log', level=logging.DEBUG,
    format='%(asctime)s %(message)s')

import os
import sys

try:
    import editor.cssedit
except ImportError:
    sys.path.append(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'editor'))
    import cssedit
    import cssedit_qt as gui
else:
    import editor.cssedit_qt as gui

testfiles = (
    "simplecss-compressed.css",
    "simplecss-short.css",
    "simplecss-medium.css",
    "simplecss-long.css",
    )

formatted_css ="""\
div p>span["red"]~a:hover {
    border: 5px solid red;
    text-decoration: none;
    content: "gargl";
}
p {
    font-family: Arial sans-serif
}
div {
    display: inline;
    float: left
}"""
def log_treedata(obj):
    obj.treetoview()
    for item in obj.treedata:
        logging.info(item)

def test_fsplit():
    for data, delim in (
            ('Hallo, daar, jongens en meisjes', ','),
            ('x { y:z; p: q;}', '}'),
            ('/* commentaar */ /* commentaar */ /* commentaar */ *', '*/')):
        logging.info(cssedit.fsplit(data, delim))

def test_load():
    for name in testfiles:
        data = cssedit.load(name)
        logging.info(data)

def test_parse():
    for name in testfiles[:2]:
        logging.info('data from ' + name)
        data = cssedit.load(name)
        result = cssedit.parse(data)
        for key, value in result.items():
            for x, y in value.items():
                logging.info('{}: {} - {}'.format(key, x, y))

def test_get_single():
    tag = 'div p>span["red"]~a:hover'
    data = 'border: 5px solid red; text-decoration: none; content: "gargl"; '
    logging.info(cssedit.get_for_single_tag(tag, data))

def test_return_single():
    data = ('div p>span["red"]~a:hover: { border: 5px solid red; text-decoration: '
        'none; content: "gargl"; }')
    logging.info(cssedit.return_for_single_tag(data))

def test_compile():
    logging.info('-- compile empty data')
    logging.info(cssedit.compile({}))
    logging.info('-- compile empty subdicts')
    logging.info(cssedit.compile({1: {'tag1': {}}, 2: {'tag2': {}}, 3: {'tag3': {}}}))
    logging.info('-- compile good data')
    logging.info(cssedit.compile({
        1: {'div p>span["red"]~a:hover': {
            'border': '5px solid red',
            'text-decoration': 'none', 'content': '"gargl"'}},
        2: {'div': {'float': 'left', 'display': 'inline'}},
        3: {'p': {'font-family': 'Arial sans-serif'}}
        }))

def test_format():
    data = cssedit.compile({
        1: {'div p>span["red"]~a:hover': {
            'border': '5px solid red',
            'text-decoration': 'none', 'content': '"gargl"'}},
        2: {'div': {'float': 'left', 'display': 'inline'}},
        3: {'p': {'font-family': 'Arial sans-serif'}}
        })
    logging.info('-- format with type empty')
    text = cssedit.format(data, format="") #retourneert None (fout)
    logging.info(text)
    logging.info('-- format with incorrect type')
    text = cssedit.format(data, format="#$%%^(^%$@") #retourneert None (fout)
    logging.info(text)
    for compression in cssedit.format_types:
        logging.info('-- format type {}'.format(compression))
        text = cssedit.format(data, format=compression)
        logging.info(text)


def test_save():
    import os
    os.remove("test.txt")
    os.remove("test2.txt")
    cssedit.save("gargl", "test.txt")
    import shutil
    shutil.copyfile("test.txt", "test2.txt")
    cssedit.save("hello\nit's me", "test2.txt", backup=False)
    cssedit.save("wrong,\nit's somebody else", "test2.txt", backup=True)

test_functions = {
    'fsplit': test_fsplit,
    'load': test_load,
    'parse': test_parse,
    'get_single': test_get_single,
    'return_single': test_return_single,
    'compile': test_compile,
    'format': test_format,
    'save': test_save,
    }
#--
def test_editor_noargs():
    logging.info("--- No arguments")
    ed = cssedit.Editor()        # raises ValueError
    logging.info("--- Positional arg only")
    ed = cssedit.Editor('snork')     # raises FileNotFoundError
    logging.info("--- Positional arg only: 1")
    ed = cssedit.Editor('snork')    # also raises FileNotFoudError
    logging.info("--- Positional arg only: 2")
    ed = cssedit.Editor('snork', 'bork') # also
    logging.info("--- Positional arg only: 3")
    ed = cssedit.Editor('snork', 'bork', 'klork') # as well
    logging.info("--- Positional arg with correct one")
    ed = cssedit.Editor('snork', filename='simplecss-compressed.css') # raises
        # TypeError: __init__() got multiple values for argument 'filename'

def test_editor_filename():
    logging.info("--- filename as positional arg")
    ed = cssedit.Editor('simplecss-compressed.css') # raises TypeError
    log_treedata(ed)
    logging.info("--- treedata for file - empty filename")
    ed = cssedit.Editor(filename="")    # raises ValueError
    log_treedata(ed)
    logging.info("--- treedata for file - nonexistant")
    ed = cssedit.Editor(filename="nonexistant") # raises FileNotFoundError
    log_treedata(ed)
    logging.info("--- treedata for file - valid file")
    ed = cssedit.Editor(filename="simplecss-compressed.css")
    log_treedata(ed)

def test_editor_tag():
    logging.info("--- treedata for empty tag")
    ed = cssedit.Editor(tag ='')    # raises ValueError
    logging.info("--- treedata for ok tag")
    ed = cssedit.Editor(tag ='div p>span["red"]~a:hover') # raises ValueError
    logging.info("--- treedata for empty tag and empty text")
    ed = cssedit.Editor(tag="", text="") # raises ValueError
    logging.info("--- treedata for ok tag and empty text")
    ed = cssedit.Editor(tag='div p>span["red"]~a:hover', text="") # raises ValueError
    logging.info("--- treedata for ok tag and nonsense text") # raises ValueError
    ed = cssedit.Editor(tag='div p>span["red"]~a:hover', text="snorckenborcken")
    # the only good one
    logging.info("--- treedata for ok tag and ok text")
    ed = cssedit.Editor(tag='div p>span["red"]~a:hover',
        text='border: 5px solid red; text-decoration: none; content: "gargl"; ')
    logging.info(ed.data)
    ed.treetoview()
    for item in ed.treedata:
        logging.info(item)

def test_editor_text():
    ## logging.info("--- treedata for nonsense text")
    ## ed = cssedit.Editor(text="snorckenbocken") # works like text only - raises ValueError
    ## logging.info("--- treedata voor text without tags")
    ## ed = cssedit.Editor(text='border: 5px solid red; text-decoration: none; '
        ## 'content: "gargl"; ') # raises ValueError
    logging.info("--- treedata voor sensible text - one tag")
    ed = cssedit.Editor(text='div p>span["red"]~a:hover { border: 5px solid red; '
        'text-decoration: none; content: "gargl"; }')
    ed.treetoview()
    for item in ed.treedata:
        logging.info(item)
    logging.info("--- treedata voor sensible text - more tags")
    ed = cssedit.Editor(text='div p>span["red"]~a:hover { border: 5px solid red; '
        'text-decoration: none; content: "gargl"; } p { font-family: Arial '
        'sans-serif} div { display: inline; float: left }')
    ed.treetoview()
    for item in ed.treedata:
        logging.info(item)
    logging.info("--- treedata voor sensible text - more tags - formatted")
    ed = cssedit.Editor(text=formatted_css)
    ed.treetoview()
    for item in ed.treedata:
        logging.info(item)


def test_editor_compileback():
    logging.info("--- compile back from fileinput")
    ed = cssedit.Editor(filename="simplecss-compressed.css")
    ed.treetoview()
    ed.viewtotree()
    logging.info(ed.data)
    logging.info("--- compile back from tag input")
    ed = cssedit.Editor(tag='div p>span["red"]~a:hover',
        text='border: 5px solid red; text-decoration: none; content: "gargl"; ')
    ed.treetoview()
    ed.viewtotree()
    logging.info(ed.data)
    logging.info("--- compile back from formatted text")
    ed = cssedit.Editor(text=formatted_css)
    ed.treetoview()
    ed.viewtotree()
    logging.info(ed.data)

def test_editor_return():
    logging.info("-- return for filename - look at files for result")
    ed = cssedit.Editor(filename="simplecss-short.css")
    ed.treetoview()
    ed.viewtotree()
    ## logging.info(ed.data)
    ed.return_to_source(savemode='short')
    return
    tag = 'div p>span["red"]~a:hover'
    logging.info("-- return for tag `{}`".format(tag))
    ed = cssedit.Editor(tag=tag,
        text='border: 5px solid red; text-decoration: none; content: "gargl"; ')
    ed.treetoview()
    ed.viewtotree()
    ed.return_to_source()
    logging.info(ed.cssdata)
    logging.info("-- return for text")
    ed = cssedit.Editor(text=formatted_css)
    ed.treetoview()
    ed.viewtotree()
    data = ed.data # backup to make this repeatable and not need getting it again
    ed.return_to_source()
    logging.info(ed.data)
    logging.info("-- return for text - format short")
    ed.data = data # repeat
    ed.return_to_source(savemode="short")
    logging.info(ed.data)
    logging.info("-- return for text - format medium")
    ed.data = data # repeat
    ed.return_to_source(savemode="medium")
    logging.info(ed.data)
    logging.info("-- return for text - format long")
    ed.data = data # repeat
    ed.return_to_source(savemode="long")
    logging.info(ed.data)
    logging.info("-- return for text - format stupid")
    ed.data = data # repeat
    ed.return_to_source(savemode="#$^&*^&%$")   # raises AttributeError, as it should
    logging.info(ed.data)
    logging.info("-- return for text - format empty")
    ed.data = data # repeat
    ed.return_to_source(savemode="") # raises AttributeError, as it should
    logging.info(ed.data)

test_editorclass = {
    'editor_noargs': test_editor_noargs,
    'editor_filename': test_editor_filename,
    'editor_tag': test_editor_tag,
    'editor_text': test_editor_text,
    'editor_compileback': test_editor_compileback,
    'editor_return': test_editor_return,
    }
#--
def test_gui(arg=''):
    if arg == 'file':
        gui.main(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "simplecss-short.css"))
    elif arg == 'tag':
        gui.main(tag='div p>span["red"]~a:hover',
            text='border: 5px solid red; text-decoration: none; content: "gargl"; ')
    elif arg == 'text':
        gui.main(text=formatted_css)
    else:
        gui.main(test='text') # raises ValueError

gui_testtypes = ('file', 'tag', 'text', '')
#--

def run_all_tests():
    for test in test_functions:
        test_functions[test]()
    for test in test_editorclass:
        test_editorclass[test]()
    for test in gui_testtypes:
        test_gui(test)

## run_all_tests()
test_gui('file')
