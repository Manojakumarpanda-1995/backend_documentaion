# Generated by Django 3.1.2 on 2020-10-11 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_projectinfo_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectusers',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
