from django.core.management.base import BaseCommand
#, CommandError
import datetime

import github2
from init_git import GitInit

from django.contrib.auth.models import User as DjangoUser
from gitcommands.models import GitUser, GitRepository, GitCommit


class Command(BaseCommand):
    args = '<git_user1 git_user2 ...>'
    help = 'enter git hub users separated by a space'

    def handle(self, *args, **options):
        for i, git_user in enumerate(args):
            self.stdout.write("\ngit_user: %s \n" % git_user)
            try:
                f = GitInit(username = git_user)

                #updating git_activity db. for DjangoUser
                user, yesorno = DjangoUser.objects.get_or_create(username = f.username)

                #updating git_activity db. for GitUser
                git_user, yesorno = GitUser.objects.get_or_create(git_user=user)

                repos = f.client.repos.list(f.username)
                self.stdout.write('total %s repositories for owner %s \n' % (len(repos), repos[0].owner))
                self.stdout.write("Displaying commits for the last day: \n")

                #iterate the repos of each user.
                for repo in repos:
                    #repo_id, yesorno = GitRepository.objects.get_or_create(repo_user = git_user)
                    repo_id = GitRepository()
                    repo_id.repo_user = git_user
                    try:
                        #updating git_activity db. for GitRepository.
                        repo_id.repo_name = repo.name
                        repo_id.repo_url = repo.url
                        repo_id.repo_language = repo.language

                        repos_created = repo.created_at
                        repos_pushed = repo.pushed_at
                        repo_id.repo_created = repos_created
                        repo_id.repo_pushed = repos_pushed
                        repo_id.repo_private = repo.private
                        repo_id.repo_watchers = repo.watchers
                        repo_id.repo_description = repo.description
                        repo_id.repo_owner = repo.owner
                        repo_id.save()

                        ucommits = f.client.commits.list(repo.owner + '/' + repo.name)#, page = 2)
                        if ((repos_created or repos_pushed) > (datetime.datetime.now() - datetime.timedelta(1))):
                            self.stdout.write('[Repo desc: {%s}\n Repo name: (%s) is a fork(%s). and is forked by (%s)\n\
                             Repo url(%s)]\n' % (repo.description, repo.name, repo.fork, repo.forks, repo.url))

                        #iterate the commits of each user.
                        for commit in ucommits:
                            #comit_id, yesorno = GitCommit.objects.get_or_create(commit_user = git_user)
                            comit_id = GitCommit()
                            comit_id.commit_user = git_user
                            tree = commit.tree
                            msg = commit.message
                            comit = commit.committed_date

                            #updating git_activity db. for GitCommit.
                            comit_id.commit_time = comit
                            comit_id.commit_message = msg
                            comit_id.commit_tree = tree
                            #todo: deal with multiple parents for merge case.
                            for item in commit.parents:
                                parents_str = item['id'] + ', '
                            comit_id.commit_parents = parents_str
                            comit_id.commit_author = commit.author['login']
                            comit_id.commit_committer = commit.committer['login']

                            if commit.added:
                                #self.stdout.write("%s filename added" % commit.added[0]['filename'])
                                comit_id.commit_mode = 'A'#commit.added[0]['filename']
                            if commit.removed:
                                #self.stdout.write("%s filename removed" % commit.removed[0]['filename'])
                                comit_id.commit_remove = 'R'#commit.removed[0]['filename']
                            if commit.modified:
                                #self.stdout.write("%s filename modified" % commit.modified[0]['filename'])
                                comit_id.commit_modify = 'M'#commit.modified[0]['filename']

                            comit_id.commit_url = repo.url + '/commit/' + commit.id
                            comit_id.save()

                            #display all commits in the last 24 hours.
                            if comit > (datetime.datetime.now() - datetime.timedelta(1)):
                                self.stdout.write("[    %s committed to:  \n" % (commit.committer['login']))
                                self.stdout.write("    (commit_tree: '%s' with message: '%s' at date: '%s' \n" % (tree, msg, comit))
                                self.stdout.write("    (commit_url: %s/commit/%s ]\n" % (repo.url, commit.id))

                    except github2.request.HttpError:
                        continue

            except UnicodeDecodeError:
                if (i <= (len(args) - 1)):
                    continue
                else:
                    break
