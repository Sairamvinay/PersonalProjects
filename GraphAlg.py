from collections import defaultdict
class ChooseError(Exception):
    pass

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
        
    #Directed check is performed so that if it is undirected, even the reverse of edges are stored
    def addEdge(self,u,v,w = 0):
        self.graph[u].append(v)
        self.weights[str(u) + '->' + str(v)] = w
        if not (self.Directed):
            self.graph[v].append(u)
            self.weights[str(v) + '->' + str(u)] = w


    def initparent(self,UnionType = "R"):

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
                raise ChooseError

        except:
            print "Wrong Choice! Please try again!!"
            

    def resetVisit(self):
        self.Visit = [False]*self.vertno

    def find(self,vertex):

        if self.parent[vertex] == vertex:
            return vertex

        return self.find(self.parent[vertex])


    def Union(self,x,y):
        if self.UnionType == "S":
            self.UnionBySize(x,y)

        else:
            self.UnionByRank(x,y)

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


    def UnionBySize(self,x,y):

        xroot = self.find(x)
        yroot = self.find(y)
        if self.unionkey[xroot] < self.unionkey[yroot]:

            self.parent[xroot] = yroot
            self.unionkey[yroot] += self.unionkey[xroot]

        else:

            self.parent[yroot] = xroot
            self.unionkey[xroot] += self.unionkey[yroot]


    
    def pickMinUnvisit(self,key):
        m = 2**31
        ind = -1
        for v in range(self.vertno):
            if (key[v] < m) and (not self.Visit[v]):
                m = key[v]
                ind = v

        return ind


    def DFS(self,node):

        self.Visit[node] = True
        print node
        adj = self.graph[node]
        for vert in adj:
            if not (self.Visit[vert]):
                self.DFS(vert)



    def BFS(self,vert):
        queue = []
        queue.append(vert)
        self.Visit = [False] * len(self.graph)
        self.Visit[vert] = True
        while queue:
            u = queue.pop(0)
            print u
            adj = self.graph[u]
            for v in adj:
                if not (self.Visit[v]):
                    queue.append(v)
                    self.Visit[v] = True


    def TopSort(self,v,order = []):
        self.Visit[v] = True
        adj = self.graph[v]
        for vert in adj:
            if not self.Visit[vert]:
                self.TopSort(vert,order)


        order.append(v)

    def Toporder(self):

        order = []
        for i in range(self.vertno):
            if not self.Visit[i]:
                self.TopSort(i,order)

        order.reverse()
        return order

    
    def Prims(self):
        parents = [-1] * self.vertno
        key = [2**31] *self.vertno
        key[0] = 0
        for v in range(self.vertno):
            minkey = self.pickMinUnvisit(key)
            self.Visit[minkey] = True
            Adj = self.graph[minkey]
            for vert in Adj:
                st = str(minkey) + '->' + str(vert)
                if (not self.Visit[vert]) and (key[vert] > self.weights[st]):
                    key[vert] = self.weights[st]
                    parents[vert] = minkey


        for vertex in range(1,self.vertno):
            print "Edge:",parents[vertex],"->",vertex,":",self.weights[str(parents[vertex]) + '->' + str(vertex)]



    def Kruskals(self,UnionType = "R"):

        sortededges = []
        for edge, weight in sorted(self.weights.items(), key=lambda item: (item[1], item[0])):
            sortededges.append((edge,weight))

        
        kruskalorder = []
        itervar = 0
        numchosen = 0
        self.initparent(UnionType)
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


g4 = Graph(4,True)
g4.addEdge(0,1,10) 
g4.addEdge(0,2,6) 
g4.addEdge(0,3,5) 
g4.addEdge(1,3,15) 
g4.addEdge(2,3,4)
print "Graph5 is here:",g4.graph
print "Kruskals:"
print g4.Kruskals("S")
print g4.Kruskals("R")
print g4.Kruskals("H")
