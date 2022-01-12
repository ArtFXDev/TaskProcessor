from enum import Enum
import src.pebbles.utils.path_utils as path_utils
import src.pebbles.utils.json_utils as json_utils


class ActionDataType(Enum):
    Empty = 0,
    Boolean = 1,
    String = 2,
    Integer = 3,
    Float = 4,
    Path = 5


class ActionData(object):

    def __init__(self,
                 label,
                 data_type=ActionDataType.Empty,
                 value=None):
        self.label = label
        self.name = path_utils.get_name_from_label(self.label)
        self.id = self.name + "_" + str(id(self))
        self.type = data_type
        self.value = value

    # Covert current ActionData object from dict to string
    def __str__(self):
        data = self.__dict__
        # Convert ActionDataType enum to string
        data['type'] = self.type.name
        return json_utils.dict_to_json(data)

    # Get json string from current ActionData object
    def to_json(self):
        return self.__str__()

    # Get a ActionData object from json string
    @staticmethod
    def from_json(json_data):
        json_dict = json_utils.json_to_dict(json_data)
        action_data = ActionData(json_dict['label'],
                                 ActionDataType[json_dict['type']],
                                 json_dict['value'])

        return action_data
