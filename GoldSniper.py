import requests
from lxml import html
import mechanize

# Define a FakeLink class to use for javascript-based links
# mechanize cannot handle javascript links so this class
# is a work around for that issue
class FakeLink(object):
	def __init__(self,url):
		self.absolute_url = url

# opens the url in a given instance of a mechanize.Browser() object
def openPage(url,browser): #Opens the page of the current URL
	browser.open(url) # May need to save in variable or return the value

# lists forms on the currently opened page in a browser instance
def listForms(browser):
	for form in browser.forms():
		print "Form name: ", form.name
		print form

# lists links on the currently opened page in a browser instance
def listLinks(browser): #lists all the links on the current url
	for link in browser.links():
		print link.text, link.url

# lists controls for a given form on the currently 
# opened page in a browser instance
def listControls(formName,browser):
	browser.select_form(formName)
	for control in browser.form.controls:
		print control
		print "type=%s, name=%s, value=%s" % (control.type, control.name, browser[control.name])

# Logs into Gold with given username and password
def login(username, password):
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	gold_url = "https://my.sa.ucsb.edu/gold/Login.aspx"

	openPage(gold_url, browser)
	browser.select_form(nr=0)
	browser["ctl00$pageContent$userNameText"] = username
	browser["ctl00$pageContent$passwordText"] = password
	response = browser.submit()
	return browser

# Navigates to Schedule page and changes quarter to given quarter
def setQuarter(quarter, browser):
	browser.follow_link(FakeLink("https://my.sa.ucsb.edu/gold/StudentSchedule.aspx"))
	browser.select_form(nr=0)
	browser["ctl00$pageContent$quarterDropDown"] = ["20154",] #Need to un-hardcode this
	response = browser.submit()
	return browser

# Enrolls in a course given the enrollment code for the course
def snipeCourse(enroll_code,browser):
	browser.select_form(nr=0)
	browser["ctl00$pageContent$EnrollCodeTextBox"] = enroll_code
	forms = browser.forms()
	i = 0
	for form in forms:
		request = form.click(name="ctl00$pageContent$AddCourseButton")
		response = browser.open(request)

	browser.select_form(nr=0)
	forms = browser.forms()
	for form in forms:
		request = form.click(name="ctl00$pageContent$AddToScheduleButton")
		response = browser.open(request)
	return browser

# Logs out of the currently logged in account
def logout(browser):
	browser.follow_link(FakeLink("https://my.sa.ucsb.edu/gold/Logout.aspx"))

# Wraps all of the above functions into one function
# This functions logs in, then sets the quarter, then snipes the course,
# and finally logs out.
def goldSniper(username,password,quarter,enroll_code):
	browser = login(username,password)
	browser = setQuarter(quarter,browser)
	browser = snipeCourse(enroll_code,browser)
	logout(browser)
