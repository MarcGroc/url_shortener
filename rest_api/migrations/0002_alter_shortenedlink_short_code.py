# Generated by Django 4.1.7 on 2023-04-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rest_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortenedlink",
            name="short_code",
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
