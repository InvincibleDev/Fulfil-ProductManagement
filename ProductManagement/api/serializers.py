from rest_framework import serializers

from api.models import Product, Webhook
from api.tasks import send_webhook
import json

class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer :: Serializer for Product
    """

    class Meta:
        model = Product
        fields = ('product_sku', 'product_name', 'product_description', 'is_active')

    # Overiding create method to send Webhooks upon product creation
    def create(self, validated_data):
        event = "PRODUCT_CREATE_EVENT"
        product_sku = validated_data.get('product_sku', "")
        product_name = validated_data.get('product_name', "")
        product_description = validated_data.get('product_description', "")
        is_active = validated_data.get('is_active', True)
        product, created = Product.objects.update_or_create(product_sku = product_sku,defaults={"product_name":product_name, "product_description":product_description,"is_active":is_active})

        if not created:
            event = "PRODUCT_UPDATE_EVENT"

        data = {
                "product_sku":product.product_sku,
                "product_name":product.product_name,
                "product_description":product.product_description,
                "is_active":product.is_active,
        }
        task = send_webhook.delay(event, product = data)
        return product

    # Overiding update method to send Webhooks upon product updation
    def update(self, instance, validated_data):
        event = "PRODUCT_UPDATE_EVENT"

        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_description = validated_data.get('product_description', instance.product_description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        data = {
                "product_sku":instance.product_sku,
                "product_name":instance.product_name,
                "product_description":instance.product_description,
                "is_active":instance.is_active,
        }
        task = send_webhook.delay(event, product = data)
        print(task.id)
        return instance

class WebhookSerializer(serializers.ModelSerializer):
    """
    Webhook Serializer :: Serializer for Webhook Model
    """
    class Meta:
        model = Webhook
        fields = ('id','event','target_url')
