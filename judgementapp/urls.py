from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from django.contrib.admin.views.decorators import staff_member_required

from judgementapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^query$', views.query_list, name='query_list'),
    url(r'^query/qrels$', views.qrels, name='query_list'),
    url(r'^query/(?P<qId>\d+)/$', views.query, name='query'),
    url(r'^query/claim/(?P<qId>\d+)/$', views.claim, name='claim'),
    url(r'^query/(?P<qId>\d+)/doc/(?P<docId>[A-Za-z0-9_\-\+\.]+)/$', views.document, name='document'),
	url(r'^query/(?P<qId>\d+)/doc/(?P<docId>[+A-Za-z0-9_\-\+\.]+)/judge/$', views.judge, name='judge'),    

	# Authentication
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^accounts/signup/$', views.signup),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
    	{'next_page': '/'}),

    (r'^about/$', TemplateView.as_view(template_name='judgementapp/about.html')),
    (r'^upload/$', staff_member_required(TemplateView.as_view(template_name='judgementapp/upload.html'))),
	url(r'^upload/save$', views.upload, name='upload'),        
)