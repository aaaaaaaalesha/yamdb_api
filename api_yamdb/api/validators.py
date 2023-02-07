from django.core.exceptions import ValidationError


def me_username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено.',
            params={'value': value},
        )
    return value
