from flask import Flask, make_response, request
import taskprocessor.rest.rest_handler as rest_handler

app = Flask(__name__)


class ActionInput:
    def __init__(self, label, name, action_type, path):
        self.label = label
        self.name = name
        self.type = action_type
        self.path = path


@app.route('/api/actions', methods=['GET', 'POST'])
def api_actions():
    if request.method == "GET":
        result = rest_handler.get_actions()
        if result is None:
            return make_response("No actions were found", 404)
        else:
            return make_response(result, 200)
    elif request.method == "POST":
        content = request.json
        action_input = ActionInput(label=content['label'], name=content['name'],
                                   action_type=content['type'], path=content['path'])
        result = rest_handler.submit_action(action_input)
        return make_response(result, 200)
    return None


@app.route('/api/actions/<action_name>', methods=['GET'])
def get_action(action_name):
    result = rest_handler.get_single_action(action_name)
    if result is None:
        return make_response("No corresponding action to the name entered was found", 404)
    else:
        return make_response(result, 200)


@app.route('/api/entities', methods=['GET'])
def get_all_entities():
    pass


@app.route('/api/entities/<entity_id>', methods=['GET'])
def get_entity(entity_id):
    pass


if __name__ == '__main__':
    app.run()
