# Generated by Django 2.1.5 on 2019-01-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('WIMPsite', '0002_auto_20190117_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtest',
            name='scale',
            field=models.CharField(choices=[('H', 'Hour'), ('D', 'Day'), ('W', 'Week')], default='D', max_length=1),
            preserve_default=False,
        ),
    ]
