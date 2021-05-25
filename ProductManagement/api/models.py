from django.db import models
from django.utils import timezone

EVENT_CHOICE=(
    ("PRODUCT_CREATE_EVENT", "PRODUCT_CREATE_EVENT"),
    ("PRODUCT_UPDATE_EVENT", "PRODUCT_UPDATE_EVENT"),
)

WEBHOOK_STATUS=(
    ("SUCCESS", "SUCCESS"),
    ("FAILURE", "FAILURE")
)

class Product(models.Model):
    product_sku = models.SlugField(primary_key=True)
    product_name = models.CharField(max_length = 100)
    product_description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'api'
        db_table = "PRODUCT"

    def __str__(self):
        return f"{self.product_sku}-{self.product_name}"

class Webhook(models.Model):
    created_timestamp = models.DateTimeField(default = timezone.now)
    event = models.CharField(max_length = 100, choices = EVENT_CHOICE)
    target_url = models.URLField(max_length=1000)

    class Meta:
        app_label = 'api'
        db_table = "WEBHOOK"

class WebhookLog(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    sent_datetime = models.DateTimeField(default = timezone.now)
    received_response = models.JSONField(null = True, blank = True)
    status = models.CharField(max_length = 100, choices = WEBHOOK_STATUS, default = "SUCCESS")

    class Meta:
        app_label = 'api'
        db_table = "WEBHOOKLOG"
