import taskprocessor.core as core


def get_actions():
    action_paths = ["../resources/"]
    am = core.ActionManager(action_paths)
    response = []
    if len(am.action_definitions) == 0:
        return "Action Definitions is Empty"
    for key, value in am.action_definitions.items():
        json_str = value.to_json()
        response.append(json_str)
    response_str = "[" + ','.join(str(x) for x in response) + "]"
    return response_str


def get_single_action(action_name):
    action_paths = ["../resources/"]
    am = core.ActionManager(action_paths)
    for key, value in am.action_definitions.items():
        new_label = value.label.lower()
        new_label = new_label.replace(" ", "")
        if new_label == action_name:
            return value.to_json()
    return "No action corresponding to the action name exists"


def submit_action(action_input):
    print(action_input.name)
    print(action_input.label)
    print(action_input.type)
    print(action_input.path)
    return 'Successful POST'
