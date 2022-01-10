
class Processor(object):

    def __init__(self, queues):
        self.task_queues = queues
        pass

    #Overrides the call operator [ () ] and process the given tasks
    def __call__(self, *args, **kwargs):
        for queue in self.task_queues:
            queue.start()
        pass
