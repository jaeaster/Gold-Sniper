import os
from flask import Flask, render_template, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
import getpass
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from GoldSniper import *
from forms import LoginForm

#create web app instance
app = Flask(__name__)

#Looks to config.py for config options
app.config.from_object('config')

#create database instance
db = SQLAlchemy(app)

#database models

#user model
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	#documents all snipes for a user, backref is a reference from a snipe to the owner
	snipes = db.relationship('Snipe', backref='sniper', lazy='dynamic')

	def __repr(self):
		return '<User %r>' % (self.nickname)

#snipe model
class Snipe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	snipe_name = db.Column(db.String(140))
	enroll_code = db.Column(db.String(10))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Snipe %r>' % (self.snipe_name)

# The following dictionaries configure the BackgroundScheduler instance
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

#fix for error: No handlers could be found for logger "apscheduler.executors.default"
import logging
logging.basicConfig()

#instantiate scheduler with config options as the arguments
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone = timezone('US/Pacific'))
scheduler.start()

#DATABASE 
#got instructions for creating db from: https://github.com/miguelgrinberg/Flask-Migrate

# create SQLAlchemy database instance


#create Migrate instance
migrate = Migrate(app, db)

#create Manager instance
#can now do migrations in terminal with -> python app.py db migrate
manager = Manager(app)
manager.add_command('db', MigrateCommand)


#routes index.html to the root of the web server
@app.route('/')
def index():
	return render_template('index.html', title='Home')

#Calls submit function when someone makes a POST request
@app.route('/submit/', methods=['POST'])
def submit():
	username = request.form['username']
	password = request.form['password']
	quarter = request.form['quarter']
	enroll_code = request.form['enroll_code']
	pass_time = request.form['passtime'] #MM/DD/YY HH:MM -> 2009-05-30 HH:MM:SS
	pass_time_arg = '20' + pass_time[6:8] + '-' + pass_time[0:2] + '-' + pass_time[3:5] + ' ' + pass_time[9:] + ':00'
	scheduler.add_job(goldSniper, 'date', run_date=pass_time_arg, args=[username,password,quarter,enroll_code])
	return render_template('index.html', title="Success")

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %
			(form.openid.data, str(form.remember_me.data)))
		return redirect('/')
	return render_template('login.html',
							title='Sign In',
							form=form,
							providers=app.config['OPENID_PROVIDERS'])

# Basically, if we are using app.py as the main module
# i.e. If we execute 'python app.py'
if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000

	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
	manager.run()
