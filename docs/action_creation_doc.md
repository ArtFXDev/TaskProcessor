# Action Creation

All actions are created through a pair of JSON and python source file.

## Example

```json
{
    "label": "Example Action",
    "inputs": [
        {
            "label": "Dummy Boolean Input",
            "type": "Boolean",
            "value": true
        },
        {
            "label": "Dummy Path Input",
            "type": "Path",
            "value": "D:/Personal_Work/Pipeline"
        }
    ],
    "outputs": [
        {
            "label": "Dummy Output",
            "type": "Path",
            "value": "D:/Personal_Work/Pipeline/test.abc"
        }
    ],
    "supported_engines": [
        "maya"
    ],
    "exec_path": "my_example_action.py"
}
```
<p align="center">my_example_action.json</p>

```python
import pymel.core as pm

pm.sphere(r=10)
```
<p align="center">my_example.py</p>

## Guidelines:
<ol>
<li>Each action should have two files:
    <ul>
    <li>A JSON file describing the action and its input.</li>
    <li>A python file containing the code for the action.</li>
    </ul>
</li>
<li>The action python file should have the same name as its corresponding JSON file.</li>
<li>Each action should have a <code>label</code> field with a readable name.</li>
<li>If a action needs any inputs, these are mentioned inside the <code>inputs</code> list.</li>
<li>Each input should have a <code>label</code>.</li>
<li>An input and output <code>type</code> can be any one of:
    <ul>
    <li><code>Empty</code></li>
    <li><code>Boolean</code></li>
    <li><code>String</code></li>
    <li><code>Float</code></li>
    <li><code>Integer</code></li>
    <li><code>Path</code></li>
    </ul>
</li>
<li>Supported engines is optional. If left empty, the action will be valid for all engines. Othewise it can be one of:</li>
    <ul>
    <li><code>maya</code></li>
    <li><code>houdini</code></li>
    <li><code>nuke</code></li>
    </ul>
<li>The relative path of the python file is written in <code>exec_path</code> field.</li>
</ol>
