import sys
import os
import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import (NodeGraph,
                         PropertiesBinWidget,
                         Port,
                         setup_context_menu)

from taskprocessor.ui import UIManager


def display_properties_bin(node):
    if not properties_bin.isVisible():
        properties_bin.show()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])

    # create graph controller.
    graph = NodeGraph()

    # set up default menu and commands.
    setup_context_menu(graph)

    ui_manager = UIManager()
    for n in ui_manager.get_node_classes():
        # register example node into the node graph.
        graph.register_node(n)

    # widget used for the node graph.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    # auto layout nodes.
    graph.auto_layout_nodes()
    # fit node selection to the viewer.
    graph.fit_to_selection()

    # create a node properties bin widget.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)

    # wire function to "node_double_clicked" signal.
    # graph.node_double_clicked.connect(display_properties_bin)

    # graph.node_created.connect(lambda node: core_handler.init_node(node))

    # disconnect invalid types
    graph.port_connected.connect(ui_manager.connect_nodes)
    graph.port_disconnected.connect(ui_manager.disconnect_nodes)
    graph.node_created.connect(ui_manager.create_node)
    graph.nodes_deleted.connect(ui_manager.delete_nodes)
    graph.property_changed.connect(ui_manager.change_node_input)

    graph_widget.show()

    app.exec_()
