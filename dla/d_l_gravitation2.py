import random
import matplotlib.pyplot as plt
import copy
import time
from math import sqrt
import numpy
from matplotlib.animation import FuncAnimation
from PIL import Image
import os
import imageio


# maximum se počítá ze všech a pravděpodobnost z kruhu
# upravit, ab se dala nastavovat pravděpodobnost
# urovnat kód
#přidat speciální budovy
# 3D model
# udělat zarovnávání cest po přesunuutí
# (nejsem si jistý přezkoumat) domy se zvedají docela random, zvedají se i ty úplně u kostela, tak by to být nemělo, upravit tu pravděpodobnost tak, aby se zvedaly ty domy na periferiích 
# město roste do kadných souřadnic!!!!!
# moná je to až moc náhodné (vstávání, sedání)

dokola = [[0,1],[1,0],[0,-1],[-1,0]]
pic = 0
signum = [[1,1],[1,-1],[-1,1],[-1,-1]]
rposun = (1,-1)

tvary = [[[0,0],[1,0]], #carky
         [[0,0],[0,1]],
         [[0,0],[-1,0]], 
         [[0,0],[0,-1]],
         [[0,0],[1,1],[1,0]],#Lka
         [[0,0],[1,1],[0,1]],
         [[0,0],[-1,-1],[-1,0]],
         [[0,0],[-1,-1],[0,-1]],
         [[0,0],[-1,1],[-1,0]],
         [[0,0],[-1,1],[0,1]],
         [[0,0],[1,-1],[1,0]],
         [[0,0],[1,-1],[0,-1]],
         [[0,0],[1,1],[1,0],[0,1]], #ctverce
         [[0,0],[-1,-1],[-1,0],[0,-1]],
         [[0,0],[1,-1],[1,0],[0,-1]],
         [[0,0],[-1,1],[-1,0],[0,1]],
         [[0,0],[2,0],[1,1],[1,0]], # tetris
         [[0,0],[-2,0],[-1,1],[-1,0]],
         [[0,0],[0,2],[1,1],[0,1]],
         [[0,0],[0,-2],[1,-1],[0,-1]],
         [[0,0],[1,1],[1,0],[2,0],[2,1]], #čtverec s hlavou
         [[0,0],[-1,-1],[-1,0],[0,-1],[-2,-1]],
         [[0,0],[1,-1],[1,0],[0,-1],[1,-2]],
         [[0,0],[-1,1],[-1,0],[0,1],[-1,2]],
         [[0,0],[1,0],[2,0]], #zizalak
         [[0,0],[0,1],[0,2]],
         [[0,0],[-1,0],[-2,0]],
         [[0,0],[0,-1],[0,-2]],            
    ]

def matrix(VYSKA, SIRKA):
    plan = [[Nic(x,y) for y in range(SIRKA)] for x in range(VYSKA)]
    return(plan)

def dis_to_nearest(fromx,fromy,id):
    d1 = 1
    d2 = 0
    while True:
        for i in signum:
            x = fromx + d1*i[0]
            y = fromy + d2*i[1]

            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].id == id:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                return distance
            
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].id == id:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                return distance

        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1

def savepic(npic):
    '''uloží aktuální figuru do frames_folder v png'''
    mapa = [[obj.farbe for obj in row] for row in mat]
    for house in houses:
        for dx,dy in house.tvar:    
            mapa[house.x + dx][house.y + dy] = 100
    plt.imshow(mapa, cmap="hot")
    plt.savefig(f"frames_folder/frame_{npic}.png", format='PNG', bbox_inches='tight')
    plt.close()  # Zavřít aktuální figuru, aby neovlivňovala další snímky
    npic += 1
    return npic

def stehovani(): 
    """zvedne domy z pole a přesune je do listu houses,usměrní pahýly sinlic, vrátí počet zvednutých domů"""
    zvednuto_domu = 0
    for row in mat:
        for cell in row:
            if cell.id == 2:
                if cell.nechces_tu_stat():
                    jekolemcesta,cesty = cell.jekolem(1)
                    cell.vztyk()
                    if jekolemcesta:
                        for cesta in cesty:
                            if cesta.zaorame():
                                cesta.zaorat()
                    zvednuto_domu +=1
    return zvednuto_domu

def propability(fromx,fromy,smatrani):
    d1 = 1
    d2 = 0
    citatel = 0
    jmenovatel = 0
    for i in range(smatrani):
        for i in signum:
            x = fromx + d1*i[0]
            y = fromy + d2*i[1]

            if 0<x<SIRKA and 0<y<VYSKA:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                citatel += mat[x][y].value*(distance**(-gama))
                jmenovatel += distance**(-gama)
                
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                citatel += mat[x][y].value*(distance**(-gama))
                jmenovatel += distance**(-gama)
                
        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1
    return citatel/jmenovatel

def maximum():
    fromx = SIRKA//2
    fromy = VYSKA//2
    d1 = 1
    d2 = 0
    citatel = 0
    jmenovatel = 0
    for i in range(smatrani):
        for i in signum:
            x = fromx + d1*i[0]
            y = fromy + d2*i[1]

            if 0<x<SIRKA and 0<y<VYSKA:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                citatel += 3*(distance**(-gama))
                jmenovatel += distance**(-gama)
                
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA:
                distance = sqrt(((fromx-(x))**2)+((fromy-(y))**2))
                citatel += 3*(distance**(-gama))
                jmenovatel += distance**(-gama)
                
        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1
    return citatel/jmenovatel

class POLE:
    def __init__(self, x,y):
        self.x = x
        self.y = y

class Nic(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 0
        self.id = 0
        self.farbe = 255

class Cesta(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 1
        self.id = 1
        self.farbe = 0
    
    def zaorame(self): 
        """vrátí True jestli cesta je konečná a k ničemu nevede"""

        pripoje = 0
        for dx,dy in dokola:
            if 0 <= self.x+dx < SIRKA and 0 <= self.y+dy < SIRKA:
                if mat[self.x+dx][self.y+dy].id > 0:
                    pripoje+=1
                    if pripoje == 2:
                        return False
        return True
    
    def zaorat(self):
        slepa = True
        x = self.x
        y = self.y
        while slepa:
            cestykolem = 0 #je to jen pojistka, která by zde neměla být potřeba ale občas se program zasekne v tom whilu
            for dx,dy in dokola:
                if mat[x+dx][y+dy].id == 1:
                    cestykolem +=1
                    mat[x][y] = Nic(x,y)
                    x +=dx
                    y +=dy
                    slepa = mat[x][y].zaorame()
                    break
            if cestykolem == 0:
                return

class Trasa:
    def __init__(self,startx,starty,kam_chci_id):
        self.startx = startx
        self.starty = starty
        self.prvky = [[startx,starty]]
        self.kam_chci_id = kam_chci_id
        self.vzdalenost = dis_to_nearest(startx,starty,kam_chci_id)
        self.hodnoceni = 0

    def pridej_cestu(self,x,y):
        self.prvky.append([x,y])

    def get_vzdalenost(self):
        self.vzdalenost = dis_to_nearest(self.prvky[-1][0],self.prvky[-1][1],self.kam_chci_id)
        return self.vzdalenost
    
    def usmernit(self):
        hrbitov = []
        prvky = self.prvky
        index = len(prvky)
        #for index in range(len(prvky)-1,0,-1):
        while index != 1:
            index -=1
            for idx in range(0,index-1):
                if sqrt((prvky[idx][0]-prvky[index][0])**2 + (prvky[idx][1]-prvky[index][1])**2 ) == 1:
                    for i in range(index-1,idx,-1):
                        hrbitov.append(prvky[i])
                    index = idx + 1
                    break



        for i in hrbitov:

            self.prvky.remove(i)

class Dum(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 4
        self.id = 2
        self.farbe = random.random()*100+100
        self.tvar = random.choice(tvary)
        self.lpozic = []

    def get_lpozic(self):
        self.lpozic = []
        for dx,dy in self.tvar:
            self.lpozic.append([self.x+dx,self.y+dy])
        return self.lpozic
    
    def posun_se(self):
        """změní souřadnice domu, posun v kříži)"""
        dx,dy = random.choice(dokola)
        if  3< (self.x+dx) < (SIRKA-4):
            self.x = dx+self.x
        if 3 < (self.y+dy) < (SIRKA-4):
            self.y = dy+self.y
    
    def muzu_sednout(self):
        #true pokud je na prázdných polích a je v přítomnosti objektu který není prázdné pole
        self.get_lpozic()

        for x,y in self.lpozic:
            if  mat[x][y].id != 0:  
                return False


        a = propability(self.x,self.y,smatrani)/max_propabiliti
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
                if mat[x+dx][y+dy].id == 1:
                    return True
        
        trasy = []
        for kolx,koly in kolem:
            if mat[kolx][koly].id == 0:
                trasy.append(Trasa(kolx,koly,1))
        
        if len(trasy) ==0:
            print("bez silnice")
            return
        
        ta_prava = trasy[0]
        for trasa in trasy:
            if trasa.get_vzdalenost()<=ta_prava.get_vzdalenost():
                ta_prava = trasa
    
        for i in range(212):
            if i % 50 ==0 and i>2:
                print("náročná cesta")

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
                if 0<x+posun[0]<VYSKA and 0<y+posun[1]<SIRKA and mat[x+posun[0]][y+posun[1]].id == 1:

                    if len(ta_prava.prvky) > 3:
                        ta_prava.usmernit() 
                    for pole in ta_prava.prvky:
                        mat[pole[0]][pole[1]] = Cesta(pole[0],pole[1])
                    
                    return
                
            trasy = []
            for posun in dokola:

                if 0<x+posun[0]<VYSKA and 0<y+posun[1]<SIRKA and mat[x+posun[0]][y+posun[1]].id == 0 and [x+posun[0],y+posun[1]] not in ta_prava.prvky:
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


    def nechces_tu_stat(self):
        
        propability_of_staying = propability(self.x,self.y, smatrani)/max_propabiliti
        r = random.random()+0.5 #0.4 je jen parametr, potenciálový val, který se musí při stěhování překročit

        if r < propability_of_staying:
            return True #zvedne se            
        else:
            return False #nezvedne se

    def vztyk(self):
        """smaže dům v poli a přidá ho do houses listu a posune ho"""
        pozice = self.get_lpozic()
        for x,y in pozice:
            mat[x][y] = Nic(x,y)
        houses.append(self)
        self.posun_se()

    def jekolem(self,id):
        """vrátí bool a objektycest, určuje jestli a kolik je v okolí buňek určitého id"""
        
        l = []
        b = False
        pozice = self.get_lpozic()
        for x,y in pozice:
            for dx,dy in dokola:
                if [x+dx,y+dy] in pozice:
                    ...
                elif mat[x+dx][y+dy].id == id:
                    b = True
                    l.append(mat[x+dx][y+dy])

        return b,l

class Kostel(Dum):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 200
        self.id = 2
        self.farbe = 50
        self.tvar =  [[0,0],[-1,0],[-1,-1],[-2,0],[-1,1]]
        self.lpozic = []

    def chces_tu_stat(self): #kostel se nestěhuje
        return False
    def vztyk(self): #kostel se nestěhuje
        ...
            
 
gama = 6
a = 300
VYSKA, SIRKA = a,a
ndomu = 3000
smatrani = 11 #23
#os.makedirs('frames_folder', exist_ok=True)


mat = matrix(VYSKA, SIRKA)
prvni = Kostel(SIRKA//2,VYSKA//2)
prvni.get_lpozic()
prvni.sednout()
mat[SIRKA//2+1][VYSKA//2] = Cesta(SIRKA//2+1,VYSKA//2)
max_propabiliti = maximum()
houses = [Dum(random.randint(5,SIRKA-6),random.randint(5,VYSKA-6)) for i in range(ndomu)]
t = time.localtime()
current_time = time.strftime("%H:%M", t)
nusedliku = 0
presunuti = 0
npic = 0


infloop = 0
while len(houses)!=0 and infloop<SIRKA*20:
    infloop +=1
    emigranti = []
    for house in houses:
        x = house.x
        y = house.y
        if house.muzu_sednout():
            house.sednout()
            house.zarid_cestu()
            emigranti.append(house)
            nusedliku +=1
            print(nusedliku)
            infloop = 0
            #maxim = max_propabiliti


        else:    
            house.posun_se() #změní souřadnice domu

    for emg in emigranti:
        houses.remove(emg)

    




tt = time.localtime()
tcurrent_time = time.strftime("%H:%M", tt)
print("začátek",current_time)
print("listova hotova:",tcurrent_time)
print("přesunuto:",presunuti)



"""obrazky = [imageio.v2.imread(f"frames_folder/frame_{i}.png") for i in range(npic)]
imageio.mimsave(f"snímky/gify/animation{nusedliku}.gif",obrazky,loop = 100, duration = 400)

# Smazání složky se snímky
for file_path in os.listdir('frames_folder'):
    os.remove(os.path.join('frames_folder', file_path))
os.rmdir('frames_folder')
"""

mapa = [[obj.farbe for obj in row] for row in mat]

plt.imshow(mapa, cmap="hot")
#plt.savefig(f"dla{VYSKA}-{nusedliku}.png")
plt.show()