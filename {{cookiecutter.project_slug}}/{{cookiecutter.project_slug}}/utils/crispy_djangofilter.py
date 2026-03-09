from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django_filters import FilterSet


class CrispyFilterSet(FilterSet):
    """
    permet d'ajouter le formHelper/Layout de crispy aux forms issu de django-filter
    https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
    https://github.com/carltongibson/django-filter/issues/1220
    """

    @property
    def form(self):
        form = super().form

        layout_components = list(form.fields.keys())
        helper = self.get_crispy_formhelper(layout_components)
        form.helper = helper

        return form

    def get_crispy_formhelper(self, fields: list):
        """
        méthode à implémenter dans l'instance concrète de FilterSet (CrispyFilterSet)
        fields est une list
        bien penser à déclarer le formhelper : helper = FormHelper()
        et à passer le form en GET : helper.form_method = "GET"
        """
        helper = FormHelper()
        helper.form_method = "GET"
        helper.form_id = "search-metacat-docs-form"
        # juste pour envoyer en htmx ;)  ... optionnel  
        # https://htmx.org/attributes/hx-boost/
        # https://noumenal.es/notes/til/htmx/progressively-enhance-a-form/
        # https://enzircle.hashnode.dev/responsive-table-with-django-and-htmx
        helper.attrs = {'hx_boost': 'true', 'hx_trigger':"change"}

        # fields['archived'].initial = False

        # fields = fields + [
        #     Submit("submit button", "Chercher"),
        #     # Reset('reset button', 'Effacer!'),
        # ]
        fields = [*fields, Submit("submit button", "Chercher")]
        helper.layout = Layout(
            # HTML('
            # <div class="spinner-border htmx-indicator" role="status">
            # <span class="visually-hidden">Loading...</span>
            # </div>'
            # ),
            HTML('<div class="progress"><div class="indeterminate"></div></div>'),
            Div(
                *fields,
                css_class="d-flex flex-row justify-content-between align-items-center",
            ),
        )

        return helper
