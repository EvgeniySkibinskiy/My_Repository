from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос API ключа возвращает статус 200"""

    # Отправяем запрос и сохраням полученный ответ с кодм статуса в status, текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверям что запрос всх питомцев возвращает не пустой список"""

    # Получаем api ключ и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправяем запрос и сохраням полученный ответ с кодм статуса в status, текст ответа в result
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные
    assert status == 200
    assert len(result['pets']) > 0

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Проверям что запрос всх питомцев возвращает не пустой список"""

    # Получаем api ключ и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Клепа", "кошка", '12', "image/Cleopatra.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Отправяем запрос и сохраням полученный ответ с кодм статуса в status, текст ответа в result
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные
    assert status == 200
    len(result['pets']) > 0



def test_add_new_pet_with_valid_data(name='Карат', animal_type='кот',
                                     age='3', pet_photo='image/Carat.jpg'):
    """Проверяем что можно добавить питомца с коретными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключь auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Клепа", "кошка", "12", "image/Cleopatra.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pet_info(name='Клеопатра', animal_type='кошка', age=12):
    """Проверяем возможность обновления информации о питоице"""

    # Получаем ключ auth_key и запрашиваем список своих питоцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то меняем имя, тип и возраст питомца
    if len(my_pets['pets']) == 0:

        pf.add_new_pet(auth_key, "Клепа", "кошка", "12", "image/Cleopatra.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа 200 и данные питомца соответствуют заданным
    assert status == 200
    assert result['name'] == name



def test_add_new_pet_without_photo(name='Карат', animal_type='кот', age=3):
    """Проверям возможность добавления данных о питомце без изображения"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа 200 и данные питомца соответствуют заданным
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo='image/Carat.jpg'):
    """Проверяем возможность добавления изображения питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление изображения питомца
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем что статус ответа 200
    assert status == 200



def test_get_api_key_for_not_registered_user(email='Zora_1@mail.ru', password='1234567'):
    """Проверяем что запрос api ключа возвращает статус 200"""

    # Отправяем запрос и сохраням полученный ответ с кодм статуса в status, текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status == 200
    assert 'key' in result

def test_add_new_pet_with_incorrect_data(name='', animal_type='', age=''):
    """Проверяем возможность внесения некоретных данных о питомце"""

    # Получаем api ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученные данные
    assert status == 200
    assert result['name'] == name


