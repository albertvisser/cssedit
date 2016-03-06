import unittest
import cssutils

import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))

try:
    import editor.cssedit as cssedit
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(HERE),'editor'))
    import cssedit
    import csseditor_qt as gui
else:
    import editor.csseditor_qt as gui

import expected_results as results
testfiles = (
    ('compressed', os.path.join(HERE, "simplecss-compressed.css")),
    ('short', os.path.join(HERE, "simplecss-short.css")),
    ('medium', os.path.join(HERE, "simplecss-medium.css")),
    ('long', os.path.join(HERE, "simplecss-long.css")),
    )
formatted_css ="""\
/* this is a stupid comment */
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

class TestFunctions(unittest.TestCase):
    """test basic cssedit functions
    """
    ## def test_format(self):
        ## testdata = [
            ## ('/**/', 'no comment'),
            ## ('div p>span["red"]~a:hover', {'border': '5px solid red',
                ## 'text-decoration': 'none', 'content': '"gargl"'}),
            ## ('div', {'float': 'left', 'display': 'inline'}),
            ## ('p', {'font-family': 'Arial sans-serif'})
            ## ]
        ## self.assertEqual(cssedit.format([]), '')
        ## self.assertEqual(cssedit.format([
            ## ('tag1', {}), ('tag2', {}), ('tag3', {})
            ## ]), 'tag1 {  } tag2 {  } tag3 {  }')
        ## self.assertEqual(cssedit.format(testdata),
                ## 'div p>span["red"]~a:hover { border: 5px solid red; content: '
                ## '"gargl"; text-decoration: none; } div { display: inline; '
                ## 'float: left; } p { font-family: Arial sans-serif; }')
        ## self.assertEqual(cssedit.format(testdata, mode="short"), "\n".join((
                ## '/* no comment */',
                ## 'div p>span["red"]~a:hover { border: 5px solid red; content: '
                    ## '"gargl"; text-decoration: none; }',
                ## 'div { display: inline; float: left; }',
                ## 'p { font-family: Arial sans-serif; }')))
        ## self.assertEqual(cssedit.format(testdata, mode="medium"), "\n".join((
                ## '/* no comment */',
                ## 'div p>span["red"]~a:hover {',
                ## '    border: 5px solid red; content: "gargl"; text-decoration: none;',
                ## '}',
                ## 'div {',
                ## '    display: inline; float: left;',
                ## '}',
                ## 'p {',
                ## '    font-family: Arial sans-serif;',
                ## '}')))
        ## self.assertEqual(cssedit.format(testdata, mode="long"), "\n".join((
                ## '/* no comment */',
                ## 'div p>span["red"]~a:hover {',
                ## '    border: 5px solid red;',
                ## '    content: "gargl";',
                ## '    text-decoration: none;',
                ## '}',
                ## 'div {',
                ## '    display: inline;',
                ## '    float: left;',
                ## '}',
                ## 'p {',
                ## '    font-family: Arial sans-serif;',
                ## '}')))

    def test_parse(self):
        data = cssedit.load(testfiles[3][1])
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 92, in test_parse
             #self.assertEqual(data, results.data['parse_function'])
        # AssertionError: cssutils.css.CSSStyleSheet(href='file:/ho[72 chars]None) != [('/**/', 'simple css in this case means [1058 chars]h'})]
        self.assertEqual(data.cssText, results.data['parse_function'])

    def test_get_return_single(self):
        tag = 'div p>span["red"]~a:hover'
        data = 'border: 5px solid red; text-decoration: none; content: "gargl";'
        data_out = 'border: 5px solid red; content: "gargl"; text-decoration: none;'
        result = {'border': '5px solid red', 'content': '"gargl"',
            'text-decoration': 'none' }
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 100, in test_get_return_single
             #self.assertEqual(str(cssedit.get_for_single_tag(data)), result)
        # AssertionError: '<cssutils.css.CSSStyleDeclaration object length=3 (all: 3) at 0x7f58125db978>' != {'text-decoration': 'none', 'border': '5px solid red', 'content': '"gargl"'}
        self.assertEqual(cssedit.get_for_single_tag(data).cssText, result)
        self.assertEqual(cssedit.return_for_single_tag(result), data_out)
        self.assertEqual(cssedit.return_for_single_tag(
            cssedit.get_for_single_tag(data)), data_out)

    def test_load(self):
        self.maxDiff = None
        for method, name in testfiles:
            if method == 'compressed':
                result = results.data['load_function']['compressed']
            else:
                result = results.data['load_function']['other']
            # Traceback (most recent call last):
            # File "/home/albert/projects/cssedit/tests/unittests.py", line 112, in test_load
                 #self.assertEqual(str(cssedit.load(name)), result)
            # AssertionError: "<cssutils.css.CSSStyleSheet object encod[135 chars]ef0>" != '* { display: inline; } div { margin: 0 0[713 chars]h; }'
            # - <cssutils.css.CSSStyleSheet object encoding='utf-8' href='file:/home/albert/projects/cssedit/tests/simplecss-compressed.css' media=None title=None namespaces={} at 0x7f580d125ef0>
            # + * { display: inline; } div { margin: 0 0 0 0; padding: 0 0 0 0; } p { text-align: center; vertical-align: middle } img { border: 1px solid } .red { color: red; font-weight: bold } #page-title { font-size: 55 } p::first-child { text-decoration: underline; } li:nth-child(3) { background-color: green } a:hover { background-color: blue } p.oms:before { content: "Hello, it's me" } div div { display: block; } ul>li>ul>li { list-style: square; } ul + p { font-style: italic } p ~ p { font-variant: small-caps; } a[title] { color: yellowish; } td[valign="top"] { font-weight: bold; } a[href*="ads"] { display: none; } a[href^="http"]{ background: url(path/to/external/icon.png) no-repeat; padding-left: 10px; } a[href$="jpg"] { text-decoration: line-through; }
            self.assertEqual(cssedit.load(name).cssText, result) # str() werkt niet

    def test_log(self):
        for logline in [
            " transition]",
            "WARNING	Property: Unknown Property name. [1:2511: flex-flow]",
            "ERROR	Unexpected token (NUMBER, 2, 1, 735)",
            "ERROR	MediaList: Invalid MediaQuery:  (-webkit-min-device-pixel-ratio:2)",
                ]:
            print(parse_log_line(logline))
    ## for x in test.log:
        ## print(x.strip())
        ## y = parse_log_line(x)
        ## print(y)
        ## z = get_definition_from_file(testdata, y.line, y.pos)
        ## print(z)


class TestSaveFunction(unittest.TestCase):
    """save function has a separate class because of special setup and teardown
    """
    def setUp(self):
        self.testcontent = "saveword\nsaveword"
        self.new_content = self.testcontent + '...'
        self.fname = "test.text"
        self.backup = self.fname + '~'
        self._delete_files()

    def _delete_files(self):
        try:
            os.remove(self.fname)
        except:
            pass
        try:
            os.remove(self.backup)
        except:
            pass

    def test_save_simple(self):
        cssedit.save(self.testcontent, self.fname)
        self.assertTrue(os.path.exists(self.fname))
        with open(self.fname) as _in:
            data = _in.read()
        self.assertEqual(data, self.testcontent + "\n") # is geschreven mbv print

    def test_save_nobackup(self):
        cssedit.save(self.testcontent, self.fname, backup=False)
        self.assertTrue(os.path.exists(self.fname))
        self.assertFalse(os.path.exists(self.backup))
        with open(self.fname) as _in:
            data = _in.read()
        self.assertEqual(data, self.testcontent + "\n") # is geschreven mbv print

    def test_save_backup(self):
        with open(self.fname, "w") as _out:
            _out.write(self.testcontent)
        cssedit.save(self.new_content, self.fname, backup=True)
        self.assertTrue(os.path.exists(self.fname))
        with open(self.fname) as _in:
            data = _in.read()
        self.assertEqual(data, self.new_content + "\n") # is geschreven mbv print
        data = ''
        self.assertTrue(os.path.exists(self.backup))
        with open(self.backup) as _in:
            data = _in.read()
        self.assertEqual(data, self.testcontent)

    def tearDown(self):
        self._delete_files()

class TestEditor(unittest.TestCase):
    """Base class, setting up some standard attributes
    """
    one_selector = ('div p>span~a:hover { border: 5px solid red; '
        'text-decoration: none; content: "gargl"; }')
    more_selectors = ('div p>span~a:hover { border: 5px solid red; '
        'text-decoration: none; content: "gargl"; } p { font-family: Arial '
        'sans-serif} div { display: inline; float: left }')
    ## tagname = 'div p>span["red"]~a:hover'
    tagname = 'div'
    bad_tagtext = "snorckenborcken"
    good_tagtext = 'border: 5px solid red; text-decoration: none; content: "gargl";'
    tagtext_sorted = 'border: 5px solid red; content: "gargl"; text-decoration: none;'

class TestEditorCreate(TestEditor):
    """Various ways of creating an Editor class
    """
    def test_editor_badargs(self):
        #--- No arguments
        with self.assertRaises(ValueError):
            ed = cssedit.Editor()
        #--- Positional arg only: 1
        with self.assertRaises(TypeError):
            ed = cssedit.Editor('snork')
        #--- Positional arg only: 2
        with self.assertRaises(TypeError):
            ed = cssedit.Editor('snork', 'bork')
        #--- Positional arg only: 3
        with self.assertRaises(TypeError):
            ed = cssedit.Editor('snork', 'bork', 'hork')
        #--- Positional arg with correct one
        with self.assertRaises(TypeError):
            ed = cssedit.Editor('snork', filename=testfiles[0][1])

    def test_editor_filename(self):
        #--- filename as positional arg
        with self.assertRaises(TypeError):
            ed = cssedit.Editor(testfiles[0][1])
        #--- treedata for file - empty filename
        with self.assertRaises(ValueError):
            ed = cssedit.Editor(filename="")
        #--- treedata for file - nonexistant
        with self.assertRaises(FileNotFoundError):
            ed = cssedit.Editor(filename="nonexistant")
        #--- treedata for file - valid file
        for method, name in testfiles:
            if method == 'compressed':
                result = results.data['editor_file']['compressed']
            else:
                result = results.data['editor_file']['other']
            ed = cssedit.Editor(filename=name)
            self.assertIsInstance(ed.data, cssutils.css.CSSStyleSheet)
            # TODO: test op inhoud verbeteren
            ## self.assertEqual(ed.data.cssText, ''.join(result))

    def test_editor_tag(self):
        #--- treedata for empty tag
        with self.assertRaises(ValueError):
            ed = cssedit.Editor(tag='')
        #--- treedata for ok tag
        with self.assertRaises(ValueError):
            ed = cssedit.Editor(tag=self.tagname)
        #--- treedata for empty tag and empty text
        with self.assertRaises(ValueError):
            ed = cssedit.Editor(tag="", text="")
        #--- treedata for ok tag and empty text
        with self.assertRaises(ValueError):
            ed = cssedit.Editor(tag=self.tagname, text="")
        #--- treedata for ok tag and nonsense text
        ## with self.assertRaises(ValueError):
            ## ed = cssedit.Editor(tag=self.tagname, text=self.bad_tagtext)
        #--- treedata for ok tag and ok text
        ed = cssedit.Editor(tag=self.tagname, text=self.good_tagtext)
        self.assertEqual(ed.data.cssText, results.data['editor_tag'])

    def test_editor_text(self):
        #--- treedata for nonsense text
        # moet wel een fout uitkomen maar wanneer?
        ## ed = cssedit.Editor(text="snorckenbocken") # works like text only - raises ValueError
        #--- treedata for text without tags
        ## with self.assertRaises(ValueError):
            ## ed = cssedit.Editor(text='border: 5px solid red; text-decoration: none; '
                ## 'content: "gargl"; ')
        #--- treedata for sensible text - one tag
        ed = cssedit.Editor(text=self.one_selector)
        self.assertEqual(ed.data.cssText, results.data['editor_text']['one'])
        ## self.assertEqual(str(ed.data.cssText), self.one_selector)
        #--- treedata for sensible text - more tags
        ed = cssedit.Editor(text=self.more_selectors)
        self.assertEqual(ed.data.cssText, results.data['editor_text']['more'])
        ## self.assertEqual(str(ed.data.cssText), self.more_selectors)
        #--- treedata voor sensible text - more tags - formatted")
        ed = cssedit.Editor(text=formatted_css)
        self.assertEqual(ed.data.cssText, results.data['editor_text']['formatted'])


class TestEditorMethods(TestEditor):

    def setUp(self):
        #--- treedata for sensible text - one tag
        self.ed = cssedit.Editor(text=self.one_selector)
        self.ed.datatotext()
        self.ed.texttodata()
        #--- treedata for sensible text - more tags
        self.edm = cssedit.Editor(text=self.more_selectors)
        self.ed.datatotext()
        self.ed.texttodata()

    def test_editor_texttotree(self):
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 298, in test_editor_texttotree
             #self.assertEqual(self.ed.treedata, results.data['editor_text2tree']['one'])
        # AssertionError: Lists differ: [] != ['div p>span["red"]~a:hover', '    border'[94 chars]one']
        #
        # Second list contains 7 additional elements.
        # First extra element 0:
        # div p>span["red"]~a:hover
        #
        # - []
        # + ['div p>span["red"]~a:hover',
        # +  '    border',
        # +  '        5px solid red',
        # +  '    content',
        # +  '        "gargl"',
        # +  '    text-decoration',
        # +  '        none']
        self.assertEqual(self.ed.treedata, results.data['editor_text2tree']['one'])
        self.assertEqual(self.edm.treedata, results.data['editor_text2tree']['more'])

    def test_editor_treetotext(self):
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 302, in test_editor_treetotext
             #self.assertEqual(self.ed.data, results.data['editor_text']['one'])
        # AssertionError: cssutils.css.CSSStyleSheet(href=None, med[13 chars]e='') != [('div p>span["red"]~a:hover', {'text-dec[63 chars]"'})]
        ## self.assertEqual(self.ed.data, results.data['editor_text']['one'])
        ## self.assertEqual(self.ed.data.cssText, ''.join(
            ## results.data['editor_text']['one']))
        self.assertEqual(self.ed.data.cssText, self.one_selector)
        ## self.assertEqual(self.edm.data, results.data['editor_text']['more'])
        self.assertEqual(self.edm.data.cssText, ''.join(self.more_selectors))

## class TestEditorReturnFile(TestEditor):

    ## def setUp(self):
        ## " make sure no backup file exists"
        ## self.orig = testfiles[1][1]
        ## self.backup = self.orig + '~'
        ## try:
            ## os.remove(self.backup)
        ## except FileNotFoundError:
            ## pass
        ## self.ed = cssedit.Editor(filename=self.orig) # short format
        ## self.ed.datatotext()
        ## self.ed.texttodata()

    ## def test_return_for_filename(self):
        ## self.ed.return_to_source(savemode='short')
        ## with open(self.orig) as _in, open(self.backup) as _in2:
            ## newtext = _in.read()
            ## origtext = _in2.read()
        ## # comments are not reinserted and sequence of properties may be different
        ## #-# self.assertEqual(newtext, origtext)

    ## def tearDown(self):
        ## "restore original file"
        ## os.rename(self.orig, self.backup + '~')
        ## os.rename(self.backup, self.orig)

class TestEditorReturnTag(TestEditor):

    def setUp(self):
        self.ed = cssedit.Editor(tag=self.tagname, text=self.good_tagtext)
        self.ed.datatotext()
        self.ed.texttodata()

    def test_return_for_tag(self):
        self.ed.return_to_source()
        # sequence of properties is different du to sorting
        self.assertEqual(self.ed.cssdata, self.tagtext_sorted)

class TestEditorReturnText(TestEditor):
    #In this class we also test the output options

    def setUp(self):
        self.ed = cssedit.Editor(text=formatted_css)
        self.ed.datatotext()
        ## self.ed.texttodata()

    def test_noformat(self):
        self.ed.return_to_source()
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 385, in test_short
             #self.assertEqual(self.ed.data, '/* this is a stupid comment */\n'
        # AssertionError: b'/* this is a stupid comment */\np {\n  [87 chars]   }' != '/* this is a stupid comment */\ndiv p>sp[158 chars]t; }'
        self.assertEqual(str(self.ed.data), 'div p>span["red"]~a:hover { border: 5px solid '
            'red; content: "gargl"; text-decoration: none; } p { font-family: '
            'Arial sans-serif; } div { display: inline; float: left; }')

    def test_short(self):
        self.ed.return_to_source(savemode="short")
        #Traceback (most recent call last):
        #File "/home/albert/projects/cssedit/tests/unittests.py", line 385, in test_short
            #self.assertEqual(self.ed.data, '/* this is a stupid comment */\n'
        #AssertionError: b'/* this is a stupid comment */\np {\n  [87 chars]   }' != '/* this is a stupid comment */\ndiv p>sp[158 chars]t; }'
        self.assertEqual(str(self.ed.data), '/* this is a stupid comment */\n'
            'div p>span["red"]~a:hover { border: 5px solid red; content: "gargl"; '
            'text-decoration: none; }\n'
            'p { font-family: Arial sans-serif; }\n'
            'div { display: inline; float: left; }')

    def test_medium(self):
        self.ed.return_to_source(savemode="medium")
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 393, in test_medium
             #self.assertEqual(self.ed.data, '/* this is a stupid comment */\n'
        # AssertionError: b'/* this is a stupid comment */\np {\n  [87 chars]   }' != '/* this is a stupid comment */\ndiv p>sp[176 chars];\n}'
        self.assertEqual(str(self.ed.data), '/* this is a stupid comment */\n'
            'div p>span["red"]~a:hover {\n'
            '    border: 5px solid red; content: "gargl"; text-decoration: none;\n'
            '}\n'
            'p {\n'
            '    font-family: Arial sans-serif;\n'
            '}\n'
            'div {\n'
            '    display: inline; float: left;\n'
            '}')

    def test_long(self):
        self.ed.return_to_source(savemode="long")
        # Traceback (most recent call last):
        # File "/home/albert/projects/cssedit/tests/unittests.py", line 406, in test_long
             #self.assertEqual(self.ed.data, '/* this is a stupid comment */\n'
        # AssertionError: b'/* this is a stupid comment */\np {\n  [87 chars]   }' != '/* this is a stupid comment */\ndiv p>sp[191 chars];\n}'
        self.assertEqual(str(self.ed.data), '/* this is a stupid comment */\n'
            'div p>span["red"]~a:hover {\n'
            '    border: 5px solid red;\n'
            '    content: "gargl";\n'
            '    text-decoration: none;\n'
            '}\n'
            'p {\n'
            '    font-family: Arial sans-serif;\n'
            '}\n'
            'div {\n'
            '    display: inline;\n'
            '    float: left;\n'
            '}')

    def test_wrongformat(self):
        with self.assertRaises(AttributeError):
            self.ed.return_to_source(savemode="compresed")

    def test_emptyformat(self):
        with self.assertRaises(AttributeError):
            self.ed.return_to_source(savemode="")
