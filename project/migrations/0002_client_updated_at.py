# Generated by Django 5.1.4 on 2024-12-13 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
