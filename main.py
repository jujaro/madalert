import logging as log
import os

log.basicConfig(
        level = log.DEBUG,
        filename = os.path.join(os.path.expanduser('~'),'log_madalert.log'),
        filemode = 'w'
)

import argparse as ap
import bottle as bt
import so.process
import emailsender as es
from pushover.target import pushover

arg_parser = ap.ArgumentParser()
arg_parser.add_argument('-c',
			help = 'Command, so_stats/so_questions',
			required = True)
arg_parser.add_argument('-token',
			help = 'App Token for pushover',
			required = False)
arg_parser.add_argument('-user',
			help = 'User key for pushover',
			required = False)
arg_parser.add_argument('-l',help = 'Login/Password for email account',
			required = False)
arg_parser.add_argument('-to',help = 'email address to send the report',
			required = False)
arg_parser.add_argument('-t',
			action = 'store_true',
			help = 'Only displays the report (don\'t send)',
			required = False)

parsed_args = arg_parser.parse_args()

if parsed_args.c == "so_stats":
	if parsed_args.t:
		show_report_only = True
	else:
		show_report_only = False
		if parsed_args.l:
			login,password = parsed_args.l.split('/')
			if parsed_args.to:
				to = parsed_args.to
			else:
				parsed_args.print_help()
				quit()
		else:
			arg_parser.print_help()
			quit()

	# Get the data
	top_day_growth, top_week_growth, top_month_growth = so.process.get_growth_results()
	# Generate the email
	msg = bt.template('email',
		top_day_growth = top_day_growth,
		top_week_growth = top_week_growth,
		top_month_growth = top_month_growth
		)
	# Send the email or show it
	if show_report_only:
		filepath = os.path.join(os.path.expanduser('~'),".tmpemail.htm")
		with open(filepath,"w") as f:
			f.write(msg)
		import webbrowser
		webbrowser.open(filepath)
	else:
		es.sendmail(
					to,
					to,
					"StackOverflow Stats",
					msg,
					login,
					password
					)


if parsed_args.c == "so_questions":
	questions = so.process.questions_to_alert()
	for q in questions:
		pushover().send_notification(
			token = parsed_args.token ,
			user = parsed_args.user,
			title = "SO Question",
			message = q["title"],
			url = q["link"]
		)
	so.process.save_questions(questions)

