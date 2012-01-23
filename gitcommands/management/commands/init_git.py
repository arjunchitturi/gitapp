#import sys
import optparse
from subprocess import Popen, PIPE

from github2.client import Github

ITEM_FMT = "* %s (%s)"
URL_USER_FMT = "http://github.com/%s"

OPTION_LIST = (
    optparse.make_option('-t', '--api-token',
            default=None, action="store", dest="api_token", type="str",
            help="Github API token. Default is to find this from git config"),
    optparse.make_option('-u', '--api-user',
            default=None, action="store", dest="api_user", type="str",
            help="Github Username. Default is to find this from git config"),
)
BY_LOWER = lambda value: value.lower()


class GitInit(object):

    def __init__(self, username=None, api_user=None, api_token=None):
        self.api_user = api_user or self.git_config_get("github.user")
        self.api_token = api_token or self.git_config_get("github.token")
        self.username = username or self.api_user
        print("U:(%s) T:(%s) F:(%s)" % (self.api_user, self.api_token,
            self.username))
        self.client = Github(self.api_user, self.api_token)

    def git_config_get(self, key):
        pipe = Popen(["git", "config", "--get", key], stdout=PIPE)
        return pipe.communicate()[0].strip()
