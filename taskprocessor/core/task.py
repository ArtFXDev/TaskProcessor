from __future__ import annotations

import taskprocessor.core as core


class Task(object):

    def __init__(self, entity: core.Entity):
        self.id: str = ""
        self.name: str = ""
        self.label: str = ""
        self.actions: list[core.ActionRuntime] = []
        self.nodes: list[core.Node] = []
        self.entity: core.Entity = entity

    def get_code(self):
        final_code = ""
        for action in self.actions:
            final_code += "\n" + action.get_exec_code()
        return final_code

    def add_action(self, action: core.ActionRuntime):
        self.actions.append(action)
        node = core.Node(action)
        self.nodes.append(node)

    def add_actions(self, actions: [core.ActionRuntime]):
        for action in actions:
            self.actions.append(action)
            node = core.Node(action)
            self.nodes.append(node)

    def link_action(self, input_action_id, index, output_action_id, output_index) -> bool:
        input_node = next((n for n in self.nodes if input_action_id == n.action.id), None)
        output_node = next((n for n in self.nodes if output_action_id == n.action.id), None)
        if input_node is None or output_node is None:
            return False
        return input_node.link_output(index, output_node, output_index)

    def unlink_action(self, input_action_id, index, output_action_id, output_index) -> bool:
        input_node = next((n for n in self.nodes if input_action_id == n.action.id), None)
        output_node = next((n for n in self.nodes if output_action_id == n.action.id), None)
        if input_node is None or output_node is None:
            return False
        return input_node.unlink_output(index, output_node, output_index)


    def remove_action(self, action: core.ActionRuntime):
        print("Removing action: " + action.definition.label)
        self.actions.remove(action)

    def start(self):
        # TODO: Implement proper task execution
        print("\n\t<----- EXECUTING ACTIONS ----->\n")
        final_code = self.get_code()
        print("\n\nFinal Code: \n {}".format(final_code))
        print("\n\t\t<----- OUTPUT FROM EXEC CODE ----->")
        exec(final_code)
        print("\n\t\t<----- END OUTPUT FROM EXEC CODE ----->")
        print("\n\t<----- COMPLETED EXECUTING ACTIONS ----->\n")

    def pause(self):
        pass

    def stop(self):
        pass
