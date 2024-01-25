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

dokola = [[0,1],[1,0],[0,-1],[-1,0]]
pic = 0
signum = [[1,1],[1,-1],[-1,1],[-1,-1]]
rposun = (1,-1)
#tvary = [[[0,0]],
#         [[0,0],[1,0]],
#        [[0,0],[0,1]],
#         [[0,0],[1,1],[1,0]]]
tvary = [[[0,0],[1,0]],
         [[0,0],[0,1]],
         [[0,0],[1,1],[1,0]],
         [[0,0],[1,1],[1,0],[0,1]],
         [[0,0],[1,1],[1,0],[2,0],[2,1]],
         [[0,0],[1,0],[2,0]],
         [[0,0],[0,1],[0,2]],
         [[0,0],[2,0],[1,1],[1,0]],
         [[0,0],[-1,-1],[-1,0]]

    ]

def jekolem(x,y,id):
    """vrátí bool a objektycest, určuje jestli a kolik je v okolí buňek určitého id"""
    l = []
    b = False
    for dx,dy in dokola:
        if mat[x+dx][y+dy].id == id:
            b = True
            l.append(mat[x+dx][y+dy])
    return b,l

"""def uloz_pic(frames):
    mapa = [[cell.farbe for cell in row] for row in mat]
    frames.append(mapa)
    

def vytvor_animaci(nkroku):
    obrazky = [imageio.imread(f"Python_my/life/life{ikrok}.png") for ikrok in range(0, nkroku)]
    imageio.mimsave("Python_my/life/Game_of_life.gif", obrazky)"""

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

def maximum():
    citatel = 0
    jmenovatel = 0
    
    for row in mat:
        for cell in row:



            distance = sqrt((((SIRKA//2+1)-(cell.x))**2)+(((VYSKA//2+1)-(cell.y))**2))
            if distance == 0:
                continue
            citatel += cell.id*(distance**(-gama))


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

def update(frame):
    ax.clear()
    ax.imshow(lmatic[frame], cmap='hot')    

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
        """vrátí bol jestli cesta je konečná a k ničemu nevede"""
        pripoje = 0
        for dx,dy in dokola:
            if mat[self.x+dx][self.y+dy].id > 0:
                pripoje+=1
                if pripoje == 2:
                    return False
        else:
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
        self.value = 1
        self.id = 2
        self.farbe = random.random()*100+100
        self.tvar = random.choice(tvary)
        self.lpozic = []

    def get_lpozic(self):
        self.lpozic = []
        for dx,dy in self.tvar:
            self.lpozic.append([self.x+dx,self.y+dy])
        return self.lpozic
    
    def muzu_sednout(self,maxim):
        #true pokud je na prázdných polích a je v přítomnosti objektu který není prázdné pole
        self.get_lpozic()

        for x,y in self.lpozic:
            if mat[x][y].id != 0:
  
                return False


        a = propability(self.x,self.y)/maxim


        r = random.random()
        #print(r)
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
            #print(ta_prava)
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
                    #print("našli jsme cestu", ta_prava.prvky)
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
        """mapa = [[obj.farbe for obj in row] for row in mat]
            
        for i in ta_prava.prvky:
            mapa[i[0]][i[1]] = 230
        mapa[ta_prava.startx][ta_prava.starty] = 0
        plt.imshow(mapa, cmap="hot")
        plt.savefig(f"dla{VYSKA}-{nusedliku}.png")"""
            #plt.show()

                #time.sleep(1)

    def chces_tu_stat(self, maxim):
        
        a = propability(self.x,self.y)/maxim
        r = random.random()+0.25 #0.1 je jen parametr, potenciálový val, který se musí při stěhování překročit
        
        if r < a:
            return True
            
        else:
            return False

    def vztyk(self,houses):
        for dx,dy in self.tvar:
            mat[self.x+dx][self.y + dy] = Nic(self.x+dx,self.y + dy)
        houses.append(self)
        return houses
        
                
class Kostel(Dum):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 5
        self.id = 2
        self.farbe = 50
        self.tvar =  [[0,0],[-1,0],[-1,-1],[-2,0],[-1,1]]
        self.lpozic = []
            
 
gama = 4
a = 50
VYSKA, SIRKA = a,a
nusedliku = 100
os.makedirs('frames_folder', exist_ok=True)


mat = matrix(VYSKA, SIRKA)
prvni = Kostel(SIRKA//2,VYSKA//2)
prvni.get_lpozic()
prvni.sednout()
mat[SIRKA//2+1][VYSKA//2] = Cesta(SIRKA//2+1,VYSKA//2)
maxim = maximum()
houses = [Dum(random.randint(3,SIRKA-3),random.randint(3,VYSKA-3)) for i in range(nusedliku)]
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
        if house.muzu_sednout(maxim):
            house.sednout()
            house.zarid_cestu()
            emigranti.append(house)
            nusedliku +=1
            print(nusedliku)
            infloop = 0
            maxim = propability(SIRKA//2,VYSKA//2+1)
            #print(len(houses))
            #mapa = [[obj.farbe for obj in row] for row in mat]
            #plt.imshow(mapa, cmap="hot")
            #plt.savefig(f"dla{VYSKA}-{nusedliku}.png")
            


        
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
        houses.remove(emg)

    if nusedliku % 50 == 0:
        mapa = [[obj.farbe for obj in row] for row in mat]
        plt.imshow(mapa, cmap="hot")
        plt.savefig(f"frames_folder/frame_{npic}.png", format='PNG', bbox_inches='tight')
        plt.close()  # Zavřít aktuální figuru, aby neovlivňovala další snímky
        npic += 1

    if nusedliku % 20 == 0:
        for row in mat:
            for cell in row:
                if cell.id == 2:
                    if cell.chces_tu_stat(maxim):
                        houses = cell.vztyk(houses)
                        b,cesty = jekolem(cell.x,cell.y,1)
                        if b:
                            for cesta in cesty:
                                if cesta.zaorame():
                                    cesta.zaorat()
                        #změnit housovi souradnice
                        presunuti+=1







tt = time.localtime()
tcurrent_time = time.strftime("%H:%M", tt)
print("začátek",current_time)
print("listova hotova:",tcurrent_time)
print("přesunuto:",presunuti)



obrazky = [imageio.v2.imread(f"frames_folder/frame_{i}.png") for i in range(npic)]
imageio.mimsave(f"snímky/gify/animation{nusedliku}.gif",obrazky, duration=1, repeat=5)

# Smazání složky se snímky
for file_path in os.listdir('frames_folder'):
    os.remove(os.path.join('frames_folder', file_path))
os.rmdir('frames_folder')


#mapa = [[obj.farbe for obj in row] for row in mat]

#plt.imshow(mapa, cmap="hot")
#plt.savefig(f"dla{VYSKA}-{nusedliku}.png")
#plt.show()