# Generated by Django 2.2.11 on 2020-04-25 09:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0102_auto_20200424_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpatientregistration',
            name='external_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='patientregistration',
            name='external_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
