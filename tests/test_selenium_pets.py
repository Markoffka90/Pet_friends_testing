from selenium.webdriver.common.by import By
from settings import valid_email, valid_password

def test_show_all_pets(driver):
   # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
   driver.find_element(By.ID, 'email').send_keys(valid_email)
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.get('https://petfriends.skillfactory.ru/my_pets')

   # список всех обьектов питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить информацию о питомце в виде строки: 'Мурзик Котэ 5'
   all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

   # проверяем что список своих питомцев не пуст
   assert len(all_my_pets) > 0

   pets_info = []

   for i in range(len(all_my_pets)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_info = all_my_pets[i].text

      # избавляемся от лишних символов '\n×'
      pet_info = pet_info.split("\n")[0]

      # добавляем в список pets_info информацию рода: имя, тип, возраст по каждому питомцу
      pets_info.append(pet_info)

   # количество питомцев пользователя из статистики.
   user_stat = driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]')
   user_stat_text = user_stat.text.split("\n")
   user_stat_text_pets = user_stat_text[1]
   parts = user_stat_text_pets.split(": ")
   number_of_pets = int(parts[1])

   # проверяем что на странице присутствуют все питомцы
   assert len(all_my_pets) == number_of_pets

def test_more_then_half_card_contains_photo(driver):
   # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
   driver.find_element(By.ID, 'email').send_keys(valid_email)
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.get('https://petfriends.skillfactory.ru/my_pets')

   # этот список image объектов , который имееют метод get_attribute('src') ,
   # благодаря которому можно посмотреть есть ли изображение питомца или нет.
   all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')

   # количество питомцев пользователя из статистики.
   user_stat = driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]')
   user_stat_text = user_stat.text.split("\n")
   user_stat_text_pets = user_stat_text[1]
   parts = user_stat_text_pets.split(": ")
   number_of_pets = int(parts[1])

   # проверяем что список изображений не пуст
   assert len(all_pets_images) > 0

   # считаем сколько карточек содержит непустое значение элемента src
   pets_with_photo = 0
   for i in range(len(all_pets_images)):
      if all_pets_images[i].get_attribute('src') != '':
         pets_with_photo += 1

   # проверяем что хотя бы у половины питомцев есть фото
   assert number_of_pets/2 <= pets_with_photo

def test_all_pets_have_name_type_age(driver):
   # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
   driver.find_element(By.ID, 'email').send_keys(valid_email)
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.get('https://petfriends.skillfactory.ru/my_pets')

   # список всех обьектов имен питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить имя питомца в виде строки: 'Мурзик'
   all_pets_names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[1]')

   # список всех обьектов пород питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить информацию о питомце в виде строки: 'Котэ'
   all_pets_types = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[2]')

   # список всех обьектов возраста питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить информацию о питомце в виде строки: '5'
   all_pets_ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[3]')

   # проверяем что списоки своих питомцев не пусты и равны
   assert len(all_pets_names) > 0
   assert len(all_pets_types) > 0
   assert len(all_pets_ages) > 0
   assert len(all_pets_names) == len(all_pets_types) == len(all_pets_ages)

   f = True
   for i in range(len(all_pets_names)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_name = all_pets_names[i].text
      pet_type = all_pets_types[i].text
      pet_age = all_pets_ages[i].text

      # если в списке есть пустое значение переменнтая f принимает значение ложь
      if pet_name == '': f = False
      if pet_type == '': f = False
      if pet_age == '': f = False

   # проверяем что у всех питомцев есть имя, возраст и порода
   assert f == True

def test_all_pets_have_uniq_name(driver):
   # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
   driver.find_element(By.ID, 'email').send_keys(valid_email)
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.get('https://petfriends.skillfactory.ru/my_pets')

   # список всех обьектов имен питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить имя питомца в виде строки: 'Мурзик'
   all_pets_names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[1]')

   pets_name = []
   for i in range(len(all_pets_names)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_name = all_pets_names[i].text

      # избавляемся от лишних символов '\n×'
      pet_name = pet_name.split("\n")[0]
      if pets_name == '': f = False

      # добавляем в список pets_name имя по каждому питомцу
      pets_name.append(pet_name)

   pets_name_uniq = list(set(pets_name))

   # проверяем что у всех питомцев разные имена
   assert len(pets_name) == len(pets_name_uniq)

def test_no_identical_pets(driver):
   # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
   driver.find_element(By.ID, 'email').send_keys(valid_email)
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.get('https://petfriends.skillfactory.ru/my_pets')

   # список всех обьектов питомца , в котром есть атрибут ".text" с помощью которого,
   # можно получить информацию о питомце в виде строки: 'Мурзик Котэ 5'
   all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

   # проверяем что список своих питомцев не пуст
   assert len(all_my_pets) > 0

   pets_info = []
   for i in range(len(all_my_pets)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_info = all_my_pets[i].text

      # избавляемся от лишних символов '\n×'
      pet_info = pet_info.split("\n")[0]

      # добавляем в список pets_info информацию рода: имя, тип, возраст,  по каждому питомцу
      pets_info.append(pet_info)

   pets_info_uniq = list(set(pets_info))

   # проверяем что в списке нет повторяющихся питомцев
   assert len(pets_info) == len(pets_info_uniq)