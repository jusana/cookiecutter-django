from .tasks_results_views import task_status


class TaskResultContextMixin:
    """
    Ajoute le resultat de la tâche 'task_id' au contexte de la vue dans laquelle
    ce mixin est inséré dans la clé 'celery_task_result' du contexte
    => nécessite que la vue ait une url associée à "task_id" en path ou query_string (GET)
    ex: path('ma_route/<str:task_id>/', MaVueAvecTaskResultContextMixin.as_view(), name='nomNom'),
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = kwargs["task_id"]
        task_result = task_status(task_id)
        context["celery_task_result"] = task_result
        return context
