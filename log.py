import logging.handlers
import logging
import os

level = logging.DEBUG

log_filename = 'log_madalert.log'

# Logging configuratio
# Handler for all the loggers
handler = logging.handlers.RotatingFileHandler(
	os.path.join(os.path.expanduser('~'),log_filename),
	maxBytes = 10*2**20,
	backupCount=20)

handler.setFormatter(
	logging.Formatter(
	'%(asctime)s|%(name)s|%(levelname)s|%(message)s'
	)
)

# get a loger with this namer
def getLogger(name):
	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)
	return logger

# Decorator to log functions
class fn_logger(object):
	def __init__(self,logfn):
		self.logfn = logfn
		
	def __call__(self,fn,*args,**kwargs):
		def wrapper(*args,**kwargs):
			self.logfn ("CALL:{}:{}:{}".format(fn.__name__,str(args),str(kwargs)))
			result = fn(*args,**kwargs)
			self.logfn("RETURN:{}:{}".format(fn.__name__,str(result)))
			return result
		return wrapper
