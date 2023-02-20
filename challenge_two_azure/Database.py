
import mysql.connector
import pymongo
import logging
logging.basicConfig(filename='log/app.log', filemode='w',level=logging.INFO)

class Database():
    def mysql_connect(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="challengtwo"
            )
            return  mydb
        except:
            logging.info('MYSQL connection issue')

    def mongodb(self):
        client = pymongo.MongoClient("mongodb+srv://hossainf114:password_mongo@cluster0.s1pyppv.mongodb.net/?retryWrites=true&w=majority")
        db = client.inuron
        return db

    def create_database(self):
        db = self.mysql_connect()
        cursor = db.cursor()
        try:
            cursor.execute('DROP TABLE `details`, `comments`')
        except:
            logging.info('Table drop issue')

        try:
            cursor.execute('create table details(id int auto_increment primary key, title varchar(155), description longtext)')
        except:
            logging.info('Table already exist featurs')

        try:
            cursor.execute('create table comments(id int auto_increment primary key, details_id int, persion_name varchar(155), comment longtext)')
        except:
            logging.info('Table already exist featurs')

# obj = Database()
# obj.create_database()