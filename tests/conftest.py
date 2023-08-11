import pytest
import json
import datetime
import  sys
from selenium import webdriver

# @pytest.fixture
# def auth_key() -> json:
#     status, result = pf.get_api_key(email=valid_email, password=valid_password)
#     assert status == 200
#     assert 'key' in result
#     return result
@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.datetime.now()
    yield
    end_time = datetime.datetime.now()
    print(f"\nTest time: {end_time - start_time}")
@pytest.fixture(autouse=True)
def start_end():
    print("\n\n Test started!")
    yield
    print(" Test finished!")

# @pytest.mark.xfail(raises=RuntimeError)

# На платформе Windows ожидаем, что тест будет падать
# @pytest.mark.xfail(sys.platform == "win32", reason="Ошибка в системной библиотеке")

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()

   # Переходим на страницу авторизации
   driver.get('https://petfriends.skillfactory.ru/login')

   driver.maximize_window()
   yield driver

   driver.quit()
