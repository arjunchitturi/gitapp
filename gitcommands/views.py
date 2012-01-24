# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
#from django.http import HttpResponse
from django.shortcuts import render_to_response#, redirect
#from django.core.urlresolvers import reverse
#from django.template.loader import render_to_string
#from django.utils import simplejson

#from bootstrap.forms import QuestionForm, AnswerForm \
#, ExampleForm, AjaxAutoComplete, PopoverForm
from gitcommands.models import GitCommit#, GitUser, GitRepository


#Home Page
def home(request):
    context = {}
    context.update(csrf(request))
    context["user"] = request.user
    context["hero_title"] = "Welcome to GitApp"
    return render_to_response("gitcommands/home.html", context)


@login_required
def inside(request):
    context = {}
    context["user"] = request.user
    return render_to_response("gitcommands/inside.html", context)


#display the list of commits.
def list_commits(request):
    c = {}
    commits = GitCommit.objects.all()
    c['commits'] = commits
    c['user'] = request.user
    #c['git_users'] = GitUser.objects.all()
    c['hero_title'] = "Hello, " + str(request.user.username) + "!"
    return render_to_response('gitcommands/list_commits.html', c)
