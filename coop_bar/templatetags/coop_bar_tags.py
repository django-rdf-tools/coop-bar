# -*- coding: utf-8 -*-

from django import template
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.template import Context
register = template.Library()
from coop_bar.bar import CoopBar
from django.conf import settings
STATIC_URL = getattr(settings, 'STATIC_URL', '')


from logging import getLogger
logger = getLogger('coop')


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
            headers += [u'<script type="text/javascript" src="%sjs/humanmsg.js"></script>' % STATIC_URL]
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
    })
        ''']

        for param in ('editable', 'form', 'edit_mode', ):
            if param in context:
                logger.debug( param + ' ? ' + str(context[param]))

        # --------- this block only added in edit_mode



        if 'edit_mode' in context and context['edit_mode']:
            footer += [u'''
    $("#coop-bar a.slide").pageSlide({width:'350px', direction:'right'});
    var toggle_save = function() {
        if (!$(".show-dirty").is(":visible")) {
            $(".show-clean").hide();
            $(".show-dirty").show();
            $("a.alert_on_click").bind('click', function(event) {
                return confirm("''' + _(u'Your modifications are not saved and will be lost. Continue?') + u'''");
            });
        };
            ''']
            if 'draft' in context:
                footer += [u'''
        $(".publish").hide();
                ''']
            footer += [u'''
    }
    $(".show-dirty").hide();
    Aloha.bind('aloha-editable-deactivated', function(event, eventProperties){
        toggle_save();
    });
    $(".djaloha-editable").keypress(function() {
        toggle_save();
    });

    $("a.update-logo img").change(toggle_save);
    $(".article select").change(toggle_save);
    $(".article input").change(toggle_save);

    //move the form submit to the coop_bar
    $("form#cms_form input[type='submit']").hide();
    $('#coopbar_save').click(function(event) {
        $("form#cms_form").submit();
        event.preventDefault();
    });
            ''']
        # -------- end of "if edit_mode"

        if 'messages' in context:
            for m in context['messages']:
                # TODO on utilise pas m.tags,
                footer += [u'''
    humanMsg.displayMsg("''' + unicode(m) + u'''");
            ''']
        footer += [u'''
});
</script>
        ''']

        footer += CoopBar().get_footer(request, context)
        return "\n".join(footer)


@register.tag
def coop_bar_footer(parser, token):
    return CoopBarFooterNode()
