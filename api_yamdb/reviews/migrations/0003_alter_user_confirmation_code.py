# Generated by Django 3.2 on 2023-02-03 18:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230203_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Код подтверждения'),
        ),
    ]