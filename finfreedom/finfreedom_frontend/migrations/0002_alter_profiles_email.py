# Generated by Django 3.2.8 on 2021-10-16 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finfreedom_frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
