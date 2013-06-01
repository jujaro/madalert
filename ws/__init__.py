import urllib2
import urllib
import json
import gzip
import StringIO
import logging as log
import log as Log
log = Log.getLogger('ws')


class jsonWS:
	'json Web Sevice'
	host = None
	version = '1'
	entity_name = None
	params = {}
	compressed = False
	protocol = 'http'
	request = 'GET'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

	def read(self,**args):
		return json.loads(self.raw_read(**args))

	def raw_read(self,**args):
		req = urllib2.Request(
			self.get_url(**args),
			headers = { 'User-Agent' : self.user_agent ,'Accept-Encoding': 'gzip'}
		)
		log.info(str(args))
		try:
			if self.request == "POST":
				f = urllib2.urlopen(req,self.get_params(**args))
			else:
				f = urllib2.urlopen(req)
		except urllib2.HTTPError,e:
			if self.compressed:
				log.fatal(str(e) + ":" + str(self.decompress(e.read())))
			else:
				log.fatal(str(e) + ":" + str(e.read()))
			raise
		if not self.compressed:
			return f.read()
		# Uncompress
		return self.decompress(f.read())

	def decompress(self,compress_data):
		# Uncompress
		stringfile = StringIO.StringIO(compress_data)
		zipfile = gzip.GzipFile(fileobj = stringfile)
		uncompress_data = zipfile.read()
		return uncompress_data


	def get_params(self,**args):
		tmp_args = args.copy()
		tmp_args.update(self.params)
		return urllib.urlencode(tmp_args)

	def get_url(self,**args):
		url =  "{protocol}://{host}/{version}/{ent_name}?{params}".format(
				protocol = self.protocol,
				host = self.host,
				version = self.version,
				ent_name = self.entity_name,
				params = self.get_params(**args) if self.request == 'GET' else ""
			)
		return url
