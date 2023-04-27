from selenium.webdriver.common.by import By


class RegistrationLocators:
    """Локаторы страницы регистрации"""
    REG_FIELD_FIRSTNAME = (By.CSS_SELECTOR, "input[name='firstName']")
    REG_FIELD_LASTNAME = (By.CSS_SELECTOR, "input[name='lastName']")
    REG_FIELD_EMAIL = (By.ID, "address")
    REG_FIELD_PASS = (By.ID, "password")
    REG_FIELD_PASS_CONFIRM = (By.CSS_SELECTOR, "input[id='password-confirm']")
    REG_BUTTON_SUBMIT = (By.CSS_SELECTOR, "button[type='submit'")
    REG_CARD_MODAL = (By.CLASS_NAME, "card-modal__title")
    REGION = (By.CSS_SELECTOR, "input.rt-input__input")
