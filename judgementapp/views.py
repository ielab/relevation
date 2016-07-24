# Create your views here.
import cStringIO as StringIO
#import re
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.servers.basehttp import FileWrapper

from django.views.decorators.csrf import csrf_exempt

from judgementapp.models import *

def index(request):
    queries = Query.objects.order_by('qId')
    output = ', '.join([q.criteria for q in queries])

    template = loader.get_template('judgementapp/index.html')
    context = Context({
        'queries': queries,
    })
    return HttpResponse(template.render(context))

def qrels(request):
    judgements = Judgement.objects.exclude(relevance=-1)


    response = HttpResponse(judgements, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=qrels.txt'
    #response['X-Sendfile'] = myfile
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

def query_list(request):
    queries = Query.objects.order_by('qId')

    return render_to_response('judgementapp/query_list.html', { 'queries': queries}, context_instance=RequestContext(request))

def query(request, qId):
    query = Query.objects.get(qId=qId)
    judgements = Judgement.objects.filter(query=query.id)

    if "difficulty" in request.POST:
        query.difficulty = int(request.POST['difficulty'])
        if "comment" in request.POST:
            query.comment = request.POST['comment']
        query.save()

    return render_to_response('judgementapp/query.html', {'query': query, 'judgements': judgements},
        context_instance=RequestContext(request))


def document(request, qId, docId):
    document = Document.objects.get(docId=docId)
    query = Query.objects.get(qId=qId)

    judgements = Judgement.objects.filter(query=query.id)
    judgement = Judgement.objects.filter(query=query.id, document=document.id)[0]
    rank = -1
    for (count, j) in enumerate(judgements):
        if j.id == judgement.id:
            rank = count+1
            break

    prev = None
    try:
        prev = Judgement.objects.filter(query=query.id).get(id=judgement.id-1)
    except:
        pass

    next = None
    try:
        next = Judgement.objects.filter(query=query.id).get(id=judgement.id+1)
    except:
        pass

    content = document.get_content()

    return render_to_response('judgementapp/document.html', {'document': document, 'query': query, 'judgement': judgement,
        'next': next, 'prev': prev, 'rank': rank, 'total_rank': judgements.count(), 'content': content.strip()}, context_instance=RequestContext(request))

@csrf_exempt
def my_ajax(request, qId, docId):

    if request.method == 'POST':
        query = get_object_or_404(Query, qId=qId)
        document = get_object_or_404(Document, docId=docId)

        relevance = None
        readability = None
        trustability = None
        comment = 'Comment'

        if 'understandability' in request.POST:
            readability = request.POST.get('understandability', None)
        if 'trustability' in request.POST:
            trustability = request.POST.get('trustability', None)

        updateJudgement(query, document, relevance, readability, trustability, comment)
        return HttpResponse('success') # if everything is OK

    # nothing went well
    return HttpRepsonse('FAIL!!!!!')


def updateJudgement(query, document, relevance=None, readability=None, trustability=None, comment='Comment'):
    judgement, created = Judgement.objects.get_or_create(query=query.id, document=document.id)

    if relevance:
        judgement.relevance = int(relevance)
    if readability:
        judgement.understandability = int(readability)
    if trustability:
        judgement.trustability = int(trustability)

    if comment != 'Comment':
        judgement.comment = comment
    judgement.save()
    return judgement

def judge(request, qId, docId):
    query = get_object_or_404(Query, qId=qId)
    document = get_object_or_404(Document, docId=docId)

    rel = request.POST['relevance']
    comment = request.POST['comment']

    judgements = Judgement.objects.filter(query=query.id)
    judgement = updateJudgement(query, document, relevance=rel, comment=comment)

    next = None
    try:
        next = Judgement.objects.filter(query=query.id).get(id=judgement.id+1)
        if 'next' in request.POST:
            document = next.document
            judgement = next
            next = Judgement.objects.filter(query=query.id).get(id=judgement.id+1)
    except:
        pass

    prev = None
    try:
        prev = Judgement.objects.filter(query=query.id).get(id=judgement.id-1)
    except:
        pass

    rank = -1
    for (count, j) in enumerate(judgements):
        if j.id == judgement.id:
            rank = count+1
            break

    content = document.get_content()

    return render_to_response('judgementapp/document.html', {'document': document, 'query': query, 'judgement': judgement,
        'next': next, 'prev': prev, 'rank': rank, 'total_rank': judgements.count(), 'content': content.strip()}, context_instance=RequestContext(request))


def upload(request):
    context = {}
    if 'queryFile' in request.FILES:
        f = request.FILES['queryFile']

        qryCount = 0
        for query in f:
            qid, qc, crit = query.split("\t", 2)

            #qid, txt, diseas = re.split("\s+", query, maxsplit=2)
            qryCount = qryCount + 1
            query = Query(qId=qid,qcode=qc,criteria=crit)
            query.save()
        context['queries'] = qryCount

    if 'resultsFile' in request.FILES:
        f = request.FILES['resultsFile']

        docCount = 0
        for result in f:
            qid, z, doc, rank, score, desc = result.split()
            docCount = docCount + 1
            doc = doc.replace('corpus/', '')

            document, created = Document.objects.get_or_create(docId=doc)
            document.text = "TBA"

            query = Query.objects.get(qId=qid)
            document.save()

            judgement = Judgement()
            judgement.query = query
            judgement.document = document
            judgement.relevance = -1
            judgement.readability = -1

            judgement.save()

        context['results'] = docCount

    return render_to_response('judgementapp/upload.html', context)


