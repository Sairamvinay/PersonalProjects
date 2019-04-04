import numpy as np

def delta(a,b):
    if a != b:
        delta = 1

    else:
        delta = 0


    return delta

def find_direct(insert,delete,subs):
    cost = min(insert,delete,subs)
    if cost == insert:
        return "Up"

    elif cost == delete:
        return "Left"

    else:
        return "Diag"

def edit_distance(X,Y):
    X = X.lower()
    Y = Y.lower()
    m = len(X)
    n = len(Y)
    edits = np.zeros((m+1,n+1)).astype(int)
    directions = np.chararray((m+1,n+1))
    directions[:] = ''
    for i in range(m+1):
        edits[i][0] = int(i)
        if i!=0:
            directions[i][0] = "Up"

    for j in range(n+1):
        edits[0][j] = int(j)
        if j != 0:
            directions[0][j] = "Left"


    for i in range(1,m+1):
        for j in range(1,n+1):

            insert = int(1 + edits[i][j-1])  #insertion
            delete = int(1 + edits[i-1][j])  #delete
            subs = int(edits[i-1][j-1] + delta(X[i-1],Y[j-1])) #substitute

            directions[i][j] = find_direct(insert,delete,subs)
            edits[i][j] = min(insert,delete,subs)


    return edits,directions

X = raw_input("Enter string X:")
Y = raw_input("Enter string Y:")
edits,directions = edit_distance(X,Y)

print "Edit Distance:", edits[len(X)][len(Y)]
print "Edits\n", edits
print "Directions\n",directions
