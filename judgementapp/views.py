# Create your views here.
import cStringIO as StringIO
from wsgiref.util import FileWrapper
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from judgementapp.models import *

@login_required
def index(request):
    queries = Query.objects.order_by('qId')
    output = ', '.join([q.text for q in queries])

    template = loader.get_template('judgementapp/index.html')
    context = RequestContext(request)
    context['queries'] = queries
    # context = Context({
    #     'queries': queries,
    # })
    return HttpResponse(template.render(context))

@login_required
def qrels(request):
    judgements = Judgement.objects.exclude(relevance=-1)


    response = HttpResponse(judgements, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=qrels.txt'
    #response['X-Sendfile'] = myfile
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

@login_required
def query_list(request):
    queries = Query.objects.order_by('qId')

    return render_to_response('judgementapp/query_list.html', { 'queries': queries}, context_instance=RequestContext(request))

@login_required
def query(request, qId):
    query = Query.objects.get(qId=qId)
    user = request.user
    judgements = Judgement.objects.filter(user=user.id, query=query.id)

    if "difficulty" in request.POST:
        query.difficulty = int(request.POST['difficulty'])
        if "comment" in request.POST:
            query.comment = request.POST['comment']
        query.save()

    query.length = len(query.text)

    return render_to_response('judgementapp/query.html', {'query': query, 'judgements': judgements},
        context_instance=RequestContext(request))

@login_required
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

@login_required
def judge(request, qId, docId):
    query = get_object_or_404(Query, qId=qId)
    document = get_object_or_404(Document, docId=docId)
    relevance = request.POST['relevance']
    comment = request.POST['comment']

    judgements = Judgement.objects.filter(query=query.id)
    judgement, created = Judgement.objects.get_or_create(query=query.id, document=document.id)
    judgement.relevance = int(relevance)
    if comment != 'Comment':
        judgement.comment = comment
    judgement.save()



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

@staff_member_required
def upload(request):
    context = {}
    if 'queryFile' in request.FILES:
        f = request.FILES['queryFile']

        qryCount = 0
        for query in f:
            qid, txt = query.split("\t", 1)
            qryCount = qryCount + 1
            query, created = Query.objects.get_or_create(qId=qid,text=txt)
        context['queries'] = qryCount

    if 'resultsFile' in request.FILES:
        f = request.FILES['resultsFile']

        docCount = 0
        for result in f:
            qid, z, doc, rank, score, desc = result.split()
            docCount = docCount + 1

            document, created = Document.objects.get_or_create(docId=doc)

            query = Query.objects.get(qId=qid)
            document.save()

            judgement = Judgement()
            judgement.query = query
            judgement.document = document
            judgement.user = request.user
            judgement.relevance = -1

            judgement.save()

        context['results'] = docCount

    return render_to_response('judgementapp/upload.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {
        'form': form,
    })



