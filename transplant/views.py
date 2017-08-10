# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import requests

from requests.exceptions import ConnectionError
from flask import Blueprint, jsonify, render_template, request
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
        keys = []

    key = 'transplant-%d' % index
    keys.append(key)
    cache.set('transplant-keys', keys)

    data = {
        'tree': request.form.get('tree'),
        'rev': request.form.get('rev'),
        'destination': request.form.get('destination'),
        'pingback_url': request.form.get('pingback_url'),
        'request_id': index
    }
    cache.set(key, data)

    return jsonify({'request_id': index})


@app_blueprint.route('/send_pingback')
def send_pingback():
    """Retrieve all data from cache, send send pingbacks and then remove."""
    unsent_keys = cache.get('transplant-keys')
    if not unsent_keys:
        return 'No pingbacks to send'

    keys = unsent_keys[:]
    responses = {}
    for key in unsent_keys:
        land = cache.get(key)
        land.update({
            'result': '',
            'trysyntax': '',
            'error_msg': '',
            'landed': True,
        })
        try:
            response = requests.request(
                method='POST',
                url=land['pingback_url'],
                data=json.dumps(land),
                headers={
                    'API-Key': os.getenv('TRANSPLANT_API_KEY'),
                    'content-type': 'application/json'
                },
            )
            responses[land['pingback_url']] = response.status_code
        except ConnectionError:
            responses[land['pingback_url']] = 'failed'

        cache.set(key, None)
        keys.remove(key)
        cache.set('transplant-keys', keys)

    return render_template('send_pingbacks.html',
                           requests_number=len(unsent_keys),
                           responses=responses)
