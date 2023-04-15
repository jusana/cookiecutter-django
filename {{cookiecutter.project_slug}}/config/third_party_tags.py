# permet d'ovverrider les "templateTags" (voire widgets) des applications tierces

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import Textarea
from django.utils import translation
from pages.models import Media
from pages.placeholders import PlaceholderNode, parse_placeholder

register = template.Library()

# Widget qui permet d'ajouter la fonction d'upload à CKEditor


class CKEditorUploaderPlaceholderNode(PlaceholderNode):
    def get_widget(self, page, language, fallback=Textarea):
        if "ckeditor" not in settings.INSTALLED_APPS:
            return fallback

        with_stmt = self.widget  # name of the widget as called in template like...
        # {% raw %}{% ckeditor_placeholder "welcome" with text_wysiwym_widget:default%}{% endraw %}
        splitted = with_stmt.split(":")

        if len(splitted) == 1:
            ck = CKEditorUploadingWidget(config_name="default")
        elif len(splitted) > 1:
            ck = CKEditorUploadingWidget(config_name=splitted[1])

        if not ck.config.get("language"):
            ck.config["language"] = translation.get_language()

        return ck


# tag qui permet d'ajouter la fonction d'upload à CKEditor
def do_ckeditorplaceholder(parser, token):
    name, params = parse_placeholder(parser, token)
    return CKEditorUploaderPlaceholderNode(name, **params)


register.tag("ckeditoruploader_placeholder", do_ckeditorplaceholder)


@register.simple_tag
def media_url_by_title(title):
    """
    retourne l'url d'un media (objet du modele Media) appelé par son titre
    """
    try:
        media = Media.objects.get(title=title)
        url = media.url.name
    except ObjectDoesNotExist:
        url = ""
    return f"{settings.MEDIA_URL}{url}"
