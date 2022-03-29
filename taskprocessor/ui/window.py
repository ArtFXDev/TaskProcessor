import sys

from Qt import QtWidgets
from NodeGraphQt.NodeGraphQt import NodeGraph, BaseNode, BackdropNode, setup_context_menu
import taskprocessor.ui as ui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # create the node graph controller.
    graph = NodeGraph()

    # set up default menu and commands.
    setup_context_menu(graph)

    # register backdrop node. (included in the NodeGraphQt module)
    # graph.register_node(BackdropNode)

    core_handler = ui.CoreHandler()

    for n in core_handler.nodes:
    # register example node into the node graph.
        graph.register_node(n)

    # create nodes.
    # node_a = graph.create_node('com.chantasticvfx.MyNode', name='Node A')
    # node_b = graph.create_node('com.chantasticvfx.MyNode', name='Node B', color='#5b162f')
    # backdrop = graph.create_node('nodeGraphQt.nodes.Backdrop', name='Backdrop')

    # wrap "backdrop" node around "node_a" and "node_b"
    # backdrop.wrap_nodes([node_a, node_b])

    # connect "node_a" input to "node_b" output.
    # node_a.set_input(0, node_b.output(0))

    # auto layout nodes.
    graph.auto_layout_nodes()

    # disconnect invalid types
    graph.port_connected.connect(lambda ip, op: op.disconnect_from(ip) if(ip.data_type != op.data_type) else None)

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.show()

    app.exec_()
