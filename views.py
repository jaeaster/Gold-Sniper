import os
from flask import Flask, render_template, request, url_for
from GoldSniper import *
import getpass
from pytz import utc #UTC is timezone for scheduler 
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.jobstores.mongodb import MongoDBJobStore
#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor



jobstores = {
	#'mongo': MongoDBJobStore()
}

executors = {
	'default': ThreadPoolExecutor(20) # Worker count = 20
}

job_defaults = {
	'coalesce': False,
	'max_instances': 3
}

#instantiate scheduler with config options as the arguments
#scheduler = BackgroundScheduler("""jobstores=jobstores""", executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler = BackgroundScheduler()
scheduler.start()

#Create sniper instance
sniper = GoldSniper()

#create web app instance
app = Flask(__name__)

#routes index.html to the root of the web server
@app.route('/')
def index():
	return render_template('index.html')

#Calls submit function when some makes a POST request
@app.route('/submit/', methods=['POST'])
def submit():
	username = request.form['username']
	password = request.form['password']
	quarter = request.form['quarter']
	enroll_code = request.form['enroll_code']
	pass_time = request.form['passtime'] #MM/DD/YY HH:MM, 2009-05-30 HH:MM:SS
	pass_time_arg = '20' + pass_time[6:8] + '-' + pass_time[0:2] + '-' + pass_time[3:5] + ' ' + pass_time[9:] + ':00'
	scheduler.add_job(sniper.goldSniper, 'date', run_date=pass_time_arg, args=[username,password,quarter,enroll_code])
	return render_template('index.html')

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)   




#other shit that was in app.py:
"""username = str(raw_input("Please enter GOLD username: "))
password = getpass.getpass("Please enter your password: ")

username = "vonmeier"
password = "C871d97d"
quarter = "20154"
enroll_code = "58677"
sniper = GoldSniper()
sniper.login(username,password)
#sniper.listLinks()
sniper.setQuarter("20154") #Fall
sniper.snipeCourse("58677")


#enroll_code = 58677
"""
