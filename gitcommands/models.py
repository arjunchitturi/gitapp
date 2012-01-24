from django.db import models
from django.contrib.auth.models import User as DjangoUser
#import datetime
# Create your models here.


class GitUser(models.Model):
    git_user = models.OneToOneField(DjangoUser)

    def __unicode__(self):
        return self.git_user.username


class GitRepository(models.Model):
    repo_user = models.ForeignKey(GitUser, related_name='repo_user')
    repo_owner = models.CharField(max_length=300)
    repo_name = models.CharField(max_length=300)
    repo_description = models.CharField(max_length=300, null=True)
    repo_language = models.CharField(max_length=100, null=True)
    repo_created = models.DateTimeField(null=True)
    repo_pushed = models.DateTimeField(null=True)
    repo_watchers = models.PositiveIntegerField(null=True)
    repo_private = models.BooleanField(default=False)
    repo_url = models.URLField()


class GitCommit(models.Model):
    '''
    MODE_CHOICES = (
        ('A', 'Added'),
        ('R', 'Removed'),
        ('M', 'Modified'),
    )
    '''
    commit_user = models.ForeignKey(GitUser, related_name='committer')
    commit_message = models.CharField(max_length=300)
    commit_time = models.DateTimeField(null=True)
    #commit_add = models.CharField(max_length=300)
    commit_mode = models.CharField(max_length=10)
    #commit_modify = models.CharField(max_length=300)
    commit_committer = models.CharField(max_length=300)
    commit_author = models.CharField(max_length=300)
    commit_parents = models.CharField(max_length=300)
    commit_tree = models.CharField(max_length=300)
    commit_url = models.URLField()
