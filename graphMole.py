# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:16:12 2019

@author: Alex
         This porgramm was written on Anaconda with Spyder 3.2.6 (Python 3.6)
"""

# Please make sure that the following imports of json, networkx and math
# are available on your system.

# Project imports
import json
import networkx as nx
# System imports
import math

# Local imports
import candidate

# Start pattern
startPattern = "Erde"

# End pattern
endPattern   = "b3-r7-r4nd7"

# Placeholder for start and end node
startNode    = ""
endNode      = ""

# Graph structure
graph = nx.Graph()

# Dictionary of key value pairs
# key = node, value = adjacency.
dataKeyValue = {}

# Method to parse and get the data in a dictionary.
def getData():
    global dataKeyValue
    with open('generatedGraph.json') as file:
        dataKeyValue = json.load(file)
        
# Method to add all nodes to the graph structure.
#
# @param: setLength
#         The length of a data set.
def addAllNodes(setLength):
    global dataKeyValue
    global startNode
    global endNode
    global graph
    for i in range(1,setLength+1):
        node = str(dataKeyValue['nodes'][i-1]['label'].replace("node_", ""))
        if(node==startPattern):
            startNode = str(i-1)
            node = str(dataKeyValue['nodes'][i-1]['label'].replace(startPattern, startNode))
        if(node==endPattern):
            endNode = str(i-1)
            node = str(dataKeyValue['nodes'][i-1]['label'].replace(endPattern, endNode))
        graph.add_node(node)

# Method to add all edges to the graph structure.
#
# @param: setLength
#         The length of a data set.
def addAllEdges(setLength):
    global dataKeyValue
    global graph
    for i in range(1,setLength+1):
        source = str(dataKeyValue['edges'][i-1]['source'])
        target = str(dataKeyValue['edges'][i-1]['target'])
        cost   = float(dataKeyValue['edges'][i-1]['cost'])
        graph.add_edge(source, target, weight=cost)

# List for the adjacency of the nodes.
adjacencyList = []
# Dictionary with key = node number and value = float numbers.
adjDict = {}

# Method to generate a dictionary of dictionaries.
def genAdjDict():
    global adjacencyList
    global graph
    adjacencyList = graph.adj
    for upperKey in adjacencyList:
        subDict = adjacencyList.get(upperKey, "")
        returnSubDict = {}
        for key in subDict:
            returnSubDict[key] = subDict.get(key, "")['weight']
            
        adjDict[str(upperKey)] = returnSubDict    

# Method to get the id of the node with the lowest
# path costs in the candidates list.
#
# @return: minCandidateId
#          The id of the candidate with currently lowest path costs.
#          If the calculate cost function return infinity due to invalidation
#          the return id is -1.
def getMinCandidateId():
    global candidateList
    global adjDict
    minValue = 100000.0
    minCandidateId = -1
    if len(candidateList)>0:
        for i in range (0, len(candidateList)):
            if minValue > candidateList[i].pathCosts:
                minValue     = candidateList[i].pathCosts
                minCandidateId = candidateList[i].idNumber
    return minCandidateId

# Method to get the index of a candidate (node) in a list.
#
# @param: idNumber
#         The idNumber of a candidate (node).
# @return: i
#          The index in some list.
def getIndexOfNode(idNumber, someList):
    if len(someList)>0:
        for i in range(0, len(someList)):
            if someList[i].idNumber == idNumber:
                return i
       
# A method to check whether a
# list contains a key or not.
#
# @param: key
#         The key to be checked.
#
# @return: boolean
#          If the list contains the key, True, else False.
def listContainsKey(key, someList):
    for i in range(0, len(someList)):
        if key == someList[i].idNumber:
            return True
    return False

# A proper path candidate
minCandidateFromList = candidate.Candidate(0, 0.0, [])

# List of node candidates for the shortest path.
candidateList = []

# List of poped (visited) candidates
popedCandList = []

# The method performs an update on the node. Therefore it is checked if the
# path costs of the next node, which is currently in the regular candidates list
# are higher than the path costs of the start node, which is already in the poped
# list, plus the current edge costs to the next node. If yes, than the path
# costs of the next node member from the candidates list are updated to the lower
# costs and the path is also updated to the path with the lower costs. The list
# constructor is necessary to avoid different identifiers points to the same list.
#
# @param: startNode
#         The start node in the edge
# @param: nextNode
#         The next node in the edge
#
def updateNode(startNode, nextNode):
    global adjDict
    global candidateList
    global popedCandList
    uSubDict = adjDict[startNode]
    try:
        if candidateList[getIndexOfNode(nextNode, candidateList)].pathCosts > popedCandList[getIndexOfNode(startNode,popedCandList)].pathCosts  + uSubDict[nextNode]:
            candidateList[getIndexOfNode(nextNode, candidateList)].pathCosts = popedCandList[getIndexOfNode(startNode,popedCandList)].pathCosts + uSubDict[nextNode]
            candidateList[getIndexOfNode(nextNode, candidateList)].pathList  = list(popedCandList[getIndexOfNode(startNode,popedCandList)].pathList)
    except:
        pass
    

# Method to find shortest path
#
# @details: The method finds a shortest path. Therefore with the start node
#           the initial node is set in the list of node candidates. Then in the 
#           while loop the node with the lowest path costs is poped from the list
#           of candidates. If the poped node is already the endnode the algorithm
#           has found the path. If not the poped node is appended to a list of
#           poped nodes for the overview. The next step handles isolated nodes in
#           graph components islands. If the node from the candidates list has
#           alreydy itself in its path, then there's a loop, and the algorithm
#           declare that there's no desired path from start node to the end node.
#           Otherwise the id number of the node with currently lowest costs is
#           appended to its path. Then after the path update the updated path list
#           is assigned to the corresponding node candidate in the list for the
#           consistency of data. Then in the for each loop the adjacency of the
#           node with the lowest path costs is checked. Therefore is is checked
#           if the key (node number) is not in the list of poped nodes. If the
#           the key (node) hasn't been handled then the update method is called.
#
#
# @param startNode
#        The start node in the path.
#
#
def findShortestPath(startNode):
    global candidateList
    global graph
    global endNode
    global minCandidateFromList
    visitedList  = []
    
    nodeList = list(graph.nodes)
    if (startNode or endNode) not in nodeList:
        minCandidateFromList.pathList  = str("NO PATH")
        minCandidateFromList.pathCosts = math.inf
        return
    
    for i in range(0, len(nodeList)):
            candidateList.append(candidate.Candidate(nodeList[i],math.inf, visitedList))
    candidateList[getIndexOfNode(startNode, candidateList)] = candidate.Candidate(startNode, 0.0, visitedList)
    
    while len(candidateList)>0:
        try:
            minCandidateFromList = candidateList.pop(getIndexOfNode(getMinCandidateId(), candidateList))
            if minCandidateFromList.idNumber == endNode:
                minCandidateFromList.pathList.append(endNode)
                break
        except:
            pass
        popedCandList.append(minCandidateFromList)
        
        if minCandidateFromList.idNumber not in minCandidateFromList.pathList:
            minCandidateFromList.pathList.append(minCandidateFromList.idNumber)
        else:  # to handle isolated graph components
            minCandidateFromList.pathList  = str("NO PATH")
            minCandidateFromList.pathCosts = math.inf
            break
        try: # for the consistency of data
            candidateList[getIndexOfNode(minCandidateFromList, candidateList)].pathList = minCandidateFromList.pathList
        except:
            pass
        
        for key in adjDict[minCandidateFromList.idNumber]:
            try:
                if not (listContainsKey(key, popedCandList)):
                    updateNode(str(minCandidateFromList.idNumber), str(key))
            except:
                pass

# Method to restore the data from CODING CHALLENGE,
# e.g node_, startPattern, endPattern
#
# @param shortestPathTuple
#        A tuple with shortest path and costs
#
def restoreData(shortestPathTuple):
    shortestPath = []
    global startPattern
    global endPattern
    print("Costs         = "+str(shortestPathTuple[1]))
    if shortestPathTuple[0][0] == startNode and shortestPathTuple[0][len(shortestPathTuple[0])-1]== endNode:
        shortestPath.append(startPattern)
        for i in range (1, len(shortestPathTuple[0])-1):
           shortestPath.append("node_"+str(shortestPathTuple[0][i]))
        shortestPath.append(endPattern)
    print("Shortest Path = "+str(shortestPath))   

# To test other path just set the bool variable to False
# and set the start node in the findShortestPath method
# to str(node number), e.g.findShortestPath(str(399))
# and the end node to "desired endnode", e.g. end node = "755"
CODING_CHALLENGE = True

if __name__ == '__main__':
    print("--- get data ---")
    getData()
    print("--- add all nodes ---")
    addAllNodes(len(dataKeyValue['nodes']))
    print("--- add all edges ---")
    addAllEdges(len(dataKeyValue['edges']))
    print("--- generating adjacency dictionary ---")
    genAdjDict()
    print("--- start find shortest path ---\n")
    findShortestPath(startNode)
    
    if CODING_CHALLENGE:
        restoreData(tuple((minCandidateFromList.pathList, minCandidateFromList.pathCosts)))
    else:
        print("Path : "+str(minCandidateFromList.pathList))
        print("Costs: "+str(minCandidateFromList.pathCosts))
    
    

     
