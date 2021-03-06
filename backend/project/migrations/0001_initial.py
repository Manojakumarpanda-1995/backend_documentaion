# Generated by Django 3.0.9 on 2020-10-02 15:23

from django.db import migrations, models
import django.db.models.deletion
import project.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('function_type', models.TextField(blank=True, null=True)),
                ('datafile', models.FileField(upload_to='')),
                ('unique_string', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('project_name_hash', models.CharField(max_length=255, unique=True)),
                ('project_id', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_created_by', to='usermanagement.Users')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_updated_by', to='usermanagement.Users')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_user_created_by', to='usermanagement.Users')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ProjectInfo')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_user_updated_by', to='usermanagement.Users')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.UserCompanyRole')),
            ],
        ),
        migrations.CreateModel(
            name='GetProgress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bulk_user_upload', models.TextField(default={})),
                ('bulk_user_download', models.TextField(default={})),
                ('get_training_logs', models.TextField(default={})),
                ('get_user_logs', models.TextField(default={})),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Users')),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('original_file_name', models.TextField(verbose_name='originalFilename')),
                ('datafile', models.FileField(upload_to=project.models.get_file_path, verbose_name='Datafile')),
                ('function_type', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Users')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('activity', models.TextField()),
                ('ip_address', models.CharField(blank=True, max_length=200, null=True)),
                ('project_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ProjectUsers')),
            ],
        ),
    ]
