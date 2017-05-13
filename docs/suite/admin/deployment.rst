Deployment Suggestions
======================

Constellation is a Django application, and as such can be deployed as
a uWSGI executable.  This is documented in depth in the `Django
Deployment Manual
<https://docs.djangoproject.com/en/1.11/topics/install/>`_.

This document contains some suggestions for how to reliably deploy
Constellation in your environment and why we diverge from suggestions
made by the Django documentation at times.


Databases
---------

We highly recommend you use the PostgreSQL database.  It is a high
performance, high quality database engine.  Unlike MySQL, PostgreSQL
is completely free with no "optional" modules that turn out to be
completely necessary for a performant install.  If you plan to use the
Constellation Forms module, you must use PostgreSQL since there are
certain database specific types that are only available with
PostgreSQL.

It is also worth pointing out that the Constellation Developer team
and the Constellation Release team perform all QA tasks with
PostgreSQL databases.


Python Runtime
--------------

The Constellation platform runs on Python 3 and would in theory run
on any specification-compliant Python interpreter.  That being said,
there are components of Constellation that require the 'Pillow'
package and this does not work on Jython.  Unless you have a specific
reason to do so, we highly recommend using the CPython interpreter
(its the standard one!) and not trying anything too exotic with your
production installation.


Sample Configuration Files
--------------------------

As Django can be annoyingly complex to setup, here are some complete
sample files with sensitive content redacted.  These files come from a
site that uses LDAP for user authentication.


settings.py
^^^^^^^^^^^

.. code-block:: python

    import os
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = '<secret_key>'

    ALLOWED_HOSTS = ["constellation.MySite.com"]

    LOGIN_URL='/login'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'guardian',
        'constellation_base',
        'constellation_orderboard',
        'constellation_devicemanager',
        'constellation_vote',
        'constellation_forms',
        'constellation_ticketbox',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'constellation.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'constellation.wsgi.application'

    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'constellation_db',
            'USER': 'constellation_dbuser',
            'PASSWORD': '<constellation_db_passwd>',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

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
    TIME_ZONE = 'America/Chicago'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    STATIC_ROOT = '/opt/constellation/static_root/'
    MEDIA_ROOT = '/opt/constellation/media_root/'


    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
        'guardian.backends.ObjectPermissionBackend',
    )

    AUTH_LDAP_SERVER_URI = "ldap://ldap.MySite.com"
    AUTH_LDAP_BIND_DN = ""
    AUTH_LDAP_BIND_PASSWORD = ""
    AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=People,dc=MySite,dc=com"

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        "ou=Group,dc=MySite,dc=com",
        ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
    )

    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_staff": ["cn=Webmasters,ou=Group,dc=MySite,dc=com",
                     "cn=Administrators,ou=Group,dc=MySite,dc=com"],
    }
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
    }

    AUTH_LDAP_MIRROR_GROUPS = True


urls.py
^^^^^^^
.. code-block:: python

    from django.conf import settings
    from django.conf.urls import url, include
    from django.conf.urls.static import static
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'', include('constellation_base.urls')),
        url(r'orderboard/', include('constellation_orderboard.urls')),
        url(r'devices/', include('constellation_devicemanager.urls')),
        url(r'vote/', include('constellation_vote.urls')),
        url(r'ticketbox/', include('constellation_ticketbox.urls')),
        url(r'forms/', include('constellation_forms.urls')),
    ]

wsgi.py
^^^^^^^
.. code-block:: python

    import os
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "constellation.settings")
    application = get_wsgi_application()


uwsgi.ini (uWSGI configuration file)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: ini

    [uwsgi]
    chdir=/opt/constellation
    module=constellation.wsgi:application
    master=True
    vacuum=True
    max-requests=5000
    socket=/tmp/constellation.sock
    chmod-socket=660
    chown-socket=constellation:nginx
    plugin=python3
    virtualenv=venv


constellation.conf (nginx configuration file)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This site uses nginx to to serve the static content and to perform the operations associated with SSL.  SSL certificates are provided by LetsEncrypt_ and managed with Acmetool_.

.. _LetsEncrypt: https://letsencrypt.org 
.. _Acmetool: https://github.com/hlandau/acme

.. code-block:: nginx

    server {
        listen 80;
        server_name constellation.MySite.com;

        location /.well-known/acme-challenge/ {
            alias /var/run/acme/acme-challenge/;
        }

        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443;
        server_name constellation.MySite.com;

        ssl on;

        # certs sent to the client in SERVER HELLO are concatenated in ssl_certificate
        ssl_certificate /var/lib/acme/live/constellation.MySite.com/fullchain;
        ssl_certificate_key /var/lib/acme/live/constellation.MySite.com/privkey;
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;


        # modern configuration. tweak to your needs.
        ssl_protocols TLSv1.2;
        ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256';
        ssl_prefer_server_ciphers on;

        # OCSP Stapling ---
        # fetch OCSP records from URL in ssl_certificate and cache them
        ssl_stapling on;
        ssl_stapling_verify on;

        ## verify chain of trust of OCSP response using Root CA and Intermediate certs
        ssl_trusted_certificate /etc/ssl/certs.pem;

        resolver 8.8.8.8;


        client_max_body_size 10M;

        location /.well-known/acme-challenge/ {
            alias /var/run/acme/acme-challenge/;
        }

        location / {
            include /etc/nginx/uwsgi_params;
            uwsgi_pass unix:/tmp/constellation.sock;
        }

        location /media {
            alias /opt/constellation/media_root;
        }

        location /static {
            alias /opt/constellation/static_root;
        }
    }
