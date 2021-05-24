from rest_framework import serializers

from api.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer :: Serializer for Product
    """

    class Meta:
        model = Product
        fields = ('product_sku', 'product_name', 'product_description', 'is_active')
