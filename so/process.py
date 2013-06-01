from source import so_Tags, so_Questions
import datetime
import model as md
import log as Log
log = Log.getLogger('so.process')


#CONSTANTS
REPORT_SIZE = 20

# Process
def collect():
	log.debug("Star collecting")
	for page in range(1,10):
		log.debug("Page:%d" % page)
		end = False
		with md.transaction():
			for rest_tag in so_Tags().get_items(pagesize = 100,page = page):
				log.debug("Tag:%s" % rest_tag)
				# Do we got to the end
				if rest_tag["count"] < 10000:
					log.info("END FOUND:%s" % rest_tag)
					end = True
					break
				md.SOTag.save_log(
						tag_name = rest_tag["name"],
						count = rest_tag["count"],
						log_date = datetime.date.today()
				)
		if end:
			break
	log.debug("End collection")

def top_growth_results():
	tags = [ t for t in md.SOTag.select().where(md.SOTag.status == "ENABLED")]
	top_day_growth = sorted(
		tags,
		key = lambda x:x.day_growth(),
		reverse = True)[0:REPORT_SIZE]
	top_week_growth = sorted(
		tags,
		key = lambda x:x.week_growth(),
		reverse = True)[0:REPORT_SIZE]
	top_month_growth = sorted(
		tags,
		key = lambda x:x.month_growth(),
		reverse = True)[0:REPORT_SIZE]
	return top_day_growth, top_week_growth, top_month_growth

def get_growth_results():
	log.info("Start collect")
	collect()
	log.info("Start process")
	md.SOTag.process_stats(datetime.date.today())
	log.info("Start report")
	return top_growth_results()

def save_questions(questions):
	with md.transaction():
		for question in questions:
			md.SOAlertedQuestions.create(
					url = question["link"],
					log_date = datetime.date.today()
					)
			log.debug("Question saved")
	log.debug("All questions saved")

def get_python_questions(page_range):
	params = {
			"tagged": "python",
			"sort" : "creation"
			}
	result = []
	for page in xrange(1,page_range+1):
		for question in so_Questions().get_items(page = page, pagesize = 100, **params):
			print question
			log.info(str(datetime.datetime.fromtimestamp(question["creation_date"])))
			result.append(question)
	return result

def so_bulletin_filter(questions):
	min_score = 5
	min_reput = 100
	ignore_set = set([
		'django','matplotlib','sqlalchemy','py2exe','pandas','numpy','tornado','opencv',
		'boto','google-app-engine','cassandra','matlab','qt','ipython','pyqt','pyqt4','flask',
		'gtk','android','jquery','pyramid','selenium','reportlabe','celery','django-celery','git',
		'svn','gtk3','scipy','pygame','gevent','wxpython','scrapy','beautifulsoup'
		])
	result = []
	for question in questions:
		if set(question['tags']).intersection(ignore_set):
			continue
		if question["score"] < min_score:
			continue
		if question["owner"].get("reputation",0) < min_reput :
			continue
		if	md.SOAlertedQuestions.exists(question["link"]):
			continue
		result.append(question)
	return result

def so_potential_answer_filter(questions):
	min_reput = 100
	ignore_set = set([
		'django','matplotlib','sqlalchemy','py2exe','pandas','numpy','tornado','opencv',
		'boto','google-app-engine','cassandra','matlab','qt','ipython','pyqt','pyqt4','flask',
		'gtk','android','jquery','pyramid','selenium','reportlabe','celery','django-celery','git',
		'svn','gtk3','scipy','pygame','gevent','wxpython','scrapy','beautifulsoup'
		])
	result = []
	for question in questions:
		if datetime.datetime.fromtimestamp(question["creation_date"]) - datetime.datetime.now() > datetime.timedelta(minutes=4):
			continue
		if set(question['tags']).intersection(ignore_set):
			continue
		if question["owner"].get("reputation",0) < min_reput :
			continue
		if question["is_answered"]:
			return
		if	md.SOAlertedQuestions.exists(question["link"]):
			continue
		result.append(question)
	return result

def so_bulletin_get():
		return so_bulletin_filter(get_python_questions(page_range = 10))
	
def so_potential_answer_get():
		return so_potential_answer_filter(get_python_questions(page_range = 1))