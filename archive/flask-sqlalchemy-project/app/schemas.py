"""Marshmallow schemas for request/response validation."""
from marshmallow import Schema, fields, validate, ValidationError, validates


class UserSchema(Schema):
    """Schema for user validation."""
    
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        error_messages={'required': 'Username is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required'}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8),
        error_messages={'required': 'Password is required'}
    )
    first_name = fields.Str(validate=validate.Length(max=50), allow_none=True)
    last_name = fields.Str(validate=validate.Length(max=50), allow_none=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(Schema):
    """Schema for updating user (all fields optional)."""
    
    username = fields.Str(validate=validate.Length(min=3, max=50))
    email = fields.Email()
    password = fields.Str(load_only=True, validate=validate.Length(min=8))
    first_name = fields.Str(validate=validate.Length(max=50), allow_none=True)
    last_name = fields.Str(validate=validate.Length(max=50), allow_none=True)


class PostSchema(Schema):
    """Schema for post validation."""
    
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={'required': 'Title is required'}
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Content is required'}
    )
    published = fields.Bool(missing=False)
    author_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested author information (optional)
    author = fields.Nested(UserSchema, dump_only=True)


class PostUpdateSchema(Schema):
    """Schema for updating post (all fields optional)."""
    
    title = fields.Str(validate=validate.Length(min=1, max=200))
    content = fields.Str(validate=validate.Length(min=1))
    published = fields.Bool()


class PaginationSchema(Schema):
    """Schema for pagination parameters."""
    
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    page_size = fields.Int(missing=20, validate=validate.Range(min=1, max=100))


class UserFilterSchema(PaginationSchema):
    """Schema for user filtering and pagination."""
    
    username = fields.Str()
    email = fields.Str()
    is_active = fields.Bool()


class PostFilterSchema(PaginationSchema):
    """Schema for post filtering and pagination."""
    
    author_id = fields.Int()
    published = fields.Bool()
    search = fields.Str()  # Search in title and content


# Schema instances for reuse
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserUpdateSchema()

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
post_update_schema = PostUpdateSchema()

pagination_schema = PaginationSchema()
user_filter_schema = UserFilterSchema()
post_filter_schema = PostFilterSchema()
