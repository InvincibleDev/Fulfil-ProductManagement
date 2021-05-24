from celery import shared_task, current_task
import json, requests
from celery.utils.log import get_task_logger
from api.models import WebhookLog, Webhook, Product
from django.db import connection

@shared_task
def send_webhook(event, product):
    data = {
            "Event" : event,
            "product" : product
    }

    webhooks = Webhook.objects.filter(event = event)
    for webhook in webhooks:
        response = requests.post(
            webhook.target_url, data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
            )
        if response.status_code != 200:
            webhook_log = WebhookLog.objects.create(
                    webhook = webhook,
                    received_response = response.text,
                    status = "FAILURE"
            )
        else:
            webhook_log = WebhookLog.objects.create(
                    webhook = webhook,
                    received_response = response.text,
                    status = "SUCCESS"
            )

    return

@shared_task
def delete_all_products():
    products = Product.objects.all()
    total = products.count()
    count = 0
    for product in products:
        product.delete()
        count += 1
        current_task.update_state(state='PROGRESS', meta={'done': count, 'total': total})
    return "success"
