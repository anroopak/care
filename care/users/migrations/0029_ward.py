# Generated by Django 2.2.11 on 2020-09-21 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20200916_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('local_body', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.LocalBody')),
            ],
            options={
                'unique_together': {('local_body', 'name')},
            },
        ),
    ]
