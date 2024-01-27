"""unittests for ./cssedit/editor/gui_qt.py
"""
import os
import sys
import pytest
# import cssutils   - als het goed is heb ik deze niet nodig
from mockgui import mockqtwidgets as mockqtw

HERE = os.path.dirname(os.path.abspath(__file__))
here = os.path.join(os.path.dirname(HERE), 'editor')
sys.path.append(here)
from cssedit.editor import gui_qt as testee


class MockMainGui():
    """stub for gui_qt.MainGui object
    """
    def __init__(self, *args):
        """stub
        """
        print('called MainGui.__init__ with args', args)


class _TestMainGui:
    """unittest for gui_qt.MainGui
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.__init__(self, master, app, title='', pos=(0, 0), size=(800, 500)) == expected_result

    def _test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.create_menu(self, menudata) == expected_result

    def _test_just_show(self, monkeypatch, capsys):
        """unittest for MainGui.just_show
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.just_show(self) == expected_result

    def _test_set_modality_and_show(self, monkeypatch, capsys):
        """unittest for MainGui.set_modality_and_show
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.set_modality_and_show(self, modal) == expected_result

    def _test_show_message(self, monkeypatch, capsys):
        """unittest for MainGui.show_message
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.show_message(self, text, title="") == expected_result

    def _test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.show_statusmessage(self, text) == expected_result

    def _test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.close(self) == expected_result

    def _test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.set_window_title(self, title='') == expected_result

    def _test_set_waitcursor(self, monkeypatch, capsys):
        """unittest for MainGui.set_waitcursor
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.set_waitcursor(self, on) == expected_result

    def _test_show_save_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_save_dialog
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.show_save_dialog(self, start, filter) == expected_result

    def _test_show_open_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_open_dialog
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.show_open_dialog(self, start, filter) == expected_result

    def _test_get_input_text(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_text
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.get_input_text(self, prompt) == expected_result

    def _test_get_input_choice(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_choice
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.get_input_choice(self, prompt, choices, editable=False) == expected_result

    def _test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_dialog
        """
        testobj = MockMainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()'
        # assert testobj.show_dialog(self, cls, *args) == expected_result


class MockTreePanel():
    """stub for gui_qt.TreePanel object
    """
    def __init__(self, *args):
        """stub
        """
        print('called TreePanel.__init__ with args', args)


class _TestTreePanel:
    """unittest for gui_qt.TreePanel
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for TreePanel.__init__
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.__init__(self, parent) == expected_result

    def _test_selectionChanged(self, monkeypatch, capsys):
        """unittest for TreePanel.selectionChanged
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.selectionChanged(self, newsel, oldsel) == expected_result

    def _test_dropEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.dropEvent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.dropEvent(self, event) == expected_result

    def _test_mousePressEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mousePressEvent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.mousePressEvent(self, event) == expected_result

    def _test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mouseReleaseEvent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.mouseReleaseEvent(self, event) == expected_result

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.keyReleaseEvent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.keyReleaseEvent(self, event) == expected_result

    def _test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.create_popupmenu(self, item) == expected_result

    def _test_remove_root(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_root
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.remove_root(self) == expected_result

    def _test_init_root(self, monkeypatch, capsys):
        """unittest for TreePanel.init_root
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.init_root(self) == expected_result

    def _test_set_root_text(self, monkeypatch, capsys):
        """unittest for TreePanel.set_root_text
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.set_root_text(self, text) == expected_result

    def _test_get_root(self, monkeypatch, capsys):
        """unittest for TreePanel.get_root
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.get_root(self) == expected_result

    def _test_activate_rootitem(self, monkeypatch, capsys):
        """unittest for TreePanel.activate_rootitem
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.activate_rootitem(self) == expected_result

    def _test_set_activeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.set_activeitem
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.set_activeitem(self, item) == expected_result

    def _test_set_focus(self, monkeypatch, capsys):
        """unittest for TreePanel.set_focus
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.set_focus(self) == expected_result

    def _test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.add_to_parent(self, titel, parent, pos=-1) == expected_result

    def _test_setcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.setcurrent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.setcurrent(self, item) == expected_result

    def _test_getcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.getcurrent
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.getcurrent(self) == expected_result

    def _test_new_treeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.new_treeitem
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.new_treeitem(self, itemtext) == expected_result

    def _test_add_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.add_subitem
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.add_subitem(self, parent, child, ix=-1) == expected_result

    def _test_remove_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_subitem
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.remove_subitem(self, parent, ix) == expected_result

    def _test_get_subitems(self, monkeypatch, capsys):
        """unittest for TreePanel.get_subitems
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.get_subitems(self, item) == expected_result

    def _test_set_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.set_itemtext
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.set_itemtext(self, item, itemtext) == expected_result

    def _test_get_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.get_itemtext
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.get_itemtext(self, item) == expected_result

    def _test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.getitemparentpos(self, item) == expected_result

    def _test_expand_item(self, monkeypatch, capsys):
        """unittest for TreePanel.expand_item
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.expand_item(self, item) == expected_result

    def _test_collapse_item(self, monkeypatch, capsys):
        """unittest for TreePanel.collapse_item
        """
        testobj = MockTreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()'
        # assert testobj.collapse_item(self, item) == expected_result


class MockLogDialog():
    """stub for gui_qt.LogDialog object
    """
    def __init__(self, *args):
        """stub
        """
        print('called LogDialog.__init__ with args', args)


class _TestLogDialog:
    """unittest for gui_qt.LogDialog
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for LogDialog.__init__
        """
        testobj = MockLogDialog()
        assert capsys.readouterr().out == 'called LogDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, log) == expected_result

    def _test_itemDoubleClicked(self, monkeypatch, capsys):
        """unittest for LogDialog.itemDoubleClicked
        """
        testobj = MockLogDialog()
        assert capsys.readouterr().out == 'called LogDialog.__init__ with args ()'
        # assert testobj.itemDoubleClicked(self, item) == expected_result

    def _test_show_context(self, monkeypatch, capsys):
        """unittest for LogDialog.show_context
        """
        testobj = MockLogDialog()
        assert capsys.readouterr().out == 'called LogDialog.__init__ with args ()'
        # assert testobj.show_context(self, item=None) == expected_result

    def _test_done(self, monkeypatch, capsys):
        """unittest for LogDialog.done
        """
        testobj = MockLogDialog()
        assert capsys.readouterr().out == 'called LogDialog.__init__ with args ()'
        # assert testobj.done(self, arg=None) == expected_result


class MockTextDialog():
    """stub for gui_qt.TextDialog object
    """
    def __init__(self, *args):
        """stub
        """
        print('called TextDialog.__init__ with args', args)


class _TestTextDialog:
    """unittest for gui_qt.TextDialog
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for TextDialog.__init__
        """
        testobj = MockTextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title='', text=''):  # , comment=False) == expected_result

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for TextDialog.on_cancel
        """
        testobj = MockTextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()'
        # assert testobj.on_cancel(self) == expected_result

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for TextDialog.on_ok
        """
        testobj = MockTextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()'
        # assert testobj.on_ok(self) == expected_result


class MockGridDialog():
    """stub for gui_qt.GridDialog object
    """
    def __init__(self, *args):
        """stub
        """
        print('called GridDialog.__init__ with args', args)


class _TestGridDialog:
    """unittest for gui_qt.GridDialog
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for GridDialog.__init__
        """
        testobj = MockGridDialog()
        assert capsys.readouterr().out == 'called GridDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title='', itemlist=None):  # , comment=False) == expected_result

    def _test_on_add(self, monkeypatch, capsys):
        """unittest for GridDialog.on_add
        """
        testobj = MockGridDialog()
        assert capsys.readouterr().out == 'called GridDialog.__init__ with args ()'
        # assert testobj.on_add(self) == expected_result

    def _test_on_del(self, monkeypatch, capsys):
        """unittest for GridDialog.on_del
        """
        testobj = MockGridDialog()
        assert capsys.readouterr().out == 'called GridDialog.__init__ with args ()'
        # assert testobj.on_del(self) == expected_result

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for GridDialog.on_cancel
        """
        testobj = MockGridDialog()
        assert capsys.readouterr().out == 'called GridDialog.__init__ with args ()'
        # assert testobj.on_cancel(self) == expected_result

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for GridDialog.on_ok
        """
        testobj = MockGridDialog()
        assert capsys.readouterr().out == 'called GridDialog.__init__ with args ()'
        # assert testobj.on_ok(self) == expected_result


class MockListDialog():
    """stub for gui_qt.ListDialog object
    """
    def __init__(self, *args):
        """stub
        """
        print('called ListDialog.__init__ with args', args)


class _TestListDialog:
    """unittest for gui_qt.ListDialog
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for ListDialog.__init__
        """
        testobj = MockListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title='', itemlist=None):  # , comment=False) == expected_result

    def _test_on_add(self, monkeypatch, capsys):
        """unittest for ListDialog.on_add
        """
        testobj = MockListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()'
        # assert testobj.on_add(self) == expected_result

    def _test_on_edit(self, monkeypatch, capsys):
        """unittest for ListDialog.on_edit
        """
        testobj = MockListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()'
        # assert testobj.on_edit(self) == expected_result

    def _test_on_del(self, monkeypatch, capsys):
        """unittest for ListDialog.on_del
        """
        testobj = MockListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()'
        # assert testobj.on_del(self) == expected_result

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for ListDialog.on_cancel
        """
        testobj = MockListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()'
        # assert testobj.on_cancel(self) == expected_result

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for ListDialog.on_ok
        """
        testobj = MockListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()'
        # assert testobj.on_ok(self) == expected_result
