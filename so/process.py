from source import so_Tags, so_Questions
import datetime
import time
import model as md
import log as Log
log = Log.getLogger('so.process')


#CONSTANTS
REPORT_SIZE = 20

# Process
@Log.fn_logger(log.debug)
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
	
@Log.fn_logger(log.debug)
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

@Log.fn_logger(log.debug)
def get_growth_results():
	log.info("Start collect")
	collect()
	log.info("Start process")
	md.SOTag.process_stats(datetime.date.today())
	log.info("Start report")
	return top_growth_results()

@Log.fn_logger(log.debug)
def save_questions(questions):
	with md.transaction():
		for question in questions:
			md.SOAlertedQuestions.create(
					url = question["link"],
					log_date = datetime.date.today()
					)
	log.debug("%d questions saved" % len(questions))
	
@Log.fn_logger(log.debug)
def get_python_questions(page_range):
	params = {
			"tagged": "python",
			"sort" : "creation"
			}
	result = []
	for page in xrange(1,page_range+1):
		log.debug("Page = page")
		for question in so_Questions().get_items(page = page, **params):
			#log.debug(str(datetime.datetime.fromtimestamp(question["creation_date"])))
			result.append(question)
	log.debug("get_python_questions returns %d questions" % len(result))
	return result

@Log.fn_logger(log.debug)
def so_bulletin_filter(questions):
	min_score = 3
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

@Log.fn_logger(log.debug)
def so_potential_answer_filter(questions,minutes):
	min_reput = 100
	ignore_set = set([
		'django','matplotlib','sqlalchemy','py2exe','pandas','numpy','tornado','opencv',
		'boto','google-app-engine','cassandra','matlab','qt','ipython','pyqt','pyqt4','flask',
		'gtk','android','jquery','pyramid','selenium','reportlabe','celery','django-celery','git',
		'svn','gtk3','scipy','pygame','gevent','wxpython','scrapy','beautifulsoup'
		])
	result = []
	for question in questions:
		log.debug("so_potential_answer_filter:Filtering: %s" % str(question))
		if ( time.time() - question["creation_date"]) > (minutes * 60):
			log.debug("filtered for creation date, no more tests")
			break
		if set(question['tags']).intersection(ignore_set):
			log.debug("filtered for tags")
			continue
		if question["owner"].get("reputation",0) < min_reput :
			log.debug("filtered for owner reputation")
			continue
		if question["is_answered"]:
			log.debug("filtered for already answered")
			continue
		if	md.SOAlertedQuestions.exists(question["link"]):
			log.debug("filtered for already alerted")
			continue
		log.debug("Added to the alert list")
		result.append(question)
	log.debug("Result: %d questions" % len(result))
	return result

@Log.fn_logger(log.debug)
def so_bulletin_get():
		return so_bulletin_filter(get_python_questions(page_range = 15))
	
@Log.fn_logger(log.debug)
def so_potential_answer_get(minutes):
		return so_potential_answer_filter(get_python_questions(page_range = 1),minutes = minutes)
