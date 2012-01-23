from django.db import models
from django.contrib.auth.models import User as DjangoUser
#import datetime
# Create your models here.


class GitUser(models.Model):
    git_user = models.OneToOneField(DjangoUser)


class GitRepository(models.Model):
    repo_user = models.ForeignKey(GitUser, related_name='repo_user')
    repo_name = models.CharField(max_length=300)
    repo_url = models.URLField()


class GitCommit(models.Model):
    MODE_CHOICES = (
        ('A', 'Added'),
        ('R', 'Removed'),
        ('M', 'Modified'),
    )
    commit_user = models.ForeignKey(GitUser, related_name='committer')
    commit_message = models.CharField(max_length=300)
    commit_time = models.DateTimeField(null=True)
    commit_mode = models.CharField(max_length=1, choices=MODE_CHOICES)
    commit_url = models.URLField()
