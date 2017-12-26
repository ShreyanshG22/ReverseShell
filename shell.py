import socket
import sys
import os
# Create socket
def socket_create():
	try:
		global host
		global port
		global s
		host = ''
		port = 2221
		s = socket.socket()
	except socket.error as err:
		print("Creation Error" + str(err))

#Bind
def socket_bind():
        try:
                global host
                global port
                global s
		print("Bind to " + str(port))
		s.bind((host, port))
		s.listen(5)
	except socket.error as err:
		print("Bind error",str(err),"\n")
		#socket_bind()

#Accept Connection
def socket_accept():
	conn, add = s.accept()
	print("Connected to",add[0],":",str(add[1]))
	send_commands(conn)
	conn.close()

#Send commands
def send_commands(conn):
	while True:
		cmd = raw_input()
		if cmd == "quit":
			conn.send(str.encode(cmd))
			conn.close()
			s.close() 
			sys.exit()
		if cmd[:4] == "copy":
			conn.send(str.encode(cmd))
			filesize = conn.recv(1024)
			f = open('new_' + cmd[5:],'wb')

			data = conn.recv(1024)
			Total = len(data)
			f.write(data)
			while Total < long(filesize) :
				data = conn.recv(1024)
				f.write(data)
				Total += len(data)
    			f.close()
    			continue
    		if cmd[:4] == "send":
    			if os.path.isfile(cmd[5:]):
    				filesize = os.path.getsize(cmd[5:])
				conn.send(str.encode(cmd + "TILL HERE"))
    				message = conn.recv(1024)
				if message == "SEND":
					conn.send(str(filesize))
					if conn.recv(1024) == "REALLY SEND" :
						f = open(cmd[5:], 'rb')
						l = f.read(1024)
						conn.send(l)
						l = f.read(1024)
						while l != "":      
							conn.send(l)
							l = f.read(1024)
						f.close()
			continue

		if len(str.encode(cmd)) > 0:
			conn.send(str.encode(cmd))
			client_response = str(conn.recv(5096))
			print(client_response), # , is equal to end='' from python3

def main():
	socket_create()
	socket_bind()
	socket_accept()

main()
