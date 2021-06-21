from graphql import GraphQLSchema

from .login import login_resolver, pin_login_resolver
from .otp import generate_otp_resolver, verify_otp_resolver
from .change_pwd import change_pwd_resolver
from .reset_pwd import reset_pwd_resolver
from .reset_pwd_with_key import reset_pwd_with_key_resolver


def bind_schema(schema: GraphQLSchema):
    schema.mutation_type.fields["login"].resolve = login_resolver
    schema.mutation_type.fields["pin_login"].resolve = pin_login_resolver

    schema.mutation_type.fields["generate_otp"].resolve = generate_otp_resolver
    schema.mutation_type.fields["verify_otp"].resolve = verify_otp_resolver

    schema.mutation_type.fields["change_password"].resolve = change_pwd_resolver
    schema.mutation_type.fields["reset_password"].resolve = reset_pwd_resolver
    schema.mutation_type.fields["reset_password_with_key"].resolve = reset_pwd_with_key_resolver
