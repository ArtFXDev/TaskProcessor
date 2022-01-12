class ActionRuntime(object):

    def __init__(self, definition):
        self.action_definition = definition
        pass

    def execute(self):
        print("Excecuting action: " + self.action_definition.label)
        pass

    def is_entity_supported(self, entity):
        pass
