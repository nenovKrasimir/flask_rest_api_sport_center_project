from marshmallow import fields, Schema


class AllCoachesResponse(Schema):
    id = fields.Integer(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_number = fields.String(required=True)
    coach_type = fields.String(required=True)


class AllDeliveryGuys(Schema):
    id = fields.Integer(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    contact = fields.String(required=True)
    regio = fields.String(required=True)