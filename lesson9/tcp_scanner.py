import socket
import argparse

cheks = {}

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

if __name__ == "__main__":

	args = init_parser().parse_args()

	target_ip = args.ip
	ports = parsePorts( args.p )

	for port in ports:
		sock = socket.socket()
		sock.settimeout( 3 )

		try:
			sock.connect( ( target_ip, port ) )
		except:
			cheks[ target_ip + ":" + str( port ) ] = 'down'
			continue

		cheks[ target_ip + ":" + str( port ) ] = 'up'
		sock.close()

	for i in cheks:
		if cheks[ i ] == 'up':
			print i, cheks[ i ]
