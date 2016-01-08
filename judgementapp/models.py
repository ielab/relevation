from django.conf import settings
from django.db import models
from xml.dom import minidom

# Create your models here.


class Document(models.Model):
	docId = models.CharField(max_length=250)
	text = models.TextField()

	def __unicode__(self):
		return self.docId

	def get_content(self):
		content = ""
		try:
			xmldoc = minidom.parse(settings.DATA_DIR+"/"+self.docId+".xml")
			eligibility_criteria = xmldoc.getElementsByTagName('eligibility')[0].getElementsByTagName('criteria')[0].getElementsByTagName('textblock')[0].firstChild.nodeValue
			content = eligibility_criteria
		except Exception:
			content = "Could not read file %s" % settings.DATA_DIR+"/"+self.docId+".xml"
		return content

class Query(models.Model):
	qId = models.IntegerField()
	text = models.CharField(max_length=250)
	difficulty = models.IntegerField(blank=True, null=True)
	comment = models.TextField(blank=True, null=True)

	instructions = models.TextField(blank=True, null=True)
	criteria = models.TextField(blank=True, null=True)
	example = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return '%s: %s' % (self.qId, self.text)

	def num_unjudged_docs(self):
		unjugded = [judgement for judgement in self.judgements() if judgement.relevance < 0]
		return len(unjugded)

	def num_judgements(self):
		return len(self.judgements())

	def judgements(self):
		return Judgement.objects.filter(query=self.id)

class Judgement(models.Model):

	labels = {-1: 'Unjudged', 0: 'Not relvant', 1: 'Somewhat relevant', 2:'Highly relevant'}

	query = models.ForeignKey(Query)
	document = models.ForeignKey(Document)
	comment = models.TextField(blank=True, null=True)

	relevance = models.IntegerField()

	def __unicode__(self):
		return '%s\t0%s\t%s\n' % (self.query.qId, self.document.docId, self.relevance)


	def label(self):
		return self.labels[self.relevance]
