from flask import Flask
from taskprocessor.core import action_manager

app = Flask(__name__)


@app.route('/api/actions', methods=['GET'])
def get_all_actions():
    return action_manager.action_definitions


@app.route('/api/actions/<action_name>', methods=['GET'])
def get_action(action_name):
    return action_manager.get_actions_by_name(action_name)


@app.route('/api/entities', methods=['GET'])
def get_all_entities():
    pass


@app.route('/api/entities/<entity_id>', methods=['GET'])
def get_entity(entity_id):
    pass


if __name__ == '__main__':
    app.run()
