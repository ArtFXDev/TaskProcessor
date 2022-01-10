import unittest
import pebbles.core.processor as processor
from pebbles.core.task_queue import TaskQueue
from pebbles.core.entity import Entity
from pebbles.core.task_runtime import TaskRuntime
from pebbles.core.task_definition import TaskDefinition


class MyTestCase(unittest.TestCase):
    def test_processor(self):
        # Create an entity with hard coded path.
        entity = Entity(
            "C:/Users/User/Desktop/SchoolFiles/Pipeline/MOVIE/ASSETS/CAR/MODELING/PUBLISHED/CAR_MODELING_V001.mb")

        # Create a task queue with the given entity.
        queue = TaskQueue(entity)

        # Create a hard coded definition for testing.
        definition1 = TaskDefinition()
        definition1.label = "Test1Label"
        definition1.name = "Test1Name"
        definition1.exe_code = "Test1Exe"

        # Create a task runtime with the given definition.
        runtime1 = TaskRuntime(definition1)

        definition2 = TaskDefinition()
        definition2.label = "Test2Label"
        definition2.name = "Test2Name"
        definition2.exe_code = "Test2Exe"

        runtime2 = TaskRuntime(definition2)

        # Add the given runtime tasks to the task queue.
        queue.add_task(runtime1)
        queue.add_task(runtime2)

        # Start the queue.
        queue.start()

        # Remove the first task from the queue.
        queue.remove_task(runtime1)


if __name__ == '__main__':
    unittest.main()
