import os
import uuid

from api.tasks import delete_all_products,process_csv
from celery.result import AsyncResult

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.files.storage import default_storage
from django.conf import settings


@api_view(["DELETE"])
def DeleteAllProducts(request):
    '''
    Input : Request to Delete all Products.
    Output : 'task_id' of the celery task
    Receives Request to delete all the Products and starts a celery task for the same
    '''
    task = delete_all_products.delay()
    return Response({"task_id":task.id})

@api_view(["POST"])
def FileUpload(request):
    '''
    Input : CSV File.
    Output : 'task_id' of the celery task
    Receives Request with a CSV File to Bulk Upload all Products and starts a celery task for the same.
    '''
    unique_file_name = str(uuid.uuid4()) + ".csv"
    data = request.data['file']
    with default_storage.open(unique_file_name, 'wb+') as destination: # store the csv file in temp folder and pass the file path to celery task
        for chunk in data.chunks():
            destination.write(chunk)
    task = process_csv.delay(destination.name)
    return Response({"task_id":task.id})

@api_view(["GET"])
def TaskProgress(request, task_id):
    '''
    Input : task_id .
    Output : Progress of the celery task
    Receives Request with a task_id of celery task to Recieve Progress of the same.
    '''
    response = {}
    task = AsyncResult(task_id)
    if task.status == "PROGRESS" or task.status == "CREATING" or  task.status == "UPDATING":
        response["status"] = task.status
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
