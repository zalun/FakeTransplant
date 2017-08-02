import json
import os
import requests

from flask import Blueprint, jsonify, request
from werkzeug.contrib.cache import SimpleCache

app_blueprint = Blueprint('app', __name__)
cache = SimpleCache()


@app_blueprint.route('/')
def index():
    return 'Pseudo Transplant'


def increment():
    """Increment the index in cache and return its new value."""
    index = cache.get('transplant-index');
    if not index:
        index = 0
    index += 1
    cache.set('transplant-index', index)
    return index


@app_blueprint.route('/autoland', methods=['POST'])
def autoland():
    """Save received data in cache and return an incremented index."""
    index = increment()
    keys = cache.get('transplant-keys')
    if not keys:
        keys = '[]'

    keys = json.loads(keys)
    key = 'transplant-%d' % index
    keys.append(key)
    cache.set('transplant-keys', json.dumps(keys))

    data = {
        'tree': request.form.get('tree'),
        'rev': request.form.get('rev'),
        'destination': request.form.get('destination'),
        'pingback_url': request.form.get('pingback_url'),
        'request_id': index
    }
    cache.set(key, json.dumps(data))

    return jsonify({'request_id': index})


@app_blueprint.route('/send_pingback')
def send_pingback():
    """Retrieve all data from cache, send send pingbacks and then remove."""
    unsent_keys = json.loads(cache.get('transplant-keys'))
    keys = unsent_keys[:]
    for key in unsent_keys:
        land = json.loads(cache.get(key))
        land.update({
            'result': '',
            'trysyntax': '',
            'error_msg': '',
            'landed': True
        })
        requests.request(
            method='POST',
            url=land['pingback_url'],
            data=json.dumps(land),
            headers={'API-Key': os.getenv('TRANSPLANT_API_KEY')}
        )
        cache.set(key, None)
        keys.remove(key)
        cache.set('transplant-keys', json.dumps(keys))

    return '%s pingbacks requested' % len(unsent_keys)
