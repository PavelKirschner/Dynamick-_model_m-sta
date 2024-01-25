import random
import matplotlib.pyplot as plt
import copy
import time
from math import sqrt
import numpy as np
from scipy.spatial.distance import euclidean

dokola = np.array([[0,1],[1,0],[0,-1],[-1,0]])
pic = 0
signum = np.array([[1,1],[1,-1],[-1,1],[-1,-1]])
#tvary = [[[0,0]],
#         [[0,0],[1,0]],
#        [[0,0],[0,1]],
#         [[0,0],[1,1],[1,0]]]

tvary = np.array([[[0,0],[1,0]],
         [[0,0],[0,1]],
         [[0,0],[1,1],[1,0]],
         [[0,0],[1,1],[1,0],[0,1]],
         [[0,0],[1,1],[1,0],[2,0],[2,1]],
         [[0,0],[1,0],[2,0]],
         [[0,0],[0,1],[0,2]],
         [[0,0],[2,0],[1,1],[1,0]],
         [[0,0],[-1,-1],[-1,0]]], dtype=object
    )

def dis_to_nearest(fromx,fromy,value):
    d1 = 1
    d2 = 0
    while True:
        for i in signum:
            x = fromx + d1*i[0]
            y = fromy + d2*i[1]

            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].value == value:
                distance = euclidean([fromx,fromy],[x,y])
                return distance
            
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].value == value:
                distance = euclidean([fromx,fromy],[x,y])
                return distance

        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1

def maximum():
    citatel = 0
    jmenovatel = 0
    
    for row in mat:
        for cell in row:

            distance = euclidean([SIRKA//2+1,VYSKA//2+1],[cell.x,cell.y])
            if distance == 0:
                continue
            citatel += cell.value*(distance**(-gama))


            jmenovatel += distance**(-gama)

    return citatel/jmenovatel

def propability(fromx,fromy):
    d1 = 1
    d2 = 0
    citatel = 0
    jmenovatel = 0
    for i in range(23):
        for i in signum:
            x = fromx + d1*i[0]
            y = fromy + d2*i[1]

            if 0<x<SIRKA and 0<y<VYSKA:
                distance = euclidean([fromx,fromy],[x,y])
                citatel += np.multiply(mat[x][y].value,(np.power(distance,-gama)))
                jmenovatel += np.power(distance,-gama)
                
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA:
                distance = euclidean([fromx,fromy],[x,y])
                citatel += np.multiply(mat[x][y].value,(np.power(distance,-gama)))
                jmenovatel += np.power(distance,-gama)
                
        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1
    return np.divide(citatel,jmenovatel)


class POLE:
    def __init__(self, x,y):
        self.x = x
        self.y = y

class Nic(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 0
        self.farbe = 255

class Cesta(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 1
        self.farbe = 0

class Trasa:
    def __init__(self,startx,starty,kam_chci_value):
        self.startx = startx
        self.starty = starty
        self.prvky = [[startx,starty]]
        self.kam_chci_value = kam_chci_value
        self.vzdalenost = dis_to_nearest(startx,starty,kam_chci_value)
        self.hodnoceni = 0

    def pridej_cestu(self,x,y):
        l = [x,y]
        self.prvky.append([x,y])

    def get_vzdalenost(self):

        self.vzdalenost = dis_to_nearest(self.prvky[-1][0],self.prvky[-1][1],self.kam_chci_value)
        return self.vzdalenost
    
    def usmernit(self):
        hrbitov = []
        prvky = self.prvky
        index = len(prvky)
        #for index in range(len(prvky)-1,0,-1):
        while index != 1:
            index -=1
            for idx in range(0,index-1):

                if euclidean([prvky[idx][0],prvky[idx][1]],[prvky[index][0],prvky[index][1]]) == 1:
                    for i in range(index-1,idx,-1):
                        hrbitov.append(prvky[i])
                    index = idx + 1
                    break



        for i in hrbitov:
            self.prvky.remove(i)
prop = 0
p = 0
class Dum(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 2
        self.farbe = random.random()*100+100
        self.tvar = np.random.choice(tvary)
        self.lpozic = []

    def get_lpozic(self):
        self.lpozic = [[self.x,self.y]]
        for dx,dy in self.tvar:
            self.lpozic.append([self.x+dx,self.y+dy])

        return self.lpozic
    
    def muzu_sednout(self,maxim):
        #true pokud je na prázdných polích a je v přítomnosti objektu který není prázdné pole
        self.get_lpozic()

        for cor in self.lpozic:

            if mat[cor[0]][cor[1]].value != 0:
                return False
            
        a = propability(self.x,self.y)/maxim
        print(a)
        global prop
        global p 
        p+=1
        prop += a

        r = random.random()

        if r < a:

            return True
        else:
            return False
    
    def sednout(self):
        for x,y in self.lpozic:
            mat[x][y] = self


    def zarid_cestu(self):
        kolem = []
        x = self.x
        y = self.y
        for dx,dy in dokola:

            if 0<x+dx<VYSKA and 0<y+dy<VYSKA and [x+dx,y+dy] not in self.lpozic:
                kolem.append([x+dx,y+dy])
                if mat[x+dx][y+dy].value == 1:
                    return True
        
        trasy = []

        for kolx,koly in kolem:
            if mat[kolx][koly].value == 0:
                trasy.append(Trasa(kolx,koly,1))
                
        if len(trasy) ==0:
            print("bez silnice")
            return
        
        ta_prava = trasy[0]
        for trasa in trasy:
            if trasa.get_vzdalenost()<=ta_prava.get_vzdalenost():
                ta_prava = trasa
    
        for i in range(212):
            x = ta_prava.prvky[-1][0]
            y = ta_prava.prvky[-1][1]

            #mapa = [[obj.farbe for obj in row] for row in mat]
            #for i in ta_prava.prvky:
            #    mapa[i[0]][i[1]] = 50
            #plt.imshow(mapa, cmap="hot")
            #global pic
            #plt.savefig(f"domy{pic}.png")
            #pic+=1
            #plt.show()


            for posun in dokola:
                if 0<x+posun[0]<VYSKA and 0<y+posun[1]<SIRKA and mat[x+posun[0]][y+posun[1]].value == 1:
                    if len(ta_prava.prvky) > 3:
                        ta_prava.usmernit() 
                    for pole in ta_prava.prvky:
                        mat[pole[0]][pole[1]] = Cesta(pole[0],pole[1])
                    
                    return
                
            trasy = []
            for posun in dokola:
                c = [x+posun[0],y+posun[1]]

                if 0<x+posun[0]<VYSKA and 0<y+posun[1]<SIRKA and mat[x+posun[0]][y+posun[1]].value == 0 and c not in ta_prava.prvky:
                    t = copy.deepcopy(ta_prava)
                    t.pridej_cestu(x+posun[0],y+posun[1])
                    trasy.append(t)

            if len(trasy) == 0:
                print("bez silnice")
                return
            
            ta_prava = trasy[0]
            for trasa in trasy:
                if trasa.get_vzdalenost()<=ta_prava.get_vzdalenost():

                    ta_prava = trasa    

        print("eror")


                

            

gama = 3
a = 50
VYSKA, SIRKA = a,a
nusedliku = 100

def matrix(VYSKA, SIRKA):
    plan = np.array([[Nic(x,y) for y in range(SIRKA)] for x in range(VYSKA)])
    return plan



mat = matrix(VYSKA, SIRKA)

mat[SIRKA//2][VYSKA//2] = Dum(SIRKA//2,VYSKA//2)
mat[SIRKA//2+1][VYSKA//2] = Cesta(SIRKA//2+1,VYSKA//2)
maxim = maximum()
houses = np.array([Dum(random.randint(3,SIRKA-3),random.randint(3,VYSKA-3)) for i in range(nusedliku)])
t = time.localtime()
current_time = time.strftime("%H:%M", t)

nusedliku = 0
infloop = 0
while len(houses)!=0 and infloop<SIRKA*20:
    infloop +=1
    emigranti = []
    for house in houses:
        x = house.x
        y = house.y
        if house.muzu_sednout(maxim):
            print(nusedliku)
            house.sednout()
            house.zarid_cestu()
            emigranti.append(house)
            nusedliku +=1
            infloop = 0
            maxim = propability(SIRKA//2,VYSKA//2+1)
            


        
        elif random.randint(0,1) == 1:
            nx = x+random.randrange(-1,2,2)
            if nx < 3 or nx > SIRKA-4:
                pass
            else:
                house.x = nx                
        else:
            ny = y+random.randrange(-1,2,2)
            if ny < 3 or ny > VYSKA-4:
                pass
            else:
                house.y = ny  

    for emg in emigranti:
        houses = np.delete(houses, np.where(houses == emg))




tt = time.localtime()
tcurrent_time = time.strftime("%H:%M", tt)
print("začátek",current_time)
print("listova hotova:",tcurrent_time)
print(prop)
print(p)
mapa = [[obj.farbe for obj in row] for row in mat]

plt.imshow(mapa, cmap="hot")
#plt.savefig(f"dla{VYSKA}-{nusedliku}.png")
plt.show()