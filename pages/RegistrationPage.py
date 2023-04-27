import time

from locators.RegistrationPageLocators import RegistrationLocators
from pages.BasePage import BasePage


class RegistrationPage(BasePage):
    """Страница регистрации с web-элементами"""

    def __init__(self, driver):
        super().__init__(driver)
        self.first_name = driver.find_element(*RegistrationLocators.REG_FIELD_FIRSTNAME)
        self.last_name = driver.find_element(*RegistrationLocators.REG_FIELD_LASTNAME)
        self.region = driver.find_element(*RegistrationLocators.REGION)
        self.email = driver.find_element(*RegistrationLocators.REG_FIELD_EMAIL)
        self.password = driver.find_element(*RegistrationLocators.REG_FIELD_PASS)
        self.pass_conf = driver.find_element(*RegistrationLocators.REG_FIELD_PASS_CONFIRM)
        self.btn = driver.find_element(*RegistrationLocators.REG_BUTTON_SUBMIT)

    def set_firstname_input(self, value):
        """Вводит имя пользователя в поле firstname"""
        self.first_name.send_keys(value)

    def set_lastname_input(self, value):
        """Вводит фамилию пользователя в поле lastname"""
        self.last_name.send_keys(value)

    def set_region_input(self, value):
        """Вводит регион в поле region"""
        self.region.send_keys(value)

    def set_email_input(self, value):
        """Вводит адрес электронной почты в поле email"""
        self.email.send_keys(value)

    def set_password_input(self, value):
        """Вводит пароль в поле password"""
        self.password.send_keys(value)

    def set_confirm_password_input(self, value):
        """Вводит пароль в поле confirm password"""
        self.pass_conf.send_keys(value)

    def click_on_registration_button(self):
        """Нажимает на кнопку 'Зарегистрироваться'"""
        self.btn.click()

    def fill_registration_form(self, firstname, lastname, region, email, password, password_confirm):
        self.set_firstname_input(firstname)
        self.set_lastname_input(lastname)
        self.set_region_input(region)
        self.set_email_input(email)
        self.set_password_input(password)
        self.set_confirm_password_input(password_confirm)
        time.sleep(30)
        self.click_on_registration_button()
