# -*- coding: utf-8 -*-
"""
@author: Alex
         This programm was written on Anaconda with Spyder 3.2.6 (Python 3.6)
"""
# Candidate class for the nodes,
# which are in a candidates list
# to be considered beeing a valid
# path.
#
class Candidate:
    # attributes
    idNumber = 0
    pathCosts = 0.0
    pathList = [] 

    # init constructor
    # @param: idNumber
    #         The correspoding id number
    #         costs
    #         The current costs for the key
    #         visitedList
    #         The inherited path of a node
    def __init__(self, idNumber, costs, visitedList):
        self.idNumber = idNumber
        self.pathCosts = costs
        self.pathList = list(visitedList)
    

