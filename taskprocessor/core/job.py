class Job(object):

    def __init__(self, tasks):
        self.tasks = tasks
        print("Initialized job")
        pass

    def start(self):
        print("Started job")
        for task in self.tasks:
            task.start()
        pass
