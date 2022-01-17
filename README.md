# Relevation!


_Relevation: A raising or lifting up._ - Wiktionary


Relevation is a system for performing relevance judgements for Information Retrieval system evaluation. Documents and queries can be uploaded to the system via the web interface. Judges can browse the uploaded documents and queries and provide their relevance assessments.

## Who is Relevation! aimed at?

Relevation! is aimed at anyone wishing to collection relevance assessment for information retrieval evaluation evaluation.

If you do use Relevation! we would appreciated it if you cited us:

B. Koopman and G. Zuccon. Relevation!: *An open source system for information retrieval relevance assessment*. In Proceedings of the 37th annual international ACM SIGIR conference on research and development in information retrieval, Gold Coast, Australia, July 2014.

## Feautures

Relevation! is build using Python's (version 2.7) Django (version 1.6) web framework and Twitter's Bootstrap.

## Setup Steps

1. Checkout relevation from github with: `git clone https://github.com/ielab/relevation.git`
2. Copy your documents into the `relevation/documents` folder.
3. Start Relevation! by running `./manage.py runserver`. Relevation! will be running at [http://127.0.0.1:8000](http://127.0.0.1:8000)
4. Go to Setup page and upload your queries and document pool. (Queries are in the form queryId[tab]queryText; the pool is in standard TREC results format.)

You can also look at a demo that shows how to setup Relevation! from scratch; the demo is available at [https://vimeo.com/ielab/relevation](https://vimeo.com/ielab/relevation).

### Input format for Queries and Rankings

#### Queries File Format

The query file has the format `queryId[tab]queryText`; e.g.,

```
20149	43-year-old woman with soft, flesh-colored, pedunculated lesions on her neck.
201410	67-year-old woman status post cardiac catheterization via right femoral artery, now with a cool, pulseless right foot and right femoral bruit.
201411	40-year-old woman with severe right arm pain and hypotension. She has no history of trauma and right arm exam reveals no significant findings.
201412	25-year-old woman with fatigue, hair loss, weight gain, and cold intolerance for 6 months.
201413	30-year-old woman who is 3 weeks post-partum, presents with shortness of breath, tachypnea, and hypoxia.
```

### Judgements File Format

The judement file in just a standard TREC results file, which is:

`queryId[tab]Q0[tab]docId[tab]score[tab]runDescription`

For example:

```
201410	Q0	NCT02371057	1	0.82393600	bm25
201410	Q0	NCT01102998	2	0.80546773	bm25
201410	Q0	NCT00494468	3	0.78496643	bm25
201410	Q0	NCT02517346	4	0.74522880	bm25
201410	Q0	NCT00881985	5	0.61913227	bm25
```

The judgement file is in the form

## Use cases

Relevation has been used in anger for:

* CLEF eHealth Evaluation Lab: 2013-2016
* [ECIR diagnose me paper](http://zuccon.net/diagnose-this.html)
* Relevance assessment collection for [Bevan Koopman's](http://koopman.id.au) PhD thesis
* [SIGIR Clinical Trials Collection paper](http://dl.acm.org/citation.cfm?id=2914672)

## Authors and Support

Relevation was designed by [Bevan Koopman](http://koopman.id.au) and [Guido Zuccon](http://zuccon.net). Relevation is an open source project still in development.
