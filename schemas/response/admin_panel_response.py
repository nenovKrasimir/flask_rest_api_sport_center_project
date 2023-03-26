from marshmallow import fields, Schema


class AllCoachesResponse(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_number = fields.String(required=True)
    coach_type = fields.String(required=True)
