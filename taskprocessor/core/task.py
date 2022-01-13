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

    def add_actions(self, actions):
        for action in actions:
            self.actions.append(action)

    def remove_action(self, action):
        print("Removing action: " + action.action_definition.label)
        self.actions.remove(action)


    def start(self):
        # TODO: Implement proper task execution
        print("\n\t<----- EXECUTING ACTIONS ----->\n")
        final_code = ""
        for action in self.actions:
            final_code += "\n" + action.get_exec_code()

        print("\n\nFinal Code: \n {}".format(final_code))
        print("\n\t\t<----- OUTPUT FROM EXEC CODE ----->")
        exec(final_code)
        print("\n\t\t<----- END OUTPUT FROM EXEC CODE ----->")
        print("\n\t<----- COMPLETED EXECUTING ACTIONS ----->\n")

    def pause(self):
        pass

    def stop(self):
        pass
