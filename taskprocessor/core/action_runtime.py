class ActionRuntime(object):

    def __init__(self, definition):
        self.action_definition = definition

    def execute(self):
        print("Executing action: " + self.action_definition.label)
        pass
