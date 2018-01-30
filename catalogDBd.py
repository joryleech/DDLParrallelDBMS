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
	
	data = conn.recv(4096).decode()
	dataSplit=data.split("\n&\n")
	DDLData=dataSplit[1]
	NodeData=dataSplit[0]
	print("Server Recieved Full-Data:" + str(data))
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
		for sent in NodeData.split("\n"):
			sentT=sent.split(":")
			if(sentT[0]=="Driver"):
				nodedriver=sentT[1]
			if(sentT[0]=="hostname"):
				nodeurl=sentT[1]
		print("tname:"+tname.split("(")[0]+"\nNodeURL:"+nodeurl+"\nnodeDriver:"+nodedriver)
		sql = "INSERT INTO DTABLES(tname, nodedriver, nodeurl, nodeuser, nodepasswd,partmtd,nodeid,partcol, partparam1, partparam2) VALUES(?,?,?,?,?,?,?,?,?,?)"
		dbConnection.execute(sql,[tname,nodedriver,nodeurl,None,None,None,None,None,None,None])
		message = "SQL Command Succeeded: Success"
		print("The Insert Was Performed Successfully")
	except(sqlite3.Error) as e: 
		print("Failed" + str(e))
		message = "SQL Command Failed:\n"+str(e)
	conn.close()
dbConnection.close()

