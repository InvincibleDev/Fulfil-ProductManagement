import os
from celery import shared_task, current_task
import json, requests
from celery.utils.log import get_task_logger
from api.models import WebhookLog, Webhook, Product
import pandas as pd
from django.db import transaction, connection

# Tried Doing the below initially, But it took insane amount of time to execute

# @shared_task
# def process_csv(file_name):
#     obj = s3.get_object(Bucket=bucket, Key=file_name)
#     df = pd.read_csv(obj['Body'])
#     count = 0
#     total = df.shape[0]
#     for index, row in df.iterrows():
#         Product.objects.update_or_create(product_sku=row["sku"],defaults={"product_name": row["name"],"product_description": row["description"]})
#         count += 1
#         current_task.update_state(state='PROGRESS', meta={'done': count, 'total': total})
#     return "SUCCESS"

@shared_task
def process_csv(file_path):
    df = pd.read_csv(file_path)
    all_skus = Product.objects.values_list('product_sku', flat=True)
    update_df = df[df['sku'].isin(all_skus)].reset_index(drop=True)
    create_df = df[~df['sku'].isin(all_skus)].reset_index(drop=True)
    create_df = create_df.drop_duplicates(subset=['sku'], keep='last')

    update_total = update_df.shape[0]
    create_total = create_df.shape[0]

    # Update Existing iterrows
    with transaction.atomic():
        for index, row in update_df.iterrows():
            Product.objects.filter(product_sku = row['sku']).update(product_name = row['name'], product_description = row['description'])
            current_task.update_state(state='UPDATING', meta={'done': index, 'total': update_total})

    # Creating New Records
    create_df_records = create_df.to_dict('records')
    product_instances = [Product(product_sku=record['sku'],product_name=record['name'],product_description=record['description']) for record in create_df_records]
    batch_size = 10000
    start = 0
    end = batch_size
    while end <= create_total:
        if end > create_total:
            end = create_total
        product_instance_batch = product_instances[start:end]
        Product.objects.bulk_create(product_instance_batch)
        start = end
        end += batch_size
        current_task.update_state(state='CREATING', meta={'done': start, 'total': create_total})

    # Delete Temp File
    if os.path.exists(file_path):
        os.remove(file_path)
    return "SUCCESS"

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
    current_task.update_state(state='PROGRESS', meta={'done': 0, 'total': 100})
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE "{Product._meta.db_table}"')
    return "success"
