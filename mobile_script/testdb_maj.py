import psycopg2
import time

tables = ['viseoApi_rendezvous','viseoApi_devis','viseoApi_commentaire']
connex = psycopg2.connect(database='mobile_101023',
                          user='etech',
                          password='3Nyy22Bv',
                          host='10.68.132.2',
                          port = '5432')

curs = connex.cursor()
last_state = {table: None for table in tables}
anciennes_donnees = {}
while True:

        for table in tables:
            curs.execute(f"""SELECT COUNT(*) FROM public."{table}";""")
            count = curs.fetchone()[0]
        #count = len(rows))
            countb = last_state[table]
            curs.execute(f"""SELECT * FROM public."{table}";""")
            rows = curs.fetchall()
            count = len(rows)
            anciennes_donnees[table] = rows
            anciennes_rows = anciennes_donnees[table]
            if countb == count:
                time.sleep(2)
                curs.execute(f"""SELECT * FROM public."{table}";""")
                nouvelles_lignes = curs.fetchall()
        

        
        # Comparez chaque ligne avec les données précédentes
                for i in range(len(nouvelles_lignes)):
                    if nouvelles_lignes[i] != anciennes_rows[i]:
                        
                        print(f"Modification détectée dans la table {table}, ligne {i}.")
                        
        # Mettez à jour les données précédentes avec les données actuelles
                        anciennes_donnees[table] = nouvelles_lignes
                        print(nouvelles_lignes[i])
            
            else:
                last_state[table] = count
                curs.execute(f"""SELECT * FROM public."{table}" ORDER BY id DESC LIMIT 1""")
                data = curs.fetchall()
                print(table, data)
                time.sleep(1)
                
           
      
           