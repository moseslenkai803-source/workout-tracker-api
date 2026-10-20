# Workout Tracker API

A RESTful API built with Flask for managing exercises and workout sessions. The API supports creating, retrieving, and deleting exercises, as well as creating, retrieving, and deleting workout records. It uses SQLAlchemy for database operations and Marshmallow for request validation and serialization.

## Features

- Create, list, retrieve, and delete exercises.
- Create, list, retrieve, and delete workouts.
- Validate incoming request data with Marshmallow.
- Store exercise and workout information in a relational database.
- Manage database schema changes with Flask-Migrate and Alembic.
- Populate the database with sample exercises and a workout.
- Run automated tests with pytest.

## Technology Stack

- Python 3.12
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- SQLAlchemy
- Marshmallow 3.20.1
- SQLite by default
- pytest

## Project Structure

```text
workout-tracker-api/
├── migrations/
│   ├── versions/
│   └── env.py
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── tests/
│   ├── conftest.py
│   ├── test_exercises.py
│   ├── test_schemas.py
│   └── test_workouts.py
├── Pipfile
├── Pipfile.lock
├── pytest.ini
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.12
- pipenv
- Git

Clone the repository and enter the project directory:

```bash
git clone https://github.com/moseslenkai803-source/workout-tracker-api.git
cd workout-tracker-api
```

Install the project dependencies:

```bash
pipenv install --dev
```

Activate the virtual environment if desired:

```bash
pipenv shell
```

The remaining commands can be run inside the activated environment, or prefixed with `pipenv run` when the environment is not activated.

## Database Setup

The application uses SQLite by default. Its database URI is configured as follows:

```python
os.getenv("DATABASE_URL") or "sqlite:///app.db"
```

You can optionally set the `DATABASE_URL` environment variable to use another supported database.

Apply the existing database migrations:

```bash
pipenv run flask --app server/app.py db upgrade
```

This creates or updates the database tables defined by the migration history.

To inspect the migration history, run:

```bash
pipenv run flask --app server/app.py db history
```

## Seed the Database

Populate the database with sample exercises and a sample workout:

```bash
pipenv run python server/seed.py
```

The seed script adds the following exercises if they do not already exist:

- Squat
- Push-up
- Plank

It also creates a sample 45-minute workout and associates it with Squat and Plank. Existing matching records and exercise associations are checked to reduce duplicate seed data.

## Running the Application

Start the Flask development server:

```bash
pipenv run python server/app.py
```

The application runs on port `5555`:

```text
http://127.0.0.1:5555
```

A successful request to the root endpoint returns:

```json
{
  "message": "Workout Tracker API is running"
}
```

The development server uses Flask debug mode. Do not use the debug server as a production deployment server.

## API Reference

All request and response bodies use JSON, except for successful DELETE requests, which return an empty response body.

### Exercises

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| GET | `/exercises` | List all exercises | 200 OK |
| GET | `/exercises/<exercise_id>` | Retrieve one exercise | 200 OK |
| POST | `/exercises` | Create an exercise | 201 Created |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise | 204 No Content |

#### Create an exercise

**POST** `/exercises`

Request body:

```json
{
  "name": "Squat",
  "category": "Strength",
  "equipment_needed": false
}
```

Required fields:

- `name`: a non-blank string of 1–100 characters.
- `category`: a non-blank string of 1–100 characters.
- `equipment_needed`: a boolean.

Example response (`201 Created`):

```json
{
  "id": 1,
  "name": "Squat",
  "category": "Strength",
  "equipment_needed": false
}
```

#### Retrieve an exercise

**GET** `/exercises/1`

Returns the exercise object when found. If the exercise does not exist, the API returns `404 Not Found`.

#### List exercises

**GET** `/exercises`

Returns a JSON array of exercises ordered by ID. An empty database produces an empty array.

#### Delete an exercise

**DELETE** `/exercises/1`

Returns `204 No Content` when the exercise is deleted. Returns `404 Not Found` if the requested exercise does not exist.

### Workouts

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| GET | `/workouts` | List all workouts | 200 OK |
| GET | `/workouts/<workout_id>` | Retrieve one workout | 200 OK |
| POST | `/workouts` | Create a workout | 201 Created |
| DELETE | `/workouts/<workout_id>` | Delete a workout | 204 No Content |

#### Create a workout

**POST** `/workouts`

Request body:

```json
{
  "date": "2026-10-20",
  "duration_minutes": 45,
  "notes": "Full-body workout"
}
```

Required fields:

- `date`: a valid date in `YYYY-MM-DD` format.
- `duration_minutes`: a positive integer.
- `notes`: an optional string or `null`.

Example response (`201 Created`):

```json
{
  "id": 1,
  "date": "2026-10-20",
  "duration_minutes": 45,
  "notes": "Full-body workout"
}
```

#### Retrieve a workout

**GET** `/workouts/1`

Returns the workout object when found. If the workout does not exist, the API returns `404 Not Found`.

#### List workouts

**GET** `/workouts`

Returns a JSON array of workouts ordered by ID. An empty database produces an empty array.

#### Delete a workout

**DELETE** `/workouts/1`

Returns `204 No Content` when the workout is deleted. Returns `404 Not Found` if the requested workout does not exist.

## Data Models

### Exercise

Represents an exercise that can be performed during a workout.

- `id`: integer primary key.
- `name`: exercise name, required.
- `category`: exercise category, required.
- `equipment_needed`: boolean indicating whether equipment is needed.

### Workout

Represents a workout session.

- `id`: integer primary key.
- `date`: workout date.
- `duration_minutes`: positive integer duration.
- `notes`: optional text.

### WorkoutExercise

Represents the association between a workout and an exercise.

- `id`: integer primary key.
- `workout_id`: foreign key referencing a workout.
- `exercise_id`: foreign key referencing an exercise.
- `sets`: positive integer.
- `reps`: positive integer.
- `duration_seconds`: optional positive integer.

The association model supports recording exercise details within a workout. Dedicated HTTP endpoints for managing these associations are not currently implemented.

## Validation and Error Responses

Marshmallow validates exercise and workout request bodies before records are created.

Invalid request data returns `400 Bad Request` with a JSON object containing an `errors` field. Examples include missing required fields, blank exercise names or categories, invalid dates, and non-positive workout durations.

Requests for nonexistent exercises or workouts return `404 Not Found` with an error message.

Successful creation returns `201 Created`. Successful deletion returns `204 No Content` with an empty body.

## Running Tests

Run the automated test suite:

```bash
pipenv run pytest -v
```

For a concise test summary:

```bash
pipenv run pytest -q
```

The test suite covers exercise endpoints, workout endpoints, schema validation, missing records, successful creation and deletion, and invalid input.

## Development Notes

- Run database migrations after changing the database schema.
- Keep request validation in the Marshmallow schemas.
- Add automated tests when introducing new functionality.
- The included Flask server is intended for development and testing.

## License

No license has been specified for this project yet.
