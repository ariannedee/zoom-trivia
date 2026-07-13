# Zoom Trivia

Play trivia over Zoom!

Built with [Cookiecutter Django](https://cookiecutter-django.readthedocs.io/en/latest/index.html)

## Game Flow

### Before the game

Admins can create games with rounds and questions from the admin view.

### Question details
- Questions can have images or audio
- If multiple choice, put options in the description
- Questions marked "lightening" should be answered verbally in Zoom and are scored by the admin immediately before moving to the next question

Users can create accounts (no email verification needed) and create/join teams.

### During the game

Everyone logs into Zoom. The admin will create breakout rooms based on people's team.

The **admin** can:
- Start the game
- Start a round
- Display a question
- Move to the next question
- Send a 2:00 timer to mark the end of round
- Mark team answers
- Display answers

The **players** can:
- See the game, round and question
- Play audio questions
- Save an answer for each question for their team
- Submit the team answers for a round
- View the answers

## Structure

- Project configuration in `config`
- Settings in `config/settings/`
- Requirements in `requirements/`
- Apps in `zoom_trivia/`

## Run locally

1. Create a virtual environment with Python 3.14 and activate it
1. Install the requirements: `pip install -r requirements/local.txt`
1. Initialize and migrate a new Sqlite db: `python manage.py migrate`
1. Create a new superuser: `python manage.py creatsuperuser`
1. Load some test data (optional): `python loaddata`
1. Run the server: `python manage.py runserver`

View the site at localhost:8000 and the admin view at localhost:8000/admin

## Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```
$ coverage run -m pytest
$ coverage html
$ open htmlcov/index.html
```

## Running tests with pytest
  
`$ pytest zoom_trivia`

## Deployment

### Using PythonAnywhere

1. Go to Web view and launch a console using the virtual env
2. $ git pull
3. $ source venv/bin/postactivate
4. $ pip install -r requirements/production.txt
5. $ ./manage.py migrate
6. $ ./manage.py collectstatic
7. $ ./manage.py compress
8. Reload server
9. $ ./manage.py createsuperuser
