import os
from flask import Flask, render_template, request, url_for
from GoldSniper import *
import getpass
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging

# Create web app instance
app = Flask(__name__)

# Looks to config.py for config options
app.config.from_object('config')

# Configuration for logs
logging.basicConfig()

# The following dictionaries configure
# the BackgroundScheduler instance

jobstores = {
	'default': SQLAlchemyJobStore(url='sqlite:///app.db')
}

executors = {
	'default': ThreadPoolExecutor(20) # Worker count = 20
}

job_defaults = {
	'coalesce': False,
	'max_instances': 3
}


# Instantiate scheduler with config options as the arguments
scheduler = BackgroundScheduler(jobstores=jobstores,
								executors=executors,
								job_defaults=job_defaults,
								timezone = timezone('US/Pacific'))
scheduler.start()


# Routes index.html to the root of the web server
@app.route('/')
def index():
	return render_template('index.html', title='Home')

# Calls submit function when someone makes a POST request
@app.route('/submit/', methods=['POST'])
def submit():
	username = request.form['username']
	password = request.form['password']
	quarter = request.form['quarter']
	enroll_code = request.form['enroll_code']
	pass_time = request.form['passtime']

	# Converts input format to usable format
	# e.g. MM/DD/YY HH:MM -> YYYY-MM-DD HH:MM:SS
	pass_time_arg = ('20' + pass_time[6:8] + '-' + pass_time[0:2]
					+ '-' + pass_time[3:5] + ' ' + pass_time[9:] 
					+ ':00')
	# save job in scheduler database
	scheduler.add_job(goldSniper,
					  'date',
					  run_date=pass_time_arg,
					  args=[username,password,quarter,enroll_code]
					  )

	return render_template('index.html', title="Success")

# Basically, if we are using app.py as the main module
# i.e. If we execute 'python app.py'
if __name__ == '__main__':

	# Bind to PORT if defined, otherwise default to 5000
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
