# Generated by Django 4.2.2 on 2023-07-05 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_patient_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='diabetesanalysis',
            name='last_checked',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
