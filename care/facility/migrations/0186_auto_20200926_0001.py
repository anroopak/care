# Generated by Django 2.2.11 on 2020-09-25 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0185_correct_blood_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpatientregistration',
            name='fit_for_blood_donation',
            field=models.BooleanField(default=None, null=True, verbose_name='Is Patient fit for donating Blood'),
        ),
        migrations.AlterField(
            model_name='patientregistration',
            name='fit_for_blood_donation',
            field=models.BooleanField(default=None, null=True, verbose_name='Is Patient fit for donating Blood'),
        ),
    ]
