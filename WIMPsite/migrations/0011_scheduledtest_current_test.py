# Generated by Django 2.1.5 on 2019-03-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('WIMPsite', '0010_auto_20190320_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtest',
            name='current_test',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
