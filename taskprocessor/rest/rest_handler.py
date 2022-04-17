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
    if response_str != "":
        return response_str
    else:
        return None


def get_single_action(action_name):
    action_paths = ["../resources/"]
    am = core.ActionManager(action_paths)
    for key, value in am.action_definitions.items():
        new_name = value.name.lower()
        new_name = new_name.replace(" ", "")
        if new_name == action_name:
            return value.to_json()
    return None


def submit_action(action_input):
    print(action_input.name)
    print(action_input.label)
    print(action_input.type)
    print(action_input.path)
    return 'Successful POST'
