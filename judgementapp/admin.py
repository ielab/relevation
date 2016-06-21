from django.contrib import admin
from judgementapp.models import Judgement, Query, Document	

admin.site.register(Judgement)
admin.site.register(Query)
admin.site.register(Document)