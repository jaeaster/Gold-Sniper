import requests
from lxml import html
import mechanize

class FakeLink(object):
	def __init__(self,url):
		self.absolute_url = url

class GoldSniper(object):

	def __init__(self): #initializes url, concert, and browser data
		self.url = "https://my.sa.ucsb.edu/gold/Login.aspx"
		self.browser = mechanize.Browser()
		self.browser.set_handle_robots(False)

	def resetURL(self, url): #Changes the URL attribute to given parameter
		self.url = url

	def openPage(self): #Opens the page of the current URL
		self.browser.open(self.url) # May need to save in variable or return the value

	def listForms(self): #lists all of the forms on the current url
		for form in self.browser.forms():
			print "Form name: ", form.name
			print form

	def listLinks(self): #lists all the links on the current url
		for link in self.browser.links():
			print link.text, link.url

	def listControls(self,formName): #Lists all of the controls for a given form
		self.browser.select_form(formName)
		for control in self.browser.form.controls:
			print control
			print "type=%s, name=%s, value=%s" % (control.type, control.name, self.browser[control.name])

	def login(self, username, password): #logs in to stubhub.com account
		self.openPage()
		self.browser.select_form(nr=0)
		self.browser["ctl00$pageContent$userNameText"] = username
		self.browser["ctl00$pageContent$passwordText"] = password
		response = self.browser.submit()

	def setQuarter(self, quarter):
		self.browser.follow_link(FakeLink("https://my.sa.ucsb.edu/gold/StudentSchedule.aspx"))
		self.browser.select_form(nr=0)
		self.browser["ctl00$pageContent$quarterDropDown"] = ["20154",]
		response = self.browser.submit()
		#ctl00$pageContent$quarterDropDown

	def snipeCourse(self,enroll_code):
		self.browser.select_form(nr=0)
		self.browser["ctl00$pageContent$EnrollCodeTextBox"] = enroll_code
		forms = self.browser.forms()
		i = 0
		for form in forms:
			request = form.click(name="ctl00$pageContent$AddCourseButton")
			response = self.browser.open(request)

		self.browser.select_form(nr=0)
		forms = self.browser.forms()
		for form in forms:
			request = form.click(name="ctl00$pageContent$AddToScheduleButton")
			response = self.browser.open(request)

	def logout(self):
		self.browser.follow_link(FakeLink("https://my.sa.ucsb.edu/gold/Logout.aspx"))

	def goldSniper(self,username,password,quarter,enroll_code):
		self.login(username,password)
		self.setQuarter(quarter)
		self.snipeCourse(enroll_code)
		self.logout()
