import requests
from django.conf import settings

class Loader:
	def get_content(self, docid):
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

class CluewebLoader(Loader):
	def get_content(self, docid):
		content = ""
		try:
			uri = settings.CLUEWEB_CGI_API + docid
			return "<a target='_blank' href='{0}'>{0}</a>".format(uri)
			# response = requests.get(uri)
			# raw_lines = response.text.split('\n')
			# warc_lines = raw_lines[25:1038]

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
