import random
import matplotlib.pyplot as plt
import copy
import time
from math import sqrt
import os
import imageio
from PIL import Image

#*------*-----*----*---*--*-*CO MŮŽU ZLEPŠIT*-*--*---*----*-----*------*
# urovnat kód
# přidat speciální budovy, aby se tvořili v místech hustého osidlení
# 3D model
# není nic jako nic, přidat k NIC různé value, které by třeba násobili pravděpodobnost usednutí. Les...pravd*0,4 VOda...pravd*0.001   louka...pravd*0.96   svah...pravd*0.89   kopec...pravd*0.80  uvody...pravd*1.2

dokola = [[0,1],[1,0],[0,-1],[-1,0]]
pic = 0
signum = [[1,1],[1,-1],[-1,1],[-1,-1]]
rposun = (1,-1)
dic_smatrani = {
    15:127,
    14:113,
    13:97,
    12:84,
    11:70,
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

def distance(fromx,fromy,kamx,kamy):
    return sqrt((fromx-kamx)**2 + (fromy - kamy)**2)

def matrix(VYSKA, SIRKA):
    plan = [[Nic(x,y) for y in range(SIRKA)] for x in range(VYSKA)]
    return(plan)

def dis_to_nearest(fromx,fromy,id):
    d1 = 1
    d2 = 0
    while True:
        for s1,s2 in signum:
            x = fromx + d1*s1
            y = fromy + d2*s2

            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].id == id:
                return distance(fromx,fromy,x,y)
            
            x = fromx + d2*s1
            y = fromy + d1*s2
            if 0<x<SIRKA and 0<y<VYSKA and mat[x][y].id == id:
                return distance(fromx,fromy,x,y)

        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1

def savepic(npic):
    '''uloží aktuální figuru do frames_folder v png'''
    mapa = [[obj.farbe for obj in row] for row in mat]
    plt.imshow(mapa, cmap="hot")
    plt.savefig(f"frames_folder/frame_{npic}.png", format='PNG', bbox_inches='tight', dpi = 600)
    plt.close()  # Zavřít aktuální figuru, aby neovlivňovala další snímky
    npic += 1
    return npic

def stehovani(): 
    """zvedne domy z pole a přesune je do listu houses,usměrní pahýly sinlic, vrátí počet zvednutých domů"""
    prace_pro_stehovaky = []
    for row in mat:
        for cell in row:
            if cell.id == 2:
                if cell.nechces_tu_stat() and cell not in prace_pro_stehovaky:
                    prace_pro_stehovaky.append(cell)
                
    for house in prace_pro_stehovaky: 
        jekolemcesta,cesty = house.jekolem(1)
        house.vztyk()
        if jekolemcesta:
            for cesta in cesty:    
                if cesta.zaorame():
                    cesta.zaorat()

    return len(prace_pro_stehovaky)

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
                dist = distance(fromx,fromy,x,y)
                citatel += mat[x][y].value*(dist**(-gama))
                jmenovatel += dist**(-gama)
                
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA:
                dist = distance(fromx,fromy,x,y)
                citatel += mat[x][y].value*(dist**(-gama))
                jmenovatel += dist**(-gama)
                
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
                dist = distance(fromx,fromy,x,y)
                citatel += 3*(dist**(-gama))
                jmenovatel += dist**(-gama)
                
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA:
                dist = distance(fromx,fromy,x,y)
                citatel += 3*(dist**(-gama))
                jmenovatel += dist**(-gama)
                
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
            
    def zaorat2(self): #neúspěšný pokus o spolehlivější odstraňování cest
        x = self.x
        y = self.y
        for dx,dy in dokola:
            if mat[x+dx][y+dy].id == 2:
                return
        neprozkoumane = [[x,y]]
        cesta_prvky = []
        potrebne = []
        while len(neprozkoumane) != 0:
            print("prvni while", len(neprozkoumane),x,y)
            copy_neprozkoumane = copy.deepcopy(neprozkoumane)
            for x,y in copy_neprozkoumane:
                potrebna = False
                for dx,dy in dokola:
                    if mat[x+dx][y+dy].id == 2:
                        neprozkoumane.remove([x,y])
                        potrebne.append([x,y])
                        potrebna = True
                        break
                if not potrebna:
                    cesta_prvky.append([x,y])
                    neprozkoumane.remove([x,y])
                    for dx,dy in dokola:        
                        if mat[x+dx][y+dy].id == 1 and [x+dx,y+dy] not in cesta_prvky and [x+dx,y+dy] not in neprozkoumane and [x+dx,y+dy] not in potrebne:
                            neprozkoumane.append([x + dx,y +dy])
            copy_cesta_prvky = copy.deepcopy(cesta_prvky)
            for x,y in copy_cesta_prvky:
                kolempotrebnych = 0
                potr = []
                for dx,dy in dokola:
                    if [x+dx,y+dy] in potrebne:
                        kolempotrebnych += 1
                        potr.append([x+dx,y+dy])
                if kolempotrebnych >1:
                    cesta_prvky.remove([x,y])
                    potrebne.append([x,y])
                    for i in potr:
                        potrebne.remove(i)


        if len(potrebne) == 0: #to je blbost, proč to tu je?
            return
        
        elif len(potrebne) == 1:
            for x,y in cesta_prvky:
                mat[x][y] = Nic(x,y)
            return
        
        #elif len(potrebne) == 2:
        #    while True:
         #       for x,y in cesta_prvky:
        #            kolemcest = 0
        #            for dx,dy in dokola:
        #                if [x+dx,y+dy] in cesta_prvky:
        #                    kolemcest +=1
        #            if kolemcest ==1:

        #                mat[x,y] = Nic(x,y)


        elif len(potrebne) > 2:
            krizovatky = [1,1,1]
            loopstop = 2*len(cesta_prvky) +5
            while len(krizovatky) > (len(potrebne)-2) and loopstop > 0:
                loopstop -=1
                print("druhy while",x,y, len(krizovatky), len(potrebne)-2, krizovatky)
                krizovatky = []
                for x,y in cesta_prvky:
                    kolemcest = 0
                    for dx,dy in dokola:
                        if mat[x+dx][y+dy].id == 1:
                            kolemcest += 1
                    if kolemcest >= 3:
                        krizovatky.append([x,y])
                if len(krizovatky)>0:    
                    nahodna_krizovatka = random.choice(krizovatky)
                    cesta_prvky.remove(nahodna_krizovatka)
                    for x,y in cesta_prvky:
                        kolemcest = 0
                        for dx,dy in dokola:
                            if [x+dx,y+dy] in cesta_prvky or [x+dx,y+dy] in potrebne:
                                kolemcest += 1
                        if kolemcest == 1:
                            cesta_prvky.append(nahodna_krizovatka)
                            break
                        else:    
                            mat[x][y] = Nic(x,y)
                        
                        
                    
            """cesty_co_zustanou = []
            for i in range(1,len(potrebne)):
                x,y = potrebne[i]
                while True:
                    moznosti = []
                    for dx,dy in dokola:
                        if mat[x+dx][y+dy].id == 1 and [x+dx,y+dy] in cesta_prvky:
                            moznosti.append([x+dx][y+dy])
                    nejvyssi = 0
                    moznost = None
                    for x,y in moznosti:
                        r = (distance(x,y,potrebne[i-1].x,potrebne[i-1].y))
                        if r > nejvyssi:
                            moznost = [x,y]
                            nejvyssi = r
                        
                    

            for l in cesta_prvky:
                if l not in cesty_co_zustanou:
                    mat[l[0]][l[1]] = Nic(l[0],l[1])
                           """

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
        self.posledni_pravdepodobnost = 0

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

        if r < a and a > self.posledni_pravdepodobnost:

            return True
            
        else:
            return False
    
    def sednout(self):
        for x,y in self.lpozic:
            mat[x][y] = self

    def zarid_cestu(self):
        self.get_lpozic()
        kolem = []
        
        for x,y in self.lpozic:
            for dx,dy in dokola:
                if 0<x+dx<VYSKA and 0<y+dy<VYSKA and [x+dx,y+dy] not in self.lpozic:
                    if mat[x+dx][y+dy].id == 1:
                        return True
                    if [x+dx,y+dy] not in kolem:
                        kolem.append([x+dx,y+dy])
                    
        
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

            # 0<x+dx<VYSKA and 0<y+dy<SIRKA
            for dx,dy in dokola:
                if mat[x+dx][y+dy].id == 1:

                    if len(ta_prava.prvky) > 3:
                        ta_prava.usmernit() 
                    for pole in ta_prava.prvky:
                        mat[pole[0]][pole[1]] = Cesta(pole[0],pole[1])
                    
                    return
                
            trasy = []
            for dx,dy in dokola:

                if mat[x+dx][y+dy].id == 0 and [x+dx,y+dy] not in ta_prava.prvky:
                    t = copy.deepcopy(ta_prava)
                    t.pridej_cestu(x+dx,y+dy)
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

    def nechces_tu_stat(self):
        
        propability_of_staying = propability(self.x,self.y, smatrani)/max_propabiliti
        r = random.random()  #0.4 je jen parametr, potenciálový val, který se musí při stěhování překročit
        propability_of_staying += potencialovy_val
        
        if r < propability_of_staying:
            return False #nezvedne se
            
        else:
            self.posledni_pravdepodobnost = propability_of_staying
            return True #zvedne se

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
            
potencialovy_val = 0.2
gama = 6.3
a = 300
VYSKA, SIRKA = a,a
ndomu = 4000
poznamka = "stehovanedomymajisvujmaxparametrpoprve"
smatrani = dic_smatrani[15]  #(0,15)index podle toho kolik polí kolem sebe chceš šmátrat
os.makedirs('frames_folder', exist_ok=True)


mat = matrix(VYSKA, SIRKA)
"""prvni = Kostel(SIRKA//2,VYSKA//2)
prvni.get_lpozic()
prvni.sednout()
mat[SIRKA//2+1][VYSKA//2] = Cesta(SIRKA//2+1,VYSKA//2)"""

prvni = Kostel(SIRKA//4,VYSKA//2)
prvni.get_lpozic()
prvni.sednout()
mat[SIRKA//4+1][VYSKA//2] = Cesta(SIRKA//4+1,VYSKA//2)

pprvni = Kostel(3*SIRKA//4,VYSKA//2)
pprvni.get_lpozic()
pprvni.sednout()
#mat[3*SIRKA//4+1][VYSKA//2] = Cesta(3*SIRKA//4+1,VYSKA//2)

"""ppprvni = Kostel(SIRKA//2,2*VYSKA//3)
ppprvni.get_lpozic()
ppprvni.sednout()
mat[SIRKA//2+1][2*VYSKA//3] = Cesta(SIRKA//2+1,2*VYSKA//3)"""

max_propabiliti = maximum()
houses = [Dum(random.randint(5,SIRKA-6),random.randint(5,VYSKA-6)) for i in range(ndomu)]
#houses = [Dum(SIRKA//2,VYSKA//2) for i in range(ndomu)]



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
        if house.muzu_sednout():
            house.sednout()
            house.zarid_cestu()
            emigranti.append(house)
            print(nusedliku)
            infloop = 0
            #maxim = max_propabiliti

            if nusedliku % (ndomu//5) == 0:
                npic = savepic(npic)

            if nusedliku % (ndomu//5) == 0: #zvednutí domů
                presunuti += stehovani()

            if nusedliku % 20 == 0:
                npic = savepic(npic)

            nusedliku +=1
        
        else:    
            house.posun_se() #změní souřadnice domu

    for emg in emigranti:
        houses.remove(emg)

    




tt = time.localtime()
tcurrent_time = time.strftime("%H:%M", tt)
print("začátek",current_time)
print("listova hotova:",tcurrent_time)
print("přesunuto:",presunuti)



obrazky = [imageio.v2.imread(f"frames_folder/frame_{i}.png") for i in range(npic)]
imageio.mimsave(f"snímky/gify/animation_nused{nusedliku}_{SIRKA}x{VYSKA}_presunuti{presunuti}_gamma{gama}_smatrani{smatrani}_potencialovyval{potencialovy_val}_{poznamka}.gif",obrazky,loop = 100, duration = 200)

# Smazání složky se snímky
for file_path in os.listdir('frames_folder'):
    os.remove(os.path.join('frames_folder', file_path))
os.rmdir('frames_folder')


mapa = [[obj.farbe for obj in row] for row in mat]

plt.imshow(mapa, cmap="hot")
plt.savefig(f"{nusedliku}_{SIRKA}x{VYSKA}_presunuti{presunuti}_gamma{gama}_smatrani{smatrani}_potencialovyval{potencialovy_val}_{poznamka}.png", dpi = 600)
#img = Image.fromarray(np.uint8(barevna_matice))
plt.show()