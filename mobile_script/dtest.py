import psycopg2
import time

tables = ['viseo_api_rendezvous','viseo_api_devis','viseo_api_chatconversation']
connex = psycopg2.connect(database='mobile_test',
                          user='openpg',
                          password='1234',
                          host='localhost',
                          port = '5432')

curs = connex.cursor()
last_state = {table: None for table in tables}

while True:

        for table in tables:
            curs.execute(f"SELECT COUNT(*) FROM {table};")
            count = curs.fetchone()[0]
        #count = len(rows))
            countb = last_state[table]
            if countb == count:
                time.sleep(2)
            else:
                last_state[table] = count
                curs.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1")
                data = curs.fetchall()
                print(table, data)
                time.sleep(1)
                
           
      
           