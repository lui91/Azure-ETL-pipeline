from con_secrets import secret_handler
import mysql.connector

class Mysql_connector:
    def __init__(self, host, db) -> None:
        self.con_settings = secret_handler()
        self.host = host
        self.db = db
        self.connection = self.set_connection()

    def set_connection(self):
        cnx = mysql.connector.connect(user=self.con_settings.user, 
                                      password=self.con_settings.password,
                                      host=self.host,
                                      database=self.db)
        return cnx

    def get_conenction(self):
        return self.connection
    
    def close_connection(self):
        self.connection.close()