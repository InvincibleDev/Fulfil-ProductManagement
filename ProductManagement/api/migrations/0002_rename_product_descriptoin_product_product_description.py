# Generated by Django 3.2.3 on 2021-05-22 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_descriptoin',
            new_name='product_description',
        ),
    ]
