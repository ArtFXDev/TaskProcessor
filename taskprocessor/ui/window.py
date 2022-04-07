import sys
import os
import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import NodeGraph, BaseNode

from taskprocessor.ui import UIManager

if __name__ == '__main__':
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])

    graph = NodeGraph()

    ui_manager = UIManager()
    ui_manager.set_engine("maya")
    for n in ui_manager.get_node_classes():
        graph.register_node(n)

    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    graph.auto_layout_nodes()
    graph.fit_to_selection()

    graph.port_connected.connect(ui_manager.connect_nodes)
    graph.port_disconnected.connect(ui_manager.disconnect_nodes)
    graph.node_created.connect(ui_manager.create_node)
    graph.nodes_deleted.connect(ui_manager.delete_nodes)
    graph.property_changed.connect(ui_manager.change_node_input)

    graph_widget.show()

    app.exec_()
