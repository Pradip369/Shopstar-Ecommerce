from django.conf import settings


EMAIL_CHANGE_VERIFICATION_DAYS = getattr(settings, 'EMAIL_CHANGE_VERIFICATION_DAYS', 7)

SITE_URL = settings.SITE_URL