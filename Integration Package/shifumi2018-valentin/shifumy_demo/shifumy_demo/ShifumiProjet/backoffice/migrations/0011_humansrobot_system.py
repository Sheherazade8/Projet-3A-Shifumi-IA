# Generated by Django 2.0.7 on 2018-07-17 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0010_merge_20180716_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='humansrobot',
            name='System',
            field=models.CharField(default='mouse_version', max_length=15),
            preserve_default=False,
        ),
    ]
