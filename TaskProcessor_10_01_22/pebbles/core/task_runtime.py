class TaskRuntime(object):

    def __init__(self, definition):
        self.task_definition = definition
        pass

    def execute(self):
        print("Excecuting task: " + self.task_definition.label)
        pass

    def is_entity_supported(self, entity):
        pass
