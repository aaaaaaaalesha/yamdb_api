from django.core.exceptions import ValidationError


def me_username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Field username can not be "me".',
            params={'value': value},
        )
