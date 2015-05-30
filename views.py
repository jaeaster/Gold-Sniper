from flask import Flask, render_template, request, url_for
from GoldSniper import *
import getpass

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/submit/', methods=['POST'])
def submit():
	username=request.form['username']
	password=request.form['password']
	quarter=request.form['quarter']
	enroll_code=request.form['enroll_code']
	sniper = GoldSniper()
	sniper.goldSniper(username,password,quarter,enroll_code)
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)    




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
