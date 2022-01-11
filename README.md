# TaskProcessor  

TaskProcessor is a tool to organize and launch CG pipeline tasks.  

It is loosely inspired by Blue Sky Studio's [TaskProcessor](data/taskProcessor.pdf).  


## Features  

The TaskProcessor comprises a UI, a Core, and a series of Tasks.  

### UI  

The UI is used do build TaskQueues from available Tasks, edit Task attributes, link TaskQueues to Entities, and launch the TaskQueues.  
The UI is coded in TypeScript.  

### Core  
  
The Core   
- discovers and list the available Task Definitions (sending these to the UI)  
- launches the TaskQueues as desired, either in a single process, or   pararellised in multiple processes, on a render farm.  
Other means of execution can be added later.  
The Core is coded in Python.  

The Core exposes it's data and features through a python API.  
On top of this python API, a REST API implements dialog with the UI.  

### Tasks  

Tasks are described in a TaskDefinition.
Tasks are implemented in Python, and use a specific DCC API.

You can read more about creating a task [here](docs/task_creation_doc.md).

## Glossary  

### Task: A script executing a pipeline action.  

### TaskQueue: A list of tasks to be executed sequentially.  

### Engine  

### DCC

### Entity

