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
        return make_response(rest_handler.get_actions(), 200)
    elif request.method == "POST":
        print("In the POST function")
        content = request.json
        action_input = ActionInput(label=content['label'], name=content['name'],
                                   action_type=content['type'], path=content['path'])
        return make_response(rest_handler.submit_action(action_input), 200)
    return None


@app.route('/api/actions/<action_name>', methods=['GET'])
def get_action(action_name):
    return make_response(rest_handler.get_single_action(action_name), 200)


@app.route('/api/entities', methods=['GET'])
def get_all_entities():
    pass


@app.route('/api/entities/<entity_id>', methods=['GET'])
def get_entity(entity_id):
    pass


if __name__ == '__main__':
    app.run()
