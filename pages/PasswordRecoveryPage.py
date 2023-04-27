from locators.PasswordRecoveryPageLocators import PasswordRecoveryLocators
from pages.BasePage import BasePage


class PasswordRecoveryPage(BasePage):
    """Страница восстановления пароля с web-элементами"""

    def __init__(self, driver):
        super().__init__(driver)
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials'
        driver.get(url)
        self.tab_email = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_TAB_EMAIL)
        self.tab_phone = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_TAB_PHONE)
        self.tab_login = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_TAB_LOGIN)
        self.tab_personal_account = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_TAB_LS)
        self.username = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_FIELD_USERNAME)
        self.btn_continue = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_BUTTON_CONTINUE)
        self.btn_reload = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_RELOAD_CAPTCHA)
        self.come_back = driver.find_element(*PasswordRecoveryLocators.NEW_PASS_BUTTON_BACK)

    def tab_email(self):
        """Выбирает восстановление пароля по 'Почта'"""
        self.tab_email()

    def tab_phone(self):
        """Выбирает тип восстановления пароля 'Телефон'"""
        self.tab_phone()

    def tab_login(self):
        """Выбирает тип восстановления пароля 'Логин'"""
        self.tab_login()

    def tab_ls(self):
        """Выбирает тип восстановления пароля 'Лицевой счёт'"""
        self.tab_personal_account()

    def enter_username(self, value):
        """Вводит адрес электронной почты в поле ввода"""
        self.username.send_keys(value)

    def btn_continue(self):
        """Нажимает на кнопку 'Продолжить'"""
        self.btn_continue()

    def btn_reload(self):
        """Нажимает на кнопку обновления изображения символов"""
        self.btn_reload()

    def btn_come_back(self):
        """Нажимает на кнопку 'Вернуться назад'"""
        self.come_back.click()
