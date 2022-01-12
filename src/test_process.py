import unittest
import pebbles.core.processor as processor
from pebbles.core.task import Task
from pebbles.core.entity import Entity
from pebbles.core.action_runtime import ActionRuntime
from pebbles.core.action_definition import ActionDefinition
from pebbles.core.job import Job
from pebbles.core.processor import Processor


class MyTestCase(unittest.TestCase):
    def test_processor(self):
        # Create an entity with hard coded path.
        entity1 = Entity(
            "C:/Users/User/Desktop/SchoolFiles/Pipeline/MOVIE/ASSETS/CAR/MODELING/PUBLISHED/CAR_MODELING_V001.mb")
        entity2 = Entity(
            "C:/Users/User/Desktop/SchoolFiles/Pipeline/MOVIE/ASSETS/CAR/SURFACING/WIP/CAR_SURFACING_V002.ma")

        task1 = Task(entity1)
        task2 = Task(entity2)

        actionDefinition1 = ActionDefinition()
        actionDefinition1.label = "Test1Label"
        actionDefinition1.name = "Test1Name"
        actionDefinition1.exe_code = "Test1Exe"

        actionRuntime1 = ActionRuntime(actionDefinition1)
        actionRuntime2 = ActionRuntime(actionDefinition1)

        task1.add_actions([actionRuntime1, actionRuntime2])
        task2.add_actions([actionRuntime1, actionRuntime2])

        job = Job([task1, task2])

        processor = Processor(job)

        processor()

        # # Create a task queue with the given entity.
        # task = Task(entity)
        #
        # # Create a hard coded definition for testing.
        # definition1 = ActionDefinition()
        # definition1.label = "Test1Label"
        # definition1.name = "Test1Name"
        # definition1.exe_code = "Test1Exe"
        #
        # # Create a task runtime with the given definition.
        # runtime1 = ActionRuntime(definition1)
        #
        # definition2 = ActionDefinition()
        # definition2.label = "Test2Label"
        # definition2.name = "Test2Name"
        # definition2.exe_code = "Test2Exe"
        #
        # runtime2 = ActionRuntime(definition2)
        #
        # # Add the given runtime tasks to the task queue.
        # task.add_action(runtime1)
        # task.add_action(runtime2)
        #
        # # Start the queue.
        # task.start()
        #
        # # Remove the first task from the queue.
        # task.remove_action(runtime1)


if __name__ == '__main__':
    unittest.main()
