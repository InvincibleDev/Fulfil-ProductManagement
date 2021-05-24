from celery import shared_task
import json, requests
from celery.utils.log import get_task_logger
from api.models import WebhookLog, Webhook

logger = get_task_logger(__name__)

@shared_task
def add_num(x, y):
    for i in range(1,100000):
        if(i == 1000):
            logger.info("done done done ")
    return x+y

@shared_task
def send_webhook(event, product):
    data = {
            "Event" : event,
            "product" : product
    }
    print(data)

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
