from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


def seed_data():
    with app.app_context():
        exercises_data = [
            {
                "name": "Squat",
                "category": "Strength",
                "equipment_needed": False,
            },
            {
                "name": "Push-up",
                "category": "Strength",
                "equipment_needed": False,
            },
            {
                "name": "Plank",
                "category": "Core",
                "equipment_needed": False,
            },
        ]

        exercises = {}

        for exercise_data in exercises_data:
            exercise = Exercise.query.filter_by(
                name=exercise_data["name"]
            ).first()

            if exercise is None:
                exercise = Exercise(**exercise_data)
                db.session.add(exercise)

            exercises[exercise_data["name"]] = exercise

        db.session.flush()

        workout = Workout.query.filter_by(
            date=date(2026, 10, 20),
            notes="Sample full-body workout",
        ).first()

        if workout is None:
            workout = Workout(
                date=date(2026, 10, 20),
                duration_minutes=45,
                notes="Sample full-body workout",
            )
            db.session.add(workout)
            db.session.flush()

        existing_links = {
            link.exercise_id
            for link in WorkoutExercise.query.filter_by(
                workout_id=workout.id
            ).all()
        }

        workout_exercises_data = [
            {
                "exercise": exercises["Squat"],
                "sets": 3,
                "reps": 12,
                "duration_seconds": None,
            },
            {
                "exercise": exercises["Plank"],
                "sets": 3,
                "reps": 1,
                "duration_seconds": 45,
            },
        ]

        for item in workout_exercises_data:
            exercise = item.pop("exercise")

            if exercise.id not in existing_links:
                db.session.add(
                    WorkoutExercise(
                        workout_id=workout.id,
                        exercise_id=exercise.id,
                        **item,
                    )
                )

        db.session.commit()
        print("Seed data created successfully.")


if __name__ == "__main__":
    seed_data()
