import psycopg2

def dbconnex(self):
    connex = psycopg2.connect(database='mobile_test',
                               user='openpg',
                               password='1234',
                               host='localhost',
                               port='5432')
    curs = connex.cursor()

    return curs, connex