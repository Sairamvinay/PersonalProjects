from collections import defaultdict
class ChooseError(Exception):
    pass

#The following Graph class contains all the required Basic Graph algorithms
# Attributes: Number of vertices and whether is it Directed or not
# and other important parameters such as parent, keys, weights and Visit which contains the visited vertex

class Graph:

    def __init__(self,vertices = 0,Directed = True):

        self.graph = defaultdict(list)
        self.Visit = []
        self.vertno = vertices
        self.weights = dict()
        self.Directed  = Directed
        self.parent = []
        self.unionkey = []
        self.UnionType = ""
        
    #Adds an edge based on Given weights and Directed or not graphs
    #Directed check is performed so that if it is undirected, even the reverse of edges (So that it is easier for manipulation) are stored
    def addEdge(self,u,v,w = 0):
        self.graph[u].append(v)
        self.weights[str(u) + '->' + str(v)] = w   #Weights are stored in dictionary in such a way the keys are strings containing u and v delimited by ->
        if not (self.Directed):
            self.graph[v].append(u)
            self.weights[str(v) + '->' + str(u)] = w


    #initializes the parent and unionkey for Kruskals
    #initializes according to the type of Union
    def initparent(self,UnionType = "R"):

        ret = True
        self.parent = [None] * self.vertno
        self.unionkey = [None] * self.vertno
        try:
            if UnionType == "S":
                for i in range(self.vertno):
                    self.parent[i] = i
                    self.unionkey[i] = 1    #Size base val is 1
                    self.UnionType = UnionType

            elif UnionType in "RH":
                for i in range(self.vertno):
                    self.parent[i] = i
                    self.unionkey[i] = 0    #Rank or Height base val is 0
                    self.UnionType = UnionType

            else:
                ret = False
                raise ChooseError

        except:
            print "Wrong Choice! Please try again!!"

        finally:
            return ret
            

    #Resets the Visit always whenever we want to perform searching through it
    def resetVisit(self):
        self.Visit = [False]*self.vertno

    #Find by Compression algorithm to do the search
        
    def find(self,vertex):

        if self.parent[vertex] == vertex:
            return vertex

        return self.find(self.parent[vertex])


    #more generic Union to do the Union operation by Size (for "S") or Rank/Height (for "H")
    def Union(self,x,y):
        if self.UnionType == "S":
            self.UnionBySize(x,y)

        else:
            self.UnionByRank(x,y)

    #Seperate functions for Union by Rank
    def UnionByRank(self,x,y):

        xroot = self.find(x)
        yroot = self.find(y)
        if self.unionkey[xroot] < self.unionkey[yroot]:

            self.parent[xroot] = yroot
            

        elif self.unionkey[yroot] < self.unionkey[xroot]:
            
            self.parent[yroot] = xroot


        else:

            self.parent[xroot] = yroot
            self.unionkey[yroot] += 1


    #Seperate functions for Union by Size
    def UnionBySize(self,x,y):

        xroot = self.find(x)
        yroot = self.find(y)
        if self.unionkey[xroot] < self.unionkey[yroot]:

            self.parent[xroot] = yroot
            self.unionkey[yroot] += self.unionkey[xroot]

        else:

            self.parent[yroot] = xroot
            self.unionkey[xroot] += self.unionkey[yroot]


    #This method finds the vertex which has the minimum key value such that the vertex is unvisited.
    #A helper method for both Dijkstras and Prims
    def pickMinUnvisit(self,key):
        m = 2**31
        ind = -1
        for v in range(self.vertno):
            if (key[v] < m) and (not self.Visit[v]):
                m = key[v]
                ind = v

        return ind

    #Standard DFS method to do Depth First Search starting from Node
    #Recursive method for DFS
    def DFS(self,node):

        self.Visit[node] = True         #Mark the current node as True
        print node                  
        adj = self.graph[node]          #if Node has no adjacent vertex, then adj = [] because of defaultdict
        for vert in adj:
            if not (self.Visit[vert]):
                self.DFS(vert)          #If Unvisited, perform DFS on that vertex


    #Standard BFS method to do Breadth First Search starting from vert
    #Iterative method using Queue (basic Python List but deletion from starting of list)
    def BFS(self,vert):
        queue = []
        queue.append(vert)
        self.resetVisit()
        self.Visit[vert] = True     #Mark current node as true
        while queue:
            u = queue.pop(0)        #This is very important as the deletion is done from beginning of queue, u contains the deleted vertex. Functionality
            print u
            adj = self.graph[u]     
            for v in adj:
                if not (self.Visit[v]):     #if not visited, enqueue adjacent vertex into queue and mark it visited
                    queue.append(v)
                    self.Visit[v] = True


    #This method does the iterative way of implementing DFS but with an order array which contains all the visited vertex
    def TopSort(self,v,order = []):
        self.Visit[v] = True
        adj = self.graph[v]
        for vert in adj:
            if not self.Visit[vert]:
                self.TopSort(vert,order)    #Very much similar to DFS() but vert is appended to order


        order.append(v)     #Difference between this method and DFS()

    #The outer significant function to do TopSort by iterating through each vertex
    def Toporder(self):

        order = []
        for i in range(self.vertno):
            if not self.Visit[i]:
                self.TopSort(i,order)

        order.reverse()         #Reverse the order because the order stores visited vertices in the opposite order
        return order


    #Kruskals algorithm method
    def Kruskals(self,UnionType = "R"):

        sortededges = []            #contains the sorted edges in (edge,weight) form
        for edge, weight in sorted(self.weights.items(), key=lambda item: (item[1], item[0])):
            sortededges.append((edge,weight))

        
        kruskalorder = []
        itervar = 0
        numchosen = 0
        ret = self.initparent(UnionType)
        if not ret:
            print "Not Possible to perform Kruskals!!"
            return 
        
        while numchosen < (self.vertno - 1):

            x,y = sortededges[itervar][0].split("->")
            z = sortededges[itervar][1]
            x = int(x)
            y = int(y)
            xroot = self.find(x)
            yroot = self.find(y)
            itervar += 1

            if xroot == yroot:
                pass

            else:
                kruskalorder.append(('->'.join([str(x),str(y)]),z))
                numchosen += 1
                self.Union(xroot,yroot)


        print "Edge",'\t',"Weight"
        for _,edge in enumerate(kruskalorder):

            print edge[0],'\t',edge[1]
                

    #Method to implement Prims MST algorithm.
    #This method picks each minimum key vertex and then iterates through each adjacent vertex and then the order is maintained using the Prims algorithm
    # k = min(weight(edge),k)
    def Prims(self):
        parents = [-1] * self.vertno
        key = [2**31] *self.vertno
        key[0] = 0                              #0 is the root key
        for v in range(self.vertno):
            minkey = self.pickMinUnvisit(key)   #uses helper method to get min unvisited key vertex
            self.Visit[minkey] = True
            Adj = self.graph[minkey]
            for vert in Adj:
                st = str(minkey) + '->' + str(vert)
                if (not self.Visit[vert]) and (key[vert] > self.weights[st]):
                    key[vert] = self.weights[st]        #the prims algorithm of updating the key
                    parents[vert] = minkey

        print "Edge",'\t',"Weight"
        for vertex in range(1,self.vertno):         #start from 1 because 0 is the root
            print parents[vertex],"->",vertex,"\t",self.weights[str(parents[vertex]) + '->' + str(vertex)]


    
    
    #Dijkstras method from the start index
    def Dijkstras(self,start):

        distances = [2**31] * self.vertno
        distances[start] = 0
        for v in range(self.vertno):
            minkey = self.pickMinUnvisit(distances)
            self.Visit[minkey] = True
            Adj = self.graph[minkey]
            for vert in Adj:
                st = str(minkey) + '->' + str(vert)
                if (not self.Visit[vert]) and ((distances[vert] > (distances[minkey] + self.weights[st]))):
                    distances[vert] = distances[minkey] + self.weights[st]


        for vertex,dist in enumerate(distances):
            print vertex,"\t",dist

        
        
#Test for BFS AND DFS
#DFS should give: 2 0 1 3
#BFS should give: 2 0 3 1
            
g = Graph(4,True)
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2) 
g.addEdge(2, 0) 
g.addEdge(2, 3) 
g.addEdge(3, 3) 
g.resetVisit()
print "Graph1 is here:",g.graph
print "DFS:"
g.DFS(2)
print '\n'
g.resetVisit()
print "BFS:"
g.BFS(2)
print '\n'

# Test for Topological Sort
#Topological Order should give: 5,4,2,3,1,0

g1 = Graph(6,True)
g1.addEdge(5, 2) 
g1.addEdge(5, 0) 
g1.addEdge(4, 0) 
g1.addEdge(4, 1) 
g1.addEdge(2, 3) 
g1.addEdge(3, 1)
g1.resetVisit()
print "Graph2 is here:",g1.graph
print "Topological Order:"
print g1.Toporder()
print '\n'

#Test for Prims
#Prims should print: 0-1 (wt = 2), 1-2 (wt = 3), 0-3(wt = 6), 1-4 (wt = 5)

g2 = Graph(5,False)
g2.addEdge(0,1,2)
g2.addEdge(0,3,6)
g2.addEdge(1,2,3)
g2.addEdge(1,3,8)
g2.addEdge(1,4,5)
g2.addEdge(2,4,7)
g2.addEdge(3,4,9)
g2.resetVisit()
print "Graph3 is here:",g2.graph
print "Prims:"
g2.Prims()
print "\n"


#Test for dijkstras
#Should print the following output:
'''
Vertex          Distance
0                0
1                4
2                12
3                19
4                21
5                11
6                9
7                8
8                14
'''

g3 = Graph(9,False) 
g3.addEdge(0,1,4)
g3.addEdge(0,7,8)
g3.addEdge(1,2,8)
g3.addEdge(1,7,11)
g3.addEdge(2,3,7)
g3.addEdge(2,5,4)
g3.addEdge(2,8,2)
g3.addEdge(3,4,9)
g3.addEdge(3,5,14)
g3.addEdge(4,5,10)
g3.addEdge(5,6,2)
g3.addEdge(6,7,1)
g3.addEdge(6,8,6)
g3.addEdge(7,8,7)
g3.resetVisit()
print "Graph4 is here:",g3.graph
print "Dijkstras:"
g3.Dijkstras(0)

#Test for Kruskals: should give this
'''
Edge 	Weight
2->3 	4
0->3 	5
0->1 	10
'''

g4 = Graph(4,True)
g4.addEdge(0,1,10) 
g4.addEdge(0,2,6) 
g4.addEdge(0,3,5) 
g4.addEdge(1,3,15) 
g4.addEdge(2,3,4)
print "Graph5 is here:",g4.graph
print "Kruskals:"                   #Making sure that all three union's give the same answer
print "Union by size:"
g4.Kruskals("S")
print "Union by Rank:"
g4.Kruskals("R")
print "Union by Height (same as rank):"
g4.Kruskals("H")
print "An incorrect parameter:"
g4.Kruskals("I")                    #A test Case to yield an error
