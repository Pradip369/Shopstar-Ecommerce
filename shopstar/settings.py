import django_heroku
import os
import dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =================================== SECRET_KEY ====================================
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = (os.environ['DEBUG'] == 'True')

ALLOWED_HOSTS = ['https://shopstarofficial.herokuapp.com/','127.0.0.1']

# ================================== Builtin Installed App ================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #For media file storing
    'cloudinary_storage',
    'cloudinary',

]

# =================================== Internal Install Apps ================================
INSTALLED_APPS += [
    'user_registration',
    'registration',
    'email_change',
    'order_detail',
    'product.apps.ProductConfig',
    'user_detail',
    'website_detail',
]


# =================================== External Install Apps ================================
INSTALLED_APPS += [
    'django.contrib.sites',
    'import_export',
    'crispy_forms',  
    'django_social_share', 
    'ckeditor', 
    'captcha',
    'google_translate',
    'admin_honeypot',
    'honeypot_signals',
    'admin_reorder',
    'django_countries',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # Whitenoise for static file
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #Admin Reorder
    'admin_reorder.middleware.ModelAdminReorder',    
]

ROOT_URLCONF = 'shopstar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # django_social_share
                'django.template.context_processors.request',
                
                # Global context use
                "shopstar.context_processors.categories",
                "shopstar.context_processors.cartitems",
            ],
        },
    },
]

WSGI_APPLICATION = 'shopstar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ====================================== Security ===========================================
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CSRF_USE_SESSIONS = True

# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF=True
# SECURE_SSL_REDIRECT = True

# SECURE_BROWSER_XSS_FILTER = True

# =============================== Authentication Backend ================================
AUTHENTICATION_BACKENDS = (
    
    'shopstar.views.UsernameOrEmailBackend',
    
    'django.contrib.auth.backends.ModelBackend',
)


# ================================== Email sending setting ===============================
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ACCOUNT_ACTIVATION_DAYS = 1


# ================================ Admin honeypot_signals =================================
MANAGERS = (
    ('Pradip', 'kpuniverse369@gmail.com',),
)
SUPPORT_EMAIL = EMAIL_HOST_USER


# ==================================== Email change time limit =========================
EMAIL_CHANGE_VERIFICATION_DAYS = 1


# ====================================== Redirect Urls Setting =============================
LOGIN_URL = '/user/accounts/login/'
LOGIN_REDIRECT_URL='/'
REGISTRATION_AUTO_LOGIN = True


# ======================================== Crispy Form ==================================
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# ===================================== Site Id(django.contrib.sites) =============================
SITE_ID = 1


# ====================================== Static File Setting =============================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'staticfiles'),
# )


# ================================== CLOUDINARY SETTINGS ======================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUD_NAME'],
    'API_KEY': os.environ['API_KEY'],
    'API_SECRET': os.environ['API_SECRET'],
    'SECURE': True,
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr','png', 'gif', 'webp']
}


# ===================================== Media File Setting ============================
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ====================================== Ck Editor setting =============================
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Strike', 'Subscript', 'Superscript', '-','Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink','Find', 'Replace', '-', 'SelectAll'],
            ['RemoveFormat', 'Source','-','Styles', 'Format', 'Font', 'FontSize','TextColor', 'BGColor']
        ]
    }
}


# ==================================== CashFree Setting ===============================
appId_cashfree = os.environ['appId_cashfree']
secret_cashfree = os.environ['secret_cashfree']
CASHFREE_MOD = os.environ['CASHFREE_MOD']
CURRENCY = os.environ['CURRENCY']

# ====================================== Delivery charges ==============================
INDIA_DELIVERY = os.environ['INDIA_DELIVERY']
FOREIGN_DELIVERY = os.environ['FOREIGN_DELIVERY']

# ================================= Recaptcha Setting ==================================
RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

# ==================================== Model Reorder ====================================
ADMIN_REORDER = (
    # Keep original label and models
    {
     'app': 'auth', 
     'label': 'Groups and Registered Users',
    },
    {
     'app': 'user_detail', 
     'label': 'User Profile and Shipping Info.',
    },
    'product',
    'order_detail',
    'email_change',
    'registration',
    'admin_honeypot',
    'sites',
    'website_detail',
)

# ================================= WhiteNoice Setting =====================================
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ================================== Heroku Setting =====================================
# django_heroku.settings(locals())