class Task(object):

    def __init__(self, entity):
        self.id = ""
        self.name = ""
        self.label = ""
        self.actions = []
        self.entity = entity
        pass

    def add_action(self, action):
        print("Adding action: " + action.action_definition.label)
        self.actions.append(action)
        pass

    def add_actions(self, actions):
        for action in actions:
            self.actions.append(action)

    def remove_action(self, action):
        print("Removing action: " + action.action_definition.label)
        self.actions.remove(action)
        pass

    def start(self):
        for action in self.actions:
            print("Starting : " + action.action_definition.label)
            action.execute()
        pass

    def pause(self):
        pass

    def stop(self):
        pass
