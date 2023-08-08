import pytest
import json
import datetime
from api import PetFriends
from settings import valid_email, valid_password
import sys
from decorators import logger

def generate_string(num):
   return "x" * num
def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'
def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

pf = PetFriends()

@pytest.fixture(scope='class')
def auth_key(email=valid_email, password=valid_password) -> json:
    status, result = pf.get_api_key(email=email, password=password)
    assert status == 200
    assert 'key' in result
    return result['key']

minversion = pytest.mark.skipif(
    sys.version_info < (6, 6), reason="at least mymodule-1.1 required"
)
# @pytest.fixture(autouse=True)
# def request_fixture(request):
#     # print(request.function.__name__)
#     if 'pet' in request.function.__name__:
#         print(f"\nЗапущен тест из сьюта Pet Friends: {request.function.__name__}")

@pytest.mark.skip(reason="Баг в продукте - <ссылка>")
@pytest.mark.auth
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Получаем API ключ для дальнейших проверок"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел успешно(статус 200) и ключ есть в ответе от сервера
    assert status == 200
    assert 'key' in result

@pytest.mark.parametrize("password", ['123456'], ids = ['invalid pass'])
@pytest.mark.parametrize("email", ['ffff@hhhh.gg'], ids = ['invalid email'])
def test_get_api_key_for_valid_user_negative(email, password):
    """Получаем API ключ для дальнейших проверок"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел не успешно(статус 403) и ключа нет в ответе от сервера
    assert status == 403
    assert 'key' not in result
