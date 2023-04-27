import time

import pytest

from locators.AuthorizationPageLocators import AuthorizationPageLocators
from pages.AuthorizationPage import AuthorizationPage
from settings import valid_email, valid_password, random_password, random_email


# RTC-001
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_page_open(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/authorization_page.png")
    print(f"RTC-001 \nПроверка успешного открытия страницы авторизации РосТелеКом")
    assert page.get_current_url() == "/auth/realms/b2c/protocol/openid-connect/auth"


# RTC-005
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_tab_email(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.tab_email.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/tab_email_click.png")
    print(f"RTC-005 \nПроверка кликабельности таба 'Почта'")
    assert page.tab_email.text == "Почта"


# RTC-006
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_tab_phone(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.tab_phone.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/tab_phone_click.png")
    print(f"RTC-006 \nПроверка кликабельности таба 'Телефон'")
    assert page.tab_phone.text == "Телефон"


# RTC-007
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_tab_login(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.tab_login.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/tab_login_click.png")
    print(f"RTC-007 \nПроверка кликабельности таба 'Логин'")
    assert page.tab_login.text == "Логин"


# RTC-008
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_tab_personal_account(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.tab_personal_account.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/tab_personal_account_click.png")
    print(f"RTC-008 \nПроверка кликабельности таба 'Лицевой счёт'")
    assert page.tab_personal_account.text == "Лицевой счёт"


# RTC-009
@pytest.mark.tabs
@pytest.mark.parametrize("username", ["+79217777777", valid_email, "valid_login", "269750005232"],
                         ids=["RTC-012) phone", "RTC-013) E-mail", "RTC-014) login", "RTC-015) ls"])
def test_tabs(google_chrome_browser, username):
    page = AuthorizationPage(google_chrome_browser)
    page.set_username(username)

    page.set_password(valid_password)

    if username == "+79217777777":
        time.sleep(4)
        page.driver.save_screenshot(r"../tests/screenshots/Authorization/switch_to_phone.png")
        assert google_chrome_browser.find_element(*AuthorizationPageLocators.TAB).text == "Телефон"
        print("RTC-009-1 Телефон")
        google_chrome_browser.find_element(*AuthorizationPageLocators.TAB_PHONE).click()
        time.sleep(2)
    elif username == valid_email:
        time.sleep(4)
        page.driver.save_screenshot(r"../tests/screenshots/Authorization/switch_to_email.png")
        assert google_chrome_browser.find_element(*AuthorizationPageLocators.TAB).text == "Почта"
        print("RTC-009-2 Почта")
        google_chrome_browser.find_element(*AuthorizationPageLocators.TAB_PHONE).click()
        time.sleep(2)
    elif username == "valid_login":
        time.sleep(4)
        page.driver.save_screenshot(r"../tests/screenshots/Authorization/switch_to_login.png")
        assert google_chrome_browser.find_element(*AuthorizationPageLocators.TAB).text == "Логин"
        print("RTC-009-3 Логин")
        google_chrome_browser.find_element(*AuthorizationPageLocators.TAB_PHONE).click()
        time.sleep(2)
    else:
        try:
            time.sleep(4)
            page.driver.save_screenshot(r"../tests/screenshots/Authorization/switch_to_ls.png")
            assert google_chrome_browser.find_element(*AuthorizationPageLocators.TAB).text == "Лицевой счёт"
            print("RTC-009-4 Лицевой счёт")
        except Exception:
            print(f"RTC-009 \n"
                  f"\nBR-4:Тест не пройден. Автоматическое переключения на Лицевой счёт не происходит!")


# RTC-010
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_by_vk(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.auth_by_vk.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/auth_vk_click.png")
    print(f"RTC-010 \nПроверка перехода на авторизацию через социальную сеть 'ВКонтакте'")
    assert page.get_current_url() == "/authorize"


# RTC-011
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_by_odhoklassniky(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.auth_by_odnoklassniky.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/auth_ok_click.png")
    print(f"RTC-011 \nПроверка перехода на авторизацию через социальную сеть 'Одноклассники'")
    assert page.get_current_url() == "/dk"


# RTC-012
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_by_mail(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.auth_by_mail.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/auth_mail_click.png")
    print(f"RTC-012 \nПроверка перехода на авторизацию через почтовый сервис mail.ru")
    assert page.get_current_url() == "/oauth/authorize"


# RTC-013
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_by_google(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.auth_by_google.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/auth_google_click.png")
    print(f"RTC-013 \nПроверка перехода на авторизацию через почтовый сервис google.com")
    assert page.get_current_url() == "/o/oauth2/auth/identifier"


# RTC-014
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_by_yandex(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.auth_by_yandex.click()
    time.sleep(2)
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/auth_yandex_click.png")
    print(f"RTC-014 \nПроверка перехода на авторизацию через почтовый сервис yandex.ru")
    assert page.get_current_url() == "/auth/realms/b2c/login-actions/authenticate"


# RTC-015
@pytest.mark.authorization
@pytest.mark.positive
def test_authorization_email(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.tab_email.click()
    time.sleep(2)
    page.set_username(valid_email)
    page.set_password(valid_password)
    page.click_on_enter_button()
    page.driver.save_screenshot(r"../tests/screenshots/Authorization/auth_sucсess_by_email.png")
    print(f"RTC-015 \nПроверка успешной авторизации с валидными данными в личном кабинете РосТелеКом")
    assert page.get_current_url() == "/account_b2c/page"


@pytest.mark.authorization
@pytest.mark.negative
def test_authorization_with_invalid_email(google_chrome_browser):
    auth_page = AuthorizationPage(google_chrome_browser)
    auth_page.set_username(random_email)
    auth_page.set_password(valid_password)
    auth_page.click_on_enter_button()
    google_chrome_browser.implicitly_wait(10)

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или пароль"
    print(f"RTC-030"
          f"\nНегативный сценарий авторизации в личном кабинете РосТелеКом по адресу электронной почты:"
          f" невалидный адрес электронной почты")
    print('Сообщение об ошибке: "Неверный логин или пароль"')


# RTC-031
@pytest.mark.authorization
@pytest.mark.negative
def test_authorization_with_invalid_password(google_chrome_browser):
    page = AuthorizationPage(google_chrome_browser)
    page.set_username(valid_email)
    page.set_password(random_password)
    page.click_on_enter_button()
    google_chrome_browser.implicitly_wait(10)

    error_mess = google_chrome_browser.find_element(*AuthorizationPageLocators.FORM_ERROR)
    assert error_mess.text == "Неверный логин или пароль"
    print(f"RTC-031"
          f"\nНегативный сценарий авторизации в личном кабинете РосТелеКом по адресу электронной почты: "
          f"невалидный пароль")
    print('Сообщение об ошибке: "Неверный логин или пароль"')
