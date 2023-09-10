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
db = 'odoo_rfid'
username = 'admin'
password = 'p@5dM_'

common = xmlrpc.client.ServerProxy(server_url+'/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(server_url + '/xmlrpc/2/object', transport=AllowNoneTransport())

def rdv_vehicle(data):
    
    rdv= {
        'id':data[0][0],
        'message': data[0][1]
    }
    rdv_id = models.execute_kw(db, uid,password, 'mail.mail', 'create', [rdv])
    if rdv_id:
        print("RDV created...")