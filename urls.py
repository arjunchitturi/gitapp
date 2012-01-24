from django.conf.urls.defaults import patterns, include#, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from gitcommands.views import inside, list_commits, home, list_repos

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gitapp.views.home', name='home'),
    # url(r'^gitapp/', include('gitapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),

    (r'^$', home),
    (r'^inside/$', inside),

    #Registration
    (r'^accounts/', include('registration.urls')),

    #Commits
    (r'^list_commits', list_commits),

    #Repos
    (r'^list_repos', list_repos),
   
)
