from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Member(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER_CHOICES = [
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    ]

    WEB_DESIGNER = 'WEB DESIGNER'
    CONTENT_MANAGER = 'CONTENT CONTENT_MANAGER'
    SOCIAL_MANAGER = 'SOCIAL SOCIAL_MANAGER'
    POSITION_CHOICES = [
        (WEB_DESIGNER, 'WEB DESIGNER'),
        (CONTENT_MANAGER, 'CONTENT MANAGER'),
        (SOCIAL_MANAGER, 'SOCIAL_MANAGER')
    ]

    Approved = 'Approved'
    Pending = 'Pending'
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=False)
    birthday = models.DateTimeField(auto_now_add=False)
    gender = models.CharField(max_length=40, choices=GENDER_CHOICES, default=MALE)
    position = models.CharField(max_length=40, choices=POSITION_CHOICES, default=WEB_DESIGNER)
    address = models.CharField(max_length=40, null=True)
    address2 = models.CharField(max_length=40, null=True)
    country = models.CharField(max_length=40, null=True)
    state_city = models.CharField(max_length=40, null=True)
    eduction = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.username.first_name


class Project(models.Model):
    Complete = 'Complete'
    Pending = 'Pending'
    Uncomplete = 'Uncomplete'
    PROJECT_STATUS_CHOICES = [
        (Complete, 'Complete'),
        (Pending, 'Pending'),
        (Uncomplete, 'Uncomplete')
    ]

    Web_design = 'Web design'
    Content = 'Content'
    Social_media_marketing = 'Social media marketing'
    PROJECT_TYPE_CHOICES = [
        (Web_design, 'Web design'),
        (Content, 'Content'),
        (Social_media_marketing, 'Social media marketing')
    ]
    name = models.CharField(max_length=40, null=True)
    description = models.TextField(max_length=200, null=True)
    project_type = models.CharField(max_length=40, choices=PROJECT_TYPE_CHOICES, default=Web_design)
    status = models.CharField(max_length=40, choices=PROJECT_STATUS_CHOICES, default=Uncomplete)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    def shortproject(self):
        return self.description[0:100]+"..."



class Task(models.Model):
    title = models.CharField(max_length=40, null=True)
    description = models.TextField(max_length=200, null=True)
    member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='member+')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author+')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL ,null=True)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(auto_now_add=False, null=True)
    due_time = models.TimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.title
    


class Activity(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=40, null=True)
    description = models.TextField(max_length=200, null=True)
    due_date = models.DateField(auto_now_add=False, null=True)
    complete = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'


class MemberRequest(models.Model):
    title = models.CharField(max_length= 40)
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Sentfrom+')
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name=' Sentto+')
    description = models.TextField(max_length=300)
    requested_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def shortrequest(self):
        return self.description[0:50]+"..."