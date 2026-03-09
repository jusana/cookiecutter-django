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
