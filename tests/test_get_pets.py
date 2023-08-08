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

@pytest.mark.pets
@pytest.mark.parametrize("filter", ['', 'my_pets'], ids= ['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(auth_key, filter):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
   Для этого сначала получаем api-ключ с помощью фикстуры get_api_key, которая записывает ключ в auth_key. Далее, используя этот ключ,
   запрашиваем список всех питомцев и проверяем, что список не пустой.
   Доступное значение параметра filter - 'my_pets' либо '' """

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что запрос прошел успешно и список питомцев не пустой
    assert status == 200
    assert len(result['pets']) > 0

@pytest.mark.parametrize("filter",
                        [
                            generate_string(255)
                            , generate_string(1001)
                            , russian_chars()
                            , russian_chars().upper()
                            , chinese_chars()
                            , special_chars()
                            , 123
                        ],
                        ids =
                        [
                            '255 symbols'
                            , 'more than 1000 symbols'
                            , 'russian'
                            , 'RUSSIAN'
                            , 'chinese'
                            , 'specials'
                            , 'digit'
                        ])
def test_get_all_pets_with_negative_filter(auth_key, filter):
    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем статус ответа
    assert status == 500

