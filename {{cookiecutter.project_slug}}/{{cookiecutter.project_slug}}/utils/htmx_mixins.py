# https://github.com/adamchainz/django-htmx/issues/117
# voir potentiellement : https://htmx.org/essays/template-fragments/
# voir potentiellement : https://github.com/clokep/django-render-block

from django.http import HttpResponseRedirect

from .form_mixins import FormSuccessMessageMixin


class HtmxPartialTemplateMixin:
    # success_url = "."

    @property
    def base_template(self) -> str:
        # raise NotImplemented
        return "base.html"

    @property
    def htmx_partial(self) -> str:
        # raise NotImplemented
        return "htmx/partial_main_content.html"

    # @property
    # def template_name(self) -> str:
    #     return self.htmx_partial if self.request.htmx else self.htmx_template # noqa

    @property
    def extra_context(self) -> dict:
        """
        On ajoute un extra context qui contient la variable de du template à "extends"  (eg base.html ou partial.html)
        """
        return (
            {"base_extends": self.htmx_partial}
            if self.request.htmx
            else {"base_extends": self.base_template}
        )  # noqa

class PartialTemplateMixin:
    """Alternative plus simple que HtmxPartialTemplateMixin s'appuyant sur "partialdef" de django 6
    Mixin pour retourner une partial template ciblant un fragment HTML spécifique (ex: photo_list.html#photo-cards)
    en cas de requête HTMX, et le template complet sinon.
    On peut ensuite faire hériter nos vues de ce mixin et définir la variable "partial_name"
    pour indiquer le fragment ciblé.
    """

    partial_name = None

    def get_template_names(self):
        template = super().get_template_names()[0]

        if self.request.htmx and self.partial_name:
            return [f"{template}#{self.partial_name}"]

        return [template]


class HtmxFormSuccessMessageMixin(FormSuccessMessageMixin):
    """
    Adds a success message on successful form htmx (hx-post) submission
    Un form en success renvoie une redirection (HttpResponseRedirect) par défaut après form_valid()
    Or htmx ne suit pas les redirections, sauf en ajoutant les bons headers http, on ajoute donc ce header (hx-redirect)
     https://htmx.org/docs/#response-headers
     https://github.com/adamchainz/django-htmx/issues/91
     https://github.com/adamchainz/django-htmx/issues/152
    """

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form, **kwargs)
        if self.request.htmx and isinstance(response, HttpResponseRedirect):
            # Set the HX-Redirect to the current location to imitate a reload
            response["HX-Redirect"] = response["Location"]
            # htmx only accepts 200's
            # response.status_code = 200
            # htmx accepts 204's (no-content ce qui evite le swap)
            response.status_code = 204

        return response
