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
def test_add_new_pet_with_valid_data(auth_key, name='Marsel', animal_type='cat',
                                     age='2', pet_photo='images/plux.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

@pytest.mark.pets
def test_delete_existing_pet(auth_key):
    """Проверяем что можно удалить уже существующего питомца"""


    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}
    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Marsel", "cat", "2", "images/marsel.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
@pytest.mark.pets
def test_successful_update_self_pet_info(auth_key, name='Plu', animal_type='cat', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    auth_key = {'key': auth_key}
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить имя, тип и возраст первого питомца в списке
    if len(my_pets['pets']) > 0:
        res = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
@pytest.mark.pets
@pytest.mark.parametrize("name"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(), special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(), special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_add_new_pet_with_valid_data_simple_metod(auth_key, name, animal_type, age):
    """Проверяем что можно добавить питомца с корректными данными простым способом"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type

    # Удаляем питомца
    pet_id = result['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                             ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                              russian_chars().upper(), chinese_chars()]
        , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
               'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_with_valid_data_simple_metod_negative(auth_key, name, animal_type, age):
    """Проверяем что нельзя добавить питомца с некорректными данными простым способом"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

    # Почему то не удаляет. udp потому что проверка не проходит и он завершает на ассерт
    pet_id = result['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
@pytest.mark.pets
def test_add_photo_for_pet(auth_key, pet_photo='images/plux.jpg'):
    """Проверяем что можно добавить фото питомца"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Plux", "cat", "2")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Добавляем фото питомца
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''
