from GoldSniper import *
import getpass

"""username = str(raw_input("Please enter GOLD username: "))
password = getpass.getpass("Please enter your password: ")
"""

username = "vonmeier"
password = "C871d97d"
quarter = "20154"
enroll_code = "58677"
sniper = GoldSniper()
"""sniper.login(username,password)
#sniper.listLinks()
sniper.setQuarter("20154") #Fall
sniper.snipeCourse("58677")


#enroll_code = 58677
"""
sniper.goldSniper(username,password,quarter,enroll_code)
