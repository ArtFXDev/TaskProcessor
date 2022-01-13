import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionManager(object):
    action_definitions = []
    action_runtimes = []

    def __init__(self, action_paths):
        self.action_paths = action_paths
        self.__init_actions()

    def __init_actions(self):
        json_files = []
        # List all json files from given list of paths
        for p in self.action_paths:
            json_files.extend(path_utils.list_files(p, extensions=["json"]))
        # Convert json files to action definition objects
        self.action_definitions = []
        self.action_runtimes = []
        for j in json_files:
            json_data = path_utils.read_file(j)
            action = core.ActionDefinition.from_json(json_data)
            self.action_definitions.append(action)
            self.action_runtimes.append(core.ActionRuntime(action))

    def get_actions_by_name(self, name):
        return [a for a in self.action_runtimes if name in a.action_definition.name]

    def get_actions_by_engine(self, engine):
        return [a for a in self.action_runtimes if engine in a.action_definition.supported_engines]

    def get_actions_by_entity_extensions(self, extensions):
        # TODO: Filter actions by the entity extensions supported by the engine
        return []
