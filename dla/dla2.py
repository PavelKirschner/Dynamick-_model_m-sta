import random
import matplotlib.pyplot as plt
from math import sqrt
import time

t = time.localtime()
current_time = time.strftime("%H:%M", t)
print("listova hotova:",current_time)

while True:
    VYSKA, SIRKA = 2000,2000
    ncastic = 444000

    def matrix(VYSKA, SIRKA):
        plan = [[0 for _ in range(SIRKA)] for _ in range(VYSKA)]
        return(plan)

    mat = matrix(VYSKA, SIRKA)
    mat[VYSKA//2][SIRKA//2] = 1


    castice = [[random.randint(1,SIRKA-2),random.randint(1,VYSKA-2)] for i in range(ncastic)]

    while len(castice)!=0:
        emigranti = []
        for index in range(len(castice)):    
            x,y = castice[index]
            
            if mat[x+1][y] == 1 or mat[x][y+1] == 1 or mat[x-1][y] == 1 or mat[x][y-1] == 1:
                mat[x][y] = 1
                emigranti.append(castice[index])

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





    plt.imshow(mat)
    plt.savefig(f"dla{VYSKA}-{ncastic}.png")
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    print("listova hotova:",current_time)


    VYSKA, SIRKA = 3000,3000
    usedliku = 0
    ncastic = 444000

    def matrix(VYSKA, SIRKA):
        plan = [[0 for _ in range(SIRKA)] for _ in range(VYSKA)]
        return(plan)

    mat = matrix(VYSKA, SIRKA)
    mat[SIRKA//2][VYSKA//2] = 1

    while usedliku<ncastic:

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

    plt.imshow(mat)
    plt.savefig(f"dla{VYSKA}-{ncastic}.png")
    print("random chodec hotova")
