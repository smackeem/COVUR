# Generated by Django 5.0.1 on 2024-01-15 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_cart_completed_alter_cart_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
    ]
