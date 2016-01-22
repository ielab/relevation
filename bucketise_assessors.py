#!/usr/bin/env python

import argparse
import results_reader

def main(results, assessors):
	results = results_reader.read(open(results))
	
	query_buckets = {}
	doc_buckets = dict(zip(range(0,assessors), [0]*assessors))

	num_docs_per_query = dict(zip(results.keys(), [len(docs) for docs in results.values()]))

	count = 0
	for qid in sorted(num_docs_per_query, key=num_docs_per_query.get, reverse=True):
		#print qid, num_docs_per_query[qid]

		idx = count % assessors
		idx = sorted(doc_buckets, key=doc_buckets.get)[0]

		query_buckets[idx] = [qid] if idx not in query_buckets else query_buckets[idx]+ [qid]
		doc_buckets[idx] = num_docs_per_query[qid] if idx not in doc_buckets else doc_buckets[idx] + num_docs_per_query[qid]

		count = count + 1

	print "Query allocations:"
	for idx in query_buckets:
		print idx+1, "\t", 
		for qid in query_buckets[idx]:
			print qid,
		print
	
	print "\nDocuments per assessor:"
	for idx in doc_buckets:
		print idx+1, "\t", doc_buckets[idx]

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Read TREC results file for relevation input and assign queries to assessors.")
	
	parser.add_argument("results", nargs='?', help="TREC style results file.")
	parser.add_argument("-a", "--assessors", type=int, default=4, help="Number of assossors/buckets to generate.");

	args = parser.parse_args()

	main(args.results, int(args.assessors))