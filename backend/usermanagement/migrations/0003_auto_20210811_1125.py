# Generated by Django 3.2.3 on 2021-08-11 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0002_auto_20210804_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accessrequest',
            name='skill_sets',
        ),
        migrations.AddField(
            model_name='workers',
            name='skill_sets',
            field=models.TextField(blank=True, db_column='Skill Sets', null=True),
        ),
    ]