# Generated by Django 2.2.5 on 2020-03-18 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("atlas", "0026_department_cost_center")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_directory_hidden",
            field=models.BooleanField(default=False),
        )
    ]
