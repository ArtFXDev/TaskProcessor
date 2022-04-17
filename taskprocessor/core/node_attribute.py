from __future__ import annotations

import taskprocessor.core as core


class NodeAttribute(object):

    def __init__(self, current_node: core.Node, input_id: str, other_node_output_id: str, other_node: core.Node):
        self.current_node: core.Node = current_node
        self.input_id: str = input_id
        self.other_node_output_id: str = other_node_output_id
        self.other_node: core.Node = other_node
