"""CSS Editor application - main, gui-independent code
"""
import os
# import sys
import contextlib

try:
    import cssedit.editor.cssedit as ed  # helper class for css specific stuff
    from cssedit.editor import gui       # helper class for visualisation (a.k.a. GUI)
except ImportError:  #  as e:
#     try:
        # deze imports werken als ik cssedit standalone opstart
        import editor.cssedit as ed  # helper class for css specific stuff
        from editor import gui       # helper class for visualisation (a.k.a. GUI)
#     except ImportError  # as e:
#         import cssedit as ed   # helper class for css specific stuff
#         import gui             # helper class for visualisation (a.k.a. GUI)


HERE = os.path.dirname(__file__)
RTYPES, CTYPES = [], set()
for components in ed.RTYPES.values():
    RTYPES.append(components[0])
    CTYPES.update([x for x in components[1]])


def get_ruletype_for_name(name):
    """return ruletype code by ruletype name
    """
    ruletype = None
    for rtype, rname in [(x, y[0]) for x, y in ed.RTYPES.items()]:
        if rname == name:
            ruletype = rtype
            break
    # if ruletype is None:
    #     continue
    return ruletype


class Editor:
    """Hoofdscherm van de applicatie
    """
    # TODO: zoeken/filteren in tags (vgl hoe dit in hotkeys is gedaan)
    # - ook in properties voor bekijken gelijksoortige stijlen


    def __init__(self, parent=None, parentpos=(0, 0), app=None):
        self.parent = parent
        self.app_title = 'CSSEdit'
        self.app_iconame = os.path.join(HERE, 'csseditor.png')
        self.gui = gui.MainGui(self, app, pos=parentpos)
        self.gui.show_statusmessage('Ready')
        self.mode = ''
        self.actiondict = {}
        self.gui.create_menu(self.get_menu_data())
        ## self.undo_stack = UndoRedoStack(self)
        self.css = None
        self.cut_item, self.cutlevel = None, 0
        self.newfile()

    def show_gui(self):
        "start gui in standalone mode"
        self.gui.just_show()

    def show_from_external(self, modal=True):
        """blokkerend gedrag instellen als aangestuurd vanuit bv. Htmledit
        """
        self.gui.set_modality_and_show(modal)

    def get_menu_data(self):
        return (
            ('&Application', (
                ('Set output &Format',
                 (('&Compressed (no linefeeds)',),  # TODO: these options
                  ('&Short',),        # should be checkable and remembered;
                  ('&Medium',),       # or would an options dialog be a better idea?
                  ('&Long',)),        # see Trac wiki
                 '', '', 'Indicate how output should be saved'),
                ('E&xit', self.exit, 'Ctrl+Q', '', 'Quit the application'),),),
            ('&File', (
                ('&New', self.newfile, 'Ctrl+Insert', '', 'Start a new css file'),
                ('&Open', self.openfile, 'Ctrl+O', '', 'Open a css file'),
                ('&Reload', self.reopenfile, 'Ctrl+R', '',
                 'Discard all changes and reopen the current css file'),
                ('&Save', self.savefile, 'Ctrl+S', '', 'Save the current css file'),
                ('Save &As', self.savefileas, 'Ctrl+Shift+S', '',
                 'Save the current css file under a different name'),
                (),
                ('Show &Log', self.show_log, 'Ctrl+Shift+L', '',
                 'Show messages from parsing this file'),),),
            ('&View', (
                # ('&Show level', self.show_level, '', '',  'Show number of levels under root'),
                # ('Expand', self.expand_item, 'Alt+Plus', '', 'Expand tree item'),
                # ('Collapse', self.collapse_item, 'Alt+Minus', '', 'Collapse tree item'),
                ('&Expand all', self.expand_all, 'Ctrl++', '', 'Expand all subitems'),
                ('&Collapse all', self.collapse_all, 'Ctrl+-', '',
                 'Collapse all subitems'),),),
            ('&Rule', (
                ('Add under root', self.add, 'Ctrl+N', '',
                 'Add a new top level CSS rule at the end'),
                ('Insert after', self.add_after, 'Ctrl+Shift+N', '',
                 'Add a new rule after the current one'),
                ('Insert before', self.add_before, 'Ctrl+Alt+N', '',
                 'Add a new rule before the current one'),
                ('Add under "rules" node', self.add_under, 'Alt+Shift+N', '',
                 'Add a new CSS rule at the end ("rules" node only)'),
                ('Delete', self.delete, 'Del,Ctrl+D', '', 'Delete the current rule'),
                ('Cut', self.cut, 'Ctrl+X', '', 'Cut (copy and delete) the current rule'),
                ('Copy', self.copy, 'Ctrl+C', '', 'Copy the current rule'),
                ('Paste after', self.paste_after, 'Ctrl+V', '',
                 'Insert the copied rule after the current one'),
                ('Paste before', self.paste_before, 'Shift+Ctrl+V', '',
                 'Insert the copied rule before the current one'),
                ('Paste under "rules" node', self.paste_under, 'Ctrl+Alt+V', '',
                 'Insert the copied rule beneath the current node ("rules" only)'),),),
            ('Rule &Component', (
                ('Edit', self.edit, 'F2,Ctrl+E', '', 'Edit a rule component'),),),)

    def getfilename(self, title='', start='', save=False):
        "pop up a dialog to get a filename"
        if title == '':
            title = 'Save File' if save else 'Open File'
        if start == '':
            start = os.getcwd()
        filter = "CSS files (*.css)"
        if save:
            filename = self.gui.show_save_dialog(start, filter)
        else:
            filename = self.gui.show_open_dialog(start, filter)
        ok = bool(filename)
        return ok, filename

    def newfile(self):
        "start a new css file"
        self.gui.tree.remove_root()
        self.project_file = ""
        self.css = ed.Editor(new=True)
        self.gui.tree.init_root()
        self.gui.tree.set_activeitem(self.gui.tree.root)
        self.gui.tree.expand_item(self.gui.tree.root)
        self.mark_dirty(False)

    def open(self, **kwargs):
        "open an existing css file"
        if 'filename' in kwargs:
            self.mode = 'file'
        elif 'tag' in kwargs:
            self.mode = 'tag'
        else:
            self.mode = 'text'
        self.newfile()
        fname = kwargs.get('filename', '')
        self.project_file = os.path.abspath(fname) if fname else ''
        self.gui.tree.set_root_text(self.project_file or "(no file)")

        with self.wait_cursor():
            self.css = ed.Editor(**kwargs)
            self.css.datatotext()
            self.texttotree()
        self.gui.show_statusmessage(self.build_loaded_message())

        self.gui.tree.activate_rootitem()
        self.gui.tree.set_focus()

    def build_loaded_message(self):
        """inform about warnings and errors on loading
        """
        mld = 'file loaded'
        warn = err = misc = 0
        for line in self.css.log:
            if line.startswith('WARNING'):
                warn += 1
            elif line.startswith('ERROR'):
                err += 1
            else:
                misc += 1
        if warn + err + misc > 0:
            mld += ' with '
            if warn > 0:
                mld += f'{warn} warnings'
                if err > 0 and misc > 0:
                    mld += ', '
                elif err > 0 or misc > 0:
                    mld += ' and '
            if err > 0:
                mld += f'{err} errors'
                if misc > 0:
                    mld += ' and '
            if misc > 0:
                mld += f'{misc} misc. messages'
        return mld

    def openfile(self):
        """callback for menu entry "open"
        """
        ok, filename = self.getfilename(title=self.app_title + ' - open file')
        if ok:
            self.open(filename=filename)

    def reopenfile(self):
        """callback for menu option "reload"
        """
        self.open(filename=self.project_file)

    def texttotree(self):
        """convert internal data to visual data
        """
        for item in self.read_rules(self.css.textdata):
            self.gui.tree.add_subitem(self.gui.tree.root, item)

    def treetotext(self):
        """convert visual data to internal data
        """
        data = []
        for rule_item in self.gui.tree.get_subitems(self.gui.tree.root):
            rule_type = self.gui.tree.get_itemtext(rule_item)
            rule_data = {}
            for key_item in self.gui.tree.get_subitems(rule_item):
                key_text = self.gui.tree.get_itemtext(key_item)
                key_data = None
                if key_text in ('text', 'data'):
                    key_data = self.gui.tree.get_itemtext(self.gui.tree.get_subitems(key_item)[0])
                elif key_text in ('selectors', 'media', 'rules'):
                    key_data = []
                    for list_item in self.gui.tree.get_subitems(key_item):
                        key_data.append(self.gui.tree.get_itemtext(list_item))
                        if key_text == 'rules':
                            # TODO: onderliggende ruledata toevoegen
                            pass
                elif key_text in ('styles',):
                    key_data = {}
                    for dict_item in self.gui.tree.get_subitems(key_item):
                        item_key = self.gui.tree.get_itemtext(dict_item)
                        item_value = self.gui.tree.get_itemtext(
                                self.gui.tree.get_subitems(dict_item)[0])
                        key_data[item_key] = item_value
                rule_data[key_text] = key_data
            data.append((rule_type, rule_data))
        return data

    def savefile(self):
        """callback for menu option "save"
        """
        if self.project_file:
            self.save()
        else:
            self.savefileas()

    def savefileas(self):
        """callback for menu option "save as"
        """
        ok, filename = self.getfilename(title=self.app_title + ' - save file as',
                                        start=self.project_file, save=True)
        if ok:
            self.project_file = filename
            self.save()
            self.gui.tree.set_root_text(self.project_file)

    def save(self):
        """save to file
        """
        self.css.filename = self.project_file
        with self.wait_cursor():
            self.css.textdata = self.treetotext()
            self.css.texttodata()
            self.css.return_to_source()
        self.mark_dirty(False)

    def show_log(self):
        """show the messages generated when loading the file
        """
        if self.css:
            gui.LogDialog(self.gui, self.css.log)
        else:
            self.show_statusmessage('Load a css file first')

    def exit(self):
        """quit the application
        """
        self.gui.close()

    def close(self):
        """for "embedded" use: return modified data to parent before closing
        """
        # print('in csseditor.close, parent is', self.parent)
        if self.parent:
            self.css.textdata = self.treetotext()
            self.css.texttodata()
            self.css.return_to_source(savemode='compressed')
            # if we've saved, the data is not bytes but a stylesheet. So we need to get the text
            try:
                print('trying to decode data.cssText')
                # nog niet gezien dat-ie hier geen exception op kreeg
                # kennelijk heb ik text2data zo aangepast dat dit niet meer hoeft
                self.parent.styledata = self.css.data.cssText
            except AttributeError:
                print('taking data as-is')
                self.parent.styledata = self.css.data
            try:
                self.parent.styledata = self.parent.styledata.decode()
            except AttributeError:
                print("'sometimes it's not bytes but already a string")
                # dat is blijkbaar als ik een inline style aan een element toevoeg
            # voor zolang als de output optie nog niet in te stellen is
            self.parent.styledata = self.parent.styledata.replace('\n', '').replace(' ', '')
            self.parent.cssfilename = self.project_file

    @contextlib.contextmanager
    def wait_cursor(self):
        """change cursor before and after executing some function
        """
        self.gui.set_waitcursor(True)
        yield
        self.gui.set_waitcursor(False)

    def determine_level_orig(self, item):
        """determine the level of a node in the tree
        """
        level = 0
        test = self.gui.tree.getitemparentpos(item)[0]
        if test == self.gui.tree.root:
            level = self.determine_level_orig(test)
        return level + 1

    def determine_level(self, item):
        """determine the level of a node in the tree
        """
        level = 0
        test = self.gui.tree.getitemparentpos(item)[0]
        while test != self.gui.tree.root:
            level += 1
            test = self.gui.tree.getitemparentpos(test)[0]
        return level

    def checkselection(self):
        """controleer of er wel iets geselecteerd is (behalve de filenaam)
        """
        sel = True
        self.item = self.gui.tree.getcurrent()
        self.itemlevel = 0
        if self.item is None or self.item == self.gui.tree.root:
            self.gui.show_message('You need to select an element or text first')
            sel = False
        else:
            self.itemlevel = self.determine_level(self.item)  # TODO: check
        return sel

    def is_rule_parent(self, item):
        """determine if a node is parent to a css rule
        """
        ok = False
        if item == self.gui.tree.root or self.gui.tree.get_itemtext(item) == "rules":
            ok = True
        if not ok:
            self.gui.show_message("Can't add or paste rule here")
        return ok

    def is_rule_item(self, item):
        """determine if a node is part of a css rule
        """
        ok = True
        test = self.gui.tree.get_itemtext(item)
        if test not in RTYPES:
            ok = False
        if not ok:
            self.gui.show_message(f"Can't do this; {test} is not a rule item")
        return ok

    def mark_dirty(self, state):
        """show the "modified" status of the data
        """
        title = self.app_title
        if state:
            title += ' (modified)'
        self.gui.set_window_title(title)
        self.project_dirty = state

    def add(self):
        """callback for menu option
        """
        self.add_rule(parent=self.gui.tree.root)

    def add_after(self):
        """callback for menu option
        """
        if not self.checkselection():
            return
        self.add_rule(after=True)

    def add_before(self):
        """callback for menu option
        """
        if not self.checkselection():
            return
        self.add_rule(after=False)

    def add_under(self):
        """callback for menu option
        """
        if not self.checkselection():
            return
        self.add_rule(parent=self.item)

    def add_rule(self, parent=None, after=None):
        """add new rule
        "at the end" is only possible on top level - otherwise use the "rules" node
        """
        if parent is None:
            parent = self.gui.tree.getitemparentpos(self.item)[0]
        if not self.is_rule_parent(parent):
            return
        if self.mode == 'tag' and len(self.gui.tree.get_subitems(parent)) == 1:
            self.gui.show_message('Only one rule allowed when editing tag style')
            return
        # collect all ruletypes, build and display choicedialog
        ruletypes = sorted([(x, y[0]) for x, y in ed.RTYPES.items()], key=lambda x: x[1])
        typename, ok = self.gui.get_input_choice("Choose type for new rule",
                                            [x[1] for x in ruletypes])
        # after selection, create the rule node and the component nodes
        # use ed.init_ruledata(ruletype) for this
        if not ok:
            return
        if self.mode == 'tag' and typename != 'STYLE_RULE':
            self.gui.show_message('Only style rule allowed when editing tag style')
            return
        # ruletype = None
        ruletype = get_ruletype_for_name(typename)
        # for rtype, name in ruletypes:
        #     if name == typename:
        #         ruletype = rtype
        #         break
        if ruletype is None:
            self.gui.show_message('Can you even choose an option that is not in the option list?')
            return
        if after is None:
            # parent = parent
            pos = -1
        else:
            pos = self.gui.tree.getitemparentpos(self.item)[1]
            if after:
                pos += 1
        newitem = self.gui.tree.add_to_parent(typename, parent, pos)
        for name in sorted([x for x in ed.init_ruledata(ruletype)]):
            self.gui.tree.add_to_parent(name, newitem)
        self.mark_dirty(True)
        self.gui.tree.expand_item(newitem)
        self.gui.tree.setcurrent(newitem)

    def edit(self):
        "start edit m.b.v. dialoog"
        if not self.checkselection():
            return
        msg = ''
        modified = False
        data = self.gui.tree.get_itemtext(self.item)
        ruletype = self.gui.tree.get_itemtext(self.gui.tree.getitemparentpos(self.item)[0]).lower()
        title = f"{self.app_title} - edit '{data}' node for {ruletype}"
        if data in ed.RTYPES:
            msg = 'Edit rule via subordinate item'
        elif data in [x for x, y, z in CTYPES if y == ed.text_type]:
            modified = self.edit_text_node(title)
        elif data in [x for x, y, z in CTYPES if y == ed.list_type]:
            modified = self.edit_list_node(title)  # rules, selectors
        elif data in [x for x, y, z in CTYPES if y == ed.table_type]:
            modified = self.edit_grid_node(title)  # styles
        else:
            msg = "You can't edit this type of node"
        if msg:
            self.gui.show_message(msg)
        elif modified:
            self.gui.tree.expand_item(self.item)
            self.mark_dirty(True)

    def edit_text_node(self, title):
        """start editing a simple text type attribute
        """
        textnode = self.gui.tree.get_subitems(self.item)[0]
        self.data = ()
        data = self.gui.tree.get_itemtext(textnode) if textnode else ''
        modified = False
        edt, newdata = self.gui.show_dialog(gui.TextDialog, title, data)
        if edt and newdata != data:
            modified = True
            if not textnode:
                self.gui.tree.add_to_parent(newdata,self.item)
            else:
                self.gui.tree.set_itemtext(textnode, newdata)
        return modified

    def edit_list_node(self, title):
        """start editing a list type attribute
        """
        itemlist = self.gui.tree.get_subitems(self.item)
        maxlen = len(itemlist)
        modified = False
        edt, newitemlist = self.gui.show_dialog(gui.ListDialog, title, itemlist)
        if edt:
            for ix, item in enumerate(newitemlist):
                if ix < maxlen:
                    # volgens mij klopt dit niet. je vergelijkt op de items en dan ga je de tekst
                    #  ervan instellen?
                    # if item != itemlist[ix]:
                    # maar is dit dan wel goed (afgezien van in het testscenario)?
                    if self.gui.tree.get_itemtext(item) != self.gui.tree.get_itemtext(itemlist[ix]):
                        modified = True
                        self.gui.tree.set_itemtext(itemlist[ix], item)
                else:
                    modified = True
                    newnode = self.gui.tree.add_to_parent(item, self.item)
                    if self.item.text(0) == 'rules':
                        ruletype = get_ruletype_for_name(item)
                        for name in sorted([x for x in ed.init_ruledata(ruletype)]):
                            self.gui.tree.add_to_parent(name, newnode)

            test = len(newitemlist)
            if test < maxlen:
                modified = True
                for ix in range(maxlen - 1, test, -1):
                    self.gui.tree.remove_subitem(self.item, ix)
        return modified

    def edit_grid_node(self, title):
        """start editing a table type attribute
        """
        subitems = self.gui.tree.get_subitems(self.item)
        itemlist = [(self.gui.tree.get_itemtext(item),
                     self.gui.tree.get_itemtext(self.gui.tree.get_subitems(item)[0]))
                    for item in subitems]  # self.gui.tree.get_subitems(self.item)]
        maxlen = len(itemlist)
        modified = False
        edt, newitemlist = self.gui.show_dialog(gui.GridDialog, title, itemlist)
        if edt:
            for ix, item in enumerate(newitemlist):
                if ix < maxlen:
                    node = subitems[ix]
                    if item[0] != itemlist[ix][0]:
                        modified = True
                        self.gui.tree.set_itemtext(node, item[0])
                    if item[1] != itemlist[ix][1]:
                        modified = True
                        self.gui.tree.set_itemtext(self.gui.tree.get_subitems(node)[0], item[1])
                else:
                    modified = True
                    newnode = self.gui.tree.add_to_parent(item[0], self.item)
                    self.gui.tree.add_to_parent(item[1], newnode)
            test = len(newitemlist)
            if test < maxlen:
                modified = True
                for ix in range(maxlen - 1, test - 1, -1):
                    self.gui.tree.remove_subitem(self.item, ix)
        return modified

    def delete(self):
        """callback for menu option
        """
        self._copy_rule(cut=True, retain=False)

    def cut(self):
        """callback for menu option
        """
        self._copy_rule(cut=True, retain=True)

    def copy(self):
        """callback for menu option
        """
        self._copy_rule(cut=False, retain=True)

    def _copy_rule(self, cut=True, retain=True):
        """retrieve a rule from the GUI
        """
        if not self.checkselection():
            return
        if not self.is_rule_item(self.item):
            return
        if retain:
            self.cut_item = self.item
            self.cutlevel = self.itemlevel
        if cut:
            # parent = self.item.parent()
            # ix = parent.indexOfChild(self.item)
            parent, ix = self.gui.tree.getitemparentpos(self.item)
            if ix > 0:
                ix -= 1
                ## prev = parent.child(ix)
            ## else:
                ## prev = parent
                ## if prev == self.gui.tree.root:
                    ## prev = parent.child(ix+1)
            # parent.removeChild(self.item)
            self.gui.tree.remove_subitem(parent, ix)
            self.mark_dirty(True)
            ## self.tree.setCurrentItem(prev)

    def paste_under(self):
        """callback for menu option
        """
        self._paste_rule(under=True)

    def paste_after(self):
        """callback for menu option
        """
        self._paste_rule()

    def paste_before(self):
        """callback for menu option
        """
        self._paste_rule(after=False)

    def _paste_rule(self, under=False, after=True):
        """add a rule into the GUI
        """
        if not self.checkselection():
            return
        parent = self.item if under else self.item.parent()
        if not self.is_rule_parent(parent):
            return
        if under:
            self._paste(self.cut_item, parent)
        else:
            # indx = parent.indexOfChild(self.item)
            # _, indx = self.gui.tree.getitemparentpos(self.item)
            indx = self.gui.tree.getitemparentpos(self.item)[1]
            if after:
                indx += 1
                ## text = 'after'
            ## else:
                ## ## indx -= 1
                ## text = 'before'
            self._paste(self.cut_item, parent, indx)
        self.mark_dirty(True)

    def _paste(self, item, parent, indx=0):
        "TODO moet dit een variant van add_rule worden?"
        raise NotImplementedError

    def expand_item(self):
        """callback for menu option
        """
        self._expand()

    def expand_all(self):
        """callback for menu option
        """
        self._expand(recursive=True)

    def _expand(self, recursive=False):
        """expandeer tree vanaf huidige item
        """
        def _expand_all(item):
            "do it recusively"
            # for ix in range(item.childCount()):
            #     sub = item.child(ix)
            for sub in self.gui.tree.get_subitems(item):
                # sub.setExpanded(True)
                self.gui.tree.expand_item(sub)
                _expand_all(sub)
        # item = self.tree.currentItem()
        item = self.gui.tree.getcurrent()
        # self.tree.expandItem(item)
        self.gui.tree.expand_item(item)
        if recursive:
            _expand_all(item)

    def collapse_item(self):
        """callback for menu option
        """
        self._collapse()

    def collapse_all(self):
        """callback for menu option
        """
        self._collapse(recursive=True)

    def _collapse(self, recursive=False):
        """collapse huidige item en daaronder
        """
        def _collapse_all(item):
            "do it recusively"
            # for ix in range(item.childCount()):
            #     sub = item.child(ix)
            for sub in self.gui.tree.get_subitems(item):
                _collapse_all(sub)
                # sub.setExpanded(False)
                self.gui.tree.collapse_item(sub)
        # item = self.tree.currentItem()
        item = self.gui.tree.getcurrent()
        if recursive:
            _collapse_all(item)
        # self.tree.collapseItem(item)
        self.gui.tree.collapse_item(item)

    # temporary methods
    def no_op(self):
        "placeholder for menu option"

    def show_level(self):
        """test method for determine_level"""
        if not self.checkselection():
            return
        level = self.determine_level(self.item)
        self.gui.show_message(f'This element is at level {level}')
        level = self.determine_level_orig(self.item)
        self.gui.show_message(f'Or is this element at level {level}?')

    def add_subitems(self, parent, item):
        """recursively add items to/under a parent
        """
        for child in self.gui.tree.get_subitems(item):
            subitem = self.gui.tree.new_treeitem(self.gui.get_itemtext(child))
            self.gui.tree.add_subitem(parent, subitem)
            self.add_subitems(subitem, child)

    def paste_item(self, item, parent, ix=-1):
        """copy item to/under a new parent
        """
        new = self.gui.tree.new_treeitem(self.gui.tree.get_itemtext(item))
        self.gui.tree.add_subitem(parent, new, ix)
        self.add_subitems(new, item)

    def read_rules(self, data):
        """recursive routine to read rules
        """
        rules = []
        for rltype, rldata in data:
            ruletypeitem = self.gui.tree.new_treeitem(rltype)
            for key in sorted(rldata):
                if key == 'seqnum':
                    continue
                value = rldata[key]
                ruletopitem = self.gui.tree.new_treeitem(key)
                self.gui.tree.add_subitem(ruletypeitem, ruletopitem)
                if key in ('text', 'data', 'name', 'uri', 'selector'):
                    rulekeyitem = self.gui.tree.new_treeitem(value)
                    self.gui.tree.add_subitem(ruletopitem, rulekeyitem)
                    continue
                if key == 'rules':
                    for rulekeyitem in self.read_rules(value):
                        self.gui.tree.add_subitem(ruletopitem, rulekeyitem)
                    continue
                for it in value:  # sorted(value): waarom sorteren?
                    with contextlib.suppress(IndexError):
                        test = it[0]
                    if test in RTYPES:  # kijk of hier een onderliggende rule binnenkomt
                        data = []
                        data.append(it)
                        for rulekeyitem in self.read_rules(data):
                            self.gui.tree.add_subitem(ruletopitem, rulekeyitem)
                        continue
                    try:
                        rulekeyitem = self.gui.tree.new_treeitem(it)
                    except TypeError:  # wrschl geen string maar een tuple
                        rulekeyitem = self.gui.tree.new_treeitem(str(it[0]))
                        rulevalueitem = self.gui.tree.new_treeitem(str(it[1]))
                        self.gui.tree.add_subitem(rulekeyitem, rulevalueitem)
                    else:
                        try:
                        # with contextlib.suppress(TypeError):
                            rulevalueitem = self.gui.tree.new_treeitem(str(value[it]))
                            self.gui.tree.add_subitem(rulekeyitem, rulevalueitem)
                        except TypeError:
                            pass
                    self.gui.tree.add_subitem(ruletopitem, rulekeyitem)
            rules.append(ruletypeitem)
        return rules
