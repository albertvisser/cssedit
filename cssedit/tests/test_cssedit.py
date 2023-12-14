"""Unit tests for CSSEDitor - herschreven voor gebruik pytest i.p.v. unittest
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
# import cssedit
from cssedit.editor import cssedit

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

class Logger:
    def __init__(self, *args):
        print(f'called logger.__init__() with arg `{args[0]}`')
    def __str__(self):
        return 'mock logger'
    def addHandler(self, *args):
        print(f'called logger.addHandler() with arg `{args[0]}`')
    def setLevel(self, *args):
        print(f'called logger.setLevel() with arg `{args[0]}`')

class LogHandler:
    def __init__(self, *args, **kwargs):
        print('called loghandler.__init__() for file `{}` mode `{}`'.format(args[0],
                                                                            kwargs['mode']))
    def __str__(self):
        return 'mock handler'
    def setFormatter(self, *args):
        print('called loghandler.setFormatter()')

class LogFormatter:
    def __init__(self, *args):
        print('called formatter.__init__()')
    def __str__(self):
        return 'formatter'

class MockStyle:
    def __init__(self, *args):
        print('called mockstyle.__init__()')
    def getCssText(self):
        return 'style text'


def _test_setlogger(monkeypatch, capsys):  # lijkt niet jofel te gaan vanwege gebruik logging?
    def mock_getlogger(*args):            # dit gaat mis omdat pytest het ook wil gebruiken?
        if args:
            print(args[0])
            return Logger(args[0])
    def mock_setlog(*args):
        print(f'called csslog.setlog with arg `{args[0]}`')
    monkeypatch.setattr(cssedit.logging, 'FileHandler', LogHandler)
    monkeypatch.setattr(cssedit.logging, 'Formatter', LogFormatter)
    monkeypatch.setattr(cssedit.logging, 'getLogger', mock_getlogger)
    monkeypatch.setattr(cssedit.cssutils.log, 'setLog', mock_setlog)
    assert str(cssedit.set_logger('logfile')) == 'mock handler'
    assert capsys.readouterr().out == ('')


def test_load(monkeypatch, capsys):
    def mock_parsestring(*args):
        return f'called cssedit.parsestring for `{args[0]}`'
    def mock_parsefile(*args):
        return f'called cssedit.parsefile for `{args[0]}`'
    monkeypatch.setattr(cssedit.cssutils, 'parseString', mock_parsestring)
    monkeypatch.setattr(cssedit.cssutils, 'parseFile', mock_parsefile)
    with contextlib.suppress(FileExistsError):
        os.mkdir('/tmp/cssedit')
    fname = '/tmp/cssedit/loadtest1'
    with open(fname, 'w') as f:
        f.write('nomedia')
    assert cssedit.load(fname) == 'called cssedit.parsefile for `/tmp/cssedit/loadtest1`'
    fname = '/tmp/cssedit/loadtest2'
    with open(fname, 'w') as f:
        f.write('contains @media (')
    assert cssedit.load(fname) == 'called cssedit.parsestring for `contains @media all and (`'


def test_get_for_single_tag(monkeypatch, capsys):
    monkeypatch.setattr(cssedit.cssutils, 'parseStyle', lambda x: f'parsed {x}')
    assert cssedit.get_for_single_tag('css') == 'parsed css'


def test_return_for_single_tag(monkeypatch, capsys):
    cssdata = ()
    assert cssedit.return_for_single_tag(cssdata) == ''
    cssdata = (types.SimpleNamespace(style=MockStyle()), )
    assert cssedit.return_for_single_tag(cssdata) == 'style text'


def test_parse(monkeypatch, capsys):
    monkeypatch.setattr(cssedit.cssutils, 'parseString', lambda x: f'parsed {x}')
    assert cssedit.parse('text') == 'parsed text'


def set_format(monkeypatch, capsys):
    "(nog) niet geïmplementeerd, dus ook (nog) geen unittest"


def test_save(monkeypatch, capsys):
    fname = '/tmp/cssedit/savetest.out'
    with contextlib.suppress(FileNotFoundError):
        os.unlink(fname)
    backup_fname = fname + '~'
    with contextlib.suppress(FileNotFoundError):
        os.unlink(backup_fname)

    data = types.SimpleNamespace(cssText=b'csstext')
    cssedit.save(data, fname)
    assert os.path.exists(fname)
    with open(fname) as f:
        test = f.read()
    assert test == 'csstext'

    data = types.SimpleNamespace(cssText=b'ook csstext')
    cssedit.save(data, fname, backup=False)
    assert not os.path.exists(backup_fname)
    with open(fname) as f:
        test = f.read()
    assert test == 'ook csstext'

    data = 'csstext'
    cssedit.save(data, fname)
    assert os.path.exists(backup_fname)
    with open(fname) as f:
        test = f.read()
    assert test == 'csstext\n'
    with open(backup_fname) as f:
        test = f.read()
    assert test == 'ook csstext'


def test_get_definition_from_file(monkeypatch, capsys):
    dirname = '/tmp/cssedit'
    with contextlib.suppress(FileExistsError):
        os.mkdir(dirname)
    for fname, line, pos, contents, result in (('testcss1', 1, 7, ['test { stuff }', ''],
                                                'test { stuff }'),
                                               ('testcss2', 3, 0, ['}', 'test {', 'stuff', '}', ''],
                                                'test {\nstuff\n}'),
                                               ('testcss3', 1, 15, ['hallo } test { stuff2 } en'
                                                ' nog wat'], 'test { stuff2 }')):
        pname = os.path.join(dirname, fname)
        with open(pname, 'w') as f:
            f.write('\n'.join(contents))
        assert cssedit.get_definition_from_file(pname, line, pos) == result


def test_init_ruledata(monkeypatch, capsys):
    assert cssedit.init_ruledata(cssedit.cssutils.css.CSSRule.STYLE_RULE) == {'selectors': [],
                                                                              'styles': {}}
    assert cssedit.init_ruledata(cssedit.cssutils.css.CSSRule.CHARSET_RULE) == {'name': ''}


def test_complete_ruledata(monkeypatch, capsys):
    cssedit.RTYPES = {'rule_class': ('rulename', [['component_name', 'component_type',
                                                   lambda x: 'result of component_function']])}
    rule = types.SimpleNamespace(type='rule_class')
    assert cssedit.complete_ruledata({}, rule) == {'component_name': 'result of component_function'}


def test_parse_log_line(monkeypatch, capsys):
    assert not cssedit.parse_log_line('wrong        Line with no tab in it')
    text = 'right\tline without opening parentheses is ok'
    assert cssedit.parse_log_line(text) == cssedit.LogLine('right', '', 'line without opening'
                                                           ' parentheses is ok', -1, -1, '')
    text = 'right\tline (ok, correctly formatted, 1, 4)'
    assert cssedit.parse_log_line(text) == cssedit.LogLine('right', 'line ok', '', 1, 4,
                                                           ' correctly formatted')
    text = 'xxx\tsubject: message: data'
    assert cssedit.parse_log_line(text) == cssedit.LogLine('xxx', 'subject', 'message', -1, -1,
                                                           'data')
    text = 'yyy\tzzz: test [2:3:result   ]'
    assert cssedit.parse_log_line(text) == cssedit.LogLine('yyy', 'zzz', 'test', 2, 3, 'result')


class MockStyleSheet:
    def __init__(self, *args):
        print('called stylesheet.__init__()')
        self.cssText = 'text from stylesheet'
    def add(self, *args):
        print('called stylesheet.add()')


class MockStyleDeclaration(dict):
    def __init__(self, *args, **kwargs):
        print('called styledeclaration.__init__()')
        self.cssText = 'text from style declaration'


class MockStyleRule(types.SimpleNamespace):
    def __init__(self, *args, **kwargs):
        print('called stylerule.__init__()')
        self.cssText = 'text from style rule'


class MockSelectorList(list):
    def __init__(self, *args, **kwargs):
        print('called selectorlist.__init__()')


class MockMediaRule(types.SimpleNamespace):
    def __init__(self, *args, **kwargs):
        print('called mediarule.__init__()')


class MockMediaList(list):
    def __init__(self, *args, **kwargs):
        print('called medialist.__init__()')


class MockRuleList(list):
    def __init__(self, *args, **kwargs):
        print('called rulelist.__init__()')


class MockComment(str):
    def __init__(self, **kwargs):
        print('called comment.__init__(`{}`)'.format(kwargs['cssText']))


class TestEditor:
    def test_init(self, monkeypatch, capsys):
        def mock_set_logger(filename):
            f = open(filename, 'w')
            f.write('log created when parsing data')
            return f
        def mock_load(*args):
            print('called cssedit.load()')
            return MockStyleSheet()
        def mock_get(*args):
            print('called cssedit.get_for_single_tag()')
            return MockStyleDeclaration()
        def mock_parse(*args):
            print('called cssedit.parse()')
            return MockStyleSheet()
        with pytest.raises(ValueError):
            cssedit.Editor()  # Not enough arguments
        with pytest.raises(TypeError):
            testobj = cssedit.Editor('snork')  # positional argument(s) only
        testobj = cssedit.Editor(new=True)
        assert testobj.data == []
        assert not hasattr(testobj, 'log')
        with pytest.raises(ValueError):
            cssedit.Editor(fake=True)  # Wrong arguments
        with pytest.raises(ValueError):
            cssedit.Editor(filename='text.css', tag='style')  # Ambiguous arguments
        with pytest.raises(ValueError):
            cssedit.Editor(filename='text.css', text='style')  # Ambiguous arguments
        with pytest.raises(ValueError):
            cssedit.Editor(tag='style')  # Not enough arguments
        with pytest.raises(ValueError):
            cssedit.Editor(filename='')  # empty filename
        monkeypatch.setattr(cssedit, 'set_logger', mock_set_logger)
        monkeypatch.setattr(cssedit, 'load', mock_load)
        testobj = cssedit.Editor(filename='text.css')
        assert type(testobj.data) == MockStyleSheet
        assert capsys.readouterr().out == ('called cssedit.load()\n'
                                           'called stylesheet.__init__()\n')
        assert testobj.log == ['log created when parsing data']
        monkeypatch.setattr(cssedit, 'get_for_single_tag', mock_get)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSStyleSheet', MockStyleSheet)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSStyleRule', MockStyleRule)
        testobj = cssedit.Editor(tag='style', text='x')
        assert capsys.readouterr().out == ('called cssedit.get_for_single_tag()\n'
                                           'called styledeclaration.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called stylerule.__init__()\n'
                                           'called stylesheet.add()\n')
        assert type(testobj.data) == MockStyleSheet
        monkeypatch.setattr(cssedit, 'parse', mock_parse)
        testobj = cssedit.Editor(text='x')
        assert capsys.readouterr().out == ('called cssedit.parse()\n'
                                           'called stylesheet.__init__()\n')
        assert type(testobj.data) == MockStyleSheet

    def test_datatotext(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called editor.__init__()')
            self.data = []
        def mock_init_ruledata(*args):
            print('called init_ruledata()')
            return {}
        def mock_complete_ruledata(*args):
            print('called complete_ruledata()')
            return args[0]
        monkeypatch.setattr(cssedit.Editor, '__init__', mock_init)
        monkeypatch.setattr(cssedit, 'init_ruledata', mock_init_ruledata)
        monkeypatch.setattr(cssedit, 'complete_ruledata', mock_complete_ruledata)
        testobj = cssedit.Editor()
        testobj.data = []
        testobj.datatotext()
        assert testobj.textdata == []
        assert capsys.readouterr().out == ('called editor.__init__()\n')
        testobj = cssedit.Editor()
        testobj.data = (types.SimpleNamespace(type='1', typeString='type 1'),)
        testobj.datatotext()
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called init_ruledata()\n'
                                           'called complete_ruledata()\n')
        assert testobj.textdata == [('type 1', {'seqnum': 0})]

    def test_texttodata(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called editor.__init__()')
            self.data = []
        monkeypatch.setattr(cssedit.Editor, '__init__', mock_init)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSStyleSheet', MockStyleSheet)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSStyleRule', MockStyleRule)
        monkeypatch.setattr(cssedit.cssutils.css, 'SelectorList', MockSelectorList)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSStyleDeclaration', MockStyleDeclaration)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSMediaRule', MockMediaRule)
        monkeypatch.setattr(cssedit.cssutils.css, 'CSSRuleList', MockRuleList)
        monkeypatch.setattr(cssedit.cssutils.stylesheets, 'MediaList', MockMediaList)
        testobj = cssedit.Editor()
        testobj.textdata = []
        testobj.texttodata()
        assert type(testobj.data) == cssedit.cssutils.css.CSSStyleSheet
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n')
        testobj = cssedit.Editor()
        testobj.textdata = [('stylerule', {'selectors': ['x'], 'styles': {'xx': 'yy'}}),
                            ('mediarule', {'media': ['y'],
                                           'rules': [('stylerule', {'selectors': ['x'],
                                                                    'styles': {'xx': 'yy'}})]}),
                            (cssedit.cssutils.css.CSSComment().typeString, {'text': 'z'}),
                            ('textrule_2', {'text': '/* z */'})]
        testobj.texttodata()
        assert type(testobj.data) == cssedit.cssutils.css.CSSStyleSheet
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
        def mock_init(self, *args):
            print('called editor.__init__()')
            self.data = []
        def mock_set_format(*args):
            print(f'called cssedit.set_format(`{args[0]}`)')
        def mock_save(*args):
            print('called cssedit.save()')
        def mock_return(*args):
            return 'returned by cssedit.return_for_single_tag()'
        monkeypatch.setattr(cssedit.Editor, '__init__', mock_init)
        monkeypatch.setattr(cssedit, 'set_format', mock_set_format)
        monkeypatch.setattr(cssedit, 'save', mock_save)
        monkeypatch.setattr(cssedit, 'return_for_single_tag', mock_return)
        testobj = cssedit.Editor()
        with pytest.raises(AttributeError):
            testobj.return_to_source(savemode='wrong')
        assert capsys.readouterr().out == ('called editor.__init__()\n')
        testobj = cssedit.Editor()
        testobj.filename = 'x'
        testobj.data = MockStyleSheet()
        testobj.return_to_source()
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called cssedit.set_format(`compressed`)\n'
                                           'called cssedit.save()\n')
        testobj = cssedit.Editor()
        testobj.filename, testobj.tag = '', 'y'
        testobj.data = MockStyleSheet()
        testobj.return_to_source()
        assert testobj.data == 'returned by cssedit.return_for_single_tag()'
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called cssedit.set_format(`compressed`)\n')
        testobj = cssedit.Editor()
        testobj.filename = testobj.tag = ''
        testobj.data = MockStyleSheet()
        testobj.return_to_source()
        assert testobj.data == 'text from stylesheet'
        assert capsys.readouterr().out == ('called editor.__init__()\n'
                                           'called stylesheet.__init__()\n'
                                           'called cssedit.set_format(`compressed`)\n')
