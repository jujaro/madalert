import db
import peewee as pw
import datetime
import logging as log

PROPORTION_FACTOR = 100000

transaction = db.db.transaction

class SOTag(db.BaseModel):
	tag_name	=	pw.CharField(null=True)
	status		=	pw.CharField(null=True)
	count		=   pw.IntegerField(null=True)
	q_of_day	=	pw.DateField(null=True)
	q_of_week	=	pw.DateField(null=True)
	q_of_month	=	pw.DateField(null=True)

	def __repr__(self):
		return "SOTag(%s)" % self.tag_name
	def day_growth(self):
		if self.q_of_day:
			return float(self.q_of_day) * PROPORTION_FACTOR / self.count
		else:
			return 0.0

	def week_growth(self):
		if self.q_of_week:
			return float(self.q_of_week) * PROPORTION_FACTOR / self.count
		else:
			return 0.0

	def month_growth(self):
		if self.q_of_month:
			return float(self.q_of_month) * PROPORTION_FACTOR / self.count
		else:
			return 0.0

	@classmethod
	def process_stats(cls,reference_date):
		with transaction():
			for tag in cls.select():
				log.debug("Tag:%s" % tag.tag_name)
				try:
					today_log = SOTagLog.select().where(
							SOTagLog.tag == tag,
							SOTagLog.log_date == reference_date
							).get()
				except pw.DoesNotExist:
					log.error("Not records found for this tag today %s" % tag.tag_name)
					raise ValueError("Not records found for today")
				# Calculate questions for this day
				try:
					yesterday_log = SOTagLog.select().where(
							SOTagLog.tag == tag,
							SOTagLog.log_date == (reference_date - datetime.timedelta(1))
							).get()
				except pw.DoesNotExist:
					log.info("Not records found for this tag yesterday %s" % tag.tag_name)
					continue
				else:
					# Save update
					tag.q_of_day = today_log.count - yesterday_log.count
				# Calculate questions for this week
				try:
					last_week_log = SOTagLog.select().where(
							SOTagLog.tag == tag,
							SOTagLog.log_date == (reference_date - datetime.timedelta(7))
							).get()
				except pw.DoesNotExist:
					log.info("Not records found for this tag last week %s" % tag.tag_name)
				else:
					# Save update
					tag.q_of_week = today_log.count - last_week_log.count
				# Calculate questions for this month
				try:
					last_month_log = SOTagLog.select().where(
							SOTagLog.tag == tag,
							SOTagLog.log_date == (reference_date - datetime.timedelta(30))
							).get()
				except pw.DoesNotExist:
					log.info("Not records found for this tag last month %s" % tag.tag_name)
				else:
					# Save update
					tag.q_of_month = today_log.count - last_month_log.count
				tag.save()

	@classmethod
	def save_log(cls, tag_name, count, log_date):
		# Validate if the tag exists.
		try:
			tag = cls.get(SOTag.tag_name == tag_name)
		except pw.DoesNotExist:
			tag = cls.create(
				tag_name = tag_name,
				status = "ENABLED"
				)
		# And create the log
		SOTagLog.create(
			tag = tag,
			count = count,
			log_date = log_date
			)
		# Also update the tag log
		tag.count = count
		tag.save()

class SOTagLog(db.Log):
	tag		=	pw.ForeignKeyField(SOTag)
	count	=	pw.IntegerField(null=True)

class SOAlertedQuestions(db.Log):
	url		= pw.CharField(null=True)

	@classmethod
	def exists(cls,url):
		try:
			cls.get(SOAlertedQuestions.url == url)
		except pw.DoesNotExist:
			return False
		else:
			return True

# Initialization
if not SOTag.table_exists():
	log.info("Creatint table for SOTag")
	SOTag.create_table()

if not SOTagLog.table_exists():
	log.info("Creatint table for SOTagLog")
	SOTagLog.create_table()

if not SOAlertedQuestions.table_exists():
	log.info("Creatint table for SOAlertedQuestions")
	SOAlertedQuestions.create_table()


