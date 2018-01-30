import socket #Networking Library
import sys #System Library. Use: Controlling Arguments
import re #Regular Expression Library: Use parsing files.
######
#Class: Node
#Function:Holds information about each node to encapsulate for single purpose.
#
######
class Node:
	nodeNumber=0
	driver=""
	hostname=""
	def __init__(self,number):
		self.nodeNumber=number
	def __str__(self):
		return "Node#:"+str(self.nodeNumber)+"\nDriver:"+str(self.driver)+"\nhostname:"+str(self.hostname)
######
#Name: Print Divide Line
#Function: Prints a single line across the screen to improve readability
#
######
def printDivideLine():
	print("-------------------------------------------")

#Catalog node arbitrary number, since not a regular node. 
global catalog 
catalog = Node(-1)

######
#Name: Set Nodes
#Function: Takes information and sets node objects to the proper values
#
######
def setNodes(listOfNodes, nodeID, infoType, value):
	IDExists=0 #If node doesn't exist create the node
	for item in listOfNodes:
		if(item.nodeNumber==nodeID):
			currentNode=item
			IDExists=1
			break
	if(IDExists==0):
		print("Adding Node#"+nodeID+" to List of Nodes")
		currentNode=Node(nodeID)		
		listOfNodes.append(currentNode)
	if(infoType=="driver"):
		currentNode.driver=value
	if(infoType=="hostname"):
		currentNode.hostname=value
######
#Name: Set Nodes
#Function: As Set Nodes but for global catalog
#
######
def setCatalog(infoType, value):
	if(infoType=="driver"):
		catalog.driver=value
	if(infoType=="hostname"):
		catalog.hostname=value

#Manages Parameters for the program, 
#Arg1 = clustercfg file
#Arg2 = ddl file
if(len(sys.argv)<3):
	print("Please Specify ClusterCFG and DDLFile as Arg1 and Arg2 respectively")
	exit()
clustercfg = sys.argv[1]
ddlfile = sys.argv[2]
print("ClusterCFG="+clustercfg)
print("ddlfile="+ddlfile)
print("Reading ClusterCFG File")
clustercfg = open(clustercfg,"r")
listOfNodes=[]

#Parses the clustercfg file for pertinant information about regular nodes.
for line in clustercfg:
	if(line!="\n"):
		temp = line.split("=")
		tempvalue=temp[1].rstrip()
		tempinfo=temp[0].split(".")[1].rstrip()
		if("catalog" in temp[0]):
			setCatalog(tempinfo,tempvalue)
		else:
			tempnode=re.findall(r'\d+', temp[0].split(".")[0])[0]
			setNodes(listOfNodes,tempnode,tempinfo,tempvalue)
clustercfg.close()
printDivideLine()

#Reads DDL into memory so that it may be sent later. Uses concatenation to avoid readline constraints.
print("Catalog:")
print(catalog)
print("Nodes:")
for item in listOfNodes:
	print(item)
printDivideLine()
print("Reading DDL to Memory")
ddlContents =""
ddlfile = open(ddlfile,"r")
for line in ddlfile:
	ddlContents+=line;
print(ddlContents)
printDivideLine()

mySocket= socket.socket()
print("Beginning Connection to Nodes")
for node in listOfNodes:
	try:
		print("Connecting to Node#:"+node.nodeNumber)
		splitHost = node.hostname.split(":")
		print("IPAddress:"+splitHost[0]+" || Port:"+ splitHost[1])
		mySocket.connect((splitHost[0],int(splitHost[1].split("/")[0])))
		mySocket.send(ddlContents.encode())
		data = mySocket.recv(4096).decode()
		print("Node["+node.nodeNumber+"] Results:"+data)
		mySocket.close()
	except:
		print("Failed, unable to connect to node#"+node.nodeNumber)

