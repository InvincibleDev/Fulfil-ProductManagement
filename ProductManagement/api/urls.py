from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.viewsets import ProductViewset

router=SimpleRouter()
router.register('product', ProductViewset, basename='product')

urlpatterns = [
    path('',include(router.urls)),
]
