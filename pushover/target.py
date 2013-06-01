# Push Over API
from ws import jsonWS

class pushover(jsonWS):
	host = 'api.pushover.net'
	version = 1
	entity_name = 'messages.json'
	compressed = False
	protocol = 'https'
	request = "POST"


	def send_notification(self,**kwargs):
		return self.read(**kwargs)




