import ssl
import os
import traceback
from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __ as anonTrav
from gremlin_python.process.traversal import P, Cardinality, TextP, T, Order, Column
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

os.environ['APP_ENV'] = "DEV"
os.environ['NEPTUNE_ENDPOINT'] = "localhost"
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile='./conf/ssl/localhost.crt')
context.load_cert_chain(certfile='./conf/ssl/localhost.crt', keyfile='./conf/ssl/localhost.key')

class gremlinConnector(object):
    def __init__(self, write: bool):
        self.write = write

    def __enter__(self):
        # Setup connection to DB
        try:
            if self.write == True:
                if os.environ['APP_ENV'] == 'DEV': # turn off ssl verification on local only due to self-signed certs
                    url = 'wss://' + os.environ['NEPTUNE_ENDPOINT'] + ':8182/gremlin'
                    self.remoteConn = DriverRemoteConnection(url, 'g', ssl=context)
                else:
                    url = 'wss://' + os.environ['NEPTUNE_ENDPOINT'] + ':8182/gremlin'
                    self.remoteConn = DriverRemoteConnection(url, 'g')
                self.g = traversal().withRemote(self.remoteConn)
            else:
                if os.environ['APP_ENV'] == 'DEV': # turn off ssl verification on local only due to self-signed certs
                    url = 'wss://' + os.environ['NEPTUNE_ENDPOINT'] + ':8182/gremlin'
                    self.remoteConn = DriverRemoteConnection(url, 'g', ssl=context)
                else:
                    url = 'wss://' + os.environ['NEPTUNE_ENDPOINT'] + ':8182/gremlin'
                    self.remoteConn = DriverRemoteConnection(url, 'g')
                self.g = traversal().withRemote(self.remoteConn).withStrategies(ReadOnlyStrategy())
            return self.g
        except Exception as e:
            # Let us know when things go wrong
            print('Encountered the following while connected to the database: ' + str(e))
            traceback.print_exc()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remoteConn.close()

context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile='./conf/ssl/localhost.crt')
context.load_cert_chain(certfile='./conf/ssl/localhost.crt', keyfile='./conf/ssl/localhost.key')

with gremlinConnector(write = True) as g:
    g.addV('person').property('name','marko').next()
    print(g.V().elementMap().toList())