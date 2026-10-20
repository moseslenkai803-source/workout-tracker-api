import pytest
from marshmallow import ValidationError

from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema


def test_exercise_schema_accepts_valid_data():
    schema = ExerciseSchema()

    result = schema.load({
        "name": "Squat",
        "category": "Strength",
        "equipment_needed": False,
    })

    assert result["name"] == "Squat"
    assert result["category"] == "Strength"
    assert result["equipment_needed"] is False


@pytest.mark.parametrize("field", ["name", "category"])
@pytest.mark.parametrize("value", ["", "   "])
def test_exercise_schema_rejects_blank_text(field, value):
    schema = ExerciseSchema()
    data = {
        "name": "Squat",
        "category": "Strength",
        "equipment_needed": False,
    }
    data[field] = value

    with pytest.raises(ValidationError):
        schema.load(data)


def test_exercise_schema_requires_equipment_needed():
    schema = ExerciseSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "name": "Squat",
            "category": "Strength",
        })


def test_workout_schema_accepts_valid_data():
    schema = WorkoutSchema()

    result = schema.load({
        "date": "2026-10-20",
        "duration_minutes": 30,
        "notes": "Leg day",
    })

    assert result["duration_minutes"] == 30
    assert result["date"].isoformat() == "2026-10-20"


@pytest.mark.parametrize("duration", [0, -1])
def test_workout_schema_rejects_nonpositive_duration(duration):
    schema = WorkoutSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "date": "2026-10-20",
            "duration_minutes": duration,
        })


def test_workout_schema_rejects_invalid_date():
    schema = WorkoutSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "date": "not-a-date",
            "duration_minutes": 30,
        })


def test_workout_exercise_schema_accepts_valid_data():
    schema = WorkoutExerciseSchema()

    result = schema.load({
        "workout_id": 1,
        "exercise_id": 2,
        "sets": 3,
        "reps": 12,
        "duration_seconds": None,
    })

    assert result["workout_id"] == 1
    assert result["exercise_id"] == 2
    assert result["sets"] == 3
    assert result["reps"] == 12


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("workout_id", 0),
        ("exercise_id", 0),
        ("sets", 0),
        ("sets", -1),
        ("reps", 0),
        ("reps", -1),
        ("duration_seconds", 0),
        ("duration_seconds", -1),
    ],
)
def test_workout_exercise_schema_rejects_nonpositive_values(field, value):
    schema = WorkoutExerciseSchema()
    data = {
        "workout_id": 1,
        "exercise_id": 2,
        "sets": 3,
        "reps": 12,
        "duration_seconds": None,
    }
    data[field] = value

    with pytest.raises(ValidationError):
        schema.load(data)
