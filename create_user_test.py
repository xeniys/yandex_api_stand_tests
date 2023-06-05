import sender_stand_request
import data


# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                              "Имя может содержать только русские или латинские буквы, длина должна " \
                                              "быть не менее 2 и не более 15 символов"


def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("AaaaаBbbbbccccc")

# Тест 3. Пользователь не создается
# Параметр fisrtName состоит из 1 символов
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")

# Тест 4. Пользователь не создается
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("AaaaаBbbbbcccccD")

# Тест 5. Успешное создание пользователя
# Параметр fisrtName состоит английских букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("Kseniia")

# Тест 6. Успешное создание пользователя
# Параметр fisrtName состоит русских букв
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Ксения")

# Тест 7. Пользователь не создается
# Параметр fisrtName содержит пробел
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Aaa BBB")

# Тест 8. Пользователь не создается
# Параметр fisrtName содержит спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Тест 9. Пользователь не создается
# Параметр fisrtName содержит цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():

    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

# Тест 12. Ошибка
# Передан другой тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
