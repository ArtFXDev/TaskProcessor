from PySide2 import QtWidgets, QtGui, QtCore
from Qt import QtCompat

import NodeGraph

from pathlib import Path

ui_path = Path(__file__).parent / 'qt' / 'window.ui'

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

from taskprocessor.ui import ui_manager



class PebblesWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PebblesWindow, self).__init__()
        QtCompat.loadUi(str(ui_path), self)
        print("open semesmeema")

        self.graph = NodeGraph()
        self.populate_tab_menu()
        self.display_graph()
        self.create_tree()

        self.graph.port_connected.connect(ui_manager.connect_nodes)
        self.graph.port_disconnected.connect(ui_manager.disconnect_nodes)
        self.graph.node_created.connect(ui_manager.create_node)
        self.graph.nodes_deleted.connect(ui_manager.delete_nodes)
        self.graph.property_changed.connect(ui_manager.change_node_input)

        ui_manager.set_on_process_listeners(progress_callback=self.update_progress)

        self.searchButton.clicked.connect(self.set_path)
        self.entitiesButton.clicked.connect(self.select_entities)

    def select_entities(self):
        indices = self.fileViewer.selectedIndexes()

        print(len(indices))

        files = [i.model().filePath(i) for i in indices]
        print(len(files))
        [print(i) for i in files]

        # files = indices.model().filePath()
        # print(files)
        # ui_manager.add_entity(files)

    def update_progress(self, task, action, total, action_progress, status):
        self.progressBar.setValue(total*100)
        pass

    def populate_tab_menu(self):
        ui_manager.get_node_classes()
        for n in ui_manager.get_node_classes():
            self.graph.register_node(n)

    def create_tree(self):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.fileViewer.setModel(self.model)

    def set_path(self):
        self.box = QtWidgets.QFileDialog
        self.select = self.box.getExistingDirectory()
        text = self.searchEdit
        text.setText(self.select)
        self.fileViewer.setRootIndex(self.model.index(self.select))

    def display_window(self):
        pw = PebblesWindow()
        pw.show()

    def display_graph(self):
        graph_widget = self.graph.widget
        self.graphHolder.addWidget(graph_widget)
        graph_widget.show()
        print(graph_widget)


# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     cs = PebblesWindow()
#     cs.show()
#     app.exec_()
