# Generated by Django 4.1.4 on 2023-11-07 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pc_keeper", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pc",
            name="password",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="pc",
            name="start_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="pc",
            name="username",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.DeleteModel(
            name="UseHistory",
        ),
    ]
