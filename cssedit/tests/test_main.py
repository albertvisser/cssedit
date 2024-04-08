"""unittests for ./cssedit/editor/main.py
"""
import types
import pytest
from cssedit.editor import main as testee

class MockEditor:
    """stub for editor.cssedit.Editor object
    """
    def __init__(self, *args, **kwargs):
        print('called CSSUtilsWrapper.__init__ with args', args, kwargs)
    def datatotext(self):
        print('called CSSUtilsWrapper.datatotext')
    def texttodata(self):
        print('called CSSUtilsWrapper.texttodata')
    def return_to_source(self, *args, **kwargs):
        print('called CSSUtilsWrapper.return_to_source with args', args, kwargs)


class MockTree:
    """stub for editor.gui.TreePanel object
    """
    def __init__(self, *args, **kwargs):
        print('called TreePanel.__init__ with args', args, kwargs)
    def remove_root(self):
        print('called TreePanel.remove_root')
    def init_root(self):
        print('called TreePanel.init_root')
    def set_activeitem(self, arg):
        print('called TreePanel.set_activeitem with arg', arg)
    def expand_item(self, arg):
        print('called TreePanel.expand_item with arg', arg)
    def setcurrent(self, arg):
        print('called TreePanel.setcurrent with arg', arg)
    def getcurrent(self):
        print('called TreePanel.getcurrent')
        return 'current item'
    def set_root_text(self, name):
        print(f"called TreePanel.set_root_text with arg '{name}'")
    def activate_rootitem(self):
        print('called TreePanel.activate_rootitem')
    def set_focus(self):
        print('called TreePanel.set_focus')
    def new_treeitem(self, *args):
        print('called TreePanel.new_treeitem with args', args)
    def add_to_parent(self, *args):
        print('called TreePanel.add_to_parent with args', args)
        return 'new item'
    def add_subitem(self, *args):
        print('called TreePanel.add_subitem with args', args)
    def get_subitems(self, arg):
        print(f'called TreePanel.get_subitems with arg {arg}')
        return ['item-1', 'item-2']
    def get_itemtext(self, arg):
        print(f'called TreePanel.get_itemtext with arg {arg}')
        return 'itemtext'
    def set_itemtext(self, *args):
        print('called TreePanel.set_itemtext with args', args)


class MockGui:
    """stub for editor.gui.MainGui object
    """
    def __init__(self, *args, **kwargs):
        print('called MainGui.__init__ with args', args, kwargs)
        self.tree = MockTree()
    def set_window_title(self, arg):
        print(f'called MainGui.set_window_title with arg `{arg}`')
    def show_statusmessage(self, message):
        print(f"called MainGui.show_statusmessage with arg '{message}'")
    def show_message(self, arg):
        print(f'called MainGui.show_message with arg `{arg}`')
    def create_menu(self, menudata):
        print(f"called MainGui.create_menu with arg '{menudata}'")
    def just_show(self):
        print("called MainGui.just_show")
    def set_modality_and_show(self, arg):
        print(f"called MainGui.set_modality_and_show with arg {arg}")
    def show_save_dialog(self, *args):
        print('called MainGui.show_save_dialog with args', args)
        return ''
    def show_open_dialog(self, *args):
        print('called MainGui.show_open_dialog with args', args)
        return 'x'
    def get_itemtext(self, arg):
        print('called MainGui.get_itemtext with arg `{arg}`')
        return arg
    def get_input_choice(self, *args):
        print('called MainGui.get_input_choice with args', args)
        return '', False
    def close(self):
        print('called MainGui.close')


class MockTextDialog:
    """stub for editor.gui.TextDialog object
    """
    def __init__(self):
        print('called TextDialog.__init__()')


class MockListDialog:
    """stub for editor.gui.ListDialog object
    """
    def __init__(self):
        print('called ListDialog.__init__()')


class MockGridDialog:
    """stub for editor.gui.GridDialog object
    """
    def __init__(self):
        print('called GridDialog.__init__()')


def test_get_ruletype_for_name(monkeypatch):
    """unittest for main.get_ruletype_for_name
    """
    monkeypatch.setattr(testee.ed, 'RTYPES', {'a': ['aa'], 'b': ['bb']})
    assert testee.get_ruletype_for_name('aa') == 'a'
    assert testee.get_ruletype_for_name('xx') is None


class TestEditor:
    """unittest for editor.main.Editor
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Editor object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Editor.__init__ with args', args)
        monkeypatch.setattr(testee.Editor, "__init__", mock_init)
        testobj = testee.Editor()
        testobj.gui = MockGui()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called MainGui.__init__ with args () {}\n'
                                           'called TreePanel.__init__ with args () {}\n')
        return testobj

    def mock_check(self):
        """stub for Editor.checkselection
        """
        print('called Editor.checkselection')
        return True

    def mock_check_false(self):
        """stub for Editor.checkselection
        """
        print('called Editor.checkselection')
        return False

    def mock_mark_dirty(self, value):
        """stub for Editor.mark_dirty
        """
        print(f'called Editor.mark_dirty with arg {value}')

    def mock_add(self, **kwargs):
        """stub for Editor.add_rule
        """
        print('called Editor.add_rule with args', kwargs)

    def mock_copy(self, **kwargs):
        """stu for Editor._copy_rule
        """
        print('called Editor._copy_rule with kwargs', kwargs)

    def mock_paste(self, **kwargs):
        """stub for Editor._paste_rule
        """
        print('called Editor._paste_rule with kwargs', kwargs)

    def test_init(self, monkeypatch, capsys):
        """unittest for Editor.__init__
        """
        def mock_get_menu_data(self):
            print('called Editor.get_menu_data')
            return "data for menu"
        def mock_newfile(self):
            print('called Editor.newfile')
        monkeypatch.setattr(testee.gui, 'MainGui', MockGui)
        monkeypatch.setattr(testee.Editor, "newfile", mock_newfile)
        monkeypatch.setattr(testee.Editor, "get_menu_data", mock_get_menu_data)
        testobj = testee.Editor(parent=None)  # , parentpos=(0, 0), app=None) == "expected_result"
        assert testobj.parent is None
        assert testobj.app_title == "CSSEdit"
        assert testobj.app_iconame == f'{testee.HERE}/csseditor.png'
        assert hasattr(testobj, 'gui')  # isinstance(testobj.gui, testee.gui.MainGui)
        assert testobj.mode == ''
        assert testobj.actiondict == {}
        assert testobj.css is None
        assert (testobj.cut_item, testobj.cutlevel) == (None, 0)
        assert capsys.readouterr().out == (
                f"called MainGui.__init__ with args ({testobj}, None) {{'pos': (0, 0)}}\n"
                "called TreePanel.__init__ with args () {}\n"
                "called MainGui.show_statusmessage with arg 'Ready'\n"
                "called Editor.get_menu_data\n"
                f"called MainGui.create_menu with arg 'data for menu'\n"
                "called Editor.newfile\n")

    def test_show_gui(self, monkeypatch, capsys):
        """unittest for Editor.show_gui
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_gui()
        assert capsys.readouterr().out == 'called MainGui.just_show\n'

    def test_show_from_external(self, monkeypatch, capsys):
        """unittest for Editor.show_from_external
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_from_external()
        assert capsys.readouterr().out == 'called MainGui.set_modality_and_show with arg True\n'
        testobj.show_from_external(modal=False)
        assert capsys.readouterr().out == 'called MainGui.set_modality_and_show with arg False\n'

    def test_getfilename(self, monkeypatch, capsys):
        """unittest for Editor.getfilename
        """
        def mock_cwd():
            print('called os.getcwd')
            return 'here'
        monkeypatch.setattr(testee.os, 'getcwd', mock_cwd)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getfilename() == (True, 'x')
        assert capsys.readouterr().out == (
                "called os.getcwd\n"
                "called MainGui.show_open_dialog with args ('here', 'CSS files (*.css)')\n")
        assert testobj.getfilename('xxx', 'yyy', True) == (False, '')
        assert capsys.readouterr().out == (
                "called MainGui.show_save_dialog with args ('yyy', 'CSS files (*.css)')\n")

    def test_newfile(self, monkeypatch, capsys):
        """unittest for Editor.newfile
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.ed, 'Editor', MockEditor)
        testobj.mark_dirty = self.mock_mark_dirty
        testobj.gui.tree.root = 'xxx'
        testobj.newfile()
        assert testobj.project_file == ''
        assert isinstance(testobj.css, testee.ed.Editor)
        assert capsys.readouterr().out == (
                "called TreePanel.remove_root\n"
                "called CSSUtilsWrapper.__init__ with args () {'new': True}\n"
                "called TreePanel.init_root\n"
                "called TreePanel.set_activeitem with arg xxx\n"
                "called TreePanel.expand_item with arg xxx\n"
                "called Editor.mark_dirty with arg False\n")

    def test_open(self, monkeypatch, capsys):
        """unittest for Editor.open
        """
        class MockWaitCursor:
            """stub
            """
            def __enter__(self):
                print('called WaitCursor.__enter__')
            def __exit__(self, *args):
                print('called WaitCursor.__exit__')
        def mock_newfile():
            print('called Editor.newfile')
        def mock_abspath(arg):
            return f'HERE/{arg}'
        def mock_texttotree():
            print('called Editor.texttotree')
        def mock_build_loaded_message():
            print("called Editor.build_loaded_message")
            return 'loaded'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.newfile = mock_newfile
        testobj.wait_cursor = MockWaitCursor
        monkeypatch.setattr(testee.ed, 'Editor', MockEditor)
        monkeypatch.setattr(testee.os.path, 'abspath', mock_abspath)
        testobj.texttotree = mock_texttotree
        testobj.build_loaded_message = mock_build_loaded_message
        testobj.open(filename='xxx')
        assert testobj.mode == 'file'
        assert testobj.project_file == 'HERE/xxx'
        assert capsys.readouterr().out == (
                "called Editor.newfile\n"
                "called TreePanel.set_root_text with arg 'HERE/xxx'\n"
                "called WaitCursor.__enter__\n"
                "called CSSUtilsWrapper.__init__ with args () {'filename': 'xxx'}\n"
                "called CSSUtilsWrapper.datatotext\n"
                "called Editor.texttotree\ncalled WaitCursor.__exit__\n"
                "called Editor.build_loaded_message\n"
                "called MainGui.show_statusmessage with arg 'loaded'\n"
                "called TreePanel.activate_rootitem\n"
                "called TreePanel.set_focus\n")
        testobj.open(tag='xxx')
        assert testobj.mode == 'tag'
        assert testobj.project_file == ''
        assert capsys.readouterr().out == (
                "called Editor.newfile\n"
                "called TreePanel.set_root_text with arg '(no file)'\n"
                "called WaitCursor.__enter__\n"
                "called CSSUtilsWrapper.__init__ with args () {'tag': 'xxx'}\n"
                "called CSSUtilsWrapper.datatotext\n"
                "called Editor.texttotree\ncalled WaitCursor.__exit__\n"
                "called Editor.build_loaded_message\n"
                "called MainGui.show_statusmessage with arg 'loaded'\n"
                "called TreePanel.activate_rootitem\n"
                "called TreePanel.set_focus\n")
        testobj.open()
        assert testobj.mode == 'text'
        assert testobj.project_file == ''
        assert capsys.readouterr().out == (
                "called Editor.newfile\n"
                "called TreePanel.set_root_text with arg '(no file)'\n"
                "called WaitCursor.__enter__\n"
                "called CSSUtilsWrapper.__init__ with args () {}\n"
                "called CSSUtilsWrapper.datatotext\n"
                "called Editor.texttotree\ncalled WaitCursor.__exit__\n"
                "called Editor.build_loaded_message\n"
                "called MainGui.show_statusmessage with arg 'loaded'\n"
                "called TreePanel.activate_rootitem\n"
                "called TreePanel.set_focus\n")

    def test_build_loaded_message(self, monkeypatch, capsys):
        """unittest for Editor.build_loaded_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.css = types.SimpleNamespace()
        testobj.css.log = ['WARNING: xxx', 'WARNING: xxx']
        assert testobj.build_loaded_message() == "file loaded with 2 warnings"
        testobj.css.log = ['ERROR: xxx', 'ERROR: xxx']
        assert testobj.build_loaded_message() == "file loaded with 2 errors"
        testobj.css.log = ['xxx', 'xxx']
        assert testobj.build_loaded_message() == "file loaded with 2 misc. messages"
        testobj.css.log = ['WARNING: xxx', 'ERROR: xxx']
        assert testobj.build_loaded_message() == "file loaded with 1 warnings and 1 errors"
        testobj.css.log = ['WARNING: xxx', 'xxx']
        assert testobj.build_loaded_message() == "file loaded with 1 warnings and 1 misc. messages"
        testobj.css.log = ['WARNING: xxx', 'ERROR: xxx', 'xxx']
        assert testobj.build_loaded_message() == (
                "file loaded with 1 warnings, 1 errors and 1 misc. messages")
        testobj.css.log = ['ERROR: xxx', 'xxx']
        assert testobj.build_loaded_message() == "file loaded with 1 errors and 1 misc. messages"
        testobj.css.log = ['xxx', 'ERROR: xxx', 'WARNING: xxx']
        assert testobj.build_loaded_message() == (
                "file loaded with 1 warnings, 1 errors and 1 misc. messages")

    def test_openfile(self, monkeypatch, capsys):
        """unittest for Editor.openfile
        """
        def mock_get(*args, **kwargs):
            print('called Editor.getfilename with args', args, kwargs)
            return False, ''
        def mock_get_2(*args, **kwargs):
            print('called Editor.getfilename with args', args, kwargs)
            return True, 'yyy'
        def mock_open(*args, **kwargs):
            print('called Editor.open with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getfilename = mock_get
        testobj.app_title = 'xxx'
        testobj.open = mock_open
        testobj.openfile()
        assert capsys.readouterr().out == (
                "called Editor.getfilename with args () {'title': 'xxx - open file'}\n")
        testobj.getfilename = mock_get_2
        testobj.openfile()
        assert capsys.readouterr().out == (
                "called Editor.getfilename with args () {'title': 'xxx - open file'}\n"
                "called Editor.open with args () {'filename': 'yyy'}\n")

    def test_reopenfile(self, monkeypatch, capsys):
        """unittest for Editor.reopenfile
        """
        def mock_open(*args, **kwargs):
            print('called Editor.open with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'xxx'
        testobj.open = mock_open
        testobj.reopenfile()
        assert capsys.readouterr().out == "called Editor.open with args () {'filename': 'xxx'}\n"

    def test_texttotree(self, monkeypatch, capsys):
        """unittest for Editor.texttotree
        """
        def mock_read_rules(*args):
            print('called Editor.read_rules with args', args)
            return ['rule', 'another rule']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.read_rules = mock_read_rules
        testobj.gui.tree.root = 'this'
        testobj.css = types.SimpleNamespace()
        testobj.css.textdata = ['stuff', 'more stuff']
        testobj.texttotree()
        assert capsys.readouterr().out == (
                "called Editor.read_rules with args (['stuff', 'more stuff'],)\n"
                "called TreePanel.add_subitem with args ('this', 'rule')\n"
                "called TreePanel.add_subitem with args ('this', 'another rule')\n")

    def test_treetotext(self, monkeypatch, capsys):
        """unittest for Editor.treetotext
        """
        counter = 0
        def mock_get_subitems(arg):
            nonlocal counter
            print('called TreePanel.get_subitems with arg', arg)
            counter += 1
            if counter == 2:
                return ['xx', 'yy', 'zz', 'aa', 'bb', 'cc', 'dd']
            return [f'x{counter}']
        tcounter = 0
        def mock_get_itemtext(arg):
            nonlocal tcounter
            print('called TreePanel.get_itemtext with arg', arg)
            tcounter += 1
            if tcounter in (2, 4, 6, 8, 10, 12):
                return ['text', 'data', 'selectors', 'media', 'rules', 'styles'][tcounter // 2 - 1]
            return f'y{tcounter}'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.root = 'here'
        testobj.gui.tree.get_subitems = mock_get_subitems
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert testobj.treetotext() == [
                ('y1', {'text': 'y3', 'data': 'y5', 'selectors': ['y7'], 'media': ['y9'],
                        'rules': ['y11'], 'styles': {'y13': 'y14'}, 'y15': None})]
        assert capsys.readouterr().out == ("called TreePanel.get_subitems with arg here\n"
                                           "called TreePanel.get_itemtext with arg x1\n"
                                           "called TreePanel.get_subitems with arg x1\n"
                                           "called TreePanel.get_itemtext with arg xx\n"
                                           "called TreePanel.get_subitems with arg xx\n"
                                           "called TreePanel.get_itemtext with arg x3\n"
                                           "called TreePanel.get_itemtext with arg yy\n"
                                           "called TreePanel.get_subitems with arg yy\n"
                                           "called TreePanel.get_itemtext with arg x4\n"
                                           "called TreePanel.get_itemtext with arg zz\n"
                                           "called TreePanel.get_subitems with arg zz\n"
                                           "called TreePanel.get_itemtext with arg x5\n"
                                           "called TreePanel.get_itemtext with arg aa\n"
                                           "called TreePanel.get_subitems with arg aa\n"
                                           "called TreePanel.get_itemtext with arg x6\n"
                                           "called TreePanel.get_itemtext with arg bb\n"
                                           "called TreePanel.get_subitems with arg bb\n"
                                           "called TreePanel.get_itemtext with arg x7\n"
                                           "called TreePanel.get_itemtext with arg cc\n"
                                           "called TreePanel.get_subitems with arg cc\n"
                                           "called TreePanel.get_itemtext with arg x8\n"
                                           "called TreePanel.get_subitems with arg x8\n"
                                           "called TreePanel.get_itemtext with arg x9\n"
                                           "called TreePanel.get_itemtext with arg dd\n")

    def test_savefile(self, monkeypatch, capsys):
        """unittest for Editor.savefile
        """
        def mock_save():
            print('called Editor.save')
        def mock_savefileas():
            print('called Editor.savefileas')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.save = mock_save
        testobj.savefileas = mock_savefileas
        testobj.project_file = 'x'
        testobj.savefile()
        assert capsys.readouterr().out == 'called Editor.save\n'
        testobj.project_file = ''
        testobj.savefile()
        assert capsys.readouterr().out == 'called Editor.savefileas\n'

    def test_savefileas(self, monkeypatch, capsys):
        """unittest for Editor.savefileas
        """
        def mock_get_cancel(*args, **kwargs):
            print('called Editor.getfilename with args', args, kwargs)
            return False, ''
        def mock_get_ok(*args, **kwargs):
            print('called Editor.getfilename with args', args, kwargs)
            return True, 'xxx'
        def mock_save():
            print('called Editor.save')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app_title = 'A Title'
        testobj.project_file = 'x'
        testobj.getfilename = mock_get_cancel
        testobj.save = mock_save
        testobj.savefileas()
        assert capsys.readouterr().out == (
                "called Editor.getfilename with args"
                " () {'title': 'A Title - save file as', 'start': 'x', 'save': True}\n")
        testobj.getfilename = mock_get_ok
        testobj.savefileas()
        assert capsys.readouterr().out == (
                "called Editor.getfilename with args"
                " () {'title': 'A Title - save file as', 'start': 'x', 'save': True}\n"
                "called Editor.save\n"
                "called TreePanel.set_root_text with arg 'xxx'\n")

    def test_save(self, monkeypatch, capsys):
        """unittest for Editor.save
        """
        class MockWaitCursor:
            """stub
            """
            def __enter__(self):
                print('called WaitCursor.__enter__')
            def __exit__(self, *args):
                print('called WaitCursor.__exit__')
        def mock_treetotext():
            print('called Editor.treetotext')
            return 'text from tree'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'xxx'
        testobj.treetotext = mock_treetotext
        testobj.mark_dirty = self.mock_mark_dirty
        testobj.css = MockEditor()
        assert capsys.readouterr().out == 'called CSSUtilsWrapper.__init__ with args () {}\n'
        testobj.wait_cursor = MockWaitCursor
        testobj.save()
        assert capsys.readouterr().out == ("called WaitCursor.__enter__\n"
                                           "called Editor.treetotext\n"
                                           "called CSSUtilsWrapper.texttodata\n"
                                           "called CSSUtilsWrapper.return_to_source with args () {}\n"
                                           "called WaitCursor.__exit__\n"
                                           "called Editor.mark_dirty with arg False\n")

    def test_show_log(self, monkeypatch, capsys):
        """unittest for Editor.show_log
        """
        def mock_log(*args):
            print('called LogDialog with args', args)
        monkeypatch.setattr(testee.gui, 'LogDialog', mock_log)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.css = None  # types.SimpleNamespace()  # ''
        testobj.show_log()
        assert capsys.readouterr().out == (
                "called MainGui.show_statusmessage with arg 'Load a css file first'\n")
        testobj.css = types.SimpleNamespace(log='xyz')
        testobj.show_log()
        assert capsys.readouterr().out == f"called LogDialog with args ({testobj.gui}, 'xyz')\n"

    def test_exit(self, monkeypatch, capsys):
        """unittest for Editor.exit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.exit()
        assert capsys.readouterr().out == "called MainGui.close\n"

    def test_close(self, monkeypatch, capsys):
        """unittest for Editor.close
        """
        def mock_treetotext():
            print('called Editor.treetotext')
            return 'text from tree'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'xxx'
        testobj.treetotext = mock_treetotext
        testobj.parent = None
        testobj.close()
        assert capsys.readouterr().out == ""
        testobj.parent = types.SimpleNamespace()
        testobj.css = MockEditor()
        assert capsys.readouterr().out == "called CSSUtilsWrapper.__init__ with args () {}\n"
        testobj.css.data = 'styletext'
        testobj.close()
        assert testobj.parent.styledata == 'styletext'
        assert testobj.parent.cssfilename == 'xxx'
        assert capsys.readouterr().out == (
                "called Editor.treetotext\n"
                "called CSSUtilsWrapper.texttodata\n"
                "called CSSUtilsWrapper.return_to_source with args () {'savemode': 'compressed'}\n"
                "trying to decode data.cssText\n"
                "taking data as-is\n"
                "'sometimes it's not bytes but already a string\n")
        testobj.css.data = types.SimpleNamespace(cssText='text')
        testobj.close()
        assert testobj.parent.styledata == 'text'
        assert testobj.parent.cssfilename == 'xxx'
        assert capsys.readouterr().out == (
                "called Editor.treetotext\n"
                "called CSSUtilsWrapper.texttodata\n"
                "called CSSUtilsWrapper.return_to_source with args () {'savemode': 'compressed'}\n"
                "trying to decode data.cssText\n"
                # "taking data as-is\n"
                "'sometimes it's not bytes but already a string\n")
        testobj.css.data = b'styletext'
        testobj.close()
        assert testobj.parent.styledata == 'styletext'
        assert testobj.parent.cssfilename == 'xxx'
        assert capsys.readouterr().out == (
                "called Editor.treetotext\n"
                "called CSSUtilsWrapper.texttodata\n"
                "called CSSUtilsWrapper.return_to_source with args () {'savemode': 'compressed'}\n"
                "trying to decode data.cssText\n"
                "taking data as-is\n")

    def test_wait_cursor(self, monkeypatch, capsys):
        """unittest for Editor.wait_cursor
        """
        def mock_set_cursor(arg):
            print(f'called MockEditorGui.set_waitcursor with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.set_waitcursor = mock_set_cursor
        with testobj.wait_cursor():
            pass
        assert capsys.readouterr().out == ("called MockEditorGui.set_waitcursor with arg True\n"
                                           "called MockEditorGui.set_waitcursor with arg False\n")

    def test_determine_level(self, monkeypatch, capsys):
        """unittest for Editor.determine_level
        """
        def mock_getitemparentpos_0(arg):
            print(f'called Tree.getitemparentpos with arg {arg}')
            return 'root', 0
        counter = 0
        expected_level = 3
        def mock_getitemparentpos(arg):
            nonlocal counter
            print(f'called Tree.getitemparentpos with arg {arg}')
            if counter == expected_level:
                return 'root', 0
            counter += 1
            return f'item-{counter}', 0
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.root = 'root'
        testobj.gui.tree.getitemparentpos = mock_getitemparentpos_0
        assert testobj.determine_level('root') == 0
        assert capsys.readouterr().out == "called Tree.getitemparentpos with arg root\n"
        testobj.gui.tree.getitemparentpos = mock_getitemparentpos
        assert testobj.determine_level('testitem') == expected_level
        assert capsys.readouterr().out == ("called Tree.getitemparentpos with arg testitem\n"
                                           "called Tree.getitemparentpos with arg item-1\n"
                                           "called Tree.getitemparentpos with arg item-2\n"
                                           "called Tree.getitemparentpos with arg item-3\n")

    def test_checkselection(self, monkeypatch, capsys):
        """unittest for Editor.checkselection
        """
        expected_level = 2
        def mock_get_return_none():
            print('called Tree.getcurrent')
        def mock_get():
            print('called Tree.getcurrent')
            return 'item'
        def mock_level(arg):
            print(f'called Editor.determine_level with arg `{arg}`')
            return expected_level
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.determine_level = mock_level
        testobj.gui.tree.getcurrent = mock_get_return_none
        assert not testobj.checkselection()
        assert testobj.itemlevel == 0
        assert capsys.readouterr().out == ("called Tree.getcurrent\n"
                                           "called MainGui.show_message with arg"
                                           " `You need to select an element or text first`\n")
        testobj.gui.tree.root = 'item'
        testobj.gui.tree.getcurrent = mock_get
        assert not testobj.checkselection()
        assert testobj.itemlevel == 0
        assert capsys.readouterr().out == ("called Tree.getcurrent\n"
                                           "called MainGui.show_message with arg"
                                           " `You need to select an element or text first`\n")
        testobj.gui.tree.root = 'root'
        testobj.gui.tree.getcurrent = mock_get
        assert testobj.checkselection()
        assert testobj.itemlevel == expected_level
        assert capsys.readouterr().out == ("called Tree.getcurrent\n"
                                           "called Editor.determine_level with arg `item`\n")

    def test_is_rule_parent(self, monkeypatch, capsys):
        """unittest for Editor.is_rule_parent
        """
        def mock_get_itemtext(arg):
            print('called TreePanel.get_itemtext with arg', arg)
            return 'rules'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.root = 'item'
        assert testobj.is_rule_parent('item')
        assert capsys.readouterr().out == ("")
        testobj.gui.tree.root = 'root'
        assert not testobj.is_rule_parent('item')
        assert capsys.readouterr().out == (
                "called TreePanel.get_itemtext with arg item\n"
                "called MainGui.show_message with arg `Can't add or paste rule here`\n")
        monkeypatch.setattr(testobj.gui.tree, 'get_itemtext', mock_get_itemtext)
        assert testobj.is_rule_parent('item')
        assert capsys.readouterr().out == "called TreePanel.get_itemtext with arg item\n"

    def test_is_rule_item(self, monkeypatch, capsys):
        """unittest for Editor.is_rule_item
        """
        monkeypatch.setattr(testee, 'RTYPES', ('x', 'y'))
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.is_rule_item('item')
        assert capsys.readouterr().out == (
                "called TreePanel.get_itemtext with arg item\n"
                "called MainGui.show_message with arg `Can't do this; itemtext is not a rule item`\n")
        monkeypatch.setattr(testee, 'RTYPES', ('itemtext', 'y'))
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_rule_item('item')
        assert capsys.readouterr().out == "called TreePanel.get_itemtext with arg item\n"

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for Editor.mark_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app_title = 'apptitle'
        testobj.mark_dirty(True)
        assert testobj.project_dirty
        assert capsys.readouterr().out == (
                "called MainGui.set_window_title with arg `apptitle (modified)`\n")
        testobj.mark_dirty(False)
        assert not testobj.project_dirty
        assert capsys.readouterr().out == ("called MainGui.set_window_title with arg `apptitle`\n")

    def test_add(self, monkeypatch, capsys):
        """unittest for Editor.add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.root = 'root'
        monkeypatch.setattr(testobj, 'add_rule', self.mock_add)
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check_false)
        testobj.add()
        assert capsys.readouterr().out == "called Editor.add_rule with args {'parent': 'root'}\n"

    def test_add_after(self, monkeypatch, capsys):
        """unittest for Editor.add_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'add_rule', self.mock_add)
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check_false)
        testobj.add_after()
        assert capsys.readouterr().out == "called Editor.checkselection\n"
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check)
        testobj.add_after()
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.add_rule with args {'after': True}\n")

    def test_add_before(self, monkeypatch, capsys):
        """unittest for Editor.add_before
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'add_rule', self.mock_add)
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check_false)
        testobj.add_before()
        assert capsys.readouterr().out == "called Editor.checkselection\n"
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check)
        testobj.add_before()
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.add_rule with args {'after': False}\n")

    def test_add_under(self, monkeypatch, capsys):
        """unittest for Editor.add_under
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'add_rule', self.mock_add)
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check_false)
        testobj.item = 'item'
        testobj.add_under()
        assert capsys.readouterr().out == "called Editor.checkselection\n"
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check)
        testobj.add_under()
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.add_rule with args {'parent': 'item'}\n")

    def test_add_rule(self, monkeypatch, capsys):
        """unittest for Editor.add_rule
        """
        def mock_is_rule(arg):
            print(f'called Editor.is_rule_parent with arg {arg}')
            return True
        def mock_is_rule_no(arg):
            print(f'called Editor.is_rule_parent with arg {arg}')
            return False
        def mock_get_subitems_1(arg):
            print(f'called TreePanel.get_subitems with arg {arg}')
            return ['item-1']
        def mock_get_subitems_n(arg):
            print(f'called TreePanel.get_subitems with arg {arg}')
            return ['item-1', 'item-n']
        def mock_parentpos(arg):
            print(f'called TreePanel.get_parentpos with {arg}')
            return 'item', 0
        def mock_get_choice(*args):
            print('called MainGui.get_input_choice with args', args)
            return 'result', True
        def mock_get_choice_2(*args):
            print('called MainGui.get_input_choice with args', args)
            return 'X', True
        def mock_get_choice_3(*args):
            print('called MainGui.get_input_choice with args', args)
            return 'B', True

        monkeypatch.setattr(testee.ed, 'RTYPES', {2: ('A', [('x', 1, 'fn')]),
                                                  1: ('B', [('y', 2, 'f2')])})
        monkeypatch.setattr(testee.ed, 'Editor', MockEditor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = 'item'
        testobj.mark_dirty = self.mock_mark_dirty
        testobj.gui.tree.getitemparentpos = mock_parentpos
        testobj.is_rule_parent = mock_is_rule_no
        testobj.add_rule()
        assert capsys.readouterr().out == ("called TreePanel.get_parentpos with item\n"
                                           "called Editor.is_rule_parent with arg item\n")
        testobj.is_rule_parent = mock_is_rule
        testobj.mode = "tag"
        testobj.gui.tree.get_subitems = mock_get_subitems_1
        testobj.add_rule()
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called TreePanel.get_subitems with arg item\n"
            "called MainGui.show_message with arg `Only one rule allowed when editing tag style`\n")
        testobj.gui.tree.get_subitems = mock_get_subitems_n
        testobj.add_rule()
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called TreePanel.get_subitems with arg item\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n")
        testobj.gui.get_input_choice = mock_get_choice
        testobj.add_rule()
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called TreePanel.get_subitems with arg item\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called MainGui.show_message with arg `Only style rule allowed when editing tag style`\n")
        testobj.gui.get_input_choice = mock_get_choice_2
        testobj.add_rule()
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called TreePanel.get_subitems with arg item\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called MainGui.show_message with arg `Only style rule allowed when editing tag style`\n")
        testobj.mode = "no-tag"
        testobj.gui.get_input_choice = mock_get_choice_2
        testobj.add_rule()
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called MainGui.show_message with arg `Can you even choose an option"
            " that is not in the option list?`\n")
        testobj.gui.get_input_choice = mock_get_choice_3
        testobj.add_rule()
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called TreePanel.add_to_parent with args ('B', 'item', -1)\n"
            "called TreePanel.add_to_parent with args ('y', 'new item')\n"
            "called Editor.mark_dirty with arg True\n"
            "called TreePanel.expand_item with arg new item\n"
            "called TreePanel.setcurrent with arg new item\n")

        testobj.add_rule(parent='parent')
        assert capsys.readouterr().out == (
            "called Editor.is_rule_parent with arg parent\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called TreePanel.add_to_parent with args ('B', 'parent', -1)\n"
            "called TreePanel.add_to_parent with args ('y', 'new item')\n"
            "called Editor.mark_dirty with arg True\n"
            "called TreePanel.expand_item with arg new item\n"
            "called TreePanel.setcurrent with arg new item\n")

        testobj.add_rule(after='after')
        assert capsys.readouterr().out == (
            "called TreePanel.get_parentpos with item\n"
            "called Editor.is_rule_parent with arg item\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called TreePanel.get_parentpos with item\n"
            "called TreePanel.add_to_parent with args ('B', 'item', 1)\n"
            "called TreePanel.add_to_parent with args ('y', 'new item')\n"
            "called Editor.mark_dirty with arg True\n"
            "called TreePanel.expand_item with arg new item\n"
            "called TreePanel.setcurrent with arg new item\n")

        testobj.add_rule('parent', 'after')
        assert capsys.readouterr().out == (
            "called Editor.is_rule_parent with arg parent\n"
            "called MainGui.get_input_choice with args ('Choose type for new rule', ['A', 'B'])\n"
            "called TreePanel.get_parentpos with item\n"
            "called TreePanel.add_to_parent with args ('B', 'parent', 1)\n"
            "called TreePanel.add_to_parent with args ('y', 'new item')\n"
            "called Editor.mark_dirty with arg True\n"
            "called TreePanel.expand_item with arg new item\n"
            "called TreePanel.setcurrent with arg new item\n")

    def test_edit(self, monkeypatch, capsys):
        """unittest for Editor.edit
        """
        counter = 0
        def mock_get_itemtext(arg):
            """stub for gui.TreeWidget.get_itemtext
            """
            nonlocal counter
            print(f'called Tree.get_itemtext with arg {arg}')
            counter += 1
            if counter == 1:
                return 'a ruletype'
            return 'data item'
        def mock_get_itemtext_textitem(arg):
            """stub for gui.TreeWidget.get_itemtext
            """
            nonlocal counter
            print(f'called Tree.get_itemtext with arg {arg}')
            counter += 1
            if counter == 1:
                return 'text'
            return 'text type'
        def mock_get_itemtext_listitem(arg):
            """stub for gui.TreeWidget.get_itemtext
            """
            nonlocal counter
            print(f'called Tree.get_itemtext with arg {arg}')
            counter += 1
            if counter == 1:
                return 'list'
            return 'list type'
        def mock_get_itemtext_tableitem(arg):
            """stub for gui.TreeWidget.get_itemtext
            """
            nonlocal counter
            print(f'called Tree.get_itemtext with arg {arg}')
            counter += 1
            if counter == 1:
                return 'grid'
            return 'table type'
        def mock_get_itemtext_other(arg):
            """stub for gui.TreeWidget.get_itemtext
            """
            nonlocal counter
            print(f'called Tree.get_itemtext with arg {arg}')
            counter += 1
            if counter == 1:
                return 'item'
            return 'wrong type'
        def mock_edit_text(arg):
            print(f'called Editor.edit_text_node with arg {arg}')
            return False
        def mock_edit_list(arg):
            print(f'called Editor.edit_list_node with arg {arg}')
            return True
        def mock_edit_grid(arg):
            print(f'called Editor.edit_grid_node with arg {arg}')
            return True
        def mock_get_parentpos(arg):
            print(f'called Tree.get_itemparentpos with arg {arg}')
            return 'node', 0
        monkeypatch.setattr(testee.ed, 'RTYPES', ['a ruletype'])
        monkeypatch.setattr(testee.ed, 'text_type', 1)
        monkeypatch.setattr(testee.ed, 'list_type', 2)
        monkeypatch.setattr(testee.ed, 'table_type', 3)
        monkeypatch.setattr(testee, 'CTYPES', [('text', 1, ''), ('list', 2, ''), ('grid', 3, '')])
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checkselection = self.mock_check_false
        testobj.edit()
        assert capsys.readouterr().out == ("called Editor.checkselection\n")
        testobj.app_title = 'App'
        testobj.checkselection = self.mock_check
        testobj.item = 'item'
        testobj.gui.tree.getitemparentpos = mock_get_parentpos
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        testobj.mark_dirty = self.mock_mark_dirty
        testobj.edit_text_node = mock_edit_text
        testobj.edit_list_node = mock_edit_list
        testobj.edit_grid_node = mock_edit_grid
        testobj.edit()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Tree.get_itemtext with arg item\n"
                "called Tree.get_itemparentpos with arg item\n"
                "called Tree.get_itemtext with arg node\n"
                "called MainGui.show_message with arg `Edit rule via subordinate item`\n")
        counter = 0
        testobj.gui.tree.get_itemtext = mock_get_itemtext_textitem
        testobj.edit()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Tree.get_itemtext with arg item\n"
                "called Tree.get_itemparentpos with arg item\n"
                "called Tree.get_itemtext with arg node\n"
                "called Editor.edit_text_node with arg App - edit 'text' node for text type\n")
        counter = 0
        testobj.gui.tree.get_itemtext = mock_get_itemtext_listitem
        testobj.edit()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Tree.get_itemtext with arg item\n"
                "called Tree.get_itemparentpos with arg item\n"
                "called Tree.get_itemtext with arg node\n"
                "called Editor.edit_list_node with arg App - edit 'list' node for list type\n"
                "called TreePanel.expand_item with arg item\n"
                "called Editor.mark_dirty with arg True\n")
        counter = 0
        testobj.gui.tree.get_itemtext = mock_get_itemtext_tableitem
        testobj.edit()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Tree.get_itemtext with arg item\n"
                "called Tree.get_itemparentpos with arg item\n"
                "called Tree.get_itemtext with arg node\n"
                "called Editor.edit_grid_node with arg App - edit 'grid' node for table type\n"
                "called TreePanel.expand_item with arg item\n"
                "called Editor.mark_dirty with arg True\n")
        counter = 0
        testobj.gui.tree.get_itemtext = mock_get_itemtext_other
        testobj.edit()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Tree.get_itemtext with arg item\n"
                "called Tree.get_itemparentpos with arg item\n"
                "called Tree.get_itemtext with arg node\n"
                "called MainGui.show_message with arg `You can't edit this type of node`\n")

    def test_edit_text_node(self, monkeypatch, capsys):
        """unittest for Editor.edit_text_node
        """
        def mock_get_subitems(arg):
            print(f'called TreePanel.get_subitems with arg {arg}')
            return ['node', 'node2']
        def mock_get_subitems_2(arg):
            print(f'called TreePanel.get_subitems with arg {arg}')
            return [None, 'Node2']
        def mock_get_itemtext(arg):
            print(f'called TreePanel.get_itemtext with arg {arg}')
            return 'nodetext'
        def mock_show(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return False, ''
        def mock_show_2(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return True, 'nodetext'
        def mock_show_3(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return True, 'Nodetext!'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = 'testitem'
        monkeypatch.setattr(testee.gui, 'TextDialog', MockTextDialog)
        testobj.gui.show_dialog = mock_show
        testobj.gui.tree.get_subitems = mock_get_subitems
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert not testobj.edit_text_node('Edit')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg testitem\n"
                "called TreePanel.get_itemtext with arg node\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockTextDialog'> ('Edit', 'nodetext') {}\n")
        testobj.gui.show_dialog = mock_show_2
        testobj.gui.tree.get_subitems = mock_get_subitems
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert not testobj.edit_text_node('Edit')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg testitem\n"
                "called TreePanel.get_itemtext with arg node\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockTextDialog'> ('Edit', 'nodetext') {}\n")
        testobj.gui.show_dialog = mock_show_2
        testobj.gui.tree.get_subitems = mock_get_subitems_2
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert testobj.edit_text_node('Edit')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg testitem\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockTextDialog'> ('Edit', '') {}\n"
                "called TreePanel.add_to_parent with args ('nodetext', 'testitem')\n")
        testobj.gui.show_dialog = mock_show_3
        testobj.gui.tree.get_subitems = mock_get_subitems
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert testobj.edit_text_node('Edit')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg testitem\n"
                "called TreePanel.get_itemtext with arg node\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockTextDialog'> ('Edit', 'nodetext') {}\n"
                "called TreePanel.set_itemtext with args ('node', 'Nodetext!')\n")
        testobj.gui.show_dialog = mock_show_3
        testobj.gui.tree.get_subitems = mock_get_subitems_2
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert testobj.edit_text_node('Edit')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg testitem\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockTextDialog'> ('Edit', '') {}\n"
                "called TreePanel.add_to_parent with args ('Nodetext!', 'testitem')\n")

    def test_edit_list_node(self, monkeypatch, capsys):
        """unittest for Editor.edit_list_node
        """
        def mock_get_subitems(arg):
            print(f'called TreePanel.get_subitems with arg {arg}')
            return ['node', 'node2']
        def mock_remove_subitem(*args):
            print('called TreePanel.remove_subitem with args', args)
        def mock_get_itemtext(arg):
            print(f'called TreePanel.get_itemtext with arg {arg}')
            return 'nodetext'
        def mock_get_itemtext_2(arg):
            print(f'called TreePanel.get_itemtext with arg {arg}')
            return arg
        def mock_show(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return False, ''
        def mock_show_2(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return True, ['node1', 'node2', 'node3']
        def mock_show_3(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return True, ['node2']
        def mock_init_ruledata(rule):
            print(f'called CSSUtilsWrapper.init_ruledata with arg `{rule}`')
            return ['init_1', 'init_2']
        monkeypatch.setattr(testee.ed, 'RTYPES', {'a': ['aa'], 'b': ['bb']})
        monkeypatch.setattr(testee.ed, 'init_ruledata', mock_init_ruledata)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = 'testitem'
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        monkeypatch.setattr(testee.gui, 'ListDialog', MockListDialog)
        testobj.gui.show_dialog = mock_show
        testobj.gui.tree.get_subitems = mock_get_subitems
        testobj.gui.tree.remove_subitem = mock_remove_subitem
        assert not testobj.edit_list_node('Edit')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg testitem\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockListDialog'> ('Edit', ['node', 'node2']) {}\n")
        testobj.gui.show_dialog = mock_show_2
        testobj.item = types.SimpleNamespace(text=lambda x: 'other' if 0 else 'rules')
        testobj.gui.tree.get_itemtext = mock_get_itemtext_2
        assert testobj.edit_list_node('Edit')
        assert capsys.readouterr().out == (
                f"called TreePanel.get_subitems with arg {testobj.item}\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockListDialog'> ('Edit', ['node', 'node2']) {}\n"
                "called TreePanel.get_itemtext with arg node1\n"
                "called TreePanel.get_itemtext with arg node\n"
                "called TreePanel.set_itemtext with args ('node', 'node1')\n"
                "called TreePanel.get_itemtext with arg node2\n"
                "called TreePanel.get_itemtext with arg node2\n"
                f"called TreePanel.add_to_parent with args ('node3', {testobj.item})\n"
                "called CSSUtilsWrapper.init_ruledata with arg `None`\n"
                "called TreePanel.add_to_parent with args ('init_1', 'new item')\n"
                "called TreePanel.add_to_parent with args ('init_2', 'new item')\n")
        testobj.gui.show_dialog = mock_show_2
        testobj.item = types.SimpleNamespace(text=lambda x: 'rules' if 0 else 'other')
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        assert testobj.edit_list_node('Edit')
        assert capsys.readouterr().out == (
                f"called TreePanel.get_subitems with arg {testobj.item}\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockListDialog'> ('Edit', ['node', 'node2']) {}\n"
                "called TreePanel.get_itemtext with arg node1\n"
                "called TreePanel.get_itemtext with arg node\n"
                "called TreePanel.get_itemtext with arg node2\n"
                "called TreePanel.get_itemtext with arg node2\n"
                f"called TreePanel.add_to_parent with args ('node3', {testobj.item})\n")
        testobj.gui.show_dialog = mock_show_3
        assert testobj.edit_list_node('Edit')
        assert capsys.readouterr().out == (
                f"called TreePanel.get_subitems with arg {testobj.item}\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockListDialog'> ('Edit', ['node', 'node2']) {}\n"
                "called TreePanel.get_itemtext with arg node2\n"
                "called TreePanel.get_itemtext with arg node\n"
                f"called TreePanel.remove_subitem with args ({testobj.item}, 1)\n")
                # hier wordt blijkbaar niks weggehaald?

    def _test_edit_grid_node(self, monkeypatch, capsys):
        """unittest for Editor.edit_grid_node
        """
        # counter = 0
        def mock_get_subitems(arg):
            # nonlocal counter
            print(f'called TreePanel.get_subitems with arg {arg}')
            # counter += 1
            # if counter > 1:
            return [f'{arg}-1', f'{arg}-2']
            # return ['node1', 'node2']
        def mock_remove_subitem(*args):
            print('called TreePanel.remove_subitem with args', args)
        def mock_get_itemtext(arg):
            print(f'called TreePanel.get_itemtext with arg {arg}')
            return arg
        def mock_show(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return False, ''
        def mock_show_2(cls, *args, **kwargs):
            print(f'called MainGui.show_dialog with args {cls}', args, kwargs)
            return True, [['node-1'], ['node-2', 'node-2-2'], ['node-3', 'node-3-1']]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = 'node'
        testobj.gui.tree.get_itemtext = mock_get_itemtext
        monkeypatch.setattr(testee.gui, 'GridDialog', MockGridDialog)
        testobj.gui.show_dialog = mock_show
        testobj.gui.tree.get_subitems = mock_get_subitems
        testobj.gui.tree.remove_subitem = mock_remove_subitem
        assert not testobj.edit_grid_node('title')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg node\n"
                "called TreePanel.get_itemtext with arg node-1\n"
                "called TreePanel.get_subitems with arg node-1\n"
                "called TreePanel.get_itemtext with arg node-1-1\n"
                "called TreePanel.get_itemtext with arg node-2\n"
                "called TreePanel.get_subitems with arg node-2\n"
                "called TreePanel.get_itemtext with arg node-2-1\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockGridDialog'>"
                " ('title', [('node-1', 'node-1-1'), ('node-2', 'node-2-1')]) {}\n")
        testobj.gui.show_dialog = mock_show_2
        assert testobj.edit_grid_node('title')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg node\n"
                "called TreePanel.get_itemtext with arg node-1\n"
                "called TreePanel.get_subitems with arg node-1\n"
                "called TreePanel.get_itemtext with arg node-1-1\n"
                "called TreePanel.get_itemtext with arg node-2\n"
                "called TreePanel.get_subitems with arg node-2\n"
                "called TreePanel.get_itemtext with arg node-2-1\n"
                "called MainGui.show_dialog with args"
                " <class 'cssedit.tests.test_main.MockGridDialog'>"
                " ('title', [('node-1', 'node-1-1'), ('node-2', 'node-2-1')]) {}\n")

    def test_delete(self, monkeypatch, capsys):
        """unittest for Editor.delete
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, '_copy_rule', self.mock_copy)
        testobj.delete()
        assert capsys.readouterr().out == (
                "called Editor._copy_rule with kwargs {'cut': True, 'retain': False}\n")

    def test_cut(self, monkeypatch, capsys):
        """unittest for Editor.cut
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, '_copy_rule', self.mock_copy)
        testobj.cut()
        assert capsys.readouterr().out == (
                "called Editor._copy_rule with kwargs {'cut': True, 'retain': True}\n")

    def test_copy(self, monkeypatch, capsys):
        """unittest for Editor.copy
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, '_copy_rule', self.mock_copy)
        testobj.copy()
        assert capsys.readouterr().out == (
                "called Editor._copy_rule with kwargs {'cut': False, 'retain': True}\n")

    def test_copy_rule(self, monkeypatch, capsys):
        """unittest for Editor._copy_rule
        """
        def mock_is_not_ruleitem(arg):
            print(f'called Editor.is_rule_item with arg `{arg}`')
            return False
        def mock_is_ruleitem(arg):
            print(f'called Editor.is_rule_item with arg `{arg}`')
            return True
        def mock_parentpos(arg):
            print(f'called Tree.getitemparentpos with arg `{arg}`')
            return 'parent', 1
        def mock_remove(*args):
            print('called Tree.remove_subitem with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mark_dirty = self.mock_mark_dirty
        testobj.checkselection = self.mock_check_false
        testobj._copy_rule()
        assert capsys.readouterr().out == ("called Editor.checkselection\n")
        testobj.checkselection = self.mock_check
        testobj.item = 'testitem'
        testobj.itemlevel = 1
        testobj.gui.tree.getitemparentpos = mock_parentpos
        testobj.gui.tree.remove_subitem = mock_remove
        testobj.is_rule_item = mock_is_not_ruleitem
        testobj._copy_rule()
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.is_rule_item with arg `testitem`\n")
        testobj.is_rule_item = mock_is_ruleitem
        testobj.cut_item, testobj.cutlevel = None, 0
        testobj._copy_rule()
        assert (testobj.cut_item, testobj.cutlevel) == ('testitem', 1)
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.is_rule_item with arg `testitem`\n"
                                           "called Tree.getitemparentpos with arg `testitem`\n"
                                           "called Tree.remove_subitem with args ('parent', 0)\n"
                                           "called Editor.mark_dirty with arg True\n")
        testobj.cut_item, testobj.cutlevel = None, 0
        testobj._copy_rule(False)
        assert (testobj.cut_item, testobj.cutlevel) == ('testitem', 1)
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.is_rule_item with arg `testitem`\n")
        testobj.cut_item, testobj.cutlevel = None, 0
        testobj._copy_rule(retain=False)
        assert (testobj.cut_item, testobj.cutlevel) == (None, 0)
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.is_rule_item with arg `testitem`\n"
                                           "called Tree.getitemparentpos with arg `testitem`\n"
                                           "called Tree.remove_subitem with args ('parent', 0)\n"
                                           "called Editor.mark_dirty with arg True\n")
        testobj.cut_item, testobj.cutlevel = None, 0
        testobj._copy_rule(cut=False, retain=False)
        assert (testobj.cut_item, testobj.cutlevel) == (None, 0)
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.is_rule_item with arg `testitem`\n")

    def test_paste_under(self, monkeypatch, capsys):
        """unittest for Editor.paste_under
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, '_paste_rule', self.mock_paste)
        testobj.paste_under()
        assert capsys.readouterr().out == (
                "called Editor._paste_rule with kwargs {'under': True}\n")

    def test_paste_after(self, monkeypatch, capsys):
        """unittest for Editor.paste_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, '_paste_rule', self.mock_paste)
        testobj.paste_after()
        assert capsys.readouterr().out == (
                "called Editor._paste_rule with kwargs {}\n")

    def test_paste_before(self, monkeypatch, capsys):
        """unittest for Editor.paste_before
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, '_paste_rule', self.mock_paste)
        testobj.paste_before()
        assert capsys.readouterr().out == (
                "called Editor._paste_rule with kwargs {'after': False}\n")

    def test_paste_rule(self, monkeypatch, capsys):
        """unittest for Editor._paste_rule
        """
        def mock_is_not_rule_parent(arg):
            print(f'called Editor.is_rule_parent with arg `{arg}`')
            return False
        def mock_is_rule_parent(arg):
            print(f'called Editor.is_rule_parent with arg `{arg}`')
            return True
        def mock_parentpos(arg):
            print(f'called Tree.getitemparentpos with arg `{arg}`')
            return 'parent', 1
        def mock_paste(*args):
            print('called Editor._paste with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = types.SimpleNamespace(__str__=lambda *x: 'testitem',
                                             parent=lambda *x: 'testparent')
        testobj.cut_item = 'cut_item'
        testobj._paste = mock_paste
        testobj.mark_dirty = self.mock_mark_dirty
        testobj.checkselection = self.mock_check_false
        testobj.is_rule_parent = mock_is_not_rule_parent
        testobj.gui.tree.getitemparentpos = mock_parentpos
        testobj._paste_rule()
        assert capsys.readouterr().out == ("called Editor.checkselection\n")
        testobj.checkselection = self.mock_check
        testobj._paste_rule()
        assert capsys.readouterr().out == ("called Editor.checkselection\n"
                                           "called Editor.is_rule_parent with arg `testparent`\n")
        testobj.checkselection = self.mock_check
        testobj.is_rule_parent = mock_is_rule_parent
        testobj._paste_rule()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Editor.is_rule_parent with arg `testparent`\n"
                f"called Tree.getitemparentpos with arg `{testobj.item}`\n"
                "called Editor._paste with args ('cut_item', 'testparent', 2)\n"
                "called Editor.mark_dirty with arg True\n")
        testobj._paste_rule(True)
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                f"called Editor.is_rule_parent with arg `{testobj.item}`\n"
                f"called Editor._paste with args ('cut_item', {testobj.item})\n"
                "called Editor.mark_dirty with arg True\n")
        testobj._paste_rule(after=False)
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Editor.is_rule_parent with arg `testparent`\n"
                f"called Tree.getitemparentpos with arg `{testobj.item}`\n"
                "called Editor._paste with args ('cut_item', 'testparent', 1)\n"
                "called Editor.mark_dirty with arg True\n")
        testobj._paste_rule(under=True, after=False)
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                f"called Editor.is_rule_parent with arg `{testobj.item}`\n"
                f"called Editor._paste with args ('cut_item', {testobj.item})\n"
                "called Editor.mark_dirty with arg True\n")

    def test_paste(self, monkeypatch, capsys):
        """unittest for Editor._paste
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        with pytest.raises(NotImplementedError):
            testobj._paste('item', 'parent')

    def test_expand_item(self, monkeypatch, capsys):
        """unittest for Editor.expand_item
        """
        def mock_expand(**kwargs):
            print('print called Editor.expand with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._expand = mock_expand
        testobj.expand_item()
        assert capsys.readouterr().out == ("print called Editor.expand with args {}\n")

    def test_expand_all(self, monkeypatch, capsys):
        """unittest for Editor.expand_all
        """
        def mock_expand(**kwargs):
            print('print called Editor.expand with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._expand = mock_expand
        testobj.expand_all()
        assert capsys.readouterr().out == (
                "print called Editor.expand with args {'recursive': True}\n")

    def test_expand(self, monkeypatch, capsys):
        """unittest for Editor._expand
        """
        def mock_expand(arg):
            """stub
            """
            print(f'called Tree.expand_item with arg `{arg}`')
        counter = 0
        def mock_get(arg):
            """stub
            """
            nonlocal counter
            print(f'called Tree.get_subitems with arg `{arg}`')
            counter += 1
            if counter == 1:
                return ['subitem']
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.expand_item = mock_expand
        testobj.gui.tree.get_subitems = mock_get
        testobj._expand()
        assert capsys.readouterr().out == ("called TreePanel.getcurrent\n"
                                           "called Tree.expand_item with arg `current item`\n")
        testobj._expand(recursive=True)
        assert capsys.readouterr().out == ("called TreePanel.getcurrent\n"
                                           "called Tree.expand_item with arg `current item`\n"
                                           "called Tree.get_subitems with arg `current item`\n"
                                           "called Tree.expand_item with arg `subitem`\n"
                                           "called Tree.get_subitems with arg `subitem`\n")

    def test_collapse_item(self, monkeypatch, capsys):
        """unittest for Editor.collapse_item
        """
        def mock_collapse(**kwargs):
            print('print called Editor.collapse with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._collapse = mock_collapse
        testobj.collapse_item()
        assert capsys.readouterr().out == ("print called Editor.collapse with args {}\n")

    def test_collapse_all(self, monkeypatch, capsys):
        """unittest for Editor.collapse_all
        """
        def mock_collapse(**kwargs):
            print('print called Editor.collapse with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._collapse = mock_collapse
        testobj.collapse_all()
        assert capsys.readouterr().out == (
                "print called Editor.collapse with args {'recursive': True}\n")

    def test_collapse(self, monkeypatch, capsys):
        """unittest for Editor._collapse
        """
        def mock_collapse(arg):
            """stub
            """
            print(f'called Tree.collapse_item with arg `{arg}`')
        counter = 0
        def mock_get(arg):
            """stub
            """
            nonlocal counter
            print(f'called Tree.get_subitems with arg `{arg}`')
            counter += 1
            if counter == 1:
                return ['subitem']
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.collapse_item = mock_collapse
        testobj.gui.tree.get_subitems = mock_get
        testobj._collapse()
        assert capsys.readouterr().out == ("called TreePanel.getcurrent\n"
                                           "called Tree.collapse_item with arg `current item`\n")
        testobj._collapse(recursive=True)
        assert capsys.readouterr().out == ("called TreePanel.getcurrent\n"
                                           "called Tree.get_subitems with arg `current item`\n"
                                           "called Tree.get_subitems with arg `subitem`\n"
                                           "called Tree.collapse_item with arg `subitem`\n"
                                           "called Tree.collapse_item with arg `current item`\n")

    def _test_no_op(self, monkeypatch, capsys):
        """unittest for Editor.no_op - does nothing, no test needed
        """

    def test_show_level(self, monkeypatch, capsys):
        """unittest for Editor.show_level
        """
        def mock_level(arg):
            print(f'called Editor.determine_level with arg `{arg}`')
        def mock_level_2(arg):
            print(f'called Editor.determine_level with arg `{arg}`')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.determine_level = mock_level
        testobj.determine_level_orig = mock_level_2
        testobj.item = 'item'
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check_false)
        testobj.show_level()
        assert capsys.readouterr().out == "called Editor.checkselection\n"
        monkeypatch.setattr(testobj, 'checkselection', self.mock_check)
        testobj.show_level()
        assert capsys.readouterr().out == (
                "called Editor.checkselection\n"
                "called Editor.determine_level with arg `item`\n"
                "called MainGui.show_message with arg `This element is at level None`\n"
                "called Editor.determine_level with arg `item`\n"
                "called MainGui.show_message with arg `Or is this element at level None?`\n")

    def test_add_subitems(self, monkeypatch, capsys):
        """unittest for Editor.add_subitems
        """
        counter = 0
        def mock_get(arg):
            nonlocal counter
            print('called TreePanel.get_subitems with arg', arg)
            counter += 1
            if counter > 1:
                return []
            return ['item-1', 'item-2']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.get_subitems = mock_get
        testobj.add_subitems('parent', 'item')
        assert capsys.readouterr().out == (
                "called TreePanel.get_subitems with arg item\n"
                "called MainGui.get_itemtext with arg `{arg}`\n"
                "called TreePanel.new_treeitem with args ('item-1',)\n"
                "called TreePanel.add_subitem with args ('parent', None)\n"
                "called TreePanel.get_subitems with arg item-1\n"
                "called MainGui.get_itemtext with arg `{arg}`\n"
                "called TreePanel.new_treeitem with args ('item-2',)\n"
                "called TreePanel.add_subitem with args ('parent', None)\n"
                "called TreePanel.get_subitems with arg item-2\n")

    def test_paste_item(self, monkeypatch, capsys):
        """unittest for Editor.paste_item
        """
        def mock_add(*args):
            print('called Editor.add_subitems with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_subitems = mock_add
        testobj.paste_item('item', 'parent')
        assert capsys.readouterr().out == (
                "called TreePanel.get_itemtext with arg item\n"
                "called TreePanel.new_treeitem with args ('itemtext',)\n"
                "called TreePanel.add_subitem with args ('parent', None, -1)\n"
                "called Editor.add_subitems with args (None, 'item')\n")
        testobj.paste_item('item', 'parent', ix=1)
        assert capsys.readouterr().out == (
                "called TreePanel.get_itemtext with arg item\n"
                "called TreePanel.new_treeitem with args ('itemtext',)\n"
                "called TreePanel.add_subitem with args ('parent', None, 1)\n"
                "called Editor.add_subitems with args (None, 'item')\n")

    def test_read_rules(self, monkeypatch, capsys):
        """unittest for Editor.read_rules
        """
        def mock_newitem(arg):
            print('called TreePanel.new_treeitem with arg', arg)
            return f'{arg}_item'
        counter = 0
        def mock_newitem_2(arg):
            nonlocal counter
            print('called TreePanel.new_treeitem with arg', arg)
            counter += 1
            if counter == 3:
                print("-- call failed with TypeError --")
                raise TypeError
            return f'{arg}_item'
        monkeypatch.setattr(testee, 'RTYPES', ['rtype'])

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.new_treeitem = mock_newitem
        assert testobj.read_rules([]) == []
        assert capsys.readouterr().out == ("")
        data = [('ruletype-1', {'seqnum': 1})]
        assert testobj.read_rules(data) == ['ruletype-1_item']
        assert capsys.readouterr().out == ("called TreePanel.new_treeitem with arg ruletype-1\n")
        data = [('rule1', {'text': 'xxx', 'data': 'yyy'}), ('rule2', {'name': 'aaa', 'uri': 'bbb'}),
                ('rule3', {'selector': 'p, q'})]
        assert testobj.read_rules(data) == ['rule1_item', 'rule2_item', 'rule3_item']
        assert capsys.readouterr().out == (
                "called TreePanel.new_treeitem with arg rule1\n"
                "called TreePanel.new_treeitem with arg data\n"
                "called TreePanel.add_subitem with args ('rule1_item', 'data_item')\n"
                "called TreePanel.new_treeitem with arg yyy\n"
                "called TreePanel.add_subitem with args ('data_item', 'yyy_item')\n"
                "called TreePanel.new_treeitem with arg text\n"
                "called TreePanel.add_subitem with args ('rule1_item', 'text_item')\n"
                "called TreePanel.new_treeitem with arg xxx\n"
                "called TreePanel.add_subitem with args ('text_item', 'xxx_item')\n"
                "called TreePanel.new_treeitem with arg rule2\n"
                "called TreePanel.new_treeitem with arg name\n"
                "called TreePanel.add_subitem with args ('rule2_item', 'name_item')\n"
                "called TreePanel.new_treeitem with arg aaa\n"
                "called TreePanel.add_subitem with args ('name_item', 'aaa_item')\n"
                "called TreePanel.new_treeitem with arg uri\n"
                "called TreePanel.add_subitem with args ('rule2_item', 'uri_item')\n"
                "called TreePanel.new_treeitem with arg bbb\n"
                "called TreePanel.add_subitem with args ('uri_item', 'bbb_item')\n"
                "called TreePanel.new_treeitem with arg rule3\n"
                "called TreePanel.new_treeitem with arg selector\n"
                "called TreePanel.add_subitem with args ('rule3_item', 'selector_item')\n"
                "called TreePanel.new_treeitem with arg p, q\n"
                "called TreePanel.add_subitem with args ('selector_item', 'p, q_item')\n")
        data = [('ruletype-1', {'key': ['a', 'value']})]
        assert testobj.read_rules(data) == ['ruletype-1_item']
        assert capsys.readouterr().out == (
                "called TreePanel.new_treeitem with arg ruletype-1\n"
                "called TreePanel.new_treeitem with arg key\n"
                "called TreePanel.add_subitem with args ('ruletype-1_item', 'key_item')\n"
                "called TreePanel.new_treeitem with arg a\n"
                "called TreePanel.add_subitem with args ('key_item', 'a_item')\n"
                "called TreePanel.new_treeitem with arg value\n"
                "called TreePanel.add_subitem with args ('key_item', 'value_item')\n")
        data = [('ruletype-1', {'key': {'xx': 'xxxxx', 'yy': 'yyyyy'}})]
        assert testobj.read_rules(data) == ['ruletype-1_item']
        assert capsys.readouterr().out == (
                "called TreePanel.new_treeitem with arg ruletype-1\n"
                "called TreePanel.new_treeitem with arg key\n"
                "called TreePanel.add_subitem with args ('ruletype-1_item', 'key_item')\n"
                "called TreePanel.new_treeitem with arg xx\n"
                "called TreePanel.new_treeitem with arg xxxxx\n"
                "called TreePanel.add_subitem with args ('xx_item', 'xxxxx_item')\n"
                "called TreePanel.add_subitem with args ('key_item', 'xx_item')\n"
                "called TreePanel.new_treeitem with arg yy\n"
                "called TreePanel.new_treeitem with arg yyyyy\n"
                "called TreePanel.add_subitem with args ('yy_item', 'yyyyy_item')\n"
                "called TreePanel.add_subitem with args ('key_item', 'yy_item')\n")
        testobj.gui.tree.new_treeitem = mock_newitem_2
        data = [('ruletype-1', {'key': [['list', 'value']]})]
        assert testobj.read_rules(data) == ['ruletype-1_item']
        assert capsys.readouterr().out == (
                "called TreePanel.new_treeitem with arg ruletype-1\n"
                "called TreePanel.new_treeitem with arg key\n"
                "called TreePanel.add_subitem with args ('ruletype-1_item', 'key_item')\n"
                "called TreePanel.new_treeitem with arg ['list', 'value']\n"
                "-- call failed with TypeError --\n"
                "called TreePanel.new_treeitem with arg list\n"
                "called TreePanel.new_treeitem with arg value\n"
                "called TreePanel.add_subitem with args ('list_item', 'value_item')\n"
                "called TreePanel.add_subitem with args ('key_item', 'list_item')\n")
