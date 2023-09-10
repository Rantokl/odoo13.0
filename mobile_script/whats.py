import pywhatkit
import time
import random
current_time = time.localtime()
hour = current_time.tm_hour
minute = current_time.tm_min + 1
def sendmes(number, sms):
    send = pywhatkit.sendwhatmsg_instantly(
        number, 
        sms,
        15,
        True,
        5
        
    
    )
    if send:
        print("Message send succeffully")
    else:
        print("Error, send message")