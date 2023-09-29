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



server_url = 'http://formation.viseo.erp'
db = 'viseo13_20230705_0830'
username = 'admin'
password = '@dm1n123!'

common = xmlrpc.client.ServerProxy(server_url+'/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(server_url + '/xmlrpc/2/object', transport=AllowNoneTransport())

def log_user(data,passwd):
    
    rdv= {
        'passwd':passwd,
        'login':data
    }
    rdv_id = models.execute_kw(db, uid,password, 'res.partner', 'write', [[data],rdv])
    if rdv_id:
        print("Login created...")