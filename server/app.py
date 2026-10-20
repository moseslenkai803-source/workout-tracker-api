import os

from flask import Flask, request
from marshmallow import ValidationError
from flask_migrate import Migrate

from models import  db, Exercise, Workout
from schemas import ExerciseSchema, WorkoutSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") or "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "Workout Tracker API is running"}

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    schema = ExerciseSchema(many=True)
    return schema.dump(exercises), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    schema = WorkoutSchema()

    try:
        validated_data = schema.load(data)
    except ValidationError as error:
        return {"errors": error.messages}, 400

    workout = Workout(**validated_data)
    db.session.add(workout)
    db.session.commit()

    return schema.dump(workout), 201


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    schema = WorkoutSchema()
    return schema.dump(workout), 200

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    schema = WorkoutSchema(many=True)
    return schema.dump(workouts), 200

@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    schema = ExerciseSchema()
    return schema.dump(exercise), 200

@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    schema = ExerciseSchema()

    try:
        validated_data = schema.load(data)
    except ValidationError as error:
        return {"errors": error.messages}, 400

    exercise = Exercise(**validated_data)

    db.session.add(exercise)
    db.session.commit()

    return schema.dump(exercise), 201


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()

    return "", 204


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()

    return "", 204

if __name__ == "__main__":
    app.run(port=5555, debug=True)