# Generated by Django 2.1.5 on 2019-04-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('WIMPsite', '0011_scheduledtest_current_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='invert_color_match',
            field=models.BooleanField(default=False),
        ),
    ]