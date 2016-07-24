from django.conf import settings
from django.db import models

# Create your models here.

class Document(models.Model):
    docId = models.CharField(max_length=250)
    text = models.TextField()

    def __unicode__(self):
        return self.docId

    def get_content(self):
        content = ""
        try:
            with open(settings.DATA_DIR+"/"+self.docId) as f:
                content = f.read()
        except Exception:
            content = "Could not read file %s" % settings.DATA_DIR+"/"+self.docId
        return content

class Query(models.Model):
    qId = models.IntegerField()
    criteria = models.CharField(max_length=512)
    qcode = models.CharField(max_length=8)
    difficulty = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.qId, self.criteria[:100])

    def num_unjudged_docs(self):
        unjugded = [judgement for judgement in self.judgements() if judgement.relevance < 0]
        return len(unjugded)

    def num_judgements(self):
        return len(self.judgements())

    def judgements(self):
        return Judgement.objects.filter(query=self.id)

class Judgement(models.Model):

    query = models.ForeignKey(Query)
    document = models.ForeignKey(Document)
    comment = models.TextField(blank=True, null=True)

    topic_labels = {-1: 'Unjudged', 0: 'Not relvant', 1: 'Somewhat relevant', 2:'Highly relevant'}
    relevance = models.IntegerField()

    understandability = models.IntegerField(default=-1)
    trustability = models.IntegerField(default=-1)

    def __unicode__(self):
        return '%s\t0%s\t%s\n' % (self.query.qId, self.document.docId, self.relevance)

    def topical_label(self):
        return self.topic_labels[self.relevance]

    def understandability_judged(self):
        return "Unjuged" if self.understandability == -1 else "Judged"

    def trustability_judged(self):
        return "Unjuged" if self.trustability == -1 else "Judged"

