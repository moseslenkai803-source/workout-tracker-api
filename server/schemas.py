from marshmallow import Schema, ValidationError, fields, validate


def non_blank(value):
    if not value.strip():
        raise ValidationError("This field cannot be blank.")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=1,
                max=100,
                error="Name must contain 1 to 100 characters.",
            ),
            non_blank,
        ],
    )

    category = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=1,
                max=100,
                error="Category must contain 1 to 100 characters.",
            ),
            non_blank,
        ],
    )

    equipment_needed = fields.Bool(required=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            error="Workout duration must be greater than zero.",
        ),
    )

    notes = fields.Str(required=False, allow_none=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(required=True, validate=validate.Range(min=1))
    exercise_id = fields.Int(required=True, validate=validate.Range(min=1))

    sets = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Sets must be greater than zero."),
    )

    reps = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Reps must be greater than zero."),
    )

    duration_seconds = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )