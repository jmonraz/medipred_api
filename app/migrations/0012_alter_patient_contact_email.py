# Generated by Django 4.2.2 on 2023-07-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_diabetesanalysis_last_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='contact_email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
