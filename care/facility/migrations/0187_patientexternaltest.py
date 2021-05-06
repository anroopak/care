# Generated by Django 2.2.11 on 2020-09-27 12:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_user_ward'),
        ('facility', '0186_auto_20200926_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientExternalTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('srf_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=1000)),
                ('age', models.IntegerField()),
                ('age_in', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('mobile_number', models.CharField(max_length=15)),
                ('is_repeat', models.BooleanField()),
                ('patient_status', models.CharField(max_length=15)),
                ('lab_name', models.CharField(max_length=255)),
                ('test_type', models.CharField(max_length=255)),
                ('sample_type', models.CharField(max_length=255)),
                ('result', models.CharField(max_length=255)),
                ('sample_collection_date', models.DateTimeField()),
                ('result_date', models.DateTimeField()),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.District')),
                ('local_body', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.LocalBody')),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Ward')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
