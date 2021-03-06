from collections import namedtuple
from bitarray import bitarray
from threading import Thread

class frame:
	def __init__(self):
		self.frame_data = namedtuple("MyFrame", "SOF ID RTR IDE R0 DLC DATA CRC ACK EOF IFS")
		self.frame_remote = namedtuple("frame_remote","SOF ID RTR IDE R0 DLC CRC ACK EOF IFS")
		self.frame_error = namedtuple("frame_error","DATA FLAG DEL OVERLOAD")
		self.frame_overload = namedtuple("frane_overload","FLAG ACTIVE DEL")
	def dataframe(self,a):
		SOF=bitarray(7)
		ID=bitarray(11)
		RTR=bitarray(1)
		IDE=bitarray(1)
		R0=bitarray(1)
		DLC=bitarray(4)
		DATA=bitarray(a)
		CRC=bitarray(16)
		ACK=bitarray(2)
		EOF=bitarray(7)
		IFS=bitarray(7)
		return(SOF+ID+RTR+IDE+R0+DLC+DATA+CRC+ACK+EOF+IFS)
	def remoteframe(self):
		SOF=bitarray(7)
		ID=bitarray(11)
		RTR=bitarray(1)
		IDE=bitarray(1)
		R0=bitarray(1)
		DLC=bitarray(0)
		CRC=bitarray(16)
		ACK=bitarray(2)
		EOF=bitarray(7)
		IFS=bitarray(7)
		return(self.frame_remote(SOF,ID,RTR,IDE,R0,DLC,CRC,ACK,EOF,IFS))
	def errorframe(self):
		DATA=bitarray(64)
		FLAG=bitarray(12)
		DEL=bitarray(8)
		OVERLOAD=bitarray(20)
		return(self.frame_error(DATA,FLAG,DEL,OVERLOAD))
	def overloadframe(self):
		FLAG=bitarray(12)
		ACTIVE=bitarray(6)
		DEL=bitarray(8)
		return(self.frame_overload(FLAG,ACTIVE,DEL))
import socket
from threading import Thread

sock=socket.socket()
port=12345
sock.connect(('',port))

f1=frame()

def sendd():
	while True:
		
		a = raw_input('message:')
		s = "".join(format(ord(x), 'b') for x in a)
		print(s)
		start = 0
		end = 64
		length = len(s)
		while True:
			if end < length:
				rr = f1.dataframe(s[start:end])
				print(len(rr))
				sock.send(rr)
				start+=64
				end+=64
			else:
				for i in range(length,end):
					s+='0'
				sock.send(f1.dataframe(s[start:end]))
				break
		if a=='close':
			break

	sock.close()

def received():
	while True:
	
		message=sock.recv(1024)
		print "client :",message
		if message=='close':
			break
	sock.close()	

t1=Thread(target=sendd)
t2=Thread(target=received)

t1.start()
t2.start()

t1.join()
t2.join()

