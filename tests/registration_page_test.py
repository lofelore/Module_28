import time

import pytest
from selenium.webdriver.common.by import By

from locators.AuthorizationPageLocators import AuthorizationPageLocators
from locators.RegistrationPageLocators import RegistrationLocators
from pages.AuthorizationPage import AuthorizationPage
from pages.RegistrationPage import RegistrationPage
from settings import *
from utils.GenerateRandomEmail import GenerateRandomEmail


# RTC-016
@pytest.mark.registration
@pytest.mark.positive
def test_open_registration_page(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.click_on_registration_button()
    page.driver.save_screenshot(r"../tests/screenshots/Registration/registration_page.png")
    print(f"RTC-016 \nПроверка успешного перехода на страницу регистрации РосТелеКом")
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/registration"


# RTC-020
@pytest.mark.registration
@pytest.mark.positive
class TestRegistration:
    """Класс проверяет успешную регистрацию в личном кабинете РосТелеКом.
    Для регистрации используется временный адрес электронной почты, получаемый в классе RandomEmail
    с помощью сайта https://www.1secmail.com.
    Класс получает код для входа на почтовый ящик и записывает сгенерированный временный электронный адрес
    в файл settings.py.
    В теле класса определяем данные для доступа к их значениям из всех методов классса."""
    result_email, status_email = GenerateRandomEmail().get_api_email()
    valid_email = result_email[0]

    def test_registration_by_email(self, google_chrome_browser):
        # Разделяем email на имя и домен для использования в последующих запросах:
        sign_at = self.valid_email.find('@')
        mail_name = self.valid_email[0:sign_at]
        mail_domain = self.valid_email[sign_at + 1:len(self.valid_email)]
        assert self.status_email == 200, 'status_email error'
        assert len(self.result_email) > 0, 'len(result_email) > 0 -> error'

        # Активируем окно регистрации, нажимаем на кнопку "Зарегистрироваться":
        auth_page = AuthorizationPage(google_chrome_browser)
        auth_page.click_on_registration_button()
        assert auth_page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

        reg_page = RegistrationPage(google_chrome_browser)

        reg_page.fill_registration_form(valid_firstname, valid_lastname, valid_region, valid_email, valid_password,
                                        valid_password)

        # Ожидаем поступление письма с кодом подтверждения на указанный адрес электронной почты:
        time.sleep(30)

        # Проверяем почтовый ящик на наличие писем и находим ID последнего письма:
        result_id, status_id = GenerateRandomEmail().get_id_letter(mail_name, mail_domain)
        id_letter = result_id[0].get('id')
        # Сверяем полученные данные с нашими ожиданиями:
        assert status_id == 200, "status_id error"
        assert id_letter > 0, "id_letter > 0 error"

        # Получаем код регистрации из письма от РосТелеКом:
        result_code, status_code = GenerateRandomEmail().get_reg_code(mail_name, mail_domain, str(id_letter))

        text_body = result_code.get("body")
        # Извлекаем код из текста методом find:
        reg_code = text_body[text_body.find("Ваш код : ") + len("Ваш код : "):
                             text_body.find("Ваш код : ") + len("Ваш код : ") + 6]
        # Сверяем полученные данные с нашими ожиданиями:
        assert status_code == 200, "status_code error"
        assert reg_code != '', "reg_code != [] error"

        # Вводим полученный код в соответствующее поле ввода:
        [int(char) for char in reg_code]
        google_chrome_browser.implicitly_wait(30)
        for i in range(0, 6):
            google_chrome_browser.find_elements(By.CSS_SELECTOR, "input[inputmode='numeric']")[i].send_keys(reg_code[i])
            google_chrome_browser.implicitly_wait(5)
        google_chrome_browser.implicitly_wait(30)

        # Проверяем, что регистрация успешно пройдена и пользователь перенаправлен
        # в свой личный кабинет на сайте РосТелеКом:
        assert reg_page.get_current_url() == "/account_b2c/page"
        time.sleep(10)

        # При успешной регистрации, перезаписываем временный email в файл settings.py:
        reg_page.driver.save_screenshot(r"../tests/screenshots/Registration/registration_success.png")
        print(f"RTC-020 \nПроверка успешной регистрации в личном кабинете РосТелеКом")
        with open(r"../settings.py", "r", encoding="utf8") as file:
            lines = []
            for line in file.readlines():
                if "valid_email" in line:
                    lines.append(f'valid_email = "{str(self.valid_email)}"\n')
                else:
                    lines.append(line)
        with open(r"../settings.py", "w", encoding="utf8") as file:
            file.writelines(lines)


@pytest.mark.registration
@pytest.mark.negatvie
@pytest.mark.parametrize("lastname", ["", generate_cyrillic_string(1), generate_cyrillic_string(31),
                                      generate_cyrillic_string(256), english_chars(),
                                      special_chars(), 78489, japanese_symbols(),
                                      chinese_symbols()],
                         ids=['RTC-033-1) empty line', 'RTC-033-2) one char', 'RTC-033-3) 31 chars',
                              'RTC-033-4) 256 chars', 'RTC-033-5) english', 'RTC-033-6) special',
                              'RTC-033-7) number', 'RTC-033-8) japanese_symbols', 'RTC-033-9) chinese_symbols'])
def test_registration_with_invalid_format_lastname(google_chrome_browser, lastname):
    auth_page = AuthorizationPage(google_chrome_browser)
    auth_page.click_on_registration_button()

    google_chrome_browser.implicitly_wait(2)
    assert auth_page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

    reg_page = RegistrationPage(google_chrome_browser)

    reg_page.fill_registration_form(valid_firstname, lastname, valid_region, valid_email, valid_password,
                                    valid_password)

    # reg_page.set_firstname_input(valid_firstname)
    # google_chrome_browser.implicitly_wait(5)
    #
    # reg_page.set_lastname_input(lastname)
    # google_chrome_browser.implicitly_wait(5)
    #
    # reg_page.set_email_input(valid_email)
    # google_chrome_browser.implicitly_wait(3)
    #
    # reg_page.set_password_input(valid_password)
    # google_chrome_browser.implicitly_wait(3)
    #
    # reg_page.set_confirm_password_input(valid_password)
    # google_chrome_browser.implicitly_wait(3)
    #
    # reg_page.click_on_registration_button()
    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.ERROR_MESSAGE)

    assert error_mess.text == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."
    print(f"RTC-033-(1-9)"
          f"\nНегативный сценарий регистрации в личном кабинете РосТелеКом: "
          f"невалидый формат Фамилии.")
    print('Сообщение об ошибке: "Необходимо заполнить поле кириллицей. От 2 до 30 символов."')


@pytest.mark.registration
@pytest.mark.negatvie
@pytest.mark.parametrize("firstname", ["", generate_cyrillic_string(1), generate_cyrillic_string(31),
                                       generate_cyrillic_string(256), english_chars(),
                                       special_chars(), 78489, japanese_symbols(),
                                       chinese_symbols()],
                         ids=['RTC-032-1) empty line', 'RTC-032-2) one char', 'RTC-032-3) 31 chars',
                              'RTC-032-4) 256 chars', 'RTC-032-5) english', 'RTC-032-6) special',
                              'RTC-032-7) number', 'RTC-032-8) japanese_symbols', 'RTC-032-9) chinese_symbols'])
def test_registration_invalid_format_firstname(google_chrome_browser, firstname):
    page = AuthorizationPage(google_chrome_browser)
    page.click_on_registration_button()
    google_chrome_browser.implicitly_wait(2)
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

    page = RegistrationPage(google_chrome_browser)
    page.set_firstname_input(firstname)
    google_chrome_browser.implicitly_wait(2)

    page.set_lastname_input(valid_lastname)
    google_chrome_browser.implicitly_wait(2)

    page.set_email_input(valid_email)
    google_chrome_browser.implicitly_wait(2)

    page.set_password_input(valid_password)
    google_chrome_browser.implicitly_wait(2)

    page.set_confirm_password_input(valid_password)
    google_chrome_browser.implicitly_wait(2)

    page.click_on_registration_button()
    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.ERROR_MESSAGE)

    assert error_mess.text == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."
    print(f"RTC-032-(1-9)"
          f"\nНегативный сценарий регистрации в личном кабинете РосТелеКом: "
          f"невалидый формат Имени.")
    print('Сообщение об ошибке: "Необходимо заполнить поле кириллицей. От 2 до 30 символов."')


# RTC-033


# RTC-034
@pytest.mark.registration
@pytest.mark.negatvie
@pytest.mark.parametrize("phone", ["", 1, 1111111111, generate_cyrillic_string(11), english_chars(), special_chars()],
                         ids=['RTC-034-1) empty line', 'RTC-034-2) one digit', 'RTC-034-3) 10_digits',
                              'RTC-034-4) string_rus', 'RTC-034-5) english_chars', 'RTC-034-6) special_chars'])
def test_registration_with_invalid_format_phone(google_chrome_browser, phone):
    page = AuthorizationPage(google_chrome_browser)
    page.click_on_registration_button()
    google_chrome_browser.implicitly_wait(2)
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

    page = RegistrationPage(google_chrome_browser)

    page.set_firstname_input(valid_firstname)
    google_chrome_browser.implicitly_wait(5)

    page.set_lastname_input(valid_lastname)
    google_chrome_browser.implicitly_wait(5)

    page.set_email_input(phone)
    google_chrome_browser.implicitly_wait(3)

    page.set_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.set_confirm_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.click_on_registration_button()

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.ERROR_MESSAGE)
    assert error_mess.text == "Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, " \
                              "или email в формате example@email.ru"
    print(f"RTC-034-(1-6)"
          f"\nНегативный сценарий регистрации в личном кабинете РосТелеКом: "
          f"невалидый формат номера телефона."
          "\nПрименена техника анализа классов эквивалентности.")
    print('Сообщение об ошибке: "Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, '
          'или email в формате example@email.ru"')


# RTC-035
@pytest.mark.registration
@pytest.mark.negatvie
@pytest.mark.parametrize("email", ["", "@", "@.", ".", generate_cyrillic_string(20),
                                   f"{cyrillic_chars()}@mail.ru", 77777],
                         ids=['RTC-035-1) empty line', 'RTC-035-2) at', 'RTC-035-3) at point',
                              'TRK-035-4) point', 'RTC-035-5) string', 'RTC-035-6) russian',
                              'RTC-035-7) digits'])
def test_registration_with_invalid_format_email(google_chrome_browser, email):
    page = AuthorizationPage(google_chrome_browser)
    page.click_on_registration_button()
    google_chrome_browser.implicitly_wait(2)
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

    page = RegistrationPage(google_chrome_browser)

    page.set_firstname_input(valid_firstname)
    google_chrome_browser.implicitly_wait(5)

    page.set_lastname_input(valid_lastname)
    google_chrome_browser.implicitly_wait(5)

    page.set_email_input(email)
    google_chrome_browser.implicitly_wait(3)

    page.set_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.set_confirm_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.click_on_registration_button()
    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.ERROR_MESSAGE)

    assert error_mess.text == "Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, " \
                              "или email в формате example@email.ru"
    print(f"RTC-035-(1-7)"
          f"\nНегативный сценарий регистрации в личном кабинете РосТелеКом: "
          f"невалидый формат адреса электронной почты.")
    print('Сообщение об ошибке: "Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, '
          'или email в формате example@email.ru"')


# RTC-036
@pytest.mark.registration
@pytest.mark.negatvie
@pytest.mark.parametrize("living_email", [valid_email], ids=["living email"])
def test_registration_with_living_account(google_chrome_browser, living_email):
    page = AuthorizationPage(google_chrome_browser)
    page.click_on_registration_button()
    google_chrome_browser.implicitly_wait(2)
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

    page = RegistrationPage(google_chrome_browser)
    page.set_firstname_input(valid_firstname)
    google_chrome_browser.implicitly_wait(5)

    page.set_lastname_input(valid_lastname)
    google_chrome_browser.implicitly_wait(5)

    page.set_email_input(living_email)
    google_chrome_browser.implicitly_wait(3)

    page.set_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.set_confirm_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.click_on_registration_button()
    time.sleep(2)
    card_modal_title = google_chrome_browser.find_element(*RegistrationLocators.REG_CARD_MODAL)

    assert card_modal_title.text == "Учётная запись уже существует"
    print(f"RTC-036"
          f"\nНегативный сценарий регистрации в личном кабинете РосТелеКом: "
          f"зарегистрированный в системе адрес электронной почты.")
    print('Сообщение об ошибке: "Учётная запись уже существует"')


# RTC-037
@pytest.mark.registration
@pytest.mark.negatvie
def test_registration_when_password_diff_password_confirm(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)  # нажимаем на кнопку "Зарегистрироваться"
    page.click_on_registration_button()
    google_chrome_browser.implicitly_wait(2)
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/registration"

    page = RegistrationPage(google_chrome_browser)
    page.set_firstname_input(valid_firstname)
    google_chrome_browser.implicitly_wait(5)

    page.set_lastname_input(valid_lastname)
    google_chrome_browser.implicitly_wait(5)

    page.set_email_input(valid_email)
    google_chrome_browser.implicitly_wait(3)

    page.set_password_input(valid_password)
    google_chrome_browser.implicitly_wait(3)

    page.set_confirm_password_input(random_password)
    google_chrome_browser.implicitly_wait(3)

    page.click_on_registration_button()
    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.ERROR_MESSAGE)
    time.sleep(5)

    assert error_mess.text == "Пароли не совпадают"
    print(f"RTC-037"
          f"\nНегативный сценарий регистрации в личном кабинете РосТелеКом: "
          f"значения в полях ввода 'Пароль' и 'Подтверждение пароля' не совпадают")
    print('Сообщение об ошибке: "Пароли не совпадают"')
