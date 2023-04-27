from selenium.webdriver.common.by import By


class PasswordRecoveryLocators:
    """Локаторы страницы восстановления пароля"""
    NEW_PASS_TAB_EMAIL = (By.ID, "t-btn-tab-mail")
    NEW_PASS_TAB_PHONE = (By.ID, "t-btn-tab-phone")
    NEW_PASS_TAB_LOGIN = (By.ID, "t-btn-tab-login")
    NEW_PASS_TAB_LS = (By.ID, "t-btn-tab-ls")
    NEW_PASS_FIELD_USERNAME = (By.ID, "username")
    NEW_PASS_BUTTON_CONTINUE = (By.ID, "reset")
    NEW_PASS_ONETIME_CODE = (By.CSS_SELECTOR, "input[inputmode='numeric']")
    NEW_PASS_NEW_PASS = (By.ID, "password-new")
    NEW_PASS_NEW_PASS_CONFIRM = (By.ID, "password-confirm")
    NEW_PASS_BTN_SAVE = (By.CSS_SELECTOR, "button[id='t-btn-reset-pass']")
    NEW_PASS_MESSAGE_ERROR = (By.ID, "form-error-message")
    NEW_PASS_MESSAGE_ERROR_EMAIL = (By.CLASS_NAME, "rt_input-container__meta--error")
    NEW_PASS_IMAGE_CAPTCHA = (By.CLASS_NAME, "rt-captcha__image")
    NEW_PASS_RELOAD_CAPTCHA = (By.CLASS_NAME, "rt-captcha__reload")
    NEW_PASS_BUTTON_BACK = (By.ID, "reset-back")
