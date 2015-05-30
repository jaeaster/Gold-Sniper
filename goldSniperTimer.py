from datetime import datetime
from threading import Timer
from GoldSniper import *


username = "vonmeier"
password = "C871d97d"
quarter = "20154"
enroll_code = "58677"
sniper = GoldSniper()

userDateTime = str(raw_input('Please enter pass date and time in this format: mm/dd/yy HH:MM   :'))

try:
    dt_passtime = datetime.strptime(userDateTime, "%m/%d/%y %H:%M")
except ValueError:
    print "Incorrect date format (correct format: mm/dd/yy HH:MM)"

delta_t = dt_passtime - datetime.now()

if(delta_t < 0):
	delta_t = 0

secs = delta_t.seconds + 1

def beasterman():     #replace with snipertimer function
	print "jonathans penis is above average"

def mySnipe():
	sniper.goldSniper(username,password,quarter,enroll_code)

t = Timer(secs, mySnipe)
t.start()

