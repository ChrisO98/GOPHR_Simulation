#!/usr/bin/env python3
import math


DENSITY = 1 #samples/meter
f = open("/home/tjcc/catkin_ws/src/gophr/nav_scripts/waypointNodes.csv","r")
rawNodes = f.readlines()
f.close()

nodes=[]
for i in rawNodes:
	#print i
	nodes.append([float(i.split(",")[0]), float(i.split(",")[1])])


if len(nodes) <=1:
	print("Insufficient nodes to create waypoint, at least 2 required")
	exit()



lastNode = nodes[0]
print(lastNode)
nodes.pop(0) # takes off first node
nodes.append(lastNode) # first node is added as the last node, weird
print(nodes) # x,y coordinate sets

f = open("/home/tjcc/catkin_ws/src/gophr/nav_scripts/file.csv","w+")

for currentNode in nodes:
	x = len(nodes)-1
	if currentNode[0] == nodes[x][0]:
		print(currentNode[0])
		#f.write(str(currentNode[0])+","+str(currentNode[1])+","+str(0)+","+str(0)+"\n")
		#print(currentNode[0],currentNode[1],0)
		break 
	diffX = currentNode[0] - lastNode[0]
	diffY = currentNode[1] - lastNode[1]
	vertexLength = math.sqrt(diffX**2 + diffY**2)
	#print(diffX, diffY)
	#print(vertexLength)
	
	numberOfSubVertices = int(DENSITY * vertexLength)
	print(numberOfSubVertices)
	
	#To avoid division by zero and, it does not make sense to not have any intermediate points
	#between nodes
	if numberOfSubVertices <=0:
		numberOfSubVertices = 1
	subVertexLengthX = diffX / numberOfSubVertices
	subVertexLengthY = diffY / numberOfSubVertices
	
	headingAngle = math.atan(diffY / diffX)

		
	for i in range(numberOfSubVertices):
		xi = lastNode[0] + subVertexLengthX*i	
		yi = lastNode[1] + subVertexLengthY*i	
		
		#representing the heading in the quatration notation
		headingZ = (1 - math.cos(headingAngle))/2
		headingW = (1 + math.cos(headingAngle))/2

		f.write(str(xi)+","+str(yi)+","+str(headingZ)+","+str(headingW)+"\n")

		print(xi,yi,headingAngle)

	lastNode = currentNode
f.close()
