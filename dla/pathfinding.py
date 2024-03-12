import random
import matplotlib.pyplot as plt
import copy
import time
from math import sqrt

dokola = [[0,1],[1,0],[0,-1],[-1,0]]
signum = [[1,1],[1,-1],[-1,1],[-1,-1]]
dic = {
    10:58,
    9:48,
    8:39,
    7:30,
    6:23,
    5:17,
    4:11,
    3:7,
    2:4,
    1:2

}

def dis_to_nearest(fromx,fromy,value):
    d1 = 1
    d2 = 0
    print(fromx,fromy)
    l = []
    ll = []
    for i in range(14):
        print("dčka",d1,d2)
        for s1,s2 in signum:
            x = fromx + d1*s1
            y = fromy + d2*s2
            l.append(x)
            ll.append(y)
            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].value == value:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                print("final answer",x,y)
                return distance
            
            x = fromx + d2*s1
            y = fromy + d1*s2
            l.append(x)
            ll.append(y)
            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].value == value:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                print("final answer",x,y)
                return distance

        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1

        plt.scatter(l,ll, s = 1000)
        plt.savefig(f"{i}")
        plt.close()

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
        self.prvky.append([x,y])

    def get_vzdalenost(self):
        self.vzdalenost = dis_to_nearest(self.prvky[-1][0],self.prvky[-1][1],self.kam_chci_value)
        return self.vzdalenost

class Dum(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 2
        self.farbe = random.random()*100+100

    def zarid_cestu(self):
        if mat[self.x+1][self.y].value ==1  or mat[self.x][self.y+1].value ==1 or mat[self.x-1][self.y].value == 1 or mat[self.x][self.y-1].value == 1:
            return
        else:
            trasy = []
            for posun in dokola:
                if mat[self.x+posun[0]][self.y+posun[1]].value == 0:
                    trasy.append(Trasa(self.x+posun[0],self.y+posun[1],1))
            
            ta_prava = trasy[0]
            for trasa in trasy[1:len(trasy)]:
                if trasa.vzdalenost<ta_prava.vzdalenost:
                    ta_prava = trasa
            while True:
                print(ta_prava)
                x = ta_prava.prvky[-1][0]
                y = ta_prava.prvky[-1][1]

                for posun in dokola:
                    if 0<x+posun[0]<VYSKA and 0<y+posun[1]<SIRKA and mat[x+posun[0]][y+posun[1]].value == 1:
                        print("našli jsme cestu", ta_prava.prvky)
                        for pole in ta_prava.prvky:
                            mat[pole[0]][pole[1]] = Cesta(pole[0],pole[1])
                        return
                trasy = []
                for posun in dokola:

                    if 0<x+posun[0]<VYSKA and 0<y+posun[1]<SIRKA and mat[x+posun[0]][y+posun[1]].value == 0:
                        t = Trasa(ta_prava.startx,ta_prava.starty,1)
                        for prvek in ta_prava.prvky[1:len(ta_prava.prvky)]:    
                            t.pridej_cestu(prvek[0],prvek[1])
                        t.pridej_cestu(x+posun[0],y+posun[1])
                        trasy.append(t)

                
                #print("trasy",trasy)
                #print("vzdalenost")
                #print(trasy[0].prvky)
                #print(trasy[1].prvky)
                #print(trasy[2].prvky)
                for i in range(len(trasy)):
                    print("vzdalenosti")
                    #print("body", trasy[i].prvky[-1],trasy[i-1].prvky[-1])
                    print(trasy[i],trasy[i].prvky,trasy[i].get_vzdalenost())
                    print(trasy[i-1],trasy[i-1].prvky,trasy[i-1].get_vzdalenost())
                    if trasy[i].get_vzdalenost()<trasy[i-1].get_vzdalenost():

                        ta_prava = trasy[i]
                print(ta_prava)
                print("-------------------")
                #time.sleep(1)

                

            



VYSKA, SIRKA = 200,200
nusedliku = 4

def matrix(VYSKA, SIRKA):
    plan = [[Nic(x,y) for y in range(SIRKA)] for x in range(VYSKA)]
    return(plan)



mat = matrix(VYSKA, SIRKA)

mat[SIRKA//2][VYSKA//2] = Dum(SIRKA//2,VYSKA//2)

#mat[6][6] = Cesta(6,6)

print("distance",dis_to_nearest(0,0,1))

houses = [Dum(random.randint(1,SIRKA-2),random.randint(1,VYSKA-2)) for i in range(nusedliku)]






mapa = [[obj.farbe for obj in row] for row in mat]

