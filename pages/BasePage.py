from urllib.parse import urlparse

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.MainPageLocators import MainPageLocators
from settings import base_url


class BasePage:
    """Класс для реализует базовые функции для переиспользования в тестовых методах.

    Атрибуты
    --------
    name : driver
        экземпляр webdriver
    surname : timeout
        неявное ожидание, по умолчанию 5 секунд
        (приватная переменная __timeout используется для всех методов)
    """

    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.base_url = base_url
        self.__timeout = timeout
        self.driver.implicitly_wait(timeout)

    def open_site(self):
        """Открывает страницу Ростелеком в браузере"""
        return self.driver.get(self.base_url)

    def find_element(self, locator):
        """Ожидает, что элемент существует в DOM"""
        return WebDriverWait(self.driver, self.__timeout).until(EC.presence_of_element_located(locator),
                                                                message=f'Not find {locator}')

    def find_list_elements(self, locator):
        """Ожидает список элементов и возвращает его"""
        return WebDriverWait(self.driver, self.__timeout).until(EC.presence_of_all_elements_located(locator),
                                                                message=f'Not find {locator}')

    def should_have_menu_authorization(self):
        menu_authorization = self.find_element(*MainPageLocators.PAGE_AUTH)
        result = menu_authorization.text
        assert result == "Авторизация"

    def get_current_url(self):
        """Получает url адрес текущей страницы"""
        url = urlparse(self.driver.current_url)
        return url.path

    def find_element_until_to_be_clickable(self, locator):
        """Ожидает пока элемент не станет кликабельным"""
        return WebDriverWait(self.driver, self.__timeout).until(EC.element_to_be_clickable(locator),
                                                                message=f'Element not clickable!')
