from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.viewsets import ProductViewset, WebhookViewset
from api.views import DeleteAllProducts, TaskProgress, FileUpload

router=SimpleRouter()
router.register('product', ProductViewset, basename='product')
router.register('webhook', WebhookViewset, basename='webhook')

urlpatterns = [
    path('deleteall/', DeleteAllProducts),
    path('fileupload/', FileUpload),
    path('taskprogress/<str:task_id>/', TaskProgress),
    path('',include(router.urls)),
]
