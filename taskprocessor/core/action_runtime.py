import six

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

import taskprocessor.utils.path_utils as path_utils


class ActionRuntime(object):

    def __init__(self, definition, definition_path):
        self.linked_io = {}
        self.action_definition = definition
        self.definition_path = definition_path

        self.exec_code = ""
        self.__init_exec_code()

    # Initializes executable code by substituting variable names (ids of inputs/outputs)
    def __init_exec_code(self):
        # TODO: Replace with a utility functions
        folder = Path(self.definition_path).parent
        exec_file_path = folder / Path(self.action_definition.exec_path)
        self.exec_code = path_utils.read_file(exec_file_path)

        sub_var_names = []
        for i in self.action_definition.inputs:
            sub_var_names.append(i.id)
        for o in self.action_definition.outputs:
            sub_var_names.append(o.id)

        self.exec_code = self.exec_code.format(*sub_var_names)

    # Links the value of an input with its input_id
    def set_input(self, input_index, value):
        input_id = self.action_definition.inputs[input_index].id
        self.linked_io[input_id] = value

    # Links the output_id of the other action to the input_id of this action.
    # This function is used to link output of one node as an input to this node.
    def link_input(self, input_index, action_name, action_output_id):
        input_id = self.action_definition.inputs[input_index].id
        # TODO: Check if the given input exists in the action
        # TODO: Check if the link to be made have same action data type
        self.linked_io[input_id] = action_output_id

    # Remove the input link
    def unlink_input(self, input_index):
        input_id = self.action_definition.inputs[input_index].id
        # TODO: Check if the given input exists in the action
        self.linked_io.pop(input_id)

    # Gets the final executable code with properly substituted variables names and values.
    def get_exec_code(self):
        # print("Code before substitution: \n{}".format(self.exec_code))
        # Replace all inputs in code with linked output variable names

        for input_id in self.linked_io.keys():
            self.exec_code = self.exec_code.replace(input_id, str(self.linked_io[input_id]))

        # print("Code after substitution: \n{}".format(self.exec_code))
        return self.exec_code

    def execute(self):
        # TODO: Remove execute function in ActionRuntime
        print("Executing action: " + self.action_definition.label)
