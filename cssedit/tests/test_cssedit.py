"""unittests for ./cssedit/editor/cssedit.py
"""
import os
import sys
import types
import contextlib
import pytest
# import cssutils

HERE = os.path.dirname(os.path.abspath(__file__))
here = os.path.join(os.path.dirname(HERE), 'editor')
sys.path.append(here)
from cssedit.editor import cssedit as testee

# import cssedit.tests.expected_results as results
# testfiles = (('compressed', os.path.join(HERE, "simplecss-compressed.css")),
#              ('short', os.path.join(HERE, "simplecss-short.css")),
#              ('medium', os.path.join(HERE, "simplecss-medium.css")),
#              ('long', os.path.join(HERE, "simplecss-long.css")),)
# formatted_css = """\
# /* this is a stupid comment */
# div p>span["red"]~a:hover {
#     border: 5px solid red;
#     text-decoration: none;
#     content: "gargl";
# }
# p {
#     font-family: Arial sans-serif
# }
# div {
#     display: inline;
#     float: left
# }"""

class MockLogger:
    """stub
    """
    def __init__(self, *args):
        print(f'called logger.__init__() with arg `{args[0]}`')
    def __str__(self):
        """stub
        """
        return 'mock logger'
    def addHandler(self, *args):
        """stub
        """
        print(f'called logger.addHandler() with arg `{args[0]}`')
    def setLevel(self, *args):
        """stub
        """
        print(f'called logger.setLevel() with arg `{args[0]}`')

class MockLogHandler:
    """stub
    """
    def __init__(self, *args, **kwargs):
        print("called loghandler.__init__() for file `{args[0]}` mode `{kwargs['mode']}")
    def __str__(self):
        """stub
        """
        return 'mock handler'
    def setFormatter(self, *args):
        """stub
        """
        print('called loghandler.setFormatter()')

class MockLogFormatter:
    """stub
    """
    def __init__(self, *args):
        print('called formatter.__init__()')
    def __str__(self):
        """stub
        """
        return 'formatter'

class MockStyle:
    """stub
    """
    def __init__(self, *args):
        print('called Style.__init__()')
    def getCssText(self):
        """stub
        """
        return 'style text'


def _test_setlogger(monkeypatch, capsys):
    """unittest for cssedit.setlogger
    """
    def mock_getlogger(*args):
        """stub
        """
        if args:
            print(args[0])
            return MockLogger(args[0])
        return None
    def mock_setlog(*args):
        """stub
        """
        print(f'called csslog.setlog with arg `{args[0]}`')
    monkeypatch.setattr(testee.logging, 'FileHandler', MockLogHandler)
    monkeypatch.setattr(testee.logging, 'Formatter', MockLogFormatter)
    monkeypatch.setattr(testee.logging, 'getLogger', mock_getlogger)
    monkeypatch.setattr(testee.cssutils.log, 'setLog', mock_setlog)
    assert str(testee.set_logger('logfile')) == 'mock handler'
    assert capsys.readouterr().out == ('')


def test_load(monkeypatch):
    """unittest for cssedit.load
    """
    def mock_parsestring(*args):
        """stub
        """
        return f'called cssedit.parsestring for `{args[0]}`'
    def mock_parsefile(*args):
        """stub
        """
        return f'called cssedit.parsefile for `{args[0]}`'
    monkeypatch.setattr(testee.cssutils, 'parseString', mock_parsestring)
    monkeypatch.setattr(testee.cssutils, 'parseFile', mock_parsefile)
    with contextlib.suppress(FileExistsError):
        os.mkdir('/tmp/cssedit')
    fname = '/tmp/cssedit/loadtest1'
    with open(fname, 'w') as f:
        f.write('nomedia')
    assert testee.load(fname) == 'called cssedit.parsefile for `/tmp/cssedit/loadtest1`'
    fname = '/tmp/cssedit/loadtest2'
    with open(fname, 'w') as f:
        f.write('contains @media (')
    assert testee.load(fname) == 'called cssedit.parsestring for `contains @media all and (`'


def test_get_for_single_tag(monkeypatch):
    """unittest for cssedit.get_for_single_tag
    """
    monkeypatch.setattr(testee.cssutils, 'parseStyle', lambda x: f'parsed {x}')
    assert testee.get_for_single_tag('css') == 'parsed css'


def test_return_for_single_tag():
    """unittest for cssedit.return_for_single_tag
    """
    cssdata = ()
    assert testee.return_for_single_tag(cssdata) == ''
    cssdata = (types.SimpleNamespace(style=MockStyle()), )
    assert testee.return_for_single_tag(cssdata) == 'style text'


def test_parse(monkeypatch):
    """unittest for cssedit.parse
    """
    monkeypatch.setattr(testee.cssutils, 'parseString', lambda x: f'parsed {x}')
    assert testee.parse('text') == 'parsed text'


def _test_set_format():
    """unittest for cssedit.set_format - (nog) niet geïmplementeerd, dus ook (nog) geen unittest
    """


def test_save():
    """unittest for cssedit.save
    """
    fname = '/tmp/cssedit/savetest.out'
    with contextlib.suppress(FileNotFoundError):
        os.unlink(fname)
    backup_fname = fname + '~'
    with contextlib.suppress(FileNotFoundError):
        os.unlink(backup_fname)

    data = types.SimpleNamespace(cssText=b'csstext')
    testee.save(data, fname)
    assert os.path.exists(fname)
    with open(fname) as f:
        test = f.read()
    assert test == 'csstext'

    data = types.SimpleNamespace(cssText=b'ook csstext')
    testee.save(data, fname, backup=False)
    assert not os.path.exists(backup_fname)
    with open(fname) as f:
        test = f.read()
    assert test == 'ook csstext'

    data = 'csstext'
    testee.save(data, fname)
    assert os.path.exists(backup_fname)
    with open(fname) as f:
        test = f.read()
    assert test == 'csstext\n'
    with open(backup_fname) as f:
        test = f.read()
    assert test == 'ook csstext'


def test_get_definition_from_file():
    """unittest for cssedit.get_definition_from_file
    """
    dirname = '/tmp/cssedit'
    with contextlib.suppress(FileExistsError):
        os.mkdir(dirname)
    assert testee.get_definition_from_file(os.path.join(dirname, 'test'), -1, 'pos') == (
            'unknown - position in css file could not be determined')
    for fname, line, pos, contents, result in (('testcss1', 1, 7, ['test { stuff }', ''],
                                                'test { stuff }'),
                                               ('testcss2', 3, 0, ['}', 'test {', 'stuff', '}', ''],
                                                'test {\nstuff\n}'),
                                               ('testcss3', 1, 15, ['hallo } test { stuff2 } en'
                                                ' nog wat'], 'test { stuff2 }')):
        pname = os.path.join(dirname, fname)
        with open(pname, 'w') as f:
            f.write('\n'.join(contents))
        assert testee.get_definition_from_file(pname, line, pos) == result


def test_init_ruledata():
    """unittest for cssedit.init_ruledata
    """
    assert testee.init_ruledata(testee.cssutils.css.CSSRule.STYLE_RULE) == {'selectors': [],
                                                                            'styles': {}}
    assert testee.init_ruledata(testee.cssutils.css.CSSRule.CHARSET_RULE) == {'name': ''}


def test_complete_ruledata():
    """unittest for cssedit.complete_ruledata
    """
    testee.RTYPES = {'rule_class': ('rulename', [['component_name', 'component_type',
                                                 lambda x: 'result of component_function']])}
    rule = types.SimpleNamespace(type='rule_class')
    assert testee.complete_ruledata({}, rule) == {'component_name': 'result of component_function'}


def test_parse_log_line():
    """unittest for cssedit.parse_log_line
    """
    assert not testee.parse_log_line('wrong        Line with no tab in it')
    text = 'right\tline without opening parentheses is ok'
    assert testee.parse_log_line(text) == testee.LogLine('right', '', 'line without opening'
                                                         ' parentheses is ok', -1, -1, '')
    text = 'right\tline (ok, correctly formatted, 1, 4)'
    assert testee.parse_log_line(text) == testee.LogLine('right', 'line ok', '', 1, 4,
                                                         ' correctly formatted')
    text = 'xxx\tsubject: message: data'
    assert testee.parse_log_line(text) == testee.LogLine('xxx', 'subject', 'message', -1, -1,
                                                         'data')
    text = 'xxx\tsubject: message'
    assert testee.parse_log_line(text) == testee.LogLine('xxx', 'subject', 'message', -1, -1,
                                                         '')
    text = 'yyy\tzzz: test [2:3:result   ]'
    assert testee.parse_log_line(text) == testee.LogLine('yyy', 'zzz', 'test', 2, 3, 'result')


class MockStyleSheet:
    """stub
    """
    def __init__(self, *args):
        print('called stylesheet.__init__()')
        self.cssText = 'text from stylesheet'
    def add(self, *args):
        """stub
        """
        print('called stylesheet.add()')
    def cssText(self, *args):
        """stub
        """
        print('called stylesheet.cssText()')


class MockStyleDeclaration(dict):
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called styledeclaration.__init__()')
        self.cssText = 'text from style declaration'


class MockStyleRule(types.SimpleNamespace):
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called stylerule.__init__()')
        self.cssText = 'text from style rule'


class MockSelectorList(list):
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called selectorlist.__init__()')


class MockMediaRule(types.SimpleNamespace):
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called mediarule.__init__()')


class MockMediaList(list):
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called medialist.__init__()')


class MockRuleList(list):
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called rulelist.__init__()')


class MockComment(str):
    """stub
    """
    def __init__(self, **kwargs):
        print(f"called comment.__init__(`{kwargs['cssText']}`)")


class TestEditor:
    """unittests for cssedit.Editor
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for Editor.init
        """
        def mock_set_logger(filename):
            """stub
            """
            print('called set_logger')  # with arg {filename}')
            f = open(filename, 'w')
            f.write('xxx')
            return f
        def mock_todata(self, text):
            print(f"called Editor.csstodata with arg '{text}'")
            return MockStyleSheet()
        def mock_todata_2(self, text):
            print(f"called Editor.csstodata with arg '{text}'")
            return None
        with pytest.raises(ValueError) as exc:
            testee.Editor()
        assert str(exc.value) == 'Not enough arguments'
        with pytest.raises(TypeError) as exc:
            testobj = testee.Editor('snork')
        assert str(exc.value) == 'Editor.__init__() takes 1 positional argument but 2 were given'
        testobj = testee.Editor(new=True)
        assert testobj.data == []
        assert not hasattr(testobj, 'log')
        with pytest.raises(ValueError) as exc:
            testee.Editor(fake=True)
        assert str(exc.value) == 'Wrong arguments'
        with pytest.raises(ValueError) as exc:
            testee.Editor(filename='text.css', tag='style')
        assert str(exc.value) == 'Ambiguous arguments'
        with pytest.raises(ValueError) as exc:
            testee.Editor(filename='text.css', text='style')
        assert str(exc.value) == 'Ambiguous arguments'
        with pytest.raises(ValueError) as exc:
            testee.Editor(tag='style')
        assert str(exc.value) == 'Not enough arguments'
        with pytest.raises(ValueError) as exc:
            testee.Editor(filename='')
        assert str(exc.value) == 'Not enough arguments'

        monkeypatch.setattr(testee, 'set_logger', mock_set_logger)
        monkeypatch.setattr(testee.Editor, 'csstodata', mock_todata)
        testobj = testee.Editor(text='x')
        assert testobj.data is not None
        assert testobj.log == ['xxx']
        assert capsys.readouterr().out == ("called set_logger\n"
                                           "called Editor.csstodata with arg 'x'\n"
                                           "called stylesheet.__init__()\n")

        monkeypatch.setattr(testee.Editor, 'csstodata', mock_todata_2)
        with pytest.raises(ValueError) as exc:
            testobj = testee.Editor(text='x')
        assert str(exc.value) == 'Invalid style data'

    def test_csstodata(self, monkeypatch, capsys):
        """unittest for Editor.csstodata
        """
        def mock_init(self, *args):
            """stub
            """
            print('called editor.__init__()')
        def mock_load(*args):
            """stub
            """
            print('called cssedit.load with args', args)
            return MockStyleSheet()
        def mock_get(*args):
            """stub
            """
            print('called cssedit.get_for_single_tag()')
            return MockStyleDeclaration()
        def mock_parse(*args):
            """stub
            """
            print('called cssedit.parse()')
            return MockStyleSheet()
        def mock_parse_2(*args):
            """stub
            """
            print('called cssedit.parse()')
            return None
        def mock_text(*args):
            """stub
            """
            print('called stylesheet.cssText()')
            return ''

        monkeypatch.setattr(testee.cssutils.css, 'CSSStyleSheet', MockStyleSheet)
        monkeypatch.setattr(testee.cssutils.css, 'CSSStyleRule', MockStyleRule)
        monkeypatch.setattr(testee, 'load', mock_load)
        monkeypatch.setattr(testee, 'get_for_single_tag', mock_get)
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        monkeypatch.setattr(testee, 'parse', mock_parse)
        testobj = testee.Editor()
        assert capsys.readouterr().out == 'called editor.__init__()\n'

        testobj.filename = 'xx'
        testobj.tag = 'yyy'
        result = testobj.csstodata('zzz')
        assert isinstance(result, MockStyleSheet)
        assert capsys.readouterr().out == ("called cssedit.load with args ('xx',)\n"
                                           'called stylesheet.__init__()\n')

        testobj.filename = ''
        testobj.tag = 'yyy'
        result = testobj.csstodata('zzz')
        assert isinstance(result, MockStyleSheet)
        assert capsys.readouterr().out == ('called cssedit.get_for_single_tag()\n'
                                           'called styledeclaration.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called stylerule.__init__()\n'
                                           'called stylesheet.add()\n')

        # monkeypatch.setattr(MockStyleSheet, 'cssText', mock_text)
        # monkeypatch.setattr(testee.cssutils.css, 'CSSStyleSheet', MockStyleSheet)
        testobj.filename = ''
        testobj.tag = ''
        result = testobj.csstodata('zzz')
        assert isinstance(result, MockStyleSheet)
        assert capsys.readouterr().out == ('called cssedit.parse()\n'
                                           'called stylesheet.__init__()\n')

        monkeypatch.setattr(testee, 'parse', mock_parse_2)
        testobj.filename = ''
        testobj.tag = ''
        result = testobj.csstodata('zzz')
        assert result is None
        assert capsys.readouterr().out == 'called cssedit.parse()\n'

    def test_datatotext(self, monkeypatch, capsys):
        """unittest for Editor.datatotext
        """
        def mock_init(self, *args):
            """stub
            """
            print('called editor.__init__()')
            self.data = []
        def mock_init_ruledata(*args):
            """stub
            """
            print('called init_ruledata()')
            return {}
        def mock_complete_ruledata(*args):
            """stub
            """
            print('called complete_ruledata()')
            return args[0]
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        monkeypatch.setattr(testee, 'init_ruledata', mock_init_ruledata)
        monkeypatch.setattr(testee, 'complete_ruledata', mock_complete_ruledata)
        testobj = testee.Editor()
        testobj.data = []
        testobj.datatotext()
        assert not testobj.textdata  # == []
        assert capsys.readouterr().out == ('called editor.__init__()\n')
        testobj = testee.Editor()
        testobj.data = (types.SimpleNamespace(type='1', typeString='type 1'),)
        testobj.datatotext()
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called init_ruledata()\n'
                                           'called complete_ruledata()\n')
        assert testobj.textdata == [('type 1', {'seqnum': 0})]

    def test_texttodata(self, monkeypatch, capsys):
        """unittest for Editor.texttodata
        """
        def mock_init(self, *args):
            """stub
            """
            print('called editor.__init__()')
            self.data = []
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        monkeypatch.setattr(testee.cssutils.css, 'CSSStyleSheet', MockStyleSheet)
        monkeypatch.setattr(testee.cssutils.css, 'CSSStyleRule', MockStyleRule)
        monkeypatch.setattr(testee.cssutils.css, 'SelectorList', MockSelectorList)
        monkeypatch.setattr(testee.cssutils.css, 'CSSStyleDeclaration', MockStyleDeclaration)
        monkeypatch.setattr(testee.cssutils.css, 'CSSMediaRule', MockMediaRule)
        monkeypatch.setattr(testee.cssutils.css, 'CSSRuleList', MockRuleList)
        monkeypatch.setattr(testee.cssutils.stylesheets, 'MediaList', MockMediaList)
        testobj = testee.Editor()
        testobj.textdata = []
        testobj.texttodata()
        assert isinstance(testobj.data, testee.cssutils.css.CSSStyleSheet)
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n')
        testobj = testee.Editor()
        testobj.textdata = [('stylerule', {'selectors': ['x'], 'styles': {'xx': 'yy'}}),
                            ('mediarule', {'media': ['y'],
                                           'rules': [('stylerule', {'selectors': ['x'],
                                                                    'styles': {'xx': 'yy'}})]}),
                            (testee.cssutils.css.CSSComment().typeString, {'text': 'z'}),
                            ('textrule_2', {'text': '/* z */'})]
        testobj.texttodata()
        assert isinstance(testobj.data, testee.cssutils.css.CSSStyleSheet)
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called stylerule.__init__()\n'
                                           'called selectorlist.__init__()\n'
                                           'called styledeclaration.__init__()\n'
                                           'called stylesheet.add()\n'
                                           'called mediarule.__init__()\n'
                                           'called medialist.__init__()\n'
                                           'called rulelist.__init__()\n'
                                           'called stylerule.__init__()\n'
                                           'called selectorlist.__init__()\n'
                                           'called styledeclaration.__init__()\n'
                                           'called stylesheet.add()\n'
                                           'called stylesheet.add()\n'
                                           'called stylesheet.add()\n')

    def test_return_to_source(self, monkeypatch, capsys):
        """unittest for Editor.return_to_source
        """
        def mock_init(self, *args):
            """stub
            """
            print('called editor.__init__()')
            self.data = []
        def mock_set_format(*args):
            """stub
            """
            print(f'called cssedit.set_format(`{args[0]}`)')
        def mock_save(*args):
            """stub
            """
            print('called cssedit.save()')
        def mock_return(*args):
            """stub
            """
            return 'returned by cssedit.return_for_single_tag()'
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        monkeypatch.setattr(testee, 'set_format', mock_set_format)
        monkeypatch.setattr(testee, 'save', mock_save)
        monkeypatch.setattr(testee, 'return_for_single_tag', mock_return)
        testobj = testee.Editor()
        with pytest.raises(AttributeError):
            testobj.return_to_source(savemode='wrong')
        assert capsys.readouterr().out == ('called editor.__init__()\n')
        testobj = testee.Editor()
        testobj.filename = 'x'
        testobj.data = MockStyleSheet()
        testobj.return_to_source()
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called cssedit.set_format(`compressed`)\n'
                                           'called cssedit.save()\n')
        testobj = testee.Editor()
        testobj.filename, testobj.tag = '', 'y'
        testobj.data = MockStyleSheet()
        testobj.return_to_source()
        assert testobj.data == 'returned by cssedit.return_for_single_tag()'
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called cssedit.set_format(`compressed`)\n')
        testobj = testee.Editor()
        testobj.filename = testobj.tag = ''
        testobj.data = MockStyleSheet()
        testobj.return_to_source()
        assert testobj.data == 'text from stylesheet'
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called cssedit.set_format(`compressed`)\n')
