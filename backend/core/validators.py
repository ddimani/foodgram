from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from core.constants import (
    MIN_COOKING_TIME,
    MAX_COOKING_TIME,
    MSG_FO_MAX_COOKING,
    MSG_FO_MIN_COOKING,
    MAX_AMOUNT_INGREDIENTS,
    MIN_AMOUNT_INGREDIENTS,
    MSG_FO_MAX_INGREDIENTS,
    MSG_FO_MIN_INGREDIENTS,
    REGEX,
    MSG_FO_USERNAME,
    CODE_FO_USERNAME
)


def validator_cooking(value):
    """Валидатор для проверки времени готовки."""
    try:
        MinValueValidator(MIN_COOKING_TIME, message=MSG_FO_MIN_COOKING)(value)
        MaxValueValidator(MAX_COOKING_TIME, message=MSG_FO_MAX_COOKING)(value)
    except ValidationError as e:
        raise e


def validator_amount(value):
    """Валидатор для проверки количества ингредиентов."""
    try:
        MinValueValidator(
            MIN_AMOUNT_INGREDIENTS,
            message=MSG_FO_MIN_INGREDIENTS
        )(value)
        MaxValueValidator(
            MAX_AMOUNT_INGREDIENTS,
            message=MSG_FO_MAX_INGREDIENTS
        )(value)
    except ValidationError as e:
        raise e


def validator_username(value):
    """Валидатор для проверки имени пользователя."""
    validator = RegexValidator(
        regex=REGEX, message=MSG_FO_USERNAME, code=CODE_FO_USERNAME
    )
    try:
        validator(value)
    except ValidationError as e:
        raise e
