# Back-End-Development-Pictures

Flask REST service completed from the IBM Skills Network template.

## Environment Setup
- Repository prepared from the provided template.
- Course Linux setup script: `bash bin/setup.sh`.
- Verified locally with Python 3.9.25; Cloud IDE provides Python 3.10.12.
- Create a virtual environment and install `requirements.txt`.

Run `python -m pytest -v tests/test_api.py` for all eleven course tests.
Run `FLASK_APP=app flask run --host=0.0.0.0 --port=3000` to start the service.
GET: /health, /count, /picture, /picture/<id>.
POST /picture; PUT and DELETE /picture/<id>.
Course sample data is stored in memory and resets on service restart.

