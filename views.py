import requests
import os


from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
	  template = loader.get_template("goldsniper/index.html")
    return HttpResponse(template.render())

def submit(request):
	if request.mehtod == 'POST':
		import app.py
    



# def db(request):

#     greeting = Greeting()
#     greeting.save()

#     greetings = Greeting.objects.all()

#     return render(request, 'db.html', {'greetings': greetings})

