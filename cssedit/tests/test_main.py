"""unittests for ./cssedit/editor/main.py
"""
import os
import sys
import pytest
# import cssutils   - als het goed is heb ik deze niet nodig

HERE = os.path.dirname(os.path.abspath(__file__))
here = os.path.join(os.path.dirname(HERE), 'editor')
sys.path.append(here)
from cssedit.editor import main as testee


class MockEditor():
    """stub for main.Editor object
    """
    def __init__(self, *args):
        """stub
        """
        print('called Editor.__init__ with args', args)

def setup_editor(monkeypatch, capsys):
    """setup and return testdouble for main.Editor object
    """
    def mock_init(self, *args):
        """stub
        """
        print('called Editor.__init__ with args', args)
    monkeypatch.setattr(testee.Editor, '__init__', mock_init)
    testobj = Editor()
    assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
    return testobj

class _TestEditor:
    """unittest for main.Editor
    """
    def _test___init__(self, monkeypatch, capsys):
        """unittest for Editor.__init__
        """
        monkeypatch.setattr(testee.Editor, 'methodname', mock_method)
        testobj = testee.Editor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.__init__(self, parent=None, parentpos=(0, 0), app=None) == expected_result

    def _test_show_gui(self, monkeypatch, capsys):
        """unittest for Editor.show_gui
        """
        # testobj = MockEditor()
        # assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        testobj = setup_testobj()
        # assert testobj.show_gui(self) == expected_result

    def _test_show_from_external(self, monkeypatch, capsys):
        """unittest for Editor.show_from_external
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.show_from_external(self, modal=True) == expected_result

    def _test_getfilename(self, monkeypatch, capsys):
        """unittest for Editor.getfilename
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.getfilename(self, title='', start='', save=False) == expected_result

    def _test_newfile(self, monkeypatch, capsys):
        """unittest for Editor.newfile
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.newfile(self) == expected_result

    def _test_open(self, monkeypatch, capsys):
        """unittest for Editor.open
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.open(self, **kwargs) == expected_result

    def _test_build_loaded_message(self, monkeypatch, capsys):
        """unittest for Editor.build_loaded_message
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.build_loaded_message(self) == expected_result

    def _test_openfile(self, monkeypatch, capsys):
        """unittest for Editor.openfile
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.openfile(self) == expected_result

    def _test_reopenfile(self, monkeypatch, capsys):
        """unittest for Editor.reopenfile
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.reopenfile(self) == expected_result

    def _test_texttotree(self, monkeypatch, capsys):
        """unittest for Editor.texttotree
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.texttotree(self) == expected_result

    def _test_treetotext(self, monkeypatch, capsys):
        """unittest for Editor.treetotext
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.treetotext(self) == expected_result

    def _test_savefile(self, monkeypatch, capsys):
        """unittest for Editor.savefile
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.savefile(self) == expected_result

    def _test_savefileas(self, monkeypatch, capsys):
        """unittest for Editor.savefileas
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.savefileas(self) == expected_result

    def _test_save(self, monkeypatch, capsys):
        """unittest for Editor.save
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.save(self) == expected_result

    def _test_show_log(self, monkeypatch, capsys):
        """unittest for Editor.show_log
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.show_log(self) == expected_result

    def _test_exit(self, monkeypatch, capsys):
        """unittest for Editor.exit
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.exit(self) == expected_result

    def _test_close(self, monkeypatch, capsys):
        """unittest for Editor.close
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.close(self) == expected_result

    def _test_wait_cursor(self, monkeypatch, capsys):
        """unittest for Editor.wait_cursor
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.wait_cursor(self) == expected_result

    def _test_determine_level(self, monkeypatch, capsys):
        """unittest for Editor.determine_level
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.determine_level(self, item) == expected_result

    def _test_checkselection(self, monkeypatch, capsys):
        """unittest for Editor.checkselection
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.checkselection(self) == expected_result

    def _test_is_rule_parent(self, monkeypatch, capsys):
        """unittest for Editor.is_rule_parent
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.is_rule_parent(self, item) == expected_result

    def _test_is_rule_item(self, monkeypatch, capsys):
        """unittest for Editor.is_rule_item
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.is_rule_item(self, item) == expected_result

    def _test_mark_dirty(self, monkeypatch, capsys):
        """unittest for Editor.mark_dirty
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.mark_dirty(self, state) == expected_result

    def _test_add(self, monkeypatch, capsys):
        """unittest for Editor.add
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.add(self) == expected_result

    def _test_add_after(self, monkeypatch, capsys):
        """unittest for Editor.add_after
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.add_after(self) == expected_result

    def _test_add_before(self, monkeypatch, capsys):
        """unittest for Editor.add_before
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.add_before(self) == expected_result

    def _test_add_under(self, monkeypatch, capsys):
        """unittest for Editor.add_under
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.add_under(self) == expected_result

    def _test_add_rule(self, monkeypatch, capsys):
        """unittest for Editor.add_rule
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.add_rule(self, parent=None, after=None) == expected_result

    def _test_edit(self, monkeypatch, capsys):
        """unittest for Editor.edit
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.edit(self) == expected_result

    def _test_edit_text_node(self, monkeypatch, capsys):
        """unittest for Editor.edit_text_node
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.edit_text_node(self, title) == expected_result

    def _test_edit_list_node(self, monkeypatch, capsys):
        """unittest for Editor.edit_list_node
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.edit_list_node(self, title) == expected_result

    def _test_edit_grid_node(self, monkeypatch, capsys):
        """unittest for Editor.edit_grid_node
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.edit_grid_node(self, title) == expected_result

    def _test_delete(self, monkeypatch, capsys):
        """unittest for Editor.delete
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.delete(self) == expected_result

    def _test_cut(self, monkeypatch, capsys):
        """unittest for Editor.cut
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.cut(self) == expected_result

    def _test_copy(self, monkeypatch, capsys):
        """unittest for Editor.copy
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.copy(self) == expected_result

    def _test__copy_rule(self, monkeypatch, capsys):
        """unittest for Editor._copy_rule
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj._copy_rule(self, cut=True, retain=True) == expected_result

    def _test_paste_under(self, monkeypatch, capsys):
        """unittest for Editor.paste_under
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.paste_under(self) == expected_result

    def _test_paste_after(self, monkeypatch, capsys):
        """unittest for Editor.paste_after
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.paste_after(self) == expected_result

    def _test_paste_before(self, monkeypatch, capsys):
        """unittest for Editor.paste_before
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.paste_before(self) == expected_result

    def _test__paste_rule(self, monkeypatch, capsys):
        """unittest for Editor._paste_rule
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj._paste_rule(self, under=False, after=True) == expected_result

    def _test__paste(self, monkeypatch, capsys):
        """unittest for Editor._paste
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj._paste(self, item, parent, indx=0) == expected_result

    def _test_expand_item(self, monkeypatch, capsys):
        """unittest for Editor.expand_item
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.expand_item(self) == expected_result

    def _test_expand_all(self, monkeypatch, capsys):
        """unittest for Editor.expand_all
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.expand_all(self) == expected_result

    def _test__expand(self, monkeypatch, capsys):
        """unittest for Editor._expand
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj._expand(self, recursive=False) == expected_result

    def _test_collapse_item(self, monkeypatch, capsys):
        """unittest for Editor.collapse_item
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.collapse_item(self) == expected_result

    def _test_collapse_all(self, monkeypatch, capsys):
        """unittest for Editor.collapse_all
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.collapse_all(self) == expected_result

    def _test__collapse(self, monkeypatch, capsys):
        """unittest for Editor._collapse
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj._collapse(self, recursive=False) == expected_result

    def _test_no_op(self, monkeypatch, capsys):
        """unittest for Editor.no_op
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.no_op(self) == expected_result

    def _test_show_level(self, monkeypatch, capsys):
        """unittest for Editor.show_level
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.show_level(self) == expected_result

    def _test_add_subitems(self, monkeypatch, capsys):
        """unittest for Editor.add_subitems
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.add_subitems(self, parent, item) == expected_result

    def _test_paste_item(self, monkeypatch, capsys):
        """unittest for Editor.paste_item
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.paste_item(self, item, parent, ix=-1) == expected_result

    def _test_read_rules(self, monkeypatch, capsys):
        """unittest for Editor.read_rules
        """
        testobj = MockEditor()
        assert capsys.readouterr().out == 'called Editor.__init__ with args ()'
        # assert testobj.read_rules(self, data) == expected_result
