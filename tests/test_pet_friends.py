from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Получаем API ключ для дальнейших проверок"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел успешно(статус 200) и ключ есть в ответе от сервера
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """Получаем список всех питомцев данного юзера"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что запрос прошел успешно и список питомцев не пустой
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Marsel', animal_type='cat',
                                     age='2', pet_photo='images/marsel.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_delete_existing_pet():
    """Проверяем что можно удалить уже существующего питомца"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
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

def test_successful_update_self_pet_info(name='Mars', animal_type='sfinks', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить имя, тип и возраст первого питомца в списке
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_with_valid_data_simple_metod(name='Plux', animal_type='cat', age='3'):
    """Проверяем что можно добавить питомца с корректными данными простым способом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_for_pet(pet_photo='images/plux.jpg'):
    """Проверяем что можно добавить фото питомца"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

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

def test_get_api_key_for_invalid_pas(email=valid_email, password='123456'):
    """Проверяем что API ключ нельзя получить при невалидном пароле"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел не успешно(статус 403) и ключа нет в ответе от сервера
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_email(email='ffff@hhhh.gg', password=valid_password):
    """Проверяем что API ключ нельзя получить при невалидном юзернейме"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Проверяем что запрос прошел не успешно(статус 403) и ключа нет в ответе от сервера
    assert status == 403
    assert 'key' not in result

def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем что нельзя получить список всех питомцев данного юзера без валидного апи ключа"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Портим переменую auth_key
    auth_key = {'key': '44f22dc2e04c75cb7b7bdb05419a5fb3f2286de4fa213a75c2c5e50'}

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что запрос не прошел и в статусе ошибка
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result

def test_add_new_pet_with_invalid_key(name='Marsel', animal_type='cat',
                                     age='3', pet_photo='images/marsel.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным апи ключом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Портим переменую auth_key
    auth_key = {'key': '44f22dc2e04c75cb7b7bdb05419a5fb3f2286de4fa213a75c2c5e50'}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем что запрос не прошел и в статусе нужная ошибка
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result
def test_add_new_pet_with_invalid_age(name='Marsel', animal_type='cat',
                                     age='r', pet_photo='images/marsel.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'age should be numeric' in result

def test_delete_existing_pet_with_indalid_key():
    """Проверяем что невозможно удалить уже существующего питомца с некорретным апи ключом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

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

def test_unsuccessful_update_self_pet_info_of_nonexisting_pet(name='Mars', animal_type='sfinks', age=1):
    """Проверяем невозможность обновления информации  питомце если его удалили"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

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

def test_add_new_pet_without_name_simple_metod(name= None,  animal_type='cat', age='3'):
    """Проверяем что нельзя добавить питомца без имени простым способом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'The browser (or proxy) sent a request that this server could not understand.' in result

def test_add_photo_in_wrong_format_for_pet(pet_photo='images/mysh-kris.gif'):
    """Проверяем что нельзя добавить гифку как фото питомца"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

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