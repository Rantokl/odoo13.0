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



server_url = 'http://localhost:8081'
db = 'analytic_odoo'
username = 'admin'
password = 'p@5dM_'

common = xmlrpc.client.ServerProxy(server_url+'/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(server_url + '/xmlrpc/2/object', transport=AllowNoneTransport())

def rdv_vehicle(data):
    
    rdv= {
        'id':data[0][0],
        'user_id':1,
        'staten':1,
        'vehicle_id':9056,
        'note':'Entretien 2500km',
    }
    rdv_id = models.execute_kw(db, uid,password, 'viseo_rdv_mobile.viseo_rdv_mobile', 'create', [rdv])
    if rdv_id:
        print("RDV created...")