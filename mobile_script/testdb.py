import time
import psycopg2
import json

# Configurez votre connexion à la base de données PostgreSQL
conn_params = {
    "dbname": "odoo_mobile",
    "user": "postgres",
    "password": "1234",
    "host": "10.68.132.2",  # ou l'adresse IP de votre serveur PostgreSQL
    "port": "5432"  # Le port par défaut de PostgreSQL est 5432
}

# Établissez une connexion à la base de données
database = 'odoo_mobile'
countb =0
conn = psycopg2.connect(database='mobile_sav',
                          user = 'postgres',
                          password='1234',
                          host='10.68.132.2',
                          port='5432')

cur = conn.cursor()

while True:
# Créez un curseur pour exécuter des requêtes SQL
    
    try:
# Récupérez la liste des tables dans le schéma public (ou modifiez le schéma au besoin)
        #cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        #tables = cur.fetchall()

# Créez un dictionnaire pour stocker les données précédentes des tables
        anciennes_donnees = {}
        table_exlure = ['viseo_api_rendezvous','viseo_api_reclamation','viseo_api_devis','viseo_api_chatconversation']
# Bouclez sur chaque table pour vérifier si elle a changé
        for table in table_exlure:
            table_name = table
        
    # Si la table n'est pas déjà enregistrée, initialisez-la avec les données actuelles
        #if table_name not in anciennes_donnees:
            cur.execute(f"SELECT * FROM {table};")
            rows = cur.fetchall()
            count = len(rows)
            anciennes_donnees[table] = rows
            anciennes_rows = anciennes_donnees[table]
        #if:
        # Comparez les données actuelles avec les données précédentes
            if countb == count:
                
                    cur.execute(f"SELECT * FROM {table_name};")
                    nouvelles_lignes = cur.fetchall()
        

        
        # Comparez chaque ligne avec les données précédentes
                    for i in range(len(nouvelles_lignes)):
                        if nouvelles_lignes[i] == anciennes_rows[i]:
                        
                            time.sleep(2)
                        else:
                            
                        
                            print(f"Modification détectée dans la table {table_name}, ligne {i}.")
                        
        # Mettez à jour les données précédentes avec les données actuelles
                            anciennes_donnees[table] = nouvelles_lignes
                            print(nouvelles_lignes[i])
                            
            else:
                    countb= count
                    query = "SELECT * FROM {table_name}ORDER BY id DESC LIMIT 1 ;"
                    cur.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1 ;")
                    
                    data = cur.fetchall()
                    # for dt in data:
                    #     print(dt)
                    #if table_name == "viseo_api_rendezvous":    
                        #print("RDV", countb)
                    
                    #elif table_name =="viseo_api_reclamation":
                        #print("Reclamation",countb)
                    #elif table_name =="viseo_api_devis":
                        #print("Devis",countb)
                    #else:
                        #print("Devis",countb)
                    time.sleep(2)
            

        
                
                
    except Exception as e:
        print(e)
        conn.close()
        

# Fermez le curseur et la connexion
    
        
        
    
