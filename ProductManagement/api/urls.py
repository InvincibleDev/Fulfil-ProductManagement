from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.viewsets import ProductViewset, WebhookViewset

router=SimpleRouter()
router.register('product', ProductViewset, basename='product')
router.register('webhook', WebhookViewset, basename='webhook')

urlpatterns = [
    path('',include(router.urls)),
]
