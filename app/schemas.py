# app/schemas.py
from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(["doctor", "member"]))

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class DepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
