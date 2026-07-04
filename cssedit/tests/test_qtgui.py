"""unittests for ./cssedit/editor/gui_qt.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from cssedit.editor import gui_qt as testee


class MockEditor:
    "stub for main.Editor"
    def __init__(self):
        print('called Editor.__init__')


class MockMainGui:
    "stub for gui_qt.MainGui"
    def __init__(self, *args):
        print('called MainGui.__init__ with args', args)


class MockTree:
    "stub for gui_qt.TreePanel"
    def __init__(self):
        print('called Tree.__init__')


class TestMainGui:
    """unittest for gui_qt.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        monkeypatch.setattr(testee.MainGui, '__init__', mock_init)
        testobj = testee.MainGui()
        testobj.app = mockqtw.MockApplication()
        testobj.master = MockEditor()
        testobj.tree = MockTree()
        assert capsys.readouterr().out == ('called MainGui.__init__ with args ()\n'
                                           'called Application.__init__\n'
                                           'called Editor.__init__\n'
                                           'called Tree.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        def mock_init(self, *args, **kwargs):
            print('called QMainWindow.__init__ with args', args, kwargs)
        def mock_set_title(self, title):
            print(f"called MainGui.set_window_title with arg '{title}'")
        monkeypatch.setattr(testee.qtw.QApplication, '__init__',
                            mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        #                   mockqtw.MockMainWindow.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon',
                            mockqtw.MockMainWindow.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.MainGui, 'set_window_title', mock_set_title)
        monkeypatch.setattr(testee.TreePanel, '__init__', mockqtw.MockTreeWidget.__init__)
        master = MockEditor()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        master.app_iconame = ''
        testobj = testee.MainGui(master, None)
        assert testobj.master == master
        assert isinstance(testobj.statusbar, mockqtw.MockStatusBar)
        assert isinstance(testobj.tree, testee.TreePanel)
        assert testobj.output_options == []
        assert capsys.readouterr().out == (
                "called Application.__init__\n"
                "called QMainWindow.__init__ with args () {}\n"
                "called MainGui.set_window_title with arg ''\n"
                "called MainWindow.move with args (10, 10)\n"
                "called MainWindow.resize with args (800, 500)\n"
                "called MainWindow.statusBar\n"
                "called StatusBar.__init__ with args ()\n"
                "called Tree.__init__\n"
                "called MainWidget.setCentralWidget with arg `TreePanel`\n")
        master.app_iconame = 'yyy'
        testobj = testee.MainGui(master, 'app', title='xxx', pos=(10, 10), size=(1800, 1500))
        assert capsys.readouterr().out == (
                "called QMainWindow.__init__ with args () {}\n"
                "called MainGui.set_window_title with arg 'xxx'\n"
                "called Icon.__init__ with arg `yyy`\n"
                "called MainWindow.setWindowIcon\n"
                "called MainWindow.move with args (20, 20)\n"
                "called MainWindow.resize with args (1800, 1500)\n"
                "called MainWindow.statusBar\n"
                "called StatusBar.__init__ with args ()\n"
                "called Tree.__init__\n"
                "called MainWidget.setCentralWidget with arg `TreePanel`\n")

    def test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        def mock_callback():
            "stub"
        def mock_define(*args):
            print(f'called Editor.define_format_submenu with args (menu, {args[1]})')
        callback1 = mock_callback
        callback2 = mock_callback
        callback3 = mock_callback
        monkeypatch.setattr(testee.MainGui, 'menuBar', mockqtw.MockMainWindow.menuBar)
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.define_format_submenu = mock_define
        testobj.master.format_option = 'xxx'
        testobj.master.actiondict = {}
        menudata = ()
        testobj.create_menu(menudata)
        assert testobj.menus == {}
        assert testobj.master.actiondict == {}
        assert capsys.readouterr().out == "called MainWindow.menuBar\ncalled MenuBar.__init__\n"
        menudata = (('menutitle',
                     (('label-1', callback1, 'x, y', 'infotekst-1'),
                      (),
                      ('xxx', ('submenu', 'data')),
                      ('label-2', callback2, '', 'infotekst-2'),
                      ('', callback3, 'z', 'infotekst-2'),
                      ('label-3', callback3, 'z', ''))),)
        testobj.create_menu(menudata)
        assert list(testobj.menus.keys()) == ['menutitle']
        assert isinstance(testobj.menus['menutitle'], mockqtw.MockMenu)
        assert list(testobj.master.actiondict.keys()) == ['label-1', 'label-2', 'label-3']
        for x in testobj.master.actiondict.values():
            assert isinstance(x, mockqtw.MockAction)
        assert capsys.readouterr().out == (
            "called MainWindow.menuBar\n"
            "called MenuBar.__init__\n"
            "called MenuBar.addMenu with arg  menutitle\n"
            "called Menu.__init__ with args ('menutitle',)\n"
            f"called Action.__init__ with args ('label-1', {testobj})\n"
            "called Action.setShortcuts with arg `['x', ' y']`\n"
            "called Action.setStatusTip with arg 'infotekst-1'\n"
            f"called Signal.connect with args ({callback1},)\n"
            "called Menu.addAction\n"
            "called Menu.addSeparator\n"
            "called Action.__init__ with args ('-----', None)\n"
            "called Editor.define_format_submenu with args (menu, ('xxx', ('submenu', 'data')))\n"
            f"called Action.__init__ with args ('label-2', {testobj})\n"
            "called Action.setStatusTip with arg 'infotekst-2'\n"
            f"called Signal.connect with args ({callback2},)\n"
            "called Menu.addAction\n"
            "called Menu.addSeparator\n"
            "called Action.__init__ with args ('-----', None)\n"
            f"called Action.__init__ with args ('label-3', {testobj})\n"
            "called Action.setShortcuts with arg `['z']`\n"
            f"called Signal.connect with args ({callback3},)\n"
            "called Menu.addAction\n")

    def test_define_format_submenu(self, monkeypatch, capsys):
        """unittest for MainGui.define_format_submenu
        """
        def mock_callback():
            "stub"
        menu = mockqtw.MockMenu()
        assert capsys.readouterr().out == "called Menu.__init__ with args ()\n"
        callback1 = mock_callback
        callback2 = mock_callback
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.output_options = []
        testobj.define_format_submenu(menu, ['title', (('item-1', callback1), ('item-2', callback2)),
                                             '', '', 'statustip'])
        assert len(testobj.output_options) == len([callback1, callback2])
        assert isinstance(testobj.output_options[0], mockqtw.MockAction)
        assert isinstance(testobj.output_options[1], mockqtw.MockAction)
        assert capsys.readouterr().out == (
                "called Menu.addMenu with args ('title',)\n"
                "called Menu.__init__ with args ()\n"
                f"called Menu.addAction with args `item-1` {callback1}\n"
                f"called Action.__init__ with args ('item-1', {callback1})\n"
                "called Action.setCheckable with arg `True`\n"
                f"called Menu.addAction with args `item-2` {callback2}\n"
                f"called Action.__init__ with args ('item-2', {callback2})\n"
                "called Action.setCheckable with arg `True`\n"
                "called Action.setChecked with arg `True`\n"
                "called Menu.setStatusTip with arg 'statustip'\n")

    def test_check_format_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_format_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.output_options = [mockqtw.MockAction(), mockqtw.MockAction(), mockqtw.MockAction(),
                                  mockqtw.MockAction()]
        assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.check_format_option(2)
        assert capsys.readouterr().out == ("called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `True`\n")

    def test_just_show(self, monkeypatch, capsys):
        """unittest for MainGui.just_show
        """
        def mock_show():
            print('called MainGui.show')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show = mock_show
        with pytest.raises(SystemExit):
            testobj.just_show()
        assert capsys.readouterr().out == ("called MainGui.show\ncalled Application.exec\n")

    def test_set_modality_and_show(self, monkeypatch, capsys):
        """unittest for MainGui.set_modality_and_show
        """
        def mock_show():
            print('called MainGui.show')
        monkeypatch.setattr(testee.MainGui, 'setWindowModality',
                            mockqtw.MockMainWindow.setWindowModality)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show = mock_show
        testobj.set_modality_and_show('')
        assert capsys.readouterr().out == (
                "called MainWindow.setWindowModality with arg"
                f" '{testee.core.Qt.WindowModality.NonModal}'\n"
                "called MainGui.show\n")
        testobj.set_modality_and_show('x')
        assert capsys.readouterr().out == (
                "called MainWindow.setWindowModality with arg"
                f" '{testee.core.Qt.WindowModality.ApplicationModal}'\n"
                "called MainGui.show\n")

    def test_show_message(self, monkeypatch, capsys):
        """unittest for MainGui.show_message
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        testobj.show_message('qqq')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `xxx` `qqq`\n")
        testobj.show_message('qqq', 'yyy')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `yyy` `qqq`\n")

    def test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statusbar = mockqtw.MockStatusBar()
        testobj.show_statusmessage('text')
        assert capsys.readouterr().out == ("called StatusBar.__init__ with args ()\n"
                                           "called StatusBar.showMessage with arg `text`\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        def mock_close():
            print('called Editor.close')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'close', mockqtw.MockMainWindow.close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.close = mock_close
        testobj.close()
        assert capsys.readouterr().out == ("called Editor.close\ncalled MainWindow.close\n")

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        monkeypatch.setattr(testee.MainGui, 'setWindowTitle', mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        testobj.set_window_title()
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `xxx`\n")
        testobj.set_window_title('yyy')
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `yyy`\n")

    def test_set_waitcursor(self, monkeypatch, capsys):
        """unittest for MainGui.set_waitcursor
        """
        monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_waitcursor(False)
        assert capsys.readouterr().out == ("called Application.restoreOverrideCursor\n")
        testobj.set_waitcursor(True)
        assert capsys.readouterr().out == (
                f"called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n"
                "called Application.setOverrideCursor with arg MockCursor\n")

    def test_show_save_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_save_dialog
        """
        def mock_save(self, *args):
            print('called FileDialog.getSaveFilename with args', *args)
            return 'sss', True
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_save)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.show_save_dialog('start', 'filter') == "sss"
        assert capsys.readouterr().out == (
                "called FileDialog.getSaveFilename with args xxx start filter\n")

    def test_show_open_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_open_dialog
        """
        def mock_open(self, *args):
            print('called FileDialog.getOpenFilename with args', *args)
            return 'ooo', True
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.show_open_dialog('start', 'filter') == "ooo"
        assert capsys.readouterr().out == (
                "called FileDialog.getOpenFilename with args xxx start filter\n")

    def test_get_input_text(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_text
        """
        def mock_get(self, *args):
            print('called InputDialog.getText with args', args)
            return 'yyy'
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.get_input_text('prompt') == "yyy"
        assert capsys.readouterr().out == "called InputDialog.getText with args ('xxx', 'prompt')\n"

    def test_get_input_choice(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_choice
        """
        def mock_get(self, *args):
            print('called InputDialog.getItem with args', args)
            return 'yyy'
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.get_input_choice('prompt', ['a', 'b'], True) == "yyy"
        assert capsys.readouterr().out == (
                "called InputDialog.getItem with args ('xxx', 'prompt', ['a', 'b'], True)\n")
        assert testobj.get_input_choice('prompt', ['a', 'b']) == "yyy"
        assert capsys.readouterr().out == (
                "called InputDialog.getItem with args ('xxx', 'prompt', ['a', 'b'], False)\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_dialog
        """
        class MockDialogParent:
            gui = mockqtw.MockDialog()
            def __init__(self, *args):
                print('called DialogParent.__init__ with args', args)
        def mock_exec():
            print('called Dialog.exec')
            return testee.qtw.QDialog.DialogCode.Accepted
        assert capsys.readouterr().out == "called Dialog.__init__ with args None () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.dialog_data = {'x': 'y'}
        cls = MockDialogParent
        assert testobj.show_dialog(cls, 'args') == (False, None)
        assert capsys.readouterr().out == (
                f"called DialogParent.__init__ with args ({testobj}, 'args')\n"
                "called Dialog.exec\n")
        cls.gui.exec = mock_exec
        assert testobj.show_dialog(cls, 'args') == (True, {'x': 'y'})
        assert capsys.readouterr().out == (
                f"called DialogParent.__init__ with args ({testobj}, 'args')\n"
                "called Dialog.exec\n")


class TestTreePanel:
    """unittest for gui_qt.TreePanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.TreePanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TreePanel.__init__ with args', args)
        monkeypatch.setattr(testee.TreePanel, '__init__', mock_init)
        testobj = testee.TreePanel()
        testobj.parent = MockMainGui()
        assert capsys.readouterr().out == ('called TreePanel.__init__ with args ()\n'
                                           'called MainGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TreePanel.__init__
        """
        parent = 'parent'
        monkeypatch.setattr(testee.qtw.QTreeWidget, '__init__',
                            mockqtw.MockTreeWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setColumnCount',
                            mockqtw.MockTreeWidget.setColumnCount)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'hideColumn',
                            mockqtw.MockTreeWidget.hideColumn)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'headerItem',
                            mockqtw.MockTreeWidget.headerItem)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setSelectionMode',
                            mockqtw.MockTreeWidget.setSelectionMode)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setUniformRowHeights',
                            mockqtw.MockTreeWidget.setUniformRowHeights)
        testobj = testee.TreePanel(parent)
        assert testobj.parent == parent
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called Tree.setColumnCount with arg `2`\n"
                                           "called Tree.hideColumn\n"
                                           "called Tree.headerItem\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setHidden with arg `True`\n"
                                           "called Tree.setSelectionMode\n"
                                           "called Tree.setUniformRowHeights with arg `True`\n")

    def _test_selectionChanged(self, monkeypatch, capsys):
        """unittest for TreePanel.selectionChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.selectionChanged('newsel', 'oldsel') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_dropEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.dropEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.dropEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'dropEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.dropEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.dropEvent with arg 'event'\n")

    def test_mousePressEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mousePressEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.mousePressEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mousePressEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mousePressEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.mousePressEvent with arg 'event'\n")

    def test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mouseReleaseEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.mouseReleaseEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mouseReleaseEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mouseReleaseEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.mouseReleaseEvent with arg 'event'\n")

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.keyReleaseEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.keyReleaseEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'keyReleaseEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.keyReleaseEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.keyReleaseEvent with arg 'event'\n")

    def _test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_popupmenu('item') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_remove_root(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_root
        """
        monkeypatch.setattr(testee.TreePanel, 'takeTopLevelItem',
                            mockqtw.MockTreeWidget.takeTopLevelItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_root()
        assert capsys.readouterr().out == "called Tree.takeTopLevelItem with arg `0`\n"

    def test_init_root(self, monkeypatch, capsys):
        """unittest for TreePanel.init_root
        """
        monkeypatch.setattr(testee.TreePanel, 'addTopLevelItem',
                            mockqtw.MockTreeWidget.addTopLevelItem)
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_root()
        assert isinstance(testobj.root, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with args (0, '(untitled)')\n"
                                           "called Tree.addTopLevelItem\n")

    def test_set_root_text(self, monkeypatch, capsys):
        """unittest for TreePanel.set_root_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_root_text('text')
        assert capsys.readouterr().out == "called TreeItem.setText with args (0, 'text')\n"

    def test_get_root(self, monkeypatch, capsys):
        """unittest for TreePanel.get_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root = root
        assert testobj.get_root() == root

    def test_activate_rootitem(self, monkeypatch, capsys):
        """unittest for TreePanel.activate_rootitem
        """
        monkeypatch.setattr(testee.TreePanel, 'setCurrentItem', mockqtw.MockTreeWidget.setCurrentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.activate_rootitem()
        assert capsys.readouterr().out == f"called Tree.setCurrentItem with arg `{testobj.root}`\n"

    def test_set_activeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.set_activeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_activeitem('item')
        assert testobj.activeitem == 'item'

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for TreePanel.set_focus
        """
        monkeypatch.setattr(testee.TreePanel, 'setFocus', mockqtw.MockTreeWidget.setFocus)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus()
        assert capsys.readouterr().out == "called Tree.setFocus\n"

    def test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        def mock_new(arg):
            print(f"called Tree.new_treeitem with arg '{arg}'")
            return 'new item'
        def mock_add(*args):
            print("called Tree.add_subitem with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.new_treeitem = mock_new
        testobj.add_subitem = mock_add
        assert testobj.add_to_parent('titel', 'parent') == "new item"
        assert capsys.readouterr().out == (
                "called Tree.new_treeitem with arg 'titel'\n"
                "called Tree.add_subitem with args ('parent', 'new item', -1)\n")
        assert testobj.add_to_parent('titel', 'parent', 3) == "new item"
        assert capsys.readouterr().out == (
                "called Tree.new_treeitem with arg 'titel'\n"
                "called Tree.add_subitem with args ('parent', 'new item', 3)\n")

    def test_setcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.setcurrent
        """
        monkeypatch.setattr(testee.TreePanel, 'setCurrentItem', mockqtw.MockTreeWidget.setCurrentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.setcurrent(item)
        assert capsys.readouterr().out == f"called Tree.setCurrentItem with arg `{item}`\n"

    def test_getcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.getcurrent
        """
        monkeypatch.setattr(testee.TreePanel, 'currentItem', mockqtw.MockTreeWidget.currentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getcurrent() == "called Tree.currentItem"

    def test_new_treeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.new_treeitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.new_treeitem('item text')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with args (0, 'item text')\n"
                                           "called TreeItem.setTooltip with args (0, 'item text')\n")

    def test_add_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.add_subitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.add_subitem(parent, 'child')
        assert capsys.readouterr().out == "called TreeItem.addChild\n"
        testobj.add_subitem(parent, 'child', 2)
        assert capsys.readouterr().out == "called TreeItem.insertChild at pos 2\n"

    def test_remove_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_subitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.remove_subitem(parent, 1)
        assert capsys.readouterr().out == ("called TreeItem.takeChild\n")

    def test_get_subitems(self, monkeypatch, capsys):
        """unittest for TreePanel.get_subitems
        """
        item = mockqtw.MockTreeItem()
        item.addChild('item0')
        item.addChild('item1')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_subitems(item) == ['item0', 'item1']
        assert capsys.readouterr().out == ("called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.child with arg 1\n")

    def test_set_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.set_itemtext
        """
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_itemtext(item, 'item text')
        assert capsys.readouterr().out == ("called TreeItem.setText with args (0, 'item text')\n"
                                           "called TreeItem.setTooltip with args (0, 'item text')\n")

    def test_get_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.get_itemtext
        """
        item = mockqtw.MockTreeItem('item text')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('item text',)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_itemtext(item) == "item text"
        assert capsys.readouterr().out == ("called TreeItem.text with arg 0\n")

    def test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        parent = mockqtw.MockTreeItem()
        def mock_parent(self):
            nonlocal parent
            print(f"called QTreeWidgetItem.parent with arg '{self}'")
            return parent
        def mock_parent_2(self):
            print(f"called QTreeWidgetItem.parent with arg '{self}'")
            return None
        monkeypatch.setattr(mockqtw.MockTreeItem, 'parent', mock_parent)
        item = mockqtw.MockTreeItem()
        parent.addChild('item0')
        parent.addChild(item)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.getitemparentpos(item)
        assert len(result) == 2
        assert isinstance(result[0], mockqtw.MockTreeItem)
        assert result[1] == 1
        assert capsys.readouterr().out == (f"called QTreeWidgetItem.parent with arg '{item}'\n"
                                           "called TreeItem.indexOfChild\n")
        monkeypatch.setattr(mockqtw.MockTreeItem, 'parent', mock_parent_2)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemparentpos(item) == (None, -1)
        assert capsys.readouterr().out == f"called QTreeWidgetItem.parent with arg '{item}'\n"

    def test_expand_item(self, monkeypatch, capsys):
        """unittest for TreePanel.expand_item
        """
        item = mockqtw.MockTreeItem('item text')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('item text',)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.expand_item(item)
        assert capsys.readouterr().out == ("called TreeItem.setExpanded with arg `True`\n")

    def test_collapse_item(self, monkeypatch, capsys):
        """unittest for TreePanel.collapse_item
        """
        item = mockqtw.MockTreeItem('item text')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('item text',)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.collapse_item(item)
        assert capsys.readouterr().out == ("called TreeItem.setExpanded with arg `False`\n")


class TestLogDialogGui:
    """unittest for gui_qt.LogDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.LogDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LogDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.LogDialogGui, '__init__', mock_init)
        testobj = testee.LogDialogGui()
        assert capsys.readouterr().out == 'called LogDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LogDialogGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='appicon')
        testobj = testee.LogDialogGui('master', parent, 'title', ('si', 'ze'))
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args {parent} () {{}}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called Dialog.setWindowIcon with args ('appicon',)\n"
                "called Dialog.resize with args ('si', 'ze')\n"
                "called VBox.__init__\n")

    def test_add_label(self, monkeypatch, capsys):
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label('labeltext')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called Label.__init__ with args ('labeltext',)\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_listbox(self, monkeypatch, capsys):
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_listbox(['data'], 'callback')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called List.__init__\n"
                "called List.addItems with arg `['data']`\n"
                "called Signal.connect with args ('callback',)\n"
                "called HBox.addWidget with arg MockListBox\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_buttons(self, monkeypatch, capsys):
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_buttons([('xx', 'callback1'), ('yy', 'callback2')])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback1',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback2',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_finish_dialog(self, monkeypatch, capsys):
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.finish_dialog()
        assert capsys.readouterr().out == (
                "called Dialog.setLayout with arg MockVBoxLayout\n"
                "called Dialog.exec\n")

    def test_get_selection(self, monkeypatch, capsys):
        """unittest for LogDialog.get_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        listbox = mockqtw.MockListBox()
        assert testobj.get_selection(listbox) == 'current item'
        assert capsys.readouterr().out == "called List.__init__\ncalled List.currentItem\n"

    def test_get_listitem_text(self, monkeypatch, capsys):
        """unittest for LogDialog.get_listitem_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockListItem()
        assert testobj.get_listitem_text(item) == ''
        assert capsys.readouterr().out == 'called ListItem.__init__\ncalled ListItem.text\n'

    def test_meld(self, monkeypatch, capsys):
        """unittest for LogDialog.meld
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.meld('title', 'text')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `title` `text`\n")

    def test_done(self, monkeypatch, capsys):
        """unittest for LogDialog.done
        """
        def mock_done(self, code):
            print(f'called Dialog.done with arg {code}')
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mock_done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.done()
        assert capsys.readouterr().out == ("called Dialog.done with arg 0\n")
        testobj.done('xxx')
        assert capsys.readouterr().out == ("called Dialog.done with arg 0\n")


class TestEditDialogGui:
    """unittest for gui_qt.EditDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.EditDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.EditDialogGui, '__init__', mock_init)
        testobj = testee.EditDialogGui('parent')
        assert capsys.readouterr().out == "called EditDialogGui.__init__ with args ('parent',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditDialogGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockWidget.resize)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='appicon')
        testobj = testee.EditDialogGui('master', parent, 'title')
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='appicon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called Dialog.setWindowIcon with args ('appicon',)\n"
                "called VBox.__init__\n")
        testobj = testee.EditDialogGui('master', parent, 'title', ('si', 'ze'))
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='appicon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called Dialog.setWindowIcon with args ('appicon',)\n"
                "called Widget.resize with args ('si', 'ze')\n"
                "called VBox.__init__\n")

    def test_add_outline(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_outline
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_outline(), testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called Frame.setFrameStyle with arg `32`\n"
                                           "called VBox.__init__\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n"
                                           "called VBox.addWidget with arg MockFrame\n")

    def test_add_label_to_outline(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_label_to_outline
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        box = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label_to_outline(box, 'text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called Label.__init__ with args ('text',)\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_buttons_to_outline(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_buttons_to_outline
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        box = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons_to_outline(box, [('xx', 'callback1'), ('yy', 'callback2')])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback1',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback2',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addSpacing\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for EditDialogGui.okcancel_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttons('oktext')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('oktext', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_finalize_dialog(self, monkeypatch, capsys):
        """unittest for EditDialogGui.finalize_dialog
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        focusfield = mockqtw.MockWidget()
        testobj.finalize_dialog(focusfield)
        assert capsys.readouterr().out == ("called Widget.__init__\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n"
                                           "called Widget.setFocus\n")

    def test_meld(self, monkeypatch, capsys):
        """unittest for EditDialogGui.meld
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.meld('title', 'message')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `title` `message`\n")

    def test_ask_question(self, monkeypatch, capsys):
        """unittest for EditDialogGui.ask_question
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ask_question('title', 'message')
        assert capsys.readouterr().out == (
                f"called MessageBox.question with args `{testobj}` `title` `message` `3` `1`\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for EditDialogGui.accept
        """
        def mock_confirm():
            print('called EditDialog.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mathter = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called EditDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestTextDialogGui:
    """unittest for gui_qt.TextDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.TextDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.TextDialogGui, '__init__', mock_init)
        testobj = testee.TextDialogGui('parent')
        assert capsys.readouterr().out == "called TextDialogGui.__init__ with args ('parent',)\n"
        return testobj

    def test_add_textfield(self, monkeypatch, capsys):
        """unittest for TextDialogGui.add_textfield
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_textfield('text')
        assert isinstance(result, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Editor.__init__ with args ({testobj},)\n"
                                           "called HBox.addSpacing\n"
                                           "called Editor.setText with arg `text`\n"
                                           "called HBox.addWidget with arg MockEditorWidget\n"
                                           "called HBox.addSpacing\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_textfield_text(self, monkeypatch, capsys):
        """unittest for TextDialogGui.get_textfield_text
        """
        textfield = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textfield_text(textfield) == 'editor text'
        assert capsys.readouterr().out == "called Editor.toPlainText\n"


class TestGridDialogGui:
    """unittest for gui_qt.GridDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.GridDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called GridDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.GridDialogGui, '__init__', mock_init)
        testobj = testee.GridDialogGui()
        assert capsys.readouterr().out == 'called GridDialogGui.__init__ with args ()\n'
        return testobj

    def test_add_table_to_outline(self, monkeypatch, capsys):
        """unittest for GridDialog.add_table_to_outline
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        box = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_table_to_outline(box, ['xxx', 'yyy'], (10, 20), None)
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['xxx', 'yyy']'\n"
                "called Table.horizontalHeader\n"
                "called Header.resizeSection with args (0, 10)\n"
                "called Header.resizeSection with args (1, 20)\n"
                "called Header.setStretchLastSection with arg True\n"
                "called Table.verticalHeader\n"
                "called Header.setVisible with arg False\n"
                "called Table.setTabKeyNavigation with arg False\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_table_to_outline(box, ['xxx', 'yyy'], (10, 20), [])
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['xxx', 'yyy']'\n"
                "called Table.horizontalHeader\n"
                "called Header.resizeSection with args (0, 10)\n"
                "called Header.resizeSection with args (1, 20)\n"
                "called Header.setStretchLastSection with arg True\n"
                "called Table.verticalHeader\n"
                "called Header.setVisible with arg False\n"
                "called Table.setTabKeyNavigation with arg False\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_table_to_outline(box, ['xxx', 'yyy'], (10, 20), [('a', 'bbb'),
                                                                              ('c', 'ddd')])
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['xxx', 'yyy']'\n"
                "called Table.horizontalHeader\n"
                "called Header.resizeSection with args (0, 10)\n"
                "called Header.resizeSection with args (1, 20)\n"
                "called Header.setStretchLastSection with arg True\n"
                "called Table.verticalHeader\n"
                "called Header.setVisible with arg False\n"
                "called Table.setTabKeyNavigation with arg False\n"
                "called Table.rowCount\n"
                "called Table.insertRow with arg '0'\n"
                "called Table.setItem with args (0, 0, QTableWidgetItem)\n"
                "called Table.setItem with args (0, 1, QTableWidgetItem)\n"
                "called Table.rowCount\n"
                "called Table.insertRow with arg '1'\n"
                "called Table.setItem with args (1, 0, QTableWidgetItem)\n"
                "called Table.setItem with args (1, 1, QTableWidgetItem)\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_getrowcount(self, monkeypatch, capsys):
        """unittest for GridDialog.getrowcount
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getrowcount(table)
        assert capsys.readouterr().out == "called Table.rowCount\n"

    def test_get_tableitem(self, monkeypatch, capsys):
        """unittest for GridDialog.get_tableitem
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.get_tableitem(table, 'row', 'col')
        assert result == 'tableitem at row, col'
        assert capsys.readouterr().out == "called Table.item with args (row, col)\n"

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for GridDialog.get_item_text
        """
        item = mockqtw.MockTableItem()
        assert capsys.readouterr().out == "called TableItem.__init__ with arg ''\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_text(item) == ''
        assert capsys.readouterr().out == "called TableItem.text\n"

    def test_add_row_to_table(self, monkeypatch, capsys):
        """unittest for GridDialog.add_row_to_table
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_row_to_table(table)
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.setRowCount with arg '1'\n")

    def test_delete_row_from_table(self, monkeypatch, capsys):
        """unittest for GridDialog.remove_row_from_table
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_row_from_table(table)
        assert capsys.readouterr().out == ("called Table.currentRow\n"
                                           "called Table.removeRow with arg '2'\n")


class TestListDialogGui:
    """unittest for gui_qt.ListDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.ListDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ListDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.ListDialogGui, '__init__', mock_init)
        parent = types.SimpleNamespace()
        testobj = testee.ListDialogGui(parent)
        assert capsys.readouterr().out == f'called ListDialogGui.__init__ with args ({parent},)\n'
        return testobj

    def test_add_list_to_outline(self, monkeypatch, capsys):
        """unittest for ListDialog.add_list_to_outline
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        box = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_list_to_outline(box, [])
        assert isinstance(result, testee.qtw.QListWidget)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addSpacing\n"
                                           "called List.__init__\n"
                                           "called HBox.addWidget with arg MockListBox\n"
                                           "called HBox.addSpacing\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_list_to_outline(box, ['x'])
        assert isinstance(result, testee.qtw.QListWidget)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addSpacing\n"
                                           "called List.__init__\n"
                                           "called List.addItems with arg `['x']`\n"
                                           "called HBox.addWidget with arg MockListBox\n"
                                           "called HBox.addSpacing\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_select_item(self, monkeypatch, capsys):
        """unittest for ListDialog.select_item
        """
        def mock_get(self, *args):
            print('called InputDialog.getItem with args', args)
            return 'yyy', 'z'
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_item('title', 'caption', ['choice']) == ('yyy', 'z')
        assert capsys.readouterr().out == ("called InputDialog.getItem with args"
                                           " ('title', 'caption', ['choice'], 0, False)\n")
        assert testobj.select_item('title', 'caption', ['choice'], 1, True) == ('yyy', 'z')
        assert capsys.readouterr().out == ("called InputDialog.getItem with args"
                                           " ('title', 'caption', ['choice'], 1, True)\n")

    def test_ask_for_text(self, monkeypatch, capsys):
        """unittest for ListDialog.ask_for_text
        """
        def mock_get(self, *args, **kwargs):
            print('called InputDialog.getText with args', args, kwargs)
            return 'yyy','z'
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_text('title', 'caption') == ('yyy', 'z')
        assert capsys.readouterr().out == ("called InputDialog.getText with args"
                                           " ('title', 'caption') {'text': ''}\n")
        assert testobj.ask_for_text('title', 'caption', 'qqq') == ('yyy', 'z')
        assert capsys.readouterr().out == ("called InputDialog.getText with args"
                                           " ('title', 'caption') {'text': 'qqq'}\n")

    def test_add_row_to_list(self, monkeypatch, capsys):
        """unittest for GridDialog.add_row_to_table
        """
        listbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_row_to_list(listbox, 'xxx')
        assert capsys.readouterr().out == "called List.addItem with arg `xxx`\n"

    def test_get_listitem(self, monkeypatch, capsys):
        """unittest for GridDialog.get_tableitem
        """
        listbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.get_listitem(listbox)
        assert result == 'current item'
        assert capsys.readouterr().out == "called List.currentItem\n"
        result = testobj.get_listitem(listbox, 1)
        assert result is None
        assert capsys.readouterr().out == "called List.item with arg 1\n"

    def test_get_itemtext(self, monkeypatch, capsys):
        """unittest for GridDialog.get_itemtext
        """
        item = mockqtw.MockTableItem()
        assert capsys.readouterr().out == "called TableItem.__init__ with arg ''\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_itemtext(item) == ''
        assert capsys.readouterr().out == "called TableItem.text\n"

    def test_set_itemtext(self, monkeypatch, capsys):
        """unittest for GridDialog.set_itemtext
        """
        item = mockqtw.MockTableItem()
        assert capsys.readouterr().out == "called TableItem.__init__ with arg ''\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_itemtext(item, 'text')
        assert capsys.readouterr().out == f"called TableItem.setText with arg 'text'\n"

    def test_delete_row_from_list(self, monkeypatch, capsys):
        """unittest for GridDialog.remove_row_from_tabele
        """
        lbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_row_from_list(lbox)
        assert capsys.readouterr().out == ("called List.currentRow\n"
                                           "called List.takeItem with arg `current row`\n")

    def test_get_list_length(self, monkeypatch, capsys):
        """unittest for ListDialog.get_list_length
        """
        lbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_list_length(lbox)
        assert capsys.readouterr().out == ("called List.count\n")
