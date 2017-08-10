# FakeTransplant

This is a simple app designed to test Mozilla's [lando-api][] service.
It has the same external APIs and behaviour as the autoland transplant
application but does no actual landings.

Install requirements via `pip install -r requirements.txt` (ideally in a
virtualenv).  It can be run locally via `gunicorn transplant.wsgi:app`.
Tests can be run with a simple `py.test`.


## Run dev environment

It is required to provide the API-Key via environment variable.

```bash
$ TRANSPLANT_API_KEY={your local API-Key} FLASK_APP=run.py flask run
```


## Usage

1. Set Lando API to work with https://fake-transplant.herokuapp.com with the 
   right API Key.
2. Create a Landing.
3. Load [send pingback][]. Page will provide the report.


[lando-api]: https://github.com/mozilla-conduit/lando-api
[send pingback]: https://fake-transplant.herokuapp.com/send_pingback

