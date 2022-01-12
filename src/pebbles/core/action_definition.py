import src.pebbles.core as core
import src.pebbles.utils.path_utils as path_utils
import src.pebbles.utils.json_utils as json_utils


class ActionDefinition(object):

    def __init__(self, label, exec_path, inputs=None, outputs=None, supported_engines=None):
        self.label = label

        self.name = path_utils.get_name_from_label(self.label)
        self.id = self.name + "_" + str(id(self))


        self.exec_path = exec_path
        self.inputs = inputs
        self.outputs = outputs
        self.supported_engines = supported_engines

    # Covert current ActionDefinition object from dict to string
    def __str__(self):
        def_data = self.__dict__
        # For each input, convert it from string to a dictionary
        def_data['inputs'] = [json_utils.json_to_dict(i.to_json()) for i in self.inputs]
        # For each output, convert it from string to a dictionary
        def_data['outputs'] = [json_utils.json_to_dict(o.to_json()) for o in self.outputs]
        # Return the string represtation of dict of current object
        return json_utils.dict_to_json(def_data)

    # Get json string from current ActionDefinition object
    def to_json(self):
        return self.__str__()

    # Get a ActionDefinition object from json string
    @staticmethod
    def from_json(json_data):
        json_dict = json_utils.json_to_dict(json_data)

        action = ActionDefinition(json_dict['label'],
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

        action.inputs = inputs
        action.outputs = outputs

        action.supported_engines = json_dict['supported_engines']

        return action


if __name__ == "__main__":
    data = path_utils.read_file('D:/Personal_Work/Pipeline/TaskProcessor/TaskProcessor/src/pebbles/resources/my_example_task.json')
    action = ActionDefinition.from_json(data)
    print("Action Object: {0}".format(action.__dict__))
    print("Action JSON: {0}".format(action.to_json()))
