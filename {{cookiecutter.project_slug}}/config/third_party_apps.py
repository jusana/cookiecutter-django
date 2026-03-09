from cookie_consent.apps import CookieConsentConf


# conf dédiée pour gérer la compatibilité default_auto_field
# AutoField vs BigAutofield
# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
class CookieConsentConf(CookieConsentConf):
    default_auto_field = "django.db.models.AutoField"
    name = "cookie_consent"
