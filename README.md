# FakeTransplant

This is a simple app designed to test Mozilla's [lando-api][] service.
It has the same external APIs and behaviour as the autoland transplant
application but does no actual landings.

Install requirements via `pip install -r requirements.txt` (ideally in a
virtualenv).  It can be run locally via `gunicorn transplant.wsgi:app`.
Tests can be run with a simple `py.test`.

[lando-api]: https://github.com/mozilla-conduit/lando-api
