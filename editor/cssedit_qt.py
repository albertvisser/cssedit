import os
import sys

import PyQt4.QtGui as gui
import PyQt4.QtCore as core

try:
    print('try importing editor from editor.cssedit')
    from editor.cssedit import Editor
except ImportError as e:
    print(e)
    print('try importing editor from cssedit')
    from cssedit import Editor

class TreePanel(gui.QTreeWidget):
    "Tree structure"
    def __init__(self, parent):
        self.parent = parent
        gui.QTreeWidget.__init__(self)
        self.setColumnCount(2)
        self.hideColumn(1)
        self.setItemHidden(self.headerItem(), True)
        ## self.setAcceptDrops(True)
        ## self.setDragEnabled(True)
        self.setSelectionMode(self.SingleSelection)
        ## self.setDragDropMode(self.InternalMove)
        ## self.setDropIndicatorShown(True)
        self.setUniformRowHeights(True)

    def selectionChanged(self, newsel, oldsel):
        """wordt aangeroepen als de selectie gewijzigd is

        de tekst van de oude selectie wordt in de itemdict geactualiseerd
        en die van de nieuwe wordt erin opgezocht en getoond"""
        # helaas zijn newsel en oldsel niet makkelijk om te rekenen naar treeitems
        ## self.parent.check_active()
        ## h = self.currentItem()
        ## self.parent.activate_item(h)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        ## dragitem = self.selectedItems()[0]
        ## dragparent = dragitem.parent()
        ## dropitem = self.itemAt(event.pos())
        ## if not dropitem:
            ## # ## event.ignore()
            ## return
        ## gui.QTreeWidget.dropEvent(self, event)
        ## count = self.topLevelItemCount()
        ## if count > 1:
            ## for ix in range(count):
                ## if self.topLevelItem(ix) == dragitem:
                    ## self.takeTopLevelItem(ix)
                    ## self.oldparent.insertChild(self.oldpos, dragitem)
                    ## self.setCurrentItem(dragitem)
                    ## break
            ## return
        ## self.parent.set_project_dirty(True)
        ## self.setCurrentItem(dragitem)
        ## dropitem.setExpanded(True)

    def mousePressEvent(self, event):
        """remember the current parent in preparation for "canceling" a dragmove
        """
        ## xc, yc = event.x(), event.y()
        ## item = self.itemAt(xc, yc)
        ## if item:
            ## self.oldparent, self.oldpos = self._getitemparentpos(item)
        gui.QTreeWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        "for showing a context menu"
        ## if event.button() == core.Qt.RightButton:
            ## xc, yc = event.x(), event.y()
            ## item = self.itemAt(xc, yc)
            ## if item:
                ## self.create_popupmenu(item)
                ## return
        gui.QTreeWidget.mouseReleaseEvent(self, event)

    def keyReleaseEvent(self, event):
        "also for showing a context menu"
        ## if event.key() == core.Qt.Key_Menu:
            ## item = self.currentItem()
            ## self.create_popupmenu(item)
            ## return
        gui.QTreeWidget.keyReleaseEvent(self, event)

    def create_popupmenu(self, item):
        """create a menu in the right place"""
        ## menu = gui.QMenu()
        ## for action in self.parent.notemenu.actions():
            ## act = menu.addAction(action)
            ## if item == self.parent.root and action.text() in ('&Add', '&Delete',
                    ## '&Forward', '&Back'):
                ## action.setEnabled(False)
        ## menu.addSeparator()
        ## for action in self.parent.treemenu.actions():
            ## menu.addAction(action)
            ## if item == self.parent.root:
                ## action.setEnabled(False)
        ## menu.exec_(self.mapToGlobal(self.visualItemRect(item).center()))
        ## if item == self.parent.root:
            ## for action in self.parent.notemenu.actions():
                ## if item == self.parent.root and action.text() in ('&Add', '&Delete',
                        ## '&Forward', '&Back'):
                    ## action.setEnabled(True)
            ## for action in self.parent.treemenu.actions():
                ## action.setEnabled(True)

    def add_to_parent(self, titel, parent, pos=-1):
        """
        """
        new = gui.QTreeWidgetItem()
        new.setText(0, titel.rstrip())
        new.setToolTip(0, titel.rstrip())
        if pos == -1:
            parent.addChild(new)
        else:
            parent.insertChild(pos, new)
        return new

    def _getitemdata(self, item):
        return item.text(0), str(item.text(1)) # kan integer zijn

    def _getitemtitle(self, item):
        "titel in de visual tree ophalen"
        return item.text(0)

    def _getitemkey(self, item):
        "sleutel voor de itemdict ophalen"
        value = item.text(1)
        try:
            value = int(value)
        except ValueError: # root item heeft tekst in plaats van itemdict key
            pass
        return value

    def _setitemtitle(self, item, title):
        item.setText(0, title)
        item.setToolTip(0, title)

    def _setitemtext(self, item, text):
        """Meant to set the text for the root item (goes in same place as the keys
        for the other items)
        """
        item.setText(1, text)

    def _getitemkids(self, item):
        return [item.child(num) for num in range(item.childCount())]

    def _getitemparentpos(self, item):
        root = item.parent()
        if root:
            pos = root.indexOfChild(item)
        else:
            pos = -1
        return root, pos

    def _getselecteditem(self):
        return self.selectedItems()[0] # gui-dependent

    def _removeitem(self, item, cut_from_itemdict):
        "removes current treeitem and returns the previous one"
        log('in _removeitem {} {}'.format(item, cut_from_itemdict))
        parent = item.parent()               # gui-dependent
        pos = parent.indexOfChild(item)
        oldloc = (parent, pos)
        if pos - 1 >= 0:
            prev = parent.child(pos - 1)
        else:
            prev = parent
            if prev == self.parent.root:
                prev = parent.child(pos + 1)
        self.parent._popitems(item, cut_from_itemdict)
        ## parent.takeChild(pos)
        # bij een undo van een add moeten met " \ " toegevoegde items ook verwijderd worden
        to_remove = [(parent, pos)]
        while True:
            log('{} {} {}'.format(item, item.childCount(), item.child(0)))
            if item.childCount() == 0:
                break
            to_remove.append((item, 0)) # er is er altijd maar één
            item = item.child(0)
        for parent, pos in reversed(to_remove):
            parent.takeChild(pos)
        #
        return oldloc, prev


class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""

    def __init__(self, parent=None):
        gui.QMainWindow.__init__(self)
        ## Mixin.__init__(self)
        offset = 40 if os.name != 'posix' else 10
        self.move(offset, offset)
        ## self.nt_icon = gui.QIcon(os.path.join(HERE, "doctree.xpm"))
        ## self.tray_icon = gui.QSystemTrayIcon(self.nt_icon, self)
        ## self.tray_icon.setToolTip("Click to revive DocTree")
        ## self.connect(self.tray_icon, core.SIGNAL('clicked'),
            ## self.revive) # werkt dit wel?
        ## self.tray_icon.activated.connect(self.revive)
        ## self.tray_icon.hide()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        ## self.opts = init_opts()
        ## self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1]) # 800, 500)
        self.resize(800, 500)
        self.setWindowTitle('CSSEdit')

        self.tree = TreePanel(self)
        self.setCentralWidget(self.tree)

        ## self.actiondict = {}
        ## menubar = self.menuBar()
        ## self.create_menu(menubar, self._get_menu_data())
        ## self.undo_stack = UndoRedoStack(self)
        self.project_dirty = False

    def create_menu(self, menubar, menudata):
        """bouw het menu en de meeste toolbars op"""
        ## for item, data in menudata:
            ## menu = menubar.addMenu(item)
            ## toolbar_added = False
            ## if item == menudata[2][0]: # "&View":
                ## self.viewmenu = menu
            ## elif item == menudata[1][0]:
                ## self.notemenu = menu
            ## elif item == menudata[3][0]:
                ## self.treemenu = menu
            ## for menudef in data:
                ## if not menudef:
                    ## menu.addSeparator()
                    ## continue
                ## label, handler, shortcut, icon, info = menudef
                ## if icon:
                    ## action = gui.QAction(gui.QIcon(os.path.join(HERE, icon)), label,
                        ## self)
                    ## if not toolbar_added:
                        ## toolbar = self.addToolBar(item)
                        ## toolbar.setIconSize(core.QSize(16,16))
                        ## toolbar_added = True
                    ## toolbar.addAction(action)
                ## else:
                    ## action = gui.QAction(label, self)
                ## if item == menudata[3][0]:
                    ## if label == '&Undo':
                        ## self.undo_item = action
                    ## elif label == '&Redo':
                        ## self.redo_item = action
                ## if shortcut:
                    ## action.setShortcuts([x for x in shortcut.split(",")])
                ## if info.startswith("Check"):
                    ## action.setCheckable(True)
                    ## info = info[5:]
                    ## if info in ('B', 'I', 'U'):
                        ## font = gui.QFont()
                        ## if info == 'B':
                            ## font.setBold(True)
                        ## elif info == 'I':
                            ## font.setItalic(True)
                        ## elif info == 'U':
                            ## font.setUnderline(True)
                        ## action.setFont(font)
                        ## info = ''
                ## if info:
                    ## action.setStatusTip(info)
                ## self.connect(action, core.SIGNAL('triggered()'), handler)
                ## # action.triggered.connect(handler) werkt hier niet
                ## if label:
                    ## menu.addAction(action)
                    ## self.actiondict[label] = action

    def show_message(self, text, title):
        gui.QMessageBox.information(self, title, text)

    def show_statusmessage(self, text):
        self.statusbar.showMessage(text)

    def set_title(self, title):
        """standaard titel updaten"""
        self.setWindowTitle("{}{} (view: {}) - DocTree".format(title,
            '*' if self.project_dirty else ''))

    def getfilename(self, title, start, save=False):
        filter = "CSS files (*.css)"
        if save:
            filename = gui.QFileDialog.getSaveFileName(self, title, start, filter)
        else:
            filename = gui.QFileDialog.getOpenFileName(self, title, start, filter)
        ok = True if filename else False
        return ok, filename

    def open(self, **kwargs):
        ## self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, "Root")
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root

        self.css = Editor(**kwargs)
        for key, value in self.css.data.items():

            for item, contents in value.items():
                selectoritem = self.tree.add_to_parent(item, self.root)
                selectoritem.setData(0, core.Qt.UserRole, key)
                for thing, stuff in contents.items():
                    propertyitem = self.tree.add_to_parent(thing, selectoritem)
                    valueitem = self.tree.add_to_parent(stuff, propertyitem)

        item_to_activate = self.root
        ## self.resize(*self.opts["ScreenSize"])
        self.root.setExpanded(True)
        self.tree.setCurrentItem(item_to_activate)
        self.tree.setFocus()

def main(**kwargs):
    app = gui.QApplication(sys.argv)
    main = MainWindow()
    ## app.setWindowIcon(main.nt_icon)
    main.show()
    print(kwargs)
    if kwargs:
        main.open(**kwargs)
    ## if err:
        ## gui.QMessageBox.information(main, "Error", err, gui.QMessageBox.Ok)
    app.exec_()
