import ssl
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile='./conf/ssl/localhost.crt')
context.load_cert_chain(certfile='./conf/ssl/localhost.crt', keyfile='./conf/ssl/localhost.key')

url = 'wss://localhost:8182/gremlin'
remoteConn = DriverRemoteConnection(url, 'g', ssl=context)

g = traversal().withRemote(remoteConn)
g.addV('person').property('name','marko').next()
results = g.V().elementMap().toList()
for result in results:
    print(result)

remoteConn.close()