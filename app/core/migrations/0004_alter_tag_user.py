# Generated by Django 3.2.21 on 2023-10-30 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20231030_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL),
        ),
    ]
