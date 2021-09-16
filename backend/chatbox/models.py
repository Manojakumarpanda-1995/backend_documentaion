from django.db import models
from django.db.models.expressions import OrderBy
from organization.models import Company
from project.models import ProjectInfo, ProjectUsers
from usermanagement.models import Users
import uuid
# Create your models here.


class ChatSession(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                blank=False, null=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.SET_NULL,
                                blank=False, null=True)
    session_id = models.CharField(max_length=500, blank=True, null=True)
    sender = models.ForeignKey(ProjectUsers, on_delete=models.SET_NULL,
                               blank=False, null=True)
    receiver = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    isActive = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, blank=True,
                                   null=True, related_name="chat_created_by")
    updated_at = models.DateField(auto_now_add=False, auto_now=True)
    updated_by = models.ForeignKey(Users, on_delete=models.SET_NULL, blank=True,
                                   null=True, related_name="chat_updated_by")

    class Meta:
        db_table = "ChatSession"


class UsersChannels(models.Model):
        
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             blank=True, null=True)
    status = models.BooleanField(default=True)
    channel_id = models.CharField(max_length=500, blank=True, null=True)
    active_from = models.DateTimeField(auto_now_add=True, auto_now=False)
    active_upto = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    class Meta:
        db_table = "UsersChannels"


class ChatHistory(models.Model):
    
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.SET_NULL, null=True)
    session_id = models.ForeignKey(ChatSession, on_delete=models.SET_NULL, null=True)
    message = models.TextField(blank=True, null=False)
    status = models.BooleanField(default=True)
    read = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    class Meta:
        db_table = "ChatHistory"
        ordering = ['-time_stamp']
