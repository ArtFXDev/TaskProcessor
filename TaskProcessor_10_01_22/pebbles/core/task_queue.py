class TaskQueue(object):

    def __init__(self, entity):
        self.id = ""
        self.name = ""
        self.label = ""
        self.tasks = []
        self.entity = entity
        pass

    def add_task(self, task):
        print("Adding task: " + task.task_definition.label)
        self.tasks.append(task)
        pass

    def remove_task(self, task):
        print("Removing task: " + task.task_definition.label)
        self.tasks.remove(task)
        pass

    def start(self):
        for task in self.tasks:
            print("Starting : " + task.task_definition.label)
            task.execute()
        pass

    def pause(self):
        pass

    def stop(self):
        pass
