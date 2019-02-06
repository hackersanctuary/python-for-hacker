import socket
import argparse
import threading
from queue import Queue

cheks = {}
TCP_TIMEOUT = 5
hostPort_queue = None

def parsePorts( buf ):
	res = []

	if "-" in buf:
		res = [int(i) for i in range( int( buf.split( '-' )[ 0 ] ), int( buf.split( '-' )[ 1 ] ) + 1 ) ]
	else:
		res = [ int( buf ) ]

	return res

def init_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument( "ip", type = str,
                    help = "target ip-addr" )
	parser.add_argument( "-p", type=str,
                    help="set port or range	with separator '-'" )

	return parser

def scanPort( host, port ):
	sock = socket.socket()
	sock.settimeout( TCP_TIMEOUT )

	try:
		sock.connect( ( host, port ) )
		cheks[ host + ":" + str( port ) ] = 'up'
	except:
		cheks[ host + ":" + str( port ) ] = 'down'

	sock.close()

def runner():
    while 1:
        host, port = hostPort_queue.get()
        scanPort( host, port )
        hostPort_queue.task_done()


if __name__ == "__main__":

	args = init_parser().parse_args()

	target_ip = args.ip
	ports = parsePorts( args.p )

	hostPort_queue = Queue()

	for _ in range( 50 ):
		thread = threading.Thread( target = runner )
		thread.daemon = True
		thread.start()

	for port in ports:
		hostPort_queue.put( (target_ip, port) )

	hostPort_queue.join()

	for i in cheks:
		if cheks[ i ] == 'up':
			print i, cheks[ i ]
