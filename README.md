django-openauth
=============

**Still being worked on.**

Requirements
-------

OpenID

* [python-openid 2.2.5](http://pypi.python.org/pypi/python-openid/)


Installation
-----------

Currently not on Pypi.  Install using whichever method workss with Github.


Setup
-----------

1. Add 'openauth.openid' to INSTALLED_APPS
2. Syncdb
3. Add openauth.openid.views.LoginView and openauth.openid.views.AuthenticationView to urlconf
4. Take a look at example.views for a rough setup
