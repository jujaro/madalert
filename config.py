import db
import peewee as pw
import log as Log
log = Log.getLogger('so.process')


class MissingConfig(Exception):
	pass

class Config(db.BaseModel):
	module = pw.CharField(null = True)
	config = pw.CharField(null = True)
	value = pw.CharField()

	@classmethod
	def get_conf(cls, module, config):
		try:
			return cls.select().where(
				cls.module == module,
				cls.config == config
				).get().value
		except pw.DoesNotExist:
			log.info("Missing configuration {}:{}".format(module,config))
			raise MissingConfig("{}.{} not Found".format(module,config))

	@classmethod
	def set_conf(cls, module, config, value):
		try:
			row = cls.select().where(
				cls.module == module,
				cls.config == config
				).get()
		except pw.DoesNotExist:
			with db.db.transaction():
				cls.create(
					module = module,
					config = config,
					value = value
					)
			log.info("Configuration created {}:{}:{}".format(
				module,config,value))
		else:
			log.info("Updating configuration {}:{}:{}".format(module,config,row.value))
			# It is there already, lets update it
			with db.db.transaction():
				row.update(value = value)
				row.save()
			log.info("Configuration updated {}:{}:{}".format(module,config,value))

if not Config.table_exists():
	log.info("Creating table config")
	Config.create_table()
