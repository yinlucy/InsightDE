#! /usr/bin/env python3
class Graph(object):
    
    def __init__(self, graph_dict=None):
        if graph_dict==None:
            graph_dict={}
        self.__graph_dict=graph_dict
        
    def vertices(self):
        return list(self.__graph_dict.keys())
    
    def add_vertex(self, vertex):
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex]={}
            
    def getNeighbors(self,vertex):
        return self.__graph_dict[vertex]
    
    def add_edge(self,vertex1,vertex2):
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].add(vertex2)
        else:
            self.__graph_dict[vertex1]={vertex2}

        if vertex2 in self.__graph_dict:
            self.__graph_dict[vertex2].add(vertex1)
        else:
            self.__graph_dict[vertex2]={vertex1}
    
    def oneFriend(self, start_vertex, end_vertex):
        if start_vertex not in self.__graph_dict: 
            return 'unverified'
        if end_vertex in self.__graph_dict[start_vertex]:
            return 'trusted'
        return 'unverified'
    
    
    def twoFriends(self, start_vertex, end_vertex):
        if start_vertex not in self.__graph_dict: 
            return 'unverified'
        if end_vertex not in self.__graph_dict: 
            return 'unverified'
        
        if end_vertex in self.__graph_dict[start_vertex]:
            return 'trusted'
        frontA=self.__graph_dict[start_vertex]
        frontB=self.__graph_dict[end_vertex]
        if not frontB.isdisjoint(frontA):
            return 'trusted'
        return 'unverified'
    
    def commonFriends(self, start_vertex, end_vertex):
        if start_vertex not in self.__graph_dict: 
            return 'unverified'
        if end_vertex not in self.__graph_dict: 
            return 'unverified'
        
        if end_vertex in self.__graph_dict[start_vertex]:
            return 'direct friends'
        frontA=self.__graph_dict[start_vertex]
        frontB=self.__graph_dict[end_vertex]
        if frontA.intersection(frontB):
            return frontA.intersection(frontB)
        return 'unverified'
    
    
    def fourFriends(self, start_vertex, end_vertex):
        usedVertex={start_vertex,end_vertex}
        if start_vertex not in self.__graph_dict: 
            return 'unverified'
        if end_vertex not in self.__graph_dict: 
            return 'unverified'
        
        frontA=self.__graph_dict[start_vertex]
        frontB=self.__graph_dict[end_vertex]
        if end_vertex in frontA:
            return 'trusted'
        
        if not frontB.isdisjoint(frontA):
            return 'trusted'
        
        for counter in range(3,5):
            newFrontA={}
            usedVertex=usedVertex.union(frontA)
            for vertex in frontA:
                if len(newFrontA)==0:
                    newFrontA=self.__graph_dict[vertex]
                else:
                    newFrontA = newFrontA.union(self.__graph_dict[vertex])
            frontA=newFrontA-newFrontA.intersection(usedVertex)
            if not frontB.isdisjoint(frontA):
                return 'trusted'
            temp=frontA
            frontA=frontB
            frontB=temp
        return 'unverified'
    
    def generalFriends(self, start_vertex, end_vertex,n):
        usedVertex={start_vertex,end_vertex}
        if start_vertex not in self.__graph_dict: 
            return 'unverified'
        if end_vertex not in self.__graph_dict: 
            return 'unverified'
        
        frontA=self.__graph_dict[start_vertex]
        frontB=self.__graph_dict[end_vertex]
        
        if end_vertex in frontA:
            return 'trusted'
        if n>1:
            if not frontB.isdisjoint(frontA):
                return 'trusted'
        if n>2:
            for counter in range(3,n+1):
                newFrontA={}
                usedVertex=usedVertex.union(frontA)
                for vertex in frontA:
                    if len(newFrontA)==0:
                        newFrontA=self.__graph_dict[vertex]
                    else:
                        newFrontA = newFrontA.union(self.__graph_dict[vertex])
                frontA=newFrontA-newFrontA.intersection(usedVertex)
                if not frontB.isdisjoint(frontA):
                    return 'trusted'
                temp=frontA
                frontA=frontB
                frontB=temp
            
        return 'unverified'


if __name__ == "__main__":

    #import csv
    from pylab import *
    import copy

    #read data
    BatchData = genfromtxt('./paymo_input/batch_payment.txt', skip_header = 1, delimiter = ',',usecols=[1,2])
    StreamData= genfromtxt('./paymo_input/stream_payment.txt', skip_header = 1, delimiter = ',',usecols=[1,2])

    g={}
    graph = Graph(g)
    
    for row in BatchData:
        if len(BatchData.shape)<2:
            graph.add_edge(int(BatchData[0]),int(BatchData[1]))
            break
        graph.add_edge(int(row[0]),int(row[1]))
   
    graphNew=copy.deepcopy(graph)
    with open('./paymo_output/output1.txt', 'w') as file:
        if len(StreamData.shape)<2:
            file.write('%s\n' % (graphNew.oneFriend(int(StreamData[0]),int(StreamData[1]))))
        else:
            for row in StreamData:
                file.write('%s\n' % (graphNew.oneFriend(int(row[0]),int(row[1]))))
                graphNew.add_edge(int(row[0]),int(row[1]))
    file.close()
    #print("1")
    
    graphTwoNew=copy.deepcopy(graph)
    with open('./paymo_output/output2.txt', 'w') as file:
        if len(StreamData.shape)<2:
            file.write('%s\n' % (graphTwoNew.twoFriends(int(StreamData[0]),int(StreamData[1]))))
        else:
            for row in StreamData:
                file.write('%s\n' % (graphTwoNew.twoFriends(int(row[0]),int(row[1]))))
                graphTwoNew.add_edge(int(row[0]),int(row[1]))
    file.close()
    #print("2")
    
    graphFourNew=copy.deepcopy(graph)
    with open('./paymo_output/output3.txt', 'w') as file:
        if len(StreamData.shape)<2:
                file.write('%s\n' % (graphFourNew.fourFriends(int(StreamData[0]),int(StreamData[1]))))
        else:
            for row in StreamData:
                file.write('%s\n' % (graphFourNew.fourFriends(int(row[0]),int(row[1]))))
                graphFourNew.add_edge(int(row[0]),int(row[1]))
    file.close()
    #print("3")



