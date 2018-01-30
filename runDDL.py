import socket
import sys
import re
class Node:
	nodeNumber=0
	driver=""
	hostname=""
	def __init__(self,number):
		self.nodeNumber=number
	def __str__(self):
		return "Node#:"+self.nodeNumber+"\nDriver:"+self.driver+"\nhostname:"+self.hostname
def printDivideLine():
	print("-------------------------------------------")
def setNodes(listOfNodes, nodeID, infoType, value):
	IDExists=0
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
for line in clustercfg:
	if(line!="\n"):
		temp = line.split("=")
		tempvalue=temp[1].rstrip()
		tempnode=re.findall(r'\d+', temp[0].split(".")[0])[0]
		tempinfo=temp[0].split(".")[1].rstrip()
		setNodes(listOfNodes,tempnode,tempinfo,tempvalue)

clustercfg.close()
printDivideLine()
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
	print("Connecting to Node#:"+node.nodeNumber)
	splitHost = node.hostname.split(":")
	print("IPAddress:"+splitHost[0]+" || Port:"+ splitHost[1])
	mySocket.connect((splitHost[0],int(splitHost[1].split("/")[0])))


