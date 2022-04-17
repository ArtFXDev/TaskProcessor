from __future__ import annotations

import taskprocessor.core as core


class Node(object):

    def __init__(self, data: core.ActionRuntime):
        self.action: core.ActionRuntime = data
        # A list of nodes which gives its output to this node
        self.adjacent_nodes: list[core.NodeAttribute] = []

    def add_adjacent_node(self, node_attribute: core.NodeAttribute):
        self.adjacent_nodes.append(node_attribute)
