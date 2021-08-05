# Generated by Django 3.0.9 on 2020-10-02 15:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('last_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('password', models.TextField(blank=True, null=True)),
                ('token', models.CharField(blank=True, max_length=500, null=True)),
                ('designation', models.CharField(blank=True, max_length=500, null=True)),
                ('active', models.NullBooleanField(default=True)),
                ('user_verified', models.NullBooleanField(default=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('reporting_manager_id', models.IntegerField(blank=True, null=True)),
                ('reporting_manager_name', models.CharField(blank=True, max_length=500, null=True)),
                ('reporting_manager_email', models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.EmailValidator()])),
                ('hashkey', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryURL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('expiry_time', models.DateTimeField()),
                ('token', models.TextField()),
                ('filename', models.TextField()),
                ('filepath', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=100, unique=True)),
                ('role_description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_created_by', to='usermanagement.Users')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_updated_by', to='usermanagement.Users')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('activity', models.TextField()),
                ('ip_address', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Users')),
            ],
        ),
        migrations.CreateModel(
            name='AccessManagement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password_attempts', models.IntegerField(default=0)),
                ('last_login_attempt', models.DateTimeField(blank=True, null=True)),
                ('otp', models.CharField(blank=True, max_length=2048, null=True)),
                ('otp_expiry_time', models.DateTimeField(blank=True, null=True)),
                ('last_otp_attempt', models.DateTimeField(blank=True, null=True)),
                ('otp_attempts', models.IntegerField(default=0)),
                ('last_password_reset_request', models.DateTimeField(blank=True, null=True)),
                ('password_reset_request_count', models.IntegerField(default=0)),
                ('verification_link_expiry', models.DateTimeField(blank=True, null=True)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Users')),
            ],
        ),
    ]
