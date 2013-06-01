# Stack Overflow API
from ws import jsonWS


class se_Class(jsonWS):
	'''Stack exchage class, access to
	any stack exchange site'''
	host = "api.stackexchange.com"
	version = '2.1'
	entity_name = None
	params = {}
	compressed = True
	protocol = 'http'
	request = 'GET'

	def get_items(self,**args):
		result = self.read(**args)
		return result["items"]


# WS Classes
class so_Class(se_Class):
	params = {
		"site":"stackoverflow"
		}

class so_Tags(so_Class):
	entity_name = 'tags'

class so_Questions(so_Class):
	entity_name = 'questions'

