
signum = [[1,1],[1,-1],[-1,1],[-1,-1]]
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
                distance = distance(fromx,fromy,x,y)
                citatel += mat[x][y].value*(distance**(-gama))
                jmenovatel += distance**(-gama)
                
            x = fromx + d2*i[0]
            y = fromy + d1*i[1]
            if 0<x<SIRKA and 0<y<VYSKA:
                distance = distance(fromx,fromy,x,y)
                citatel += mat[x][y].value*(distance**(-gama))
                jmenovatel += distance**(-gama)
                
        if d1 == d2:
            d1 += 1
            d2 = 0
        else:
            d2 += 1
    return citatel/jmenovatel
    
def stehovani(): 
    """zvedne domy z pole a p�esune je do listu houses,usm�rn� pah�ly sinlic, vr�t� po�et zvednut�ch dom�"""
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

class Cesta(POLE):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.value = 1
        self.id = 1
        self.farbe = 0
    
    def zaorame(self): 
        """vr�t� True jestli cesta je kone�n� a k ni�emu nevede"""
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
            cestykolem = 0 #je to jen pojistka, kter� by zde nem�la b�t pot�eba ale ob�as se program zasekne v tom whilu
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
                
             
def muzu_sednout(self):
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
        return
    
    ta_prava = trasy[0]
    for trasa in trasy:
        if trasa.get_vzdalenost()<=ta_prava.get_vzdalenost():
            ta_prava = trasa

    for i in range(212):
        x = ta_prava.prvky[-1][0]
        y = ta_prava.prvky[-1][1]

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
            return

        ta_prava = trasy[0]
        for trasa in trasy:
            if trasa.get_vzdalenost()<=ta_prava.get_vzdalenost():
                ta_prava = trasa    


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


potencialovy_val = 0.35
gama = 4
a = 100
VYSKA, SIRKA = a,a
ndomu = 800
smatrani = dic_smatrani[8]  #index podle toho kolik pol� kolem sebe chce� �m�trat

mat = matrix(VYSKA, SIRKA)
mat[SIRKA//2][VYSKA//2] = Kostel(SIRKA//2,VYSKA//2)
mat[SIRKA//2+1][VYSKA//2] = Cesta(SIRKA//2+1,VYSKA//2)
houses = [Dum(random.randint(5,SIRKA-6),random.randint(5,VYSKA-6)) for i in range(ndomu)]

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
            nusedliku +=1
            house.zarid_cestu()
            emigranti.append(house)
            infloop = 0
            
            if nusedliku % (ndomu//5) == 0:
                npic = savepic(npic)

            if nusedliku % (ndomu//5) == 0: #zvednut� dom�
                presunuti += stehovani()
 
        else:    
            house.posun_se() #zm�n� sou�adnice domu

    for emg in emigranti:
        houses.remove(emg)