from django.contrib import messages


class FormSuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """

    success_message = ""

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data, **kwargs)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data, **kwargs):
        return self.success_message % dict(cleaned_data, **kwargs)


# TODO: faire FormSuccessMessageMixin avec polling result de task celery !
class FormSuccessMessageTaskResultMixin(FormSuccessMessageMixin):
    """
    Permet d'avoir un success message après l'envoi d'un form (le cas échéant)
    ET d'appeler le polling pour récupérer le resultat de la tâche lancée par le POST (form_valid()) du form
    """

    success_message = "La tâche <span id='task-id' \
                                      hx-get='%(task_status)s' \
                                      hx-trigger='load' \
                                      hx-swap='innerHTML' \
                                      class='text-decoration-underline' \
                                      >task-id</span>' \
                        a bien été envoyée.\
                        <br>Merci !"
    task_result_class = ""

    def get_success_message(self, cleaned_data, **kwargs):
        return self.success_message % dict(cleaned_data, **kwargs)
