import socket
import sqlite3
import sys
if(len(sys.argv)<3):
	print("Please Specify IPAddress and Port as Arg1 and Arg2 respectively")
	exit()
IPAddress = sys.argv[1]
Port = sys.argv[2]

print("Connecting to the DBMS")
dbConnection = sqlite3.connect("dbfile")

print("Running Server Program")

mySocket=socket.socket()

mySocket.bind((IPAddress,int(Port)))
quit=0
while quit == 0:
	print("Beginning Listening")
	mySocket.listen(1)
	conn,addr = mySocket.accept()
	print("Server Connection From "+ str(addr))
	data = conn.recv(4096).decode()
	print("Server Recieved:" + str(data))
	if(str(data).rstrip=="quit"):
		quit=1
		break
	try: 
		dbConnection.execute(str(data))
		dbConnection.commit()
		message = "SQL Command Succeeded"
		conn.send(message.encode())
	except(sqlite3.Error) as e: 
		print("Failed" + str(e))
		message = "SQL Command Failed:\n"+str(e)
		conn.send(message.encode())
	conn.close()
dbConnection.close()

