from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils
import taskprocessor.utils.json_utils as json_utils


class ActionDefinition(object):

    def __init__(self,
                 label: str = "dummy_action_def",
                 exec_path: str = "dummy/path/action.py",
                 inputs: [core.ActionData] = None,
                 outputs: [core.ActionData] = None,
                 supported_engines: [str] = None):

        self.filepath: str = ""
        self.label: str = label
        self.name: str = path_utils.get_name_from_label(self.label)

        self.exec_path: str = exec_path
        self.inputs: list[core.ActionData] = inputs
        self.outputs: list[core.ActionData] = outputs
        self.supported_engines: list[str] = supported_engines

    # Covert current ActionDefinition object from dict to string
    def __str__(self) -> str:
        def_data = self.__dict__

        # Remove filepath from final json
        if def_data.get('filepath', None) is not None:
            def_data.pop('filepath')
        # For each input, convert it from string to a dictionary
        def_data['inputs'] = [json_utils.json_to_dict(i.to_json()) for i in self.inputs]
        # For each output, convert it from string to a dictionary
        def_data['outputs'] = [json_utils.json_to_dict(o.to_json()) for o in self.outputs]
        # Return the string representation of dict of current object
        return json_utils.dict_to_json(def_data)

    # Get json string from current ActionDefinition object
    def to_json(self) -> str:
        return self.__str__()

    # Get a ActionDefinition object from json string
    @staticmethod
    def from_json(json_data: str) -> ActionDefinition:
        # TODO: Throw exceptions on fail
        json_dict = json_utils.json_to_dict(json_data)

        action_def = ActionDefinition(json_dict['label'],
                                      json_dict['exec_path'])

        # For each input as a dictionary, convert it to a string and then convert it to a ActionData object
        inputs_arr = json_dict['inputs']
        inputs = []
        for i in inputs_arr:
            inputs.append(core.ActionData.from_json(json_utils.dict_to_json(i)))

        # For each output as a dictionary, convert it to a string and then convert it to a ActionData object
        outputs_arr = json_dict['outputs']
        outputs = []
        for o in outputs_arr:
            outputs.append(core.ActionData.from_json(json_utils.dict_to_json(o)))

        action_def.inputs = inputs
        action_def.outputs = outputs

        action_def.supported_engines = json_dict['supported_engines']

        return action_def
