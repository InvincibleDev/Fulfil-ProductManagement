from django.contrib import admin
from api.models import Product, Webhook, WebhookLog
# Register your models here.
admin.site.register([Product, Webhook, WebhookLog])
