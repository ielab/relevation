# Relevation!


_Relevation: A raising or lifting up._ - Wiktionary


Relevation is a system for performing relevance judgements for Information Retrieval system evaluation. Documents and queries can be uploaded to the system via the web interface. Judges can browse the uploaded documents and queries and provide their relevance assessments.

## Who is Relevation! aimed at?

Relevation is aimed at anyone wishing to collection relevance assessment for information retrieval evaluation evaluation.

## Feautures

Relevation! is build using Python's Django web framework and Twitter's Bootstrap.

## Setup Steps

1. Checkout relevation from github with: `git clone https://github.com/ielab/relevation.git`
2. Copy your documents into the `relevation/documents` folder.
3. Start Relevation! by running `./manage.py runserver`. Relevation! will be running at [http://127.0.0.1:8000](http://127.0.0.1:8000)
4. Go to Setup page and upload your queries and document pool. (Queries are in the form queryId[tab]queryText; the pool is in standard TREC results format.)

You can also look at a demo that shows how to setup Relevation! from scratch; the demo is available at [https://vimeo.com/ielab/relevation](https://vimeo.com/ielab/relevation).

## Use cases

Relevation has been used in anger for:

* CLEF eHealth Evaluation Lab 2013
* Relevance assessment collection for [Bevan Koopman's](http://koopman.id.au) PhD thesis

## Authors and Support

Relevation was designed by [Bevan Koopman](http://koopman.id.au) and [Guido Zuccon](http://zuccon.net). Relevation is an open source project still in development.
