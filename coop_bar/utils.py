# -*- coding: utf-8 -*-

from django.conf import settings

def make_link(url, label, icon, id=None, classes=None):
    icon_url = settings.STATIC_URL+icon
    
    extra_args = [u'id="{0}"'.format(id)] if id else []
    if classes:
        extra_args += [u'class="{0}"'.format(u' '.join(classes))]
        
    return u'<a href="{url}" style="background-image:url({icon_url})"{args}>{label}</a>'.format(
        url=url, icon_url=icon_url, args=u' '.join(extra_args), label=label
    )

