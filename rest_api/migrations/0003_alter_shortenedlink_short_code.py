# Generated by Django 4.1.7 on 2023-04-11 11:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rest_api", "0002_alter_shortenedlink_short_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortenedlink",
            name="short_code",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
