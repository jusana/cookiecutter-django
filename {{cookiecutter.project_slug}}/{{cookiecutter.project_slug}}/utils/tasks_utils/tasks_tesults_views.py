from celery.result import AsyncResult
from django.http import JsonResponse


def task_status(task_id):
    task = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task.status,
        "result": task.result,
        # 'result': task.get()
    }
    return response


def task_status_view(request, task_id):
    task = task_status(task_id)

    if task["result"] == "FAILURE" or task["status"] == "PENDING":
        response = {
            "task_id": task_id,
            "status": task["status"],
            "result": str(task["result"]),
        }
        return JsonResponse(response, status=200)

    response = {
        "task_id": task_id,
        "status": task["status"],
        "result": task["result"],
        # 'result': task.get()
    }
    return JsonResponse(task, status=200)
