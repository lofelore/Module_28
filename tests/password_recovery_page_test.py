import time

import pytest

from locators.AuthorizationPageLocators import AuthorizationPageLocators
from locators.PasswordRecoveryPageLocators import PasswordRecoveryLocators
from pages.AuthorizationPage import AuthorizationPage
from pages.PasswordRecoveryPage import PasswordRecoveryPage
from settings import *
from utils.GenerateRandomEmail import GenerateRandomEmail


# RTC-021
@pytest.mark.password_recovery
@pytest.mark.positive
def test_password_recovery_page_open(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.forgot_password_button.click()
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/password_recovery_page.png")
    print(f"RTC-021 \nПроверка перехода на страницу восстановления пароля в личном кабинете РосТелеКом")
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/reset-credentials"


# RTC-023
@pytest.mark.password_recovery
@pytest.mark.positive
def test_password_recovery_tab_email(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.tab_email.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/tab_email_click.png")
    print(f"RTC-023 \nПроверка кликабельности таба 'Почта'")
    assert page.tab_email.text == "Почта"


# RTC-024
@pytest.mark.password_recovery
@pytest.mark.positive
def test_password_recovery_tab_phone(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.tab_phone.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/tab_phone_click.png")
    print(f"RTC-024 \nПроверка кликабельности таба 'Телефон'")
    assert page.tab_phone.text == "Телефон"


# RTC-025
@pytest.mark.password_recovery
@pytest.mark.positive
def test_password_recovery_tab_login(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.tab_login.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/tab_login_click.png")
    print(f"RTC-025 \nПроверка кликабельности таба 'Логин'")
    assert page.tab_login.text == "Логин"


# RTC-026
@pytest.mark.password_recovery
@pytest.mark.positive
def test_password_recovery_tab_personal_account(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.tab_personal_account.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/tab_personal_account_click.png")
    print(f"RTC-026 \nПроверка кликабельности таба 'Лицевой счёт'")
    assert page.tab_personal_account.text == "Лицевой счёт"


# RTC-027
def test_reload_captcha(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    google_chrome_browser.implicitly_wait(10)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/first_captcha.png")
    first_captcha = google_chrome_browser.find_element(*PasswordRecoveryLocators.NEW_PASS_IMAGE_CAPTCHA)
    page.btn_reload.click()
    time.sleep(5)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/new_captcha.png")
    new_captcha = google_chrome_browser.find_element(*PasswordRecoveryLocators.NEW_PASS_IMAGE_CAPTCHA)
    print(f"RTC-027 \nПроверка обновления каптчи на странице восстановления РосТелеКом")

    assert new_captcha != first_captcha


# RTC-028
def test_password_recovery_back_button(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.btn_come_back()
    print(f"RTC-028 \nПроверка кликабельности кнопки 'Вернуться назад'"
          f"на странице восстановления пароля РосТелеКом")
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/authenticate"


# RTC-029
@pytest.mark.password_recovery
@pytest.mark.positive
def test_password_recovery_by_email(google_chrome_browser):
    # Разделяем email на имя и домен для использования в последующих запросах:
    sign_at = valid_email.find("@")
    mail_name = valid_email[0:sign_at]
    mail_domain = valid_email[sign_at + 1:len(valid_email)]

    page = PasswordRecoveryPage(google_chrome_browser)
    page.enter_username(valid_email)
    time.sleep(50)  # время на ручной!! ввод символов с картинки
    page.btn_continue.click()

    # Ожидаем поступление письма с кодом восстановления на указанный адрес электронной почты:
    time.sleep(30)

    # Проверяем почтовый ящик на наличие писем и находим ID последнего письма:
    result_id, status_id = GenerateRandomEmail().get_id_letter(mail_name, mail_domain)
    id_letter = result_id[0].get("id")
    # Сверяем полученные данные с нашими ожиданиями
    assert status_id == 200, "status_id error"
    assert id_letter > 0, "id_letter > 0 error"

    # Получаем код восстановления из письма от РосТелеКом:
    result_code, status_code = GenerateRandomEmail().get_reg_code(mail_name, mail_domain, str(id_letter))

    text_body = result_code.get("body")
    # Извлекаем код из текста методом find:
    reg_code = text_body[text_body.find("Ваш код: ") + len("Ваш код: "):
                         text_body.find("Ваш код: ") + len("Ваш код: ") + 6]
    # Сверяем полученные данные с нашими ожиданиями
    assert status_code == 200, "status_code error"
    assert reg_code != '', "reg_code != [] error"

    reg_digit = [int(char) for char in reg_code]

    google_chrome_browser.implicitly_wait(50)
    for i in range(0, 6):
        google_chrome_browser.find_elements(*PasswordRecoveryLocators.NEW_PASS_ONETIME_CODE)[i].send_keys(reg_code[i])
        google_chrome_browser.implicitly_wait(5)
    # browser.implicitly_wait(30)
    time.sleep(10)
    new_pass = random_password
    google_chrome_browser.find_element(*PasswordRecoveryLocators.NEW_PASS_NEW_PASS).send_keys(new_pass)
    time.sleep(3)
    google_chrome_browser.find_element(*PasswordRecoveryLocators.NEW_PASS_NEW_PASS_CONFIRM).send_keys(new_pass)
    google_chrome_browser.find_element(*PasswordRecoveryLocators.NEW_PASS_BTN_SAVE).click()
    time.sleep(30)
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/password_recovery_by_email_success.png")
    print(f"RTC-029 \nПроверка восстановления пароля по эл.почте в личном кабинете РосТелеКом")

    assert page.get_current_url() == "/auth/realms/b2c/login-actions/authenticate"

    # В случае успешной смены пароля, перезаписываем его в файл settings:
    with open(r"../settings.py", "r", encoding="utf8") as file:
        lines = []
        for line in file.readlines():
            if "valid_password" in line:
                lines.append(f"valid_password = '{random_password}'\n")
            else:
                lines.append(line)
    with open(r"../settings.py", "w", encoding="utf8") as file:
        file.writelines(lines)


@pytest.mark.password_recovery
@pytest.mark.negative
def test_password_recovery_with_wrong_captcha(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.enter_username(valid_email)
    google_chrome_browser.implicitly_wait(10)
    time.sleep(30)  # вводим капчу ручками
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/password_recovery_by_wrong_captcha.png")
    page.btn_continue.click()

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или текст с картинки"
    print(f"RTC-038"
          f"\nНегативный сценарий восстановления пароля по адресу электронной почты: неверные символы с картинки")
    print('Сообщение об ошибке: "Неверный логин или текст с картинки"')


# RTC-039
@pytest.mark.password_recovery
@pytest.mark.negative
def test_password_recovery_with_wrong_email(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.enter_username(random_email)
    google_chrome_browser.implicitly_wait(10)
    time.sleep(30)  # вводим капчу ручками
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/password_recovery_by_wrong_email.png")
    page.btn_continue.click()

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или текст с картинки"
    print(f"RTC-039"
          f"\nНегативный сценарий восстановления пароля по адресу электронной почты: "
          f"невалидный адрес электронной почты")
    print('Сообщение об ошибке: "Неверный логин или текст с картинки"')


# RTC-040
@pytest.mark.password_recovery
@pytest.mark.negative
def test_password_recovery_with_wrong_phone(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.enter_username(invalid_phone)
    google_chrome_browser.implicitly_wait(10)
    time.sleep(30)  # вводим капчу ручками
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/password_recovery_by_wrong_phone.png")
    page.btn_continue.click()

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или текст с картинки"
    print(f"RTC-040"
          f"\nНегативный сценарий восстановления пароля по номеру телефона: "
          f"невалидный номер мобильного телефона")
    print('Сообщение об ошибке: "Неверный логин или текст с картинки"')


# RTC-041
@pytest.mark.password_recovery
@pytest.mark.negative
def test_password_recovery_with_wrong_login(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.enter_username(invalid_login)
    google_chrome_browser.implicitly_wait(10)
    time.sleep(30)  # вводим капчу ручками
    page.driver.save_screenshot(r"../tests/screenshots/Password_recovery/password_recovery_by_wrong_login.png")
    page.btn_continue.click()

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или текст с картинки"
    print(f"RTC-041"
          f"\nНегативный сценарий восстановления пароля по логину: "
          f"невалдиный логин")
    print('Сообщение об ошибке: "Неверный логин или текст с картинки"')


# RTC-042
@pytest.mark.password_recovery
@pytest.mark.negative
def test_password_recovery_with_wrong_personal_account(google_chrome_browser):
    page = PasswordRecoveryPage(google_chrome_browser)
    page.tab_personal_account.click()
    google_chrome_browser.implicitly_wait(2)
    page.enter_username(invalid_ls)
    google_chrome_browser.implicitly_wait(10)
    time.sleep(30)  # вводим капчу ручками
    page.driver.save_screenshot(
        r"../tests/screenshots/Password_recovery/password_recovery_by_wrong_personal_account.png")
    page.btn_continue.click()

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или текст с картинки"
    print(f"RTC-042"
          f"\nНегативный сценарий восстановления пароля по номеру лицевого счёта: "
          f"невалидный лицевой счёт")
    print('Сообщение об ошибке: "Неверный логин или текст с картинки"')
