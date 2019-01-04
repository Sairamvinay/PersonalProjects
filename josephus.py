def Josephus2(n,k=2):
   cntrl = n
   while (len(L) != 1):
      print L
      del L[1::2]
      if cntrl % 2 == 1:
         cntrl += 1
         del L[0]

      cntrl += len(L)

   print L

def Josephus(n,k):
   cntrl = n
   while (len(L) != 1):
      print L
      if len(L) == 2:
         del L[1]
         break

      del L[1::k]
      if cntrl % k == 0:
         cntrl += 1
         del L[0]
         if len(L) == 1:
            break

      cntrl+= len(L)

   print L


n = input("Enter number of people in the circle:")
L = range(1,n+1)
k = input("Enter k value:")
if k == 2:
   Josephus2(n)


else:
   Josephus(n,k)

