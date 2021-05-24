from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from api.models import Product, Webhook, WebhookLog
from api.serializers import ProductSerializer,WebhookSerializer

from.tasks import add_num

class ProductViewset(viewsets.ModelViewSet):
    # TODO: Add Class Description
    """

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter,  DjangoFilterBackend]
    search_fields = ['product_sku', 'product_name', 'product_description']
    filterset_fields = ['is_active']

class WebhookViewset(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
