from python_orange_sms import utils

def sms(phone):
    SENDER_NAME = 'OceanTrade' 
    AUTH_TOKEN = 'Basic cGxST2tGUjdoQXEwZkRwVDdqb0FhekRHMU54ZEtOenE6c2luUnVOSjBOek54TjNVYQ==' 

    message = "Bonjour, bienvenue à Gallaxy Village, merci de voir KFP" 
    recipient_phone_number="261344900642" 
    dev_phone_number='261326043944' 

    sms = utils.SMS(AUTH_TOKEN = AUTH_TOKEN, SENDER_NAME= SENDER_NAME )
    res = sms.send_sms(message=message,
              dev_phone_number=dev_phone_number,       recipient_phone_number=recipient_phone_number )

    print(res)

    if res.status_code == 201:
        print('EVERYTHING RIGHT : ', res.text)
        print('SMS sent successfully!!!') 
    else:
        print('SAME THING WRONG : ', res.text) 