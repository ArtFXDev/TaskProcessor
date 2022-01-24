# TaskProcessor  

TaskProcessor is a tool to organize and launch CG pipeline tasks.  

It is loosely inspired by Blue Sky Studio's [TaskProcessor](data/taskProcessor.pdf).  


## Features  

The TaskProcessor comprises a UI, a Core, and a series of Tasks.  

### UI  

The UI is used to build `Tasks` from available `Actions`, edit Action attributes, link `Tasks` to `Entities`.
The list of `Tasks` is known as a `Job`, which is sent to the `Processor` for launching.
The UI is coded in TypeScript.  

### Core  
  
The Core   
- list the available Actions (as defined in ActionDefinitions) and sends these to the UI
- launches the Jobs as desired, either in a single process, or pararellised in multiple processes, on a render farm.  
Other means of execution can be added later.  
The Core is coded in Python.  

The Core exposes it's data and features through a python API.  
On top of this python API, a REST API implements dialog with the UI.  

### Actions  

An Action is described in an `ActionDefinition`.
Actions are implemented in Python, and use a specific DCC API.

You can read more about creating an action [here](docs/action_creation_doc.md).

## Glossary  

### Action
A script executing an atomic pipeline action. 
Examples: scene open, quality check, publish, export, save as.

An Action can have attributes (input and output attributes).
An Action is implemented and described in an ActionDefinition.
Actions are chained together to form a Task. Action Attributes can be linked together.

### Task
A list of Actions to be executed sequentially.  
A Task is linked to an Entity, which the Task acts on.

### Job
A list of Tasks.
The Processor launches the Job in one or more separate processes.
The Processor can launch the Job on a Farm, split into one Taks per render blade (this will be implemented in a secodn iteration)

### DCC
Digital Content Creation Tool.

Examples: Maya, Houdnin, Nuke

### Engine  
The unified API representation of a DCC.

### Entity
A unit of pipeline data, typically a scene file (Shot scene file or Asset scene file), or on a more abstract level a Shot, an Asset, a Sequence, a Step (pipeline Task).



