
"""
Data Tree for the ArrayViewer
"""
# Author: Alex Schwarz <alex.schwarz@informatik.tu-chemnitz.de>
from natsort import realsorted, ns
from dash import html
from dash_treeview_antd import TreeView


def _lowercase(key):
    """ Convenience Function. Return lowercase of string. """
    return key.lower()

html.Summary([
    html.Summary([
        html.Tr("A"),
        html.Tr("B"),
        html.Tr("C"),
    ]),
    html.Summary("A")])

class TV(html.Div):
    class TV_item(html.Summary):
        def __init__(self, children):
            self.children = children
            super().__init__(children=children)

    def __init__(self, id, children):
        super().__init__(id=id)
        self.currItem = None
        self.head = html.Div("Content")
        self.tli = generate_tree({'title': 'Parent', 'key': '0', 'children': [{
            'title': 'Child', 'key': '0-0', 'children': [
                {'title': 'Subchild1', 'key': '0-0-1'},
                {'title': 'Subchild2', 'key': '0-0-2'},
                {'title': 'Subchild3', 'key': '0-0-3'},
            ]}]})

    def generate_tree(self, children):
        if children is not None:
            return self.TV_item([self.generate_tree(ch) for ch in children])

    def currentItem(self):
        """ Return the current Item """
        return self.currItem

    def topLevelItem(self, key):
        """ Return Item that is one level above the current item. """
        if key == 0:
            return self.head
        return self.head  # TODO

    def topLevelItemCount(self):
        return len(self.tli)

    def indexFromItem(self, key, value):

class DataTree():
    """ Class Definition for the Data Tree. """
    def __init__(self, viewer, parent=None):
        """ Initialize the Datatree """
        super().__init__(parent)
        self.old_trace = []
        self.similar_items = []
        self.checkableItems = []
        self.changing_item = None
        self.viewer = viewer
        self.keys = viewer.keys
        self.noPrintTypes = viewer.noPrintTypes
        self._current_item = None
        self._current_tree = None

        # Add the Tree Widgets
        self.Tree = TreeView("fileTree")

        # Add an alternative Tree Widget
        self.secTree = TreeView("dataTree")
        # self.secTree.currentItemChanged.connect(self.viewer._change_tree)

        # Connect Signal at the end to avoid errors
        # self.currentChanged.connect(self._update_treetab)
        # self.setAcceptDrops(True)

    def clear_tree(self):
        """ Clear the Tree. """
        self.checkableItems = []
        self.update_tree()

    def current_item(self):
        """ Return the currently selected Item. """
        return self._current_item

    def is_files_tree(self):
        """ Return True if the currently open Tree is the "Files"-Tree. """
        return self._current_tree == self.Tree

    def _finish_renaming(self):
        """ Finish the renaming of a data-key. """
        if not self.old_trace:
            return
        new_trace = self.viewer._get_obj_trace(self.changing_item)
        if new_trace == self.old_trace:
            return
        # self.Tree.itemChanged.disconnect(self._finish_renaming)
        # Check if the name exists in siblings
        itemIndex = self.Tree.indexFromItem(self.changing_item, 1)
        siblingTxt = []
        if self.changing_item.parent():
            for n in range(self.changing_item.parent().childCount()):
                if itemIndex.sibling(n, 1) != itemIndex:
                    siblingTxt.append(itemIndex.sibling(n, 1).data(0))
        else:
            for n in range(self.Tree.topLevelItemCount()):
                if self.Tree.topLevelItem(n) != self.changing_item:
                    siblingTxt.append(itemIndex.sibling(n, 1).data(0))
        if new_trace[-1] in siblingTxt:
            self.changing_item.setData(0, 1, self.old_trace[-1])
            self.old_trace = []
            return
        # Replace the key
        self.viewer.set_data(new_trace, self.viewer.pop(self.old_trace))
        # If element is top-level-item
        if not self.changing_item.parent() and self.old_trace[0] in self.keys:
            self.keys[self.keys.index(self.old_trace[0])] = new_trace[0]
        self.old_trace = []
        # Make Item non-editable
        # self.changing_item.setFlags(Qt.ItemFlag(61))

    def remove_from_checkables(self, item_list):
        """ Remove items from the checkableItems list. As it causes errors. """
        for item in item_list:
            if item in self.checkableItems:
                self.checkableItems.remove(item)
            if item.childCount() > 0:
                self.remove_from_checkables(item.takeChildren())

    def rename_key(self):
        """ Start the renaming of a data-key. """
        self.changing_item = self.Tree.currentItem()
        self.old_trace = self.viewer._get_obj_trace(self.changing_item)
        # Make Item editable
        # self.changing_item.setFlags(Qt.ItemFlag(63))
        # self.Tree.editItem(self.changing_item, 1)
        # self.Tree.itemChanged.connect(self._finish_renaming)

    def _update_subtree(self, item, data):
        """ Add a new subtree to the current QTreeWidgetItem. """
        return
        for n, k in enumerate(realsorted(data.keys(), alg=ns.IC|ns.NA)):
            item.addChild([None, k])
            child = item.child(n)
            if isinstance(data[k], dict):
                self._update_subtree(child, data[k])
            elif not isinstance(data[k], self.noPrintTypes):
                child.setCheckState(0, Qt.Unchecked)
                self.checkableItems.append(child)

    def _update_subtree_sec(self, item, data):
        """ Add a new subtree to the current QTreeWidgetItem. """
        return
        if not isinstance(data, dict):
            for s in self.similar_items:
                sitem = QTreeWidgetItem([None, s])
                sitem.setToolTip(1, s)
                item.addChild(sitem)
            if not isinstance(data, self.noPrintTypes):
                for c in range(item.childCount()):
                    item.child(c).setCheckState(0, Qt.Unchecked)
                    self.checkableItems.append(item.child(c))
        else:
            for n, k in enumerate(realsorted(data.keys(), alg=ns.IC|ns.NA)):
                item.addChild(QTreeWidgetItem([None, k]))
                child = item.child(n)
                if isinstance(data[k], dict):
                    self._update_subtree(child, data[k])
                else:
                    for s in self.similar_items:
                        sitem = QTreeWidgetItem([None, s])
                        sitem.setToolTip(0, s)
                        child.addChild(sitem)
                    if not isinstance(data[k], self.noPrintTypes):
                        for c in range(child.childCount()):
                            child.child(c).setCheckState(0, Qt.Unchecked)
                            self.checkableItems.append(child.child(c))

    def update_tree(self):
        """ Add new data to TreeWidget. """
        itemList = []
        self.checkableItems = []
        for i in self.keys:
            item = {"title": i, key: i}
            self._update_subtree(item, self.viewer._data[i])
            itemList.append(item)
        self.Tree.clear()
        self.Tree.addTopLevelItems(itemList)
        if self.currentWidget() == self.secTree:
            self._update_treetab(1)

    def _update_treetab(self, index):
        """ Update the currently selected treetab, on switching. """
        if self.viewer.diffBtn.isVisible():
            self.viewer._start_diff()
        if index == 1:
            self._update_tree_sec()
        else:
            self.update_tree()

    def _update_tree_sec(self):
        """ Generate the data tree. """
        self.checkableItems = []
        # get TopLevelItem of the current item as a reference
        ref = self.Tree.currentItem()
        self.secTree.clear()
        if ref is None:
            ref = self.Tree.topLevelItem(0)
            if ref is None:
                return
        while ref.parent() is not None:
            ref = ref.parent()
        flipped_var = self.viewer._data[ref.text(1)].keys()
        # Find all with a similar structure
        self.similar_items = []
        for i in range(self.Tree.topLevelItemCount()):
            top_level_key = self.Tree.topLevelItem(i).text(1)
            if self.viewer._data[top_level_key].keys() == flipped_var:
                self.similar_items.append(top_level_key)
        # Build the tree
        itemList = []
        for k in flipped_var:
            item = QTreeWidgetItem([None, k])
            self._update_subtree_sec(item, self.viewer._data[ref.text(1)][k])
            itemList.append(item)
        for k in self.keys:
            if k[:4] == "Diff":
                item = QTreeWidgetItem([None, k])
                self._update_subtree(item, self.viewer._data[k])
                itemList.append(item)
        self.secTree.addTopLevelItems(itemList)
