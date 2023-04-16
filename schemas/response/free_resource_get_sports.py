from marshmallow import fields, Schema


class AllSportsResponse(Schema):
    model_type = fields.String(required=True)
