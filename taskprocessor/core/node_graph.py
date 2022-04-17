from __future__ import annotations

import taskprocessor.core as core


class NodeGraph(object):

    def __init__(self, actions: list[core.ActionRuntime]):
        self.nodes: list[core.Node] = []

        # Initialize nodes
        for a in actions:
            node = core.Node(a)
            self.nodes.append(node)

        # Link nodes
        for n in self.nodes:
            for (input_id, input_value) in n.action.input_params.items():
                if type(input_value) == tuple:
                    other_node = next((n for n in self.nodes if n.action == input_value[1]))
                    node_attrib = core.NodeAttribute(n, input_id, input_value[0], other_node)
                    n.add_adjacent_node(node_attrib)

        # Sort nodes in proper execution order
        self.__sort()

    def print_graph(self):
        for n in self.nodes:
            print("\n")
            print("{} <-----".format(n.action.definition.name), end=" ")
            for na in n.adjacent_nodes:
                print("{}".format(na.other_node.action.definition.name), end=", ")
        print("\n")

    def __sort_helper(self, node: core.Node, visited: dict[core.Node, bool], stack: list[core.Node]):
        visited[node] = True
        for nd in node.adjacent_nodes:
            if visited[nd.other_node] is False:
                self.__sort_helper(nd.other_node, visited, stack)
        stack.append(node)

    def __sort(self):
        visited: dict[core.Node, bool] = {}
        node_stack: list[core.Node] = []
        for n in self.nodes:
            visited[n] = False

        for n in self.nodes:
            if visited[n] is False:
                self.__sort_helper(n, visited, node_stack)

        self.nodes = node_stack

    def get_actions(self) -> list[core.ActionRuntime]:
        actions: list[core.ActionRuntime] = []
        for n in self.nodes:
            actions.append(n.action)
        return actions




