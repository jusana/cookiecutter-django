# permet d'ovverrider les "templateTags" (voire widgets) des applications tierces

from django import template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import Textarea
from django.utils import translation
from django_ckeditor_5.widgets import CKEditor5Widget
from pages.models import Media
from pages.placeholders import PlaceholderNode, parse_placeholder

register = template.Library()

# Widget qui permet d'ajouter ckeditor5

class CKEditor5PlaceholderNode(PlaceholderNode):
    def get_widget(self, page, language, fallback=Textarea):
        if "django_ckeditor_5" not in settings.INSTALLED_APPS:
            return fallback

        with_stmt = self.widget  # name of the widget as called in template like...
        # {% raw %}{% ckeditor_placeholder "welcome" with text_wysiwym_widget:default%}{% endraw %}
        splitted = with_stmt.split(":")

        if len(splitted) == 1:
            ck = CKEditor5Widget(config_name="default")
        elif len(splitted) > 1:
            ck = CKEditor5Widget(config_name=splitted[1])

        if not ck.config.get("language"):
            ck.config["language"] = translation.get_language()

        return ck


# tag qui permet d'ajouter la fonction CKEditor5
def do_ckeditor5placeholder(parser, token):
    name, params = parse_placeholder(parser, token)
    return CKEditor5PlaceholderNode(name, **params)


register.tag("ckeditor5_placeholder", do_ckeditor5placeholder)


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
