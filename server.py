import apscheduler.scheduler as sch
import config
import so.process
import bottle as bt
import emailsender as es
import log as Log
from pushover.target import pushover

log = Log.getLogger('server')

sched = sch.Scheduler()
sched.start()

@sched.cron_schedule(day = '1-31', hour = '8', minute = '0')
def so_growth_stats_mail():
	'''Sends statistics of stack overflow'''
	# Collect results
	top_day_growth, top_week_growth, top_month_growth = so.process.get_growth_results()
	# Create a template
	msg = bt.template('so_stats',
		top_day_growth = top_day_growth,
		top_week_growth = top_week_growth,
		top_month_growth = top_month_growth
		)
	#Send to email results
	es.sendmail(
			frm = config.Config().get_conf("mail", "from_addr"), 
			to = config.Config().get_conf("mail", "recipient"), 
			subject = "Stack Overflow Statistics", 
			message = msg, 
			login = config.Config().get_conf("mail", "user-login"), 
			password = config.Config().get_conf("mail", "password")
			)

@sched.cron_schedule(day = '1-31', hour = '5-17', minute = '0')
def so_bulletin_mail():
	# Collect the results
	questions = so.process.so_bulletin_get()
	# Create the template
	msg = bt.template('so_bulletin',questions=questions)
	# Send the email
	es.sendmail(
			frm = config.Config().get_conf("mail", "from_addr"), 
			to = config.Config().get_conf("mail", "recipient"), 
			subject = "Stack Overflow Bulletin", 
			message = msg, 
			login = config.Config().get_conf("mail", "user-login"), 
			password = config.Config().get_conf("mail", "password")
			)
	# Save the result
	so.process.save_questions(questions)


@sched.cron_schedule(day = '1-31', hour = '5-17', minute = '0')
def so_potential_answer_push_notification():
	log.info('so_potential_answer_push_notification')
	# Collect the results
	questions = so.process.so_potential_answer_get()
	log.info('%d questions' % len(questions))
	# Send the push notifications
	for q in questions:
		pushover().send_notification(
			token = config.Config().get_conf("pushover", "token"),
			user = config.Config().get_conf("pushover", "user"),
			title = "SO Question",
			message = q["title"],
			url = q["link"]
		)
	# Save the result
	so.process.save_questions(questions)

so_potential_answer_push_notification()
raw_input('Hit <Enter> to finish')
