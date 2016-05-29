from django.contrib import admin
from django.conf import settings
import judgementapp
from judgementapp.models import Judgement, Query

admin.site.register(Judgement)
admin.site.register(Query)

doc_class = getattr(judgementapp.models, settings.DOCUMENT_TYPE)
admin.site.register(doc_class)