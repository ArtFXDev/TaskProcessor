from taskprocessor.ui import ActionDataType

NODE_IO_TYPE_COLORS = {
    ActionDataType.Empty: (33, 33, 33),
    ActionDataType.Path: (213, 0, 0),
    ActionDataType.String: (197, 17, 98),
    ActionDataType.Float: (170, 0, 255),
    ActionDataType.Integer: (48, 79, 254),
    ActionDataType.Boolean: (0, 200, 83),
    ActionDataType.Object: (255, 171, 0),
    ActionDataType.Vector2: (0, 121, 107),
    ActionDataType.Vector3: (0, 105, 92),
    ActionDataType.Vector4: (0, 77, 64),
}

NODE_COLORS = {
    "maya": (2, 104, 105),
    "python": (36, 83, 121),
    "houdini": (177, 49, 2)
}

from .base_node_tp import BaseNodeTP
