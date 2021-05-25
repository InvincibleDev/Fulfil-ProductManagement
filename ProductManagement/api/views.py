import boto3
import uuid
import os
from api.tasks import delete_all_products,process_csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.result import AsyncResult
from django.core.files.storage import default_storage
from django.conf import settings

@api_view(["DELETE"])
def DeleteAllProducts(request):
    task = delete_all_products.delay()
    return Response({"task_id":task.id})

@api_view(["POST"])
def FileUpload(request):
    unique_file_name = str(uuid.uuid4()) + ".csv"
    data = request.data['file']
    with default_storage.open(unique_file_name, 'wb+') as destination:
        for chunk in data.chunks():
            destination.write(chunk)
    task = process_csv.delay(destination.name)
    return Response({"task_id":task.id})

@api_view(["GET"])
def TaskProgress(request, task_id):
    response = {}
    task = AsyncResult(task_id)
    if task.status == "PROGRESS":
        response["status"] = "PROGRESS"
        response["progress_percentage"] = (int(task.info["done"]) / int(task.info["total"])) * 100
    if task.status == "CREATING":
        response["status"] = "CREATING"
        response["progress_percentage"] = (int(task.info["done"]) / int(task.info["total"])) * 100
    if  task.status == "UPDATING":
        response["status"] = "UPDATING"
        response["progress_percentage"] = (int(task.info["done"]) / int(task.info["total"])) * 100
    if task.status == "FAILURE" or task.status == "REVOKED":
        response["status"] = "FAILED"
        response["progress_percentage"] = 0
    if task.status == "PENDING":
        response["status"] = "PENDING"
        response["progress_percentage"] = 0
    if task.status == "SUCCESS":
        response["status"] = "SUCCESS"
        response["progress_percentage"] = 100
    return Response(response)
