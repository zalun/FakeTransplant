from flask import Blueprint, jsonify

app_blueprint = Blueprint('app', __name__)

@app_blueprint.route('/')
def index():
    return 'Pseudo Transplant'


@app_blueprint.route('/autoland', methods=['POST'])
def autoland():
    return jsonify({'request_id': 1})
