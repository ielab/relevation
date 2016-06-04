from django.conf import settings
from django.db import models

import doc_loader

# Create your models here.


class Document(models.Model):
	docId = models.CharField(max_length=250)

	# document loader dependent on settings
	loader_cls = settings.DOCUMENT_TYPE + "Loader"
	loader_inst = getattr(doc_loader, loader_cls)()

	def __unicode__(self):
		return self.docId

	def get_content(self):
		return Document.loader_inst.get_content(self.docId)

class Query(models.Model):
	qId = models.IntegerField()
	text = models.CharField(max_length=250)
	difficulty = models.IntegerField(blank=True, null=True)
	comment = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	criteria = models.TextField(blank=True, null=True)

	example = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return '%s: %s' % (self.qId, self.text)

	def num_unjudged_docs(self):
		return self.num_judgements() - len(self.judgements())

	def num_judgements(self):
		return len(self.judgement_templates())

	def prepare_judgements(self, userid):
		self._judgements = [judgement for judgement in Judgement.objects.filter(user=userid, query=self.id) if judgement.relevance != -1]

	def judgements(self):
		return self._judgements

	def judgement_templates(self):
		return JudgementTemplate.objects.filter(query=self.id)

class JudgementTemplate(models.Model):
	query = models.ForeignKey(Query)
	document = models.ForeignKey(Document)

	def __unicode__(self):
		return '%s\t%s\n' % (self.query.qId, self.document.docId)

class Judgement(models.Model):

	labels = {-1: 'Unjudged', 0: 'Not relvant', 1: 'Somewhat relevant', 2:'Highly relevant'}

	query = models.ForeignKey(Query)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	document = models.ForeignKey(Document)
	comment = models.TextField(blank=True, null=True)

	relevance = models.IntegerField()

	def __unicode__(self):
		return '%s\t%s\t%s\t%s\n' % (self.query.qId, self.user.username, self.document.docId, self.relevance)


	def label(self):
		return self.labels[self.relevance]
