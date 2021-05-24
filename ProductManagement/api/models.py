from django.db import models

# Create your models here.
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
