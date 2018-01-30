import socket
import sqlite3
if(len(sys.argv)<3):
	print("Please Specify IPAddress and Port as Arg1 and Arg2 respectively")
	exit()
IPAddress = sys.argv[1]
Port = sys.argv[2]

print("Connecting to the DBMS")
conn sqlite3.connect("dbfile")

print("Running Server Program")

mySocket=socket.socket()

mySocket.bind((IPAddress,Port))
print("Beginning Listening")
mySocket.listen(1)
conn,addr = mySocket.accept()
print("Server Connection From "+ str(addr))

data = conn.recv(4096).decode()
print("Server Recieved:" + str(data))

