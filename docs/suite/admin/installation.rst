Installing Modules
==================

In general there are two ways to install modules for Constellation.
Modules are either installed using the Python pip system, or are
installed by manually downloading wheels and then loading those wheels
manually with pip.  Downloading and expanding tarballs is expressly
not supported for production use.


The Easy Way
------------

To install from pip, install the desired application package.  The
Constellation packages are only available for Python3 at this time.
Most packages within the suite will take the format of
:code:`Constellation-<module name>` where the :code:`<module name>`
will be a single word identifying the module.  For example,
Constellation Vote is contained by the :code:`Constellation-Vote`
package.

Many modules have additional dependencies, if you do not have these
dependencies installed, they will be installed alongside the
Constellation Module currently being installed.  To prevent package
name collisions between Python 2 and Python 3, as well as to avoid
polluting the global :code:`$PYTHONPATH`, we recommend using
VirtualEnv_.

.. _VirtualEnv: https://virtualenv.pypa.io/en/stable/


The Slightly Difficult Way
--------------------------

If you cannot use pip in an online mode, but still have the tools
available to you (i.e. you have a firewall that does not permit
connections to pypi.python.org) then you can manually download the
wheels and install them by hand.

To install the wheels, use :code:`pip install <wheel>`.  After you
have installed all the necessary wheels, you can enable the modules as
though they had been installed by pip.


The Hard Way
------------

If there is a compelling reason to not use Python pip it is possible
to download the distribution tarballs from GitHub and decompress them
manually.  This installation mechanism is beyond the scope of this
document and is fully unsupported by the Constellation Developers,
however a similar method is used as part of the development process.



Enabling the Module
===================

Once you have installed your module by one of the three mechanisms
above, it is necessary to enable it in your Django installation.  To
do so add :code:`constellation_<modulename>` to your
:code:`INSTALLED_APPS` variable in your config file.  Many
applications within the suite also require Django-Guardian to function
correctly, this requires you to add :code:`guardian` to your
:code:`INSTALLED_APPS` as well.  All apps within the suite expect the
Constellation-Base module to be loaded.

The section should look something like this:

.. code-block:: python

   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'guardian',
       'constellation_base',
       'constellation_<modulename>',
   ]


Additionally, many apps will need you to add the Guardian back-end to
the :code:`AUTHENTICATION_BACKENDS` section of your configuration
file.  The section should look like this:

.. code-block:: python

   AUTHENTICATION_BACKENDS = (
       'django.contrib.auth.backends.ModelBackend',  # this is default
       'guardian.backends.ObjectPermissionBackend',
   )


Once you've enabled the module in your settings file, the last thing
to do is to mount the module's routes to a URL within your Django
installation.  The is covered in detail in the Django documentation,
but the minimum lines necessary in your root :code:`urls.py` file are
as follows:

.. code-block:: python

   from django.conf import settings
   from django.conf.urls import url, include
   from django.conf.urls.static import static
   from django.contrib import admin

   urlpatterns = [
       url(r'^admin/', admin.site.urls),
       url(r'', include('constellation_base.urls')),
       url(r'<route name>/', include('constellation_<modulename>.urls')),
   ]

While it is technically possible to put anything in the :code:`<route
name>` field, we recommend putting the application's name in this
field for consistency.
