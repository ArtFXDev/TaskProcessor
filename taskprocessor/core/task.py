import taskprocessor.core as core


class Task(object):

    def __init__(self, entity: core.Entity):
        self.id = ""
        self.name = ""
        self.label = ""
        self.actions = []
        self.entity = entity

    def get_code(self):
        final_code = ""
        for action in self.actions:
            final_code += "\n" + action.get_exec_code()
        return final_code

    def add_action(self, action: core.ActionRuntime):
        print("Adding action: " + action.definition.label)
        self.actions.append(action)

    def add_actions(self, actions: [core.ActionRuntime]):
        for action in actions:
            self.actions.append(action)

    def remove_action(self, action: core.ActionRuntime):
        print("Removing action: " + action.definition.label)
        self.actions.remove(action)

    def start(self):
        # TODO: Implement proper task execution
        print("\n\t<----- EXECUTING ACTIONS ----->\n")
        final_code = self.get_code()
        print("\n\nFinal Code: \n {}".format(final_code))
        print("\n\t\t<----- OUTPUT FROM EXEC CODE ----->")
        exec(final_code)
        print("\n\t\t<----- END OUTPUT FROM EXEC CODE ----->")
        print("\n\t<----- COMPLETED EXECUTING ACTIONS ----->\n")

    def pause(self):
        pass

    def stop(self):
        pass
