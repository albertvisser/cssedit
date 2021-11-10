"""Unit tests for CSSEDitor
"""
import os
import sys
import types
import pytest
# import cssutils

HERE = os.path.dirname(os.path.abspath(__file__))
here = os.path.join(os.path.dirname(HERE), 'editor')
sys.path.append(here)
# import cssedit
import cssedit.editor.cssedit as cssedit

import cssedit.tests.expected_results as results
testfiles = (('compressed', os.path.join(HERE, "simplecss-compressed.css")),
             ('short', os.path.join(HERE, "simplecss-short.css")),
             ('medium', os.path.join(HERE, "simplecss-medium.css")),
             ('long', os.path.join(HERE, "simplecss-long.css")),)
formatted_css = """\
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

class Logger:
    def __init__(self, *args):
        print('called logger.__init__() with arg `{}`'.format(args[0]))
    def __str__(self):
        return 'mock logger'
    def addHandler(self, *args):
        print('called logger.addHandler() with arg `{}`'.format(args[0]))
    def setLevel(self, *args):
        print('called logger.setLevel() with arg `{}`'.format(args[0]))

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
        print('called csslog.setlog with arg `{}`'.format(args[0]))
    monkeypatch.setattr(cssedit.logging, 'FileHandler', LogHandler)
    monkeypatch.setattr(cssedit.logging, 'Formatter', LogFormatter)
    monkeypatch.setattr(cssedit.logging, 'getLogger', mock_getlogger)
    monkeypatch.setattr(cssedit.cssutils.log, 'setLog', mock_setlog)
    import pdb; pdb.set_trace()
    assert str(cssedit.set_logger('logfile')) == 'mock handler'
    assert capsys.readouterr().out == ('')


def test_load(monkeypatch, capsys):
    def mock_parsestring(*args):
        return 'called cssedit.parsestring for `{}`'.format(args[0])
    def mock_parsefile(*args):
        return 'called cssedit.parsefile for `{}`'.format(args[0])
    monkeypatch.setattr(cssedit.cssutils, 'parseString', mock_parsestring)
    monkeypatch.setattr(cssedit.cssutils, 'parseFile', mock_parsefile)
    try:
        os.mkdir('/tmp/cssedit')
    except FileExistsError:
        pass
    fname = '/tmp/cssedit/loadtest1'
    with open(fname, 'w') as f:
        f.write('nomedia')
    assert cssedit.load(fname) == 'called cssedit.parsefile for `/tmp/cssedit/loadtest1`'
    fname = '/tmp/cssedit/loadtest2'
    with open(fname, 'w') as f:
        f.write('contains @media (')
    assert cssedit.load(fname) == 'called cssedit.parsestring for `contains @media all and (`'


def test_get_for_single_tag(monkeypatch, capsys):
    monkeypatch.setattr(cssedit.cssutils, 'parseStyle', lambda x: 'parsed {}'.format(x))
    assert cssedit.get_for_single_tag('css') == 'parsed css'


def test_return_for_single_tag(monkeypatch, capsys):
    cssdata = ()
    assert cssedit.return_for_single_tag(cssdata) == ''
    cssdata = (types.SimpleNamespace(style=MockStyle()), )
    assert cssedit.return_for_single_tag(cssdata) == 'style text'


def test_parse(monkeypatch, capsys):
    monkeypatch.setattr(cssedit.cssutils, 'parseString', lambda x: 'parsed {}'.format(x))
    assert cssedit.parse('text') == 'parsed text'


def set_format(monkeypatch, capsys):
    "(nog) niet geïmplementeerd, dus ook (nog) geen unittest"


def test_save(monkeypatch, capsys):
    fname = '/tmp/cssedit/savetest.out'
    try:
        os.unlink(fname)
    except FileNotFoundError:
        pass
    backup_fname = fname + '~'
    try:
        os.unlink(backup_fname)
    except FileNotFoundError:
        pass

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
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass
    for fname, line, pos, contents, result in (('testcss1', 1, 7, ['test { stuff }', ''],
                                                'test { stuff }'),
                                               ('testcss2', 3, 0, ['}', 'test {', 'stuff', '}', ''],
                                                'test {\nstuff\n}'),
                                               ('testcss3', 1, 15, ['hallo } test { stuff2 } en'
                                                ' nog wat'], 'test { stuff2 }')):
        fname = os.path.join(dirname, fname)
        with open(fname, 'w') as f:
            f.write('\n'.join(contents))
        assert cssedit.get_definition_from_file(fname, line, pos) == result


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
    assert cssedit.parse_log_line(text) == cssedit.LogLine('right',
            '', 'line without opening parentheses is ok', -1, -1, '')
    text = 'right\tline (ok, correctly formatted, 1, 4)'
    assert cssedit.parse_log_line(text) == cssedit.LogLine('right',
            'line ok', '', 1, 4, ' correctly formatted')
    text = 'xxx\tsubject: message: data'
    assert cssedit.parse_log_line(text) == cssedit.LogLine('xxx', 'subject', 'message', -1, -1,
                                                           'data')
    text = 'yyy\tzzz: test [2:3:result   ]'
    assert cssedit.parse_log_line(text)== cssedit.LogLine('yyy', 'zzz', 'test', 2, 3, 'result')

class MockStyleSheet:
    def __init__(self, *args):
        print('called stylesheet.__init__()')
    def add(self, *args):
        print('called stylesheet.add()')
    def cssText(self):
        return 'text from stylesheet'

class MockStyleDeclaration:
    def __init__(self, *args, **kwargs):
        print('called styledeclaration.__init__()')
    def cssText(self):
        return 'text from style declaration'

class MockStyleRule:
    def __init__(self, *args, **kwargs):
        print('called stylerule.__init__()')
    def cssText(self):
        return 'text from style rule'

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
        testobj = cssedit.Editor(new=True)
        assert testobj.data == []
        assert not hasattr(testobj, 'log')
        with pytest.raises(ValueError):
            cssedit.Editor(fake=True)  # Wrong arguments
        with pytest.raises(ValueError):
            cssedit.Editor(filename='text.css', tag='style') # Ambiguous arguments
        with pytest.raises(ValueError):
            cssedit.Editor(filename='text.css', text='style') # Ambiguous arguments
        with pytest.raises(ValueError):
            cssedit.Editor(tag='style') # Not enough arguments
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
