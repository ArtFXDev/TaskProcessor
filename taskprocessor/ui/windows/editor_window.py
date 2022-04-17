from PySide2 import QtWidgets, QtGui, QtCore
from Qt import QtCompat

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

from taskprocessor.ui.windows import EDITOR_WINDOW_UI_PATH
from taskprocessor.ui import ui_manager


class EditorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(EditorWindow, self).__init__()
        QtCompat.loadUi(EDITOR_WINDOW_UI_PATH, self)
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

        ui_manager.set_on_process_listeners(start_callback=self.on_process_started,
                                            progress_callback=self.on_process_progressed,
                                            error_callback=self.on_process_error,
                                            completed_callback=self.on_process_completed)

        self.runButton.clicked.connect(ui_manager.run)
        self.searchButton.clicked.connect(self.set_path)
        self.entitiesButton.clicked.connect(self.update_entities)

    def __del__(self):
        ui_manager.remove_on_process_listeners(start_callback=self.on_process_started,
                                               progress_callback=self.on_process_progressed,
                                               error_callback=self.on_process_error,
                                               completed_callback=self.on_process_completed)

    def update_entities(self):
        indices = self.fileViewer.selectedIndexes()
        files = [i.model().filePath(i) for i in indices]
        ui_manager.set_entities(files)

    def on_process_started(self, status):
        print(f"Execution Started: {status}")

    def on_process_progressed(self, task, action, total, action_progress, status):
        print(f"Execution Progress: {task} | {action} | {total} | {action_progress}")
        self.progressBar.setValue(int(total * 100.0))

    def on_process_error(self, error):
        # print(f"Execution Error: {error}")
        pass

    def on_process_completed(self, is_success, status):
        print(f"Execution Completed: {is_success} | {status}")
        self.progressBar.setValue(0)

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

    def display_graph(self):
        graph_widget = self.graph.widget
        self.graphHolder.addWidget(graph_widget)
        graph_widget.show()

    @staticmethod
    def display():
        pw = EditorWindow()
        pw.show()
