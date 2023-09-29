from datetime import datetime, timedelta
import random
#print(datetime.date.today())

import xmlrpc.client
#import datetime
class AllowNoneTransport(xmlrpc.client.Transport):
    def __init__(self, use_datetime=False, allow_none=True):
        super().__init__(use_datetime)
        self.allow_none = allow_none
        
    def get_encoder(self, *args, **kwargs):
        encoder = super().get_encoder(*args, **kwargs)
        encoder.allow_none = self.allow_none
        return encoder
    

start_date = datetime.now()
start_date = datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S')
start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
#start_date = datetime.strptime(str(start_date), '%Y-%m-%d %H:%M:%S')
server_url = 'http://127.0.0.1:8081'
db = 'analytic_odoo'
username = 'admin'
password = 'p@5dM_'

common = xmlrpc.client.ServerProxy(server_url+'/xmlrpc/2/common')

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(server_url + '/xmlrpc/2/object', transport=AllowNoneTransport())

    
imran = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7154,
    'place': 10,
    'vehicle_id':9056,
    'note':'Entretien 2500km',
}
zoheir = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7155,
    'place': 11,
    'vehicle_id':6027,
    'note':'Entretien 5000km',
}
zara = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7156,
    'place': 12,
    'vehicle_id':8103,
    'note':'Entretien 5000km',
}
latifa = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'state':'entretient',
    'status':'accepted',
    'mecano': 7157,
    'place': 13,
    'vehicle_id':5348,
    'note':'Entretien 5000km',
}
jisca = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7158,
    'place': 14,
    'vehicle_id':8194,
    'note':'Entretien 5000km',
}
tovo = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7159,
    'place': 15,
    'vehicle_id':8962,
    'note':'Entretien 5000km',
}
roumana = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7160,
    'place': 16,
    'vehicle_id':7687,
    'note':'Entretien 5000km',
}

andry = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7161,
    'place': 17,
    'vehicle_id':4199,
    'note':'Entretien 5000km',
}
mourtaza = {
    'user_id':2,
    'atelier':6,
    'choice':'pl',
    'staten':1,
    'status':'accepted',
    'mecano': 7162,
    'place': 18,
    'vehicle_id':8243,
    'note':'Entretien 5000km',
}

table = [imran,zoheir,zara, jisca,roumana,andry,mourtaza,tovo,latifa]

for i in table:
    record_id = models.execute_kw(db, uid,password, 'viseo_rdv_mobile.viseo_rdv_mobile', 'create', [i])

    if record_id:
        print("RDV create successfully")
    else:
        print("Error")