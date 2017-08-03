# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from transplant.views import app_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(app_blueprint)

    return app
