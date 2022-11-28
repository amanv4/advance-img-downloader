from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from config import database_config
from Logger import Logging

logger_ins = Logging('Advance Image Extractor')  # Creating an instance of custom logger
logger_ins.initialize_logger()  # Instantiating the logger instance


class Connect_Database:

    def __init__(self):
        
        # This function will instantiate the session for the Cassandra database
    
        try:
            cloud_config = {
                'secure_connect_bundle': database_config.cloud_config_path
            }
            auth_provider = PlainTextAuthProvider(database_config.cassandra_client_id,
                                                  database_config.cassandra_client_secret)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = cluster.connect()

        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(__init__) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def connect_keyspace(self):
        
        # This function will use the given keyspace as the default method to work on.
       
        try:
            self.session.set_keyspace(database_config.keyspace_name)
        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(connect_keyspace) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def create_table(self):
        
        # This function will create the table if it does not exists in the keyspace
    
        try:
            self.session.execute('CREATE TABLE IF NOT EXISTS {} '
                                 '(id UUID, email text, url text, PRIMARY KEY (id, email, url));'
                                 .format(database_config.table_name))
        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(create_table) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def select_query(self, req_id):
        
        # This function will execute and return the select query on the table

        try:
            return self.session.execute('SELECT id, email, url FROM {} WHERE id={}'.format(database_config.table_name,
                                                                                           req_id))
        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(select_query) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def insert_url(self, uuid, email, url):
       
       # This function will insert the data into the table

        try:
            self.session.execute(
                "INSERT INTO " + database_config.table_name + " (id, email, url) VALUES (%s, %s, %s)",
                (uuid, email, url))

        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(insert_url) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def shutdown(self):
       
        # This function will close the cassandra session
    
        try:
            self.session.shutdown()
        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(shutdown) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def delete_url(self, req_id):
        
        # This function will delete the url for given request ID

        try:
            self.session.execute('DELETE FROM {} WHERE id={}'.format(database_config.table_name, req_id))
        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(shutdown) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def drop_table(self):
       
        # This function will drop the given table from the keyspace

        try:
            self.session.execute('DROP TABLE IF EXISTS {}'.format(database_config.table_name))
        except Exception as e:
            logger_ins.print_log('(Connect_Database.py(drop_table) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)
