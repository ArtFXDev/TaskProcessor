
class Processor(object):

    def __init__(self, job):
        self.job = job
        pass

    # Overrides the call operator [ () ] and process the given tasks
    def __call__(self, *args, **kwargs):
        # TODO: Add job execution.
        self.job.start()
        pass
