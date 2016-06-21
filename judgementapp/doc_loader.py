import requests
from django.conf import settings

class Loader:
	def get_content(self, docid):
		raise NotImplementedError()

	def get_cached_url(self, docid):
		raise NotImplementedError()

class FileLoader(Loader):
	def get_content(self, docid):
		content = ""
		try:
			with open(settings.DATA_DIR + "/" + docid) as f:
				content = f.read()
		except Exception:
			content = "Could not read file %s" % settings.DATA_DIR + "/" + docid
		return content

	def get_cached_url(self, docid):
		return settings.DATA_DIR + "/" + docid

class CluewebLoader(Loader):
	def get_content(self, docid):
		content = ""
		try:
			uri = settings.CLUEWEB_CGI_API + "J=" + docid
			response = requests.get(uri)
			raw_lines = response.text.split('\n')
			content = raw_lines[24]

			# return "<a target='_blank' href='{0}'>{0}</a>".format(uri)

			# # read off warc header
			# blank_line_count = 0
			# for split, line in enumerate(warc_lines):
			# 	if not line.strip():
			# 		blank_line_count += 1
			# 	if blank_line_count == 2:
			# 		break
			# content = "\n".join(["<iframe>"] + warc_lines[split:] + ["</iframe>"])
		except Exception:
			content = "Could not read content from %s" % uri
		return content

	def get_cashed_url(self, docId):
		return settings.CLUEWEB_CGI_API + "e=" + docId