# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import pytest
import requests_mock
from transplant.app import create_app
from transplant.views import increment, cache


@pytest.fixture
def app():
    """Needed for pytest-flask."""
    app = create_app()
    return app


@pytest.fixture
def clean_cache():
    cache.set('transplant-index', None)
    cache.set('transplant-keys', None)


def test_increment_id(clean_cache):
    assert increment() == 1
    assert increment() == 2
    cache.set('transplant-index', 0)


def test_autoland_response(client, clean_cache):
    data = {
        'tree': 'tree',
        'rev': 'rev',
        'destination': 'destination',
        'pingback_url': 'http://pingback_url'
    }
    response = client.post(
        '/autoland',
        data=json.dumps(data)
    )
    assert response.status_code == 200
    assert response.json == {'request_id': 1}
    assert cache.get('transplant-index') == 1
    assert cache.get('transplant-keys') == ["transplant-1"]


def test_pingback(client, clean_cache):
    cache.set('transplant-keys', ["transplant-1", "transplant-2"])
    data1 = {
        'tree': 'tree1',
        'rev': 'rev1',
        'destination': 'destination1',
        'pingback_url': 'http://landoapi.test/update/1',
        'request_id': 1
    }
    data2 = {
        'tree': 'tree2',
        'rev': 'rev2',
        'destination': 'destination2',
        'pingback_url': 'http://landoapi.test/update/2',
        'request_id': 2
    }
    cache.set('transplant-1', data1)
    cache.set('transplant-2', data2)
    with requests_mock.mock() as mocker:
        mocker.post(
            'http://landoapi.test/update/1',
            json={},
            status_code=202
        )
        mocker.post(
            'http://landoapi.test/update/2',
            json={},
            status_code=202
        )
        response = client.get('/send_pingback')

    assert response.status_code == 200

    # Data provided for pingback is extended with this object
    update_data = {
        'landed': True,
        'result': '',
        'trysyntax': '',
        'error_msg': ''
    }
    data1.update(update_data)
    data2.update(update_data)
    # Is updated data removed from cache?
    assert cache.get('transplant-keys') == []
    assert cache.get('transplant-1') == None
    assert cache.get('transplant-2') == None
    # Is pingback called?
    assert mocker.called
    assert mocker.call_count == 2
    history = mocker.request_history
    h = history[0]
    assert h.url == 'http://landoapi.test/update/1'
    assert h.json() == data1
    assert h.headers.get('API-Key') == os.getenv('TRANSPLANT_API_KEY')
    assert h.headers.get('content-type') == 'application/json'
    h = history[1]
    assert h.url == 'http://landoapi.test/update/2'
    assert h.json() == data2
    assert h.headers.get('API-Key') == os.getenv('TRANSPLANT_API_KEY')
    assert h.headers.get('content-type') == 'application/json'


def test_pingback_no_server(client, clean_cache):
    cache.set('transplant-keys', ["transplant-1"])
    data1 = {
        'tree': 'tree1',
        'rev': 'rev1',
        'destination': 'destination1',
        'pingback_url': 'http://landoapi.nonexisting/update/1',
        'request_id': 1
    }
    cache.set('transplant-1', data1)
    response = client.get('/send_pingback')
    print(response.data)
    compare_string = (
        b'<html>\n'
        b'  <body>\n'
        b'    <p>Pingbacks requested: 1</p>\n'
        b'    <dl>\n    \n'
        b'      <dt>http://landoapi.nonexisting/update/1</dt>\n'
        b'      <dd>failed</dd>\n    \n'
        b'    </dl>\n'
        b'  </body>\n'
        b'</html>'
    )
    assert response.data[:len(compare_string)] == compare_string
    assert response.status_code == 200
