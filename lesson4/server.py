import SocketServer
import sys 
from hashlib import md5
import threading
import time

password_hash = '5f4dcc3b5aa765d61d8327deb882cf99'

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
    	self.request.sendall( "Auth panel\nEnter the username: ")
        username = self.request.recv( 1024 ).strip()

        if username != "admin":
        	self.request.sendall( "[-] Username is invalid!\nExit\n" )
        	return -1

        self.request.sendall( "Enter the password: " )
        password = self.request.recv( 1024 ).strip()

        if md5( password ).hexdigest() != password_hash:
        	self.request.sendall( "[-] Password is invalid!\nExit\n" )
        	return -2

        self.request.sendall( "Welcome admin!\n" )

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":

	if len( sys.argv ) > 1:
		port = int( sys.argv[ 1 ] )
	else:
		print "Usage python " + sys.argv[ 0 ] + " <port>"
		sys.exit( -1 )

	HOST, PORT = "0.0.0.0", port

	server = ThreadedTCPServer( ( HOST, PORT ), RequestHandler )
	ip, port = server.server_address

	server_thread = threading.Thread( target = server.serve_forever )
	server_thread.daemon = False
	server_thread.start()

	while True:
		try:
			time.sleep( 1 )
		except:
			break

	server.shutdown()
	server.server_close()
