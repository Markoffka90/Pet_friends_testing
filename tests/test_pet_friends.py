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

# @minversion
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

@pytest.mark.pets
def test_add_new_pet_with_valid_data(auth_key, name='Marsel', animal_type='cat',
                                     age='2', pet_photo='images/marsel.jpg'):
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
def test_successful_update_self_pet_info(auth_key, name='Mars', animal_type='bobteil', age=1):
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

 #########################################################################


@pytest.mark.auth
def test_get_api_key_for_invalid_pas(email=valid_email, password='123456'):
    """Проверяем что API ключ нельзя получить при невалидном пароле"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел не успешно(статус 403) и ключа нет в ответе от сервера
    assert status == 403
    assert 'key' not in result

@pytest.mark.auth
def test_get_api_key_for_invalid_email(email='ffff@hhhh.gg', password=valid_password):
    """Проверяем что API ключ нельзя получить при невалидном юзернейме"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел не успешно(статус 403) и ключа нет в ответе от сервера
    assert status == 403
    assert 'key' not in result
@pytest.mark.pets
def test_get_all_pets_with_invalid_key(auth_key, filter=''):
    """Проверяем что нельзя получить список всех питомцев данного юзера без валидного апи ключа"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Портим переменую auth_key
    auth_key = {'key': '44f22dc2e04c75cb7b7bdb05419a5fb3f2286de4fa213a75c2c5e50'}

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что запрос не прошел и в статусе ошибка
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result
@pytest.mark.pets
def test_add_new_pet_with_invalid_key(auth_key, name='Marsel', animal_type='cat',
                                     age='3', pet_photo='images/marsel.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным апи ключом"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Портим переменую auth_key
    auth_key = {'key': '44f22dc2e04c75cb7b7bdb05419a5fb3f2286de4fa213a75c2c5e50'}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем что запрос не прошел и в статусе нужная ошибка
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result

@pytest.mark.pets
@pytest.mark.xfail
def test_add_new_pet_with_invalid_age(auth_key, name='Marsel', animal_type='cat',
                                     age='r', pet_photo='images/marsel.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'age should be numeric' in result
@pytest.mark.pets
@pytest.mark.xfail
def test_delete_existing_pet_with_indalid_key(auth_key):
    """Проверяем что невозможно удалить уже существующего питомца с некорретным апи ключом"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Marsel", "cat", "2", "images/marsel.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Портим переменую auth_key
    auth_key = {'key': '44f22dc2e04c75cb7b7bdb05419a5fb3f2286de4fa213a75c2c5e50'}

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    # Проверяем что запрос не прошел и в статусе нужная ошибка
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result
@pytest.mark.pets
def test_unsuccessful_update_self_pet_info_of_nonexisting_pet(auth_key, name='Mars', animal_type='sfinks', age=1):
    """Проверяем невозможность обновления информации  питомце если его удалили"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Добавляем нового питомца, сохраняем айди в переменную pet_id
    _, my_pet = pf.add_new_pet(auth_key, "Bars", "cat", "2", "images/barsik.jpg")
    pet_id = my_pet['id']
    print(pet_id)
    # Удаляем питомца по айди
    _, _, = pf.delete_pet(auth_key, pet_id)

    # Пытаемся проапдейтить удаленного питомца
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'Pet with this id wasn&#x27;t found!' in result
@pytest.mark.pets
def test_add_new_pet_without_name_simple_metod(auth_key, name=None,  animal_type='cat', age='3'):
    """Проверяем что нельзя добавить питомца без имени простым способом"""

    # Ключ api сохраняем в переменую auth_key
    auth_key = {'key': auth_key}

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'The browser (or proxy) sent a request that this server could not understand.' in result
@pytest.mark.pets
def test_add_photo_in_wrong_format_for_pet(auth_key, pet_photo='images/mysh-kris.gif'):
    """Проверяем что нельзя добавить гифку как фото питомца"""

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
    assert status == 500
    assert 'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application' in result

# def test_delete_all_pets(auth_key):
#
#     # Ключ api сохраняем в переменую auth_key
#     auth_key = {'key': auth_key}
#
#     # Запрашиваем список своих питомцев
#     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#     print(len(my_pets['pets']))
#     i = len(my_pets['pets'])
#     while i > 0:
#         p_id = my_pets['pets'][i-1]['id']
#         _, _, = pf.delete_pet(auth_key, p_id)
#         i -= 1
