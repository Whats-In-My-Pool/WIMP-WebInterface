# Generated by Django 2.1.5 on 2019-01-29 19:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('WIMPsite', '0005_testresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='time_run',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
