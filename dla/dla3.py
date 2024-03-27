import random
import matplotlib.pyplot as plt
import copy
import time

VYSKA, SIRKA = 20,20
ncastic = 70

def matrix(VYSKA, SIRKA):
    plan = [[0 for _ in range(SIRKA)] for _ in range(VYSKA)]
    return(plan)

mat = matrix(VYSKA, SIRKA)
mat[SIRKA//2][VYSKA//2] = 1


castice = [[random.randint(1,SIRKA-2),random.randint(1,VYSKA-2)] for i in range(ncastic)]

t = time.localtime()
current_time = time.strftime("%H:%M", t)
print("začátek",current_time)

ncastic = 0

while len(castice)!=0:

    emigranti = []
    for index in range(len(castice)):    
        x,y = castice[index]
        
        if mat[x+1][y] == 1 or mat[x][y+1] == 1 or mat[x-1][y] == 1 or mat[x][y-1] == 1:
            mat[x][y] = 1
            emigranti.append(castice[index])
            ncastic +=1
            print(ncastic)
        elif random.randint(0,1) == 1:
            nx = x+random.randrange(-1,2,2)
            if nx < 1 or nx > SIRKA-2:
                pass
            else:
                castice[index][0] = nx                
        else:
            ny = y+random.randrange(-1,2,2)
            if ny < 1 or ny > VYSKA-2:
                pass
            else:
                castice[index][1] = ny  
    for emg in emigranti:
        castice.remove(emg)


tt = time.localtime()
tcurrent_time = time.strftime("%H:%M", tt)
print("začátek",current_time)
print("listova hotova:",tcurrent_time)


plt.imshow(mat, cmap="gnuplot")
plt.show()