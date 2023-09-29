import random
import string
from rpcloginuser import log_user
import psycopg2
characters = string.ascii_letters + string.digits



conn = psycopg2.connect(database='mobile_sav',
                          user = 'postgres',
                          password='1234',
                          host='10.68.132.2',
                          port='5432')

curs = conn.cursor()

curs.execute(""" SELECT id FROM viseo_account_user""")

rows = curs.fetchall()
if rows:
    for row in rows:
        password = ''.join(random.choice(characters) for i in range(8))
        query = """UPDATE public.viseo_account_user
	                SET password=%s,login=%s
	                    WHERE id= %s;
                    """
        curs.execute(query,(password,row[0],row[0]))
        log_user(row[0],password)
        print(row[0], password, "Created success")
        
        conn.commit()