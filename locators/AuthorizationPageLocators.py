from selenium.webdriver.common.by import By


class AuthorizationPageLocators:
    TAB_EMAIL = (By.ID, "t-btn-tab-mail")
    FIELD_USERNAME = (By.ID, "username")
    FIELD_PASS = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "kc-login")
    REGISTER_BUTTON = (By.ID, "kc-register")
    FORGOT_PASSWORD_BUTTON = (By.ID, "forgot_password")
    ERROR_MESSAGE = (By.CLASS_NAME, "rt-input-container__meta--error")
    FORM_ERROR = (By.ID, "form-error-message")
    TAB_PHONE = (By.ID, "t-btn-tab-phone")
    TAB_PERSONAL_ACCOUNT = (By.ID, "t-btn-tab-ls")
    TAB_LOGIN = (By.ID, "t-btn-tab-login")
    AUTH_BY_VK = (By.ID, "oidc_vk")
    AUTH_BY_OK = (By.ID, "oidc_ok")
    AUTH_BY_MAIL = (By.ID, "oidc_mail")
    AUTH_BY_GOOGLE = (By.ID, "oidc_google")
    AUTH_BY_YANDEX = (By.ID, "oidc_ya")
    TAB = (By.CSS_SELECTOR, ".rt-tab.rt-tab--small.rt-tab--active")
