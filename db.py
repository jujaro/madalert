import peewee as pw
import os
import logging as log

DATABASEFILENAME = os.path.join(
	os.path.expanduser('~'),
	'madalert.db'
	)
log.debug('USING DBFILE %s' % DATABASEFILENAME)

db = pw.SqliteDatabase(DATABASEFILENAME,threadlocals=True)

class BaseModel(pw.Model):
	class Meta:
		database = db

class Log(BaseModel):
	log_date = pw.DateField(null=True)

