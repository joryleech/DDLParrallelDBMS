import socket
import sqlite3
import sys
if(len(sys.argv)<3):
	print("Please Specify IPAddress and Port as Arg1 and Arg2 respectively")
	exit()
IPAddress = sys.argv[1]
Port = sys.argv[2]

print("Connecting to the DBMS")
dbConnection = sqlite3.connect("catalogDB")

print("Running Server Program")
mySocket=socket.socket()
mySocket.bind((IPAddress,int(Port)))

#Attempts to create a database table
try:
	dbConnection.execute("CREATE TABLE DTABLES(tname char(32), nodedriver char(64), nodeurl char(128), nodeuser char(16), nodepasswd char(16), partmtd int, nodeid int, partcol char(32),partparam1 char(32),partparam2 char(32))")
	dbConnection.commit()
	print("Successfully Created Table")
except(sqlite3.Error) as e:
	print("Catalog Table Already Exists:"+str(e))
		

quit=0
while quit == 0:
	print("Beginning Listening")
	mySocket.listen(1)
	conn,addr = mySocket.accept()
	print("Server Connection From "+ str(addr))
	
	NodeData = conn.recv(4096).decode()
	print("Server Recieved Node Data:" + str(NodeData))
	mySocket.send(("Recieved").encode())
	DDLData = conn.recv(4096).decode()
	mySocket.send(("Recieved").encode())
	print("Server Recieved DDL Data:" + str(DDLData))
	if(str(data).rstrip=="quit"):
		quit=1
		break
	try: 
		tname=""
		nodedriver=""
		nodeurl=""
		foundWord=0
		for word in DDLData.split():
			if foundWord==1:
				tname=word	
				break
			if(word=="TABLE"):
				foundWord=1
		sql = "INSERT INTO DTABLES(tname, nodedriver, nodeurl, nodeuser, nodepasswd,partmtd,nodeid,partcol, partparam1, partparam2) VALUES(?,?,?,?,?,?,?,?,?,?)"
		message = "SQL Command Succeeded: Success"
		conn.send(message.encode())
	except(sqlite3.Error) as e: 
		print("Failed" + str(e))
		message = "SQL Command Failed:\n"+str(e)
		conn.send(message.encode())
	conn.close()
dbConnection.close()

