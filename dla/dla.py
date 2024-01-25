import random
import matplotlib.pyplot as plt
from math import sqrt


VYSKA, SIRKA = 200,200
usedliku = 0

def matrix(VYSKA, SIRKA):
    plan = [[0 for _ in range(SIRKA)] for _ in range(VYSKA)]
    return(plan)

mat = matrix(VYSKA, SIRKA)
mat[SIRKA//2][VYSKA//2] = 1

while usedliku<1000:

    x = random.randint(1,SIRKA-2)
    y = random.randint(1,VYSKA-2)
    if sqrt((x-SIRKA//2)**2+(y-VYSKA//2)**2)< int(SIRKA*0.3):
        continue
    while True:
        if mat[x+1][y] == 1 or mat[x][y+1] == 1 or mat[x-1][y] == 1 or mat[x][y-1] == 1:
            mat[x][y] = 1
            usedliku += 1

            break
        elif random.randint(0,1) == 1:
            nx = random.randrange(-1,2,2)
            if x+nx < 1 or x+nx > SIRKA-2:
                ...
            else:
                x += nx
        else:
            ny = random.randrange(-1,2,2)
            if y+ny < 1 or y+ny > VYSKA-2:
                ...
            else:
                y += ny
print(usedliku)
plt.imshow(mat)
plt.show()