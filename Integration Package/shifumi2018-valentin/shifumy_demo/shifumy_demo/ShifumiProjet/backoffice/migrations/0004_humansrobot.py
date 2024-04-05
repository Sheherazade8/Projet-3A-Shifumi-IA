# Generated by Django 2.0.6 on 2018-06-07 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0003_auto_20180606_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='humansRobot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part', models.IntegerField()),
                ('round', models.IntegerField()),
                ('human', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)])),
                ('Computer', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]