NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
MEASUREMENT_UNIT = 64
USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254

MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 43200
MSG_FO_MIN_COOKING = f'Значение не может быть меньше {MIN_COOKING_TIME}!'
MSG_FO_MAX_COOKING = f'Значение не может быть больше {MAX_COOKING_TIME}!'

SHORT_LINK_MAX_LENGTH = 16
MAX_ATTEMPTS = 10
MIN_AMOUNT_INGREDIENTS = 1
MAX_AMOUNT_INGREDIENTS = 32000
MSG_FO_MIN_INGREDIENTS = f'Значение не может быть меньше {MIN_AMOUNT_INGREDIENTS}!'
MSG_FO_MAX_INGREDIENTS = f'Значение не может быть больше {MAX_AMOUNT_INGREDIENTS}!'

REGEX = r'^[\w.@+-]+\Z'
MSG_FO_USERNAME='Введите корректное имя пользователя. Разрешены только буквы, цифры и символы @/./+/-/_.'
CODE_FO_USERNAME = 'invalid_username'

EMPTY_VALUE_ADMIN_PANEL = '-empty-'

ERROR_TAG = 'Добавьте хотя бы один тег!'
ERROR_MESSAGE_DUBLICATE_TAGS = ('Проверьте теги на дубликаты! Найдены дубликаты: '
                  '{dublicates}')
ERROR_INGREDIENTS = 'Добавьте хотя бы один ингредиент!'
ERROR_MESSAGE_DUBLICATE_INGRED = ('Проверьте ингредиенты на дубликаты! Найдены дубликаты: '
                  '{dublicates}')

IMAGE_ERROR = 'Необходимо добавить изображение!'

RECIPE_ADD_ERR0R = 'Этот рецепт уже добавлен в список покупок!'

ERROR_ME_FOLLOW = 'Нельзя подписаться на самого себя!'

FOLLOWING_ERROR = 'Такая подписка уже существует!'

PREFIX_SHORT_LINK_RECIPE = 's/'

NO_CONTENT = 'Список покупок пуст!'

PAGE_SIZE = 6


RECIPE_FILTER_CHOICES = (
    (0, False),
    (1, True)
)
