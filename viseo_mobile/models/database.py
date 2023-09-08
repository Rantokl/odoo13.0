import psycopg2

def dbconnex(self):
    connex = psycopg2.connect(database='mobile_test',
                               user='postgres',
                               password='1234',
                               host='10.68.132.2',
                               port='5432')
    curs = connex.cursor()

    return curs, connex