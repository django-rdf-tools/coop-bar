Configurable toolbar
===============================================


Quick Start, Docs, Contributing
-------------------------------

* `What is coop_bar good for?`_
* `Quickstart`_

.. _What is coop_bar good for?: #good-for
.. _Quick start?: #quick-start

.. _good-for:

What is coop_bar good for?
------------------------------------
django-coop is a set of several apps for building cooperative websites. It is based on Django.

Thses apps may need a to display an admin toolbar. For example, the CMS component may use this bar
to display edit, cancel and save links.

coop_bar tries to provide a simple and configurable mechanism

.. _quick-start:

Quick start
------------------------------------
in settings.py, add coop_bar to the INSTALLED_APPS and os.path.abspath(PROJECT_PATH+'/coop_bar/static/') to the STATICFILES_DIRS

in urls.py add (r'^coop_bar/', include('coop_bar.urls')) to the urlpatterns

in each app that needs to access coop_bar, create a coop_bar_cfg.py file
In this file, add a load_commands function as follow
    ...
    from django.core.urlresolvers import reverse
    from django.utils.translation import ugettext as _

    def django_admin_command(request, context):
        if request.user.is_staff:
            return u'<a href="{0}">{1}</a>'.format(reverse("admin:index"), _('Admin'))

    def load_commands(coop_bar):
        coop_bar.register_command(django_admin_command)
    ...

In load_commands, you can register as much callback as you want. A callback (django_admin_command in previous example)
is just a function with request and context as args. It returns some html code to display in the bar or None.

In your base.html, add the following template tags
    ...
    {% load coop_bar_tags %}
    <html>
    <head>
        ...
        {% coop_bar_headers %}
    </head>
    <body>
        ...
        {% coop_bar %}
    </body>
    ...
License
=======

coop_bar uses the same license as Django (BSD-like).
