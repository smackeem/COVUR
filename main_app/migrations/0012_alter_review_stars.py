# Generated by Django 4.2.9 on 2024-01-21 04:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.PositiveIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(limit_value=5)]),
        ),
    ]
