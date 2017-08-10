# FakeTransplant

This is a simple app designed to test Mozilla's [lando-api][] service.
It has the same external APIs and behaviour as the autoland transplant
application but does no actual landings.


## Usage

Set Lando API to work with https://fake-transplant.herokuapp.com with the
API Key (ask in IRC `mozilla#conduit` for the right one).

Create a Landing using Lando API (via Swagger UI or Lando UI).

Navigate to [send pingback][] endpoint. Page will provide the report.


## Development

Install requirements via `pip install -r requirements.txt` (ideally in a
virtualenv).  It can be run locally via `gunicorn transplant.wsgi:app`.

Tests can be run with a simple `py.test`.

It is required to provide the API-Key via environment variable
`TRANSPLANT_API_KEY`.


[lando-api]: https://github.com/mozilla-conduit/lando-api
[send pingback]: https://fake-transplant.herokuapp.com/send_pingback

