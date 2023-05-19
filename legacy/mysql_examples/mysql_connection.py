import os
from sqlalchemy import create_engine


class Mysql_connector:
    def __init__(self, host, db) -> None:
        self.port = 3306
        self.host = host
        self.db = db
        self.connection = self.set_connection()

    def set_connection(self):
        cnx = create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            os.environ['USER'],
            os.environ['PASSWORD'],
            self.host, 
            self.port, 
            self.db
        ))
        print(os.environ['PASSWORD'])
        connection = cnx.connect()
        return connection

    def get_conenction(self):
        return self.connection
    
    def close_connection(self):
        self.connection.close()

    def create_schema(self):
        pass

test = Mysql_connector("localhost", "flights")