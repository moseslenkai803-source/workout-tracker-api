
from datetime import date

from app import app
from models import db, Workout


def test_get_workouts_returns_json_list(client):
    with app.app_context():
        workout = Workout(
            date=date(2026, 10, 20),
            duration_minutes=30,
            notes="Leg day",
        )
        db.session.add(workout)
        db.session.commit()

    response = client.get("/workouts")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["date"] == "2026-10-20"
    assert data[0]["duration_minutes"] == 30
    assert data[0]["notes"] == "Leg day"
    assert data[0]["id"] is not None

def test_get_workouts_returns_empty_list_when_none_exist(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []

def test_get_workout_by_id_returns_one_workout(client):
    with app.app_context():
        workout = Workout(
            date=date(2026, 10, 20),
            duration_minutes=45,
            notes="Upper body",
        )
        db.session.add(workout)
        db.session.commit()
        workout_id = workout.id

    response = client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data["id"] == workout_id
    assert data["date"] == "2026-10-20"
    assert data["duration_minutes"] == 45
    assert data["notes"] == "Upper body"

def test_get_workout_by_id_returns_404_when_not_found(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json() == {"error": "Workout not found"}


def test_create_workout_returns_created_workout(client):
    payload = {
        "date": "2026-10-20",
        "duration_minutes": 60,
        "notes": "Full body workout",
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 201
    assert response.is_json

    data = response.get_json()
    assert data["id"] is not None
    assert data["date"] == "2026-10-20"
    assert data["duration_minutes"] == 60
    assert data["notes"] == "Full body workout"


def test_create_workout_returns_400_for_missing_fields(client):
    payload = {
        "date": "2026-10-20",
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 400
    assert response.is_json
    assert "errors" in response.get_json()


def test_create_workout_returns_400_for_invalid_date(client):
    payload = {
        "date": "not-a-date",
        "duration_minutes": 30,
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 400
    assert response.is_json
    assert "errors" in response.get_json()


def test_delete_workout_returns_204(client):
    with app.app_context():
        workout = Workout(
            date=date(2026, 10, 20),
            duration_minutes=30,
            notes="Leg day",
        )
        db.session.add(workout)
        db.session.commit()
        workout_id = workout.id

    response = client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 204
    assert response.data == b""

    with app.app_context():
        deleted_workout = db.session.get(Workout, workout_id)
        assert deleted_workout is None


def test_delete_workout_returns_404_when_not_found(client):
    response = client.delete("/workouts/999")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json() == {"error": "Workout not found"}
