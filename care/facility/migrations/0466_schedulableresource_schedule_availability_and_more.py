# Generated by Django 5.1.1 on 2024-11-08 08:02

import care.facility.models.mixins.permissions.facility
import django.contrib.postgres.fields.ranges
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('facility', '0465_merge_20240923_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchedulableResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('resource_id', models.PositiveIntegerField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.facility')),
                ('resource_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=255)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.schedulableresource')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, care.facility.models.mixins.permissions.facility.FacilityRelatedPermissionMixin),
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=255)),
                ('slot_type', models.IntegerField(choices=[(1, 'Open'), (2, 'Appointment')], default=1)),
                ('slot_size_in_minutes', models.IntegerField(default=0)),
                ('tokens_per_slot', models.IntegerField(default=0)),
                ('days_of_week', models.JSONField(default=list)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.schedule')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, care.facility.models.mixins.permissions.facility.FacilityRelatedPermissionMixin),
        ),
        migrations.CreateModel(
            name='ScheduleException',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=255)),
                ('slot_type', models.IntegerField(choices=[(1, 'Open'), (2, 'Appointment')], default=1)),
                ('slot_size_in_minutes', models.IntegerField(default=0)),
                ('tokens_per_slot', models.IntegerField(default=0)),
                ('is_available', models.BooleanField()),
                ('datetime_range', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.schedulableresource')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, care.facility.models.mixins.permissions.facility.FacilityRelatedPermissionMixin),
        ),
    ]
