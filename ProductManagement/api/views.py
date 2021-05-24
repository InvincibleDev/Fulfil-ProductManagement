from api.tasks import delete_all_products
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.result import AsyncResult

@api_view(["DELETE"])
def DeleteAllProducts(request):
    task = delete_all_products.delay()
    print(task.id)
    return Response({"task_id":task.id})

@api_view(["GET"])
def TaskProgress(request, task_id):
    response = {}
    task = AsyncResult(task_id)
    if task.status == "PROGRESS":
        response["status"] = "STARTED"
        response["progress_percentage"] = (int(task.info["done"]) / int(task.info["total"])) * 100
    if task.status == "FAILED" or task.status == "REVOKED":
        response["status"] = "FAILED"
        response["progress_percentage"] = 0
    if task.status == "PENDING":
        response["status"] = "PENDING"
        response["progress_percentage"] = 0
    if task.status == "SUCCESS":
        response["status"] = "SUCCESS"
        response["progress_percentage"] = 100

    print(response)
    return Response(response)
