import pywhatkit
import time
import random
import pyautogui
from pynput.keyboard import Key, Controller
current_time = time.localtime()
hour = current_time.tm_hour
minute = current_time.tm_min + 1
keyboard = Controller()
number = "+261384900555"
sms= "Bonjour ceci est un test d'envoi"
send = pywhatkit.sendwhatmsg_instantly(
    number, 
    sms,
    5,
    False,
    15
    )

time.sleep(1)
pyautogui.click()
time.sleep(1)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(5)
with keyboard.pressed(Key.ctrl.value):
    keyboard.press('w')
    keyboard.release('w')

print("Tab closed...")
if send:
    print("Message send succeffully")
else:
    print("Error, send message")