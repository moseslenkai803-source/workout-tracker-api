from app import app
from models import db, Exercise


def test_get_exercises_returns_json_list(client):
    with app.app_context():
        db.session.add(
            Exercise(
                name="Squat",
                category="Strength",
                equipment_needed=False,
            )
        )
        db.session.commit()

    response = client.get("/exercises")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Squat"
    assert data[0]["category"] == "Strength"
    assert data[0]["equipment_needed"] is False

def test_get_exercise_by_id_returns_one_exercise(client):
    with app.app_context():
        exercise = Exercise(
            name="Push-up",
            category="Strength",
            equipment_needed=False,
        )
        db.session.add(exercise)
        db.session.commit()
        exercise_id = exercise.id

    response = client.get(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data["id"] == exercise_id
    assert data["name"] == "Push-up"
    assert data["category"] == "Strength"
    assert data["equipment_needed"] is False

def test_get_exercise_by_id_returns_404_when_not_found(client):
    response = client.get("/exercises/999")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json() == {"error": "Exercise not found"}

def test_create_exercise_returns_created_exercise(client):
    payload = {
        "name": "Deadlift",
        "category": "Strength",
        "equipment_needed": True,
    }

    response = client.post("/exercises", json=payload)

    assert response.status_code == 201
    assert response.is_json

    data = response.get_json()
    assert data["id"] is not None
    assert data["name"] == "Deadlift"
    assert data["category"] == "Strength"
    assert data["equipment_needed"] is True

def test_create_exercise_returns_400_for_missing_fields(client):
    payload = {
        "name": "Deadlift",
    }

    response = client.post("/exercises", json=payload)

    assert response.status_code == 400
    assert response.is_json
    assert "errors" in response.get_json()

def test_delete_exercise_returns_204(client):
    with app.app_context():
        exercise = Exercise(
            name="Deadlift",
            category="Strength",
            equipment_needed=True,
        )
        db.session.add(exercise)
        db.session.commit()
        exercise_id = exercise.id

    response = client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 204
    assert response.data == b""

    with app.app_context():
        deleted_exercise = db.session.get(Exercise, exercise_id)
        assert deleted_exercise is None

def test_delete_exercise_returns_404_when_not_found(client):
    response = client.delete("/exercises/999")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json() == {"error": "Exercise not found"}