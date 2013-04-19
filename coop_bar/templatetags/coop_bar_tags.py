# -*- coding: utf-8 -*-

from django import template
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.template import Context
register = template.Library()
from coop_bar.bar import CoopBar
from django.conf import settings
STATIC_URL = getattr(settings, 'STATIC_URL', '')
from coop_bar import settings as bar_settings
from logging import getLogger


class CoopBarNode(template.Node):
    def render(self, context):
        request = context.get("request", None)
        commands = CoopBar().get_commands(request, context)
        if commands:  # hide admin-bar if nothing to display
            t = get_template("coop_bar.html")
            return t.render(Context({'commands': commands}))
        return u''


@register.tag
def coop_bar(parser, token):
    return CoopBarNode()


class CoopBarHeaderNode(template.Node):
    def render(self, context):
        request = context.get("request", None)
        headers = [u'<link rel="stylesheet" href="%scss/coop_bar.css" type="text/css" />' % STATIC_URL]
        headers += [u'<script type="text/javascript" src="%sjs/jquery-ui-1.8.14.custom.min.js"></script>' % STATIC_URL]
        # ajout des librairies nécessaires à colorbox
        headers += [u'<script type="text/javascript" charset="utf-8" src="%sjs/jquery.colorbox-min.js"></script>' % STATIC_URL]
        headers += [u'<script type="text/javascript" charset="utf-8" src="%sjs/jquery.form.js"></script>' % STATIC_URL]
        headers += [u'<script type="text/javascript" src="%sjs/colorbox.coop.js"></script>' % STATIC_URL]
        headers += [u'<script type="text/javascript" src="%sjs/jquery.pageslide.js"></script>' % STATIC_URL]
        headers += [u'<link rel="stylesheet" href="%scss/colorbox.css" type="text/css" />' % STATIC_URL]
        if 'messages' in context:
            headers += [u'<script type="text/javascript" src="%sjs/jquery.humanmsg.js"></script>' % STATIC_URL]
            headers += [u'<script type="text/javascript" src="%sjs/jquery.easing.1.3.js"></script>' % STATIC_URL]
        headers += CoopBar().get_headers(request, context)
        return "\n".join(headers)


@register.tag
def coop_bar_headers(parser, token):
    return CoopBarHeaderNode()


class CoopBarFooterNode(template.Node):
    def render(self, context):
        request = context.get("request", None)
        footer = [u'''
<script type="text/javascript">
$(document).ready(function(){
        ''']
        footer += [u'''
    $("#coop-bar").draggable();
    $("a.colorbox-form").colorboxify({
        close_popup_and_media_slide: function() {
            $.colorbox.close();
            $("#coopbar_medialibrary").click();
        }
    });
        ''']

        # messages framework display

        logger = getLogger('default')
        from django.contrib import messages
        msg_list = messages.get_messages(request)

        if msg_list:
            from django.template.defaultfilters import escapejs
            for m in msg_list:
                logger.debug(unicode(m))
                footer += [u'''
    humanMsg.displayMsg("''' + escapejs(unicode(m)) + u'''", "''' + unicode(m.tags) + u'''");
                ''']
            if len(msg_list) > 1 or bar_settings.DISPLAY_MESSAGES_LOG:
                footer += [u'''
    $("#humanMsgLog p").show();
                ''']

        footer += CoopBar().get_footer(request, context)  # TODO profiler cette méthode (cache ?)
        footer += [u'''
});
</script>''']
        return "\n".join(footer)


@register.tag
def coop_bar_footer(parser, token):
    return CoopBarFooterNode()
