from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.viewsets import ProductViewset, WebhookViewset
from api.views import DeleteAllProducts, TaskProgress, FileUpload

# router for generating all endpoints for both viewsets
router=SimpleRouter()
router.register('product', ProductViewset, basename='product')
router.register('webhook', WebhookViewset, basename='webhook')

urlpatterns = [
    path('deleteall/', DeleteAllProducts), # Delete All Products Endpoint
    path('fileupload/', FileUpload), # File Upload for Bulk creation of Products Endpoint
    path('taskprogress/<str:task_id>/', TaskProgress), # Endpoint to track Progress of async tasks.
    path('',include(router.urls)),
]
