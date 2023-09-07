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
conn = psycopg2.connect(database='odoo_mobile',
                          user = 'postgres',
                          password='1234',
                          host='10.68.132.2',
                          port='5432')

cur = conn.cursor()
while True:
# Créez un curseur pour exécuter des requêtes SQL
    
    
# Récupérez la liste des tables dans le schéma public (ou modifiez le schéma au besoin)
        #cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        #tables = cur.fetchall()

# Créez un dictionnaire pour stocker les données précédentes des tables
        anciennes_donnees = {}
        table_exlure = ['viseo_rdv_mobile_viseo_rdv_mobile','fleet_claim','viseo_api_devis','viseo_api_chatconversation']
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
                
                cur.execute(f"SELECT * FROM {table};")
                nouvelles_lignes = cur.fetchall()
        

        
        # Comparez chaque ligne avec les données précédentes
                for i in range(len(nouvelles_lignes)):
                    if nouvelles_lignes[i] != anciennes_rows[i]:
                        print(f"Modification détectée dans la table {table_name}, ligne {i}.")
                        
        # Mettez à jour les données précédentes avec les données actuelles
                        anciennes_donnees[table] = nouvelles_lignes
                        print(nouvelles_lignes[i])
            else:
                countb= count
                print("Record created", countb)
                time.sleep(1)
                
        

# Fermez le curseur et la connexion
    
        
        
    
