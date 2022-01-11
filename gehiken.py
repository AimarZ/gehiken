import random
import pygame
import os,sys
from PIL import Image
import requests
from io import BytesIO
import urllib.request

#Fitxategi baten izena emanda, fitxategi horretatik ausazko lerro batetik izena, ikuspenak eta irudiaren URL-a itzultzen ditu. "Random" parametroarekin edozein fitxategi hartu
#Jokuaren barruan erabiltzeko prestatuta, event-ak kudeatzeko
def lortuErrenkadaJokuan(fitx="Random"):
    if(fitx=="Idazleak.txt"):
        zenbat=231
    elif(fitx=="Aktoreak.txt"):
        zenbat=75
    elif(fitx=="Futbolariak.txt"):
        zenbat=105
    elif(fitx=="Abesleak.txt"):
        zenbat=42
    elif(fitx=="Random"):
        fitx= random.choice(["Idazleak.txt","AktoreakIrudiekin.txt","Futbolariak.txt","Abesleak.txt"])
        if(fitx=="Idazleak.txt"):
            zenbat=231
        elif(fitx=="AktoreakIrudiekin.txt"):
            zenbat=75
        elif(fitx=="Futbolariak.txt"):
            zenbat=105
        elif(fitx=="Abesleak.txt"):
            zenbat=42
    with open(fitx, encoding=("utf-8")) as fp:
        ind= random.randint(1,zenbat)
        enumerate(fp)
        for i, line in enumerate(fp):
            if i==ind:
                return line.split(",")
            for event in pygame.event.get(): #Kudeatu jokuko event-ak, izoztu ez dadin
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if(pos[0]>=1210 and pos[0]<=1245 and pos[1]>=40 and pos[1]<=80):
                        pygame.display.quit()
                        sys.exit()   
    return("")


#Handitzen doazen zenbakien animazioa sortzeko funtzioa
def animatu(zenb,zenbBerria,window,eskala, this_image2,testu2,testu2B,testu2_rect):
    myfont1= pygame.font.Font("brandon-grotesque-bold-italic.ttf", 100)
    i=0 
    handipena=1 #Iterazio bakoitzean i zenbat handituko den.
    if(eskala==1):
        handipena=5
    color=(255,255,255) #Hasieratu zenbakiaren kolorea txurira
    while(i<=zenbBerria): #i ikuspen berriak baino txikiagoa den bitartean
        itxaron=10 #Itxaron= zenbat milisegundu itxaroten diren animazioaren frame bakoitzeko
        
        #ITXARON ALDAGAIAREKIN JOKATU, ANIMAZIOA MOTELAGOA/AZKARRAGOA EGITEKO MOMENTU BATZUETAN
        if zenbBerria>500: #Ikuspen berriak nahiko handiak badira, frame azkarragoak (animazioak asko ez irauteko)
            itxaron=3
        if zenbBerria>5000: #Ikuspen berriak dexente handiak badira, frame azkarragoak
            itxaron=1
        if zenbBerria>10000: #Ikuspen berriak oso handiak badira, frame oso azkarrak
            itxaron=0
        if(zenb<4 and i<=zenb+1): #zenb oso txikia bada, hasieran animazio oso motela emozioa emateko
            itxaron=1000
        elif(zenb<10 and i<=zenb+1): #Zenbat nahiko txikia bada, hasieran animazio motela emozioa emateko
            itxaron=300
        elif(i<=zenb and i>=zenb-20): #Zenbaki berria aurreko artikuluaren zenbakitik gertu badago, moteldu emozioa emateko
            itxaron=200
        elif(i<zenb): #Bestela, orokorrean kalkulatu itxaron aldagaiaren balioa erlatiboki
                      #i zenb-etik gero eta gertuago egon, orduan eta motelagoa.
            itxaron= int(100/abs(zenb-i))
        if(i>zenb): #Eskuineko barrak aurrekoa gainditu badu, aldatu kolorea berdera.
            color=(0, 149, 63)
        if(i>zenb+5000 and zenbBerria>20000): #Artikulu berriaren ikuspenak ikaragarri handiak badira eta jada aurrekoa gainditu
                                              #bada, atera eta bukatu animazioa. Ez da nahi asko irautea.
            break
        if(i>10000 and zenb>20000 and zenbBerria>20000): #Bien ikuspenak ikaragarri handiak badira eta jada aurrekoa gainditu
                                                         #bada, atera eta bukatu animazioa. Ez da nahi asko irautea.
            break

        pygame.time.delay(itxaron) #Itxaron milisegundu batzuk
        zenbakia = myfont1.render(f"{i}", True, color)
        zenbakiaB = myfont1.render(f"{i}", True, (0,0,0))
        pygame.draw.rect(window,(0,0,0),(640,100,640,680)) #Ezabatu aurreko irudia + zenbakia
        
        window.blit(this_image2, (640,100)) #Marraztu berriz irudia gainetik
        #Marraztu zenbakia 5 aldiz oso gertu, bordeak jartzeko
        window.blit(zenbakiaB,(900,403)) 
        window.blit(zenbakiaB,(900,397))
        window.blit(zenbakiaB,(903,400))
        window.blit(zenbakiaB,(897,400))
        window.blit(zenbakia,(900,400))
        
        #Marraztu testua 5 aldiz oso gertu, bordeak jartzeko
        window.blit(testu2B, (testu2_rect.x+3,testu2_rect.y))
        window.blit(testu2B, (testu2_rect.x-3,testu2_rect.y))
        window.blit(testu2B, (testu2_rect.x,testu2_rect.y+3))
        window.blit(testu2B, (testu2_rect.x,testu2_rect.y-3))
        window.blit(testu2, testu2_rect)
        
        pygame.display.update()
        i+=handipena
        for event in pygame.event.get(): #Kudeatu jokuko gertaerak
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if(pos[0]>=1210 and pos[0]<=1245 and pos[1]>=40 and pos[1]<=80):
                    pygame.display.quit()
                    sys.exit()         

    

#MAIN METODOA
#Parametro gisa pasa zein fitxategitik hartuko diren balioak ("Random" = edozein)
def main(fitx="Random"):
    
    beltza = pygame.Color(0, 0, 0)      
    txuria = pygame.Color(255, 255, 255)  
    berdea = pygame.Color(0, 149, 63)      
    gorria = pygame.Color(255, 0, 0)       
    urdina = pygame.Color(0, 0, 255)    
    
    
    windowsize=(1280,780)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30,20) #Leihoaren posizioa 
    pygame.display.init()
    pygame.font.init()
    window = pygame.display.set_mode(windowsize)
    pygame.display.set_caption('Gehiago ala gutxiago?')
    background = pygame.image.load('gehiken.png')
    window.fill(beltza)
    window.blit(background, (0, 0)) 
    


    myfont1= pygame.font.Font("brandon-grotesque-bold-italic.ttf", 40)
    myfont2= pygame.font.Font("brandon-grotesque-bold-italic.ttf", 50)
    myfont3= pygame.font.Font("brandon-grotesque-bold-italic.ttf", 100)
    
    eskala=5 #Definitu eskala (ikuspen bakoitzak zenbat pixel balioko dituen)
    puntuak=0 #Puntuazioa 0-ra hasieratu

    
    errenkada= lortuErrenkadaJokuan(fitx)
    izena= errenkada[0] 
    zenb= int(errenkada[1])
    URL= errenkada[2]
    
    #Lortu irudia url-tik
    response = requests.get(URL)
    with urllib.request.urlopen(URL) as url:
        with open('temp.png', 'wb') as f:
            f.write(url.read())
    
    #Kargatu irudia
    this_image = pygame.image.load('temp.png')
    this_image = pygame.transform.scale(this_image, (640, 680))
    this_image.convert_alpha()
    this_image.set_alpha(100)
            
    bukatu=False
    hurrengoa_prest= False
    izenaNext = None
    zenbNext= None
    #JOKUAREN ITERAZIO NAGUSIA
    while(not bukatu):
        
        window.fill(beltza)
        erantzuna=0
        pygame.time.delay(20)
        
        ixa = myfont2.render("X", True, gorria) #Definitu X bat, jokutik ateratzeko izango dena
        window.blit(ixa,(1210,20)) #Jarri X leihoan
        if(len(izena)>27): #Lortu den izena oso luzea bada, moztu eta jarri 3 puntu
            izena=izena[:27]+"..."
        
        window.blit(this_image, (0,100)) #Marraztu 1. irudia
        
        
        testu1 = myfont1.render(f"{izena}", True, txuria)
        testu1B = myfont1.render(f"{izena}", True, beltza)
        PosDiferentzia1= len(izena)-17
        testu1_rect = testu1.get_rect(center=(330, 585))   
        
        #Marraztu izena (5 aldiz, bordea lortzeko)
        window.blit(testu1B, (testu1_rect.x+3,testu1_rect.y))
        window.blit(testu1B, (testu1_rect.x-3,testu1_rect.y))
        window.blit(testu1B, (testu1_rect.x,testu1_rect.y+3))
        window.blit(testu1B, (testu1_rect.x,testu1_rect.y-3))
        window.blit(testu1, testu1_rect)
        
        #Marraztu bere ikuspen kopurua (5 aldiz, bordea lortzeko)
        zenb1= myfont3.render(f"{zenb}", True, txuria)
        zenb1B= myfont3.render(f"{zenb}", True, beltza)
        window.blit(zenb1B,(283,400))
        window.blit(zenb1B,(277,400))
        window.blit(zenb1B,(280,403))
        window.blit(zenb1B,(280,397))
        window.blit(zenb1,(280,400))
        pygame.display.update()
        
        if(not hurrengoa_prest): #Hurrengo pertsona ez badago prest, irakurri
            errenkadaBerria= lortuErrenkadaJokuan(fitx) #Lortu 2. errenkada
            izenBerria = errenkadaBerria[0]
            zenbBerria = int(errenkadaBerria[1])
            URL = errenkadaBerria[2]
            response = requests.get(URL)
            with urllib.request.urlopen(URL) as url:
                with open('temp.png', 'wb') as f:
                    f.write(url.read())
            this_image2 = pygame.image.load('temp.png')
            this_image2 = pygame.transform.scale(this_image2, (640, 680))
            this_image2.convert_alpha()
            this_image2.set_alpha(100)
            window.blit(this_image2, (640,100))
        else:
            izenBerria = izenaNext
            zenbBerria = zenbNext
            this_image2 = pygame.image.load('tempNext.png')
            this_image2 = pygame.transform.scale(this_image2, (640, 680))
            this_image2.convert_alpha()
            this_image2.set_alpha(100)
            window.blit(this_image2, (640,100))
                
        
        
        
        testu2 = myfont1.render(f"{izenBerria}", True, txuria)
        testu2B = myfont1.render(f"{izenBerria}", True, beltza)
        testu2_rect = testu2.get_rect(center=(950, 585))
        window.blit(testu2B, (testu2_rect.x+3,testu2_rect.y))
        window.blit(testu2B, (testu2_rect.x-3,testu2_rect.y))
        window.blit(testu2B, (testu2_rect.x,testu2_rect.y+3))
        window.blit(testu2B, (testu2_rect.x,testu2_rect.y-3))
        window.blit(testu2, testu2_rect)
        
        #Idatzi zenbait testu
        gehiago = myfont2.render("GEHIAGO", True, berdea)
        gehiagoB = myfont2.render("GEHIAGO", True, beltza)
        window.blit(gehiagoB,(353,650))
        window.blit(gehiagoB,(347,650))
        window.blit(gehiagoB,(350,647))
        window.blit(gehiagoB,(350,653))
        window.blit(gehiago,(350,650))
        ala = myfont2.render(" ala ", True, txuria)
        alaB = myfont2.render(" ala ", True, beltza)
        window.blit(alaB,(603,650))  
        window.blit(alaB,(597,650))  
        window.blit(alaB,(600,653))  
        window.blit(alaB,(600,647))   
        window.blit(ala,(600,650))   
        gutxiago = myfont2.render("GUTXIAGO?", True, gorria)
        gutxiagoB = myfont2.render("GUTXIAGO?", True, beltza)
        window.blit(gutxiagoB,(713,650)) 
        window.blit(gutxiagoB,(707,650)) 
        window.blit(gutxiagoB,(710,653)) 
        window.blit(gutxiagoB,(710,647)) 
        window.blit(gutxiago,(710,650)) 
        pygame.display.update()
        
        while(not erantzuna): #Itxaron erabiltzailearen erantzunaren zain
            
            for event in pygame.event.get(): #Bitartean kudeatu gertaerak
                if event.type == pygame.MOUSEBUTTONUP: 
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if(pos[0]>=347 and pos[0]<=563 and pos[1]>=665 and pos[1]<=704):
                        erantzuna=1 #gehiago
                    elif(pos[0]>=710 and pos[0]<=964 and pos[1]>=665 and pos[1]<=704):
                        erantzuna=2 #gutxiago
                    elif(pos[0]>=1210 and pos[0]<=1245 and pos[1]>=40 and pos[1]<=80):
                        bukatu=True
                        break
            if bukatu:
                break
                
        if(bukatu):
            break
        
        #Ezabatu leiho osoa eta marraztu gauzak
        window.fill(beltza)
        window.blit(ixa,(1210,20))
        window.blit(this_image, (0,100))
        window.blit(testu1B, (testu1_rect.x+3,testu1_rect.y))
        window.blit(testu1B, (testu1_rect.x-3,testu1_rect.y))
        window.blit(testu1B, (testu1_rect.x,testu1_rect.y+3))
        window.blit(testu1B, (testu1_rect.x,testu1_rect.y-3))
        window.blit(testu1, testu1_rect)
        
        window.blit(zenb1B,(283,400))
        window.blit(zenb1B,(277,400))
        window.blit(zenb1B,(280,403))
        window.blit(zenb1B,(280,397))
        window.blit(zenb1,(280,400))
        
        #Animatu zenbakiaren handipena
        animatu(zenb,zenbBerria,window,eskala,this_image2,testu2,testu2B,testu2_rect)
        
        #Marraztu gauzak berriz
        window.fill(beltza)
        window.blit(ixa,(1210,20))
        window.blit(this_image, (0,100))
        window.blit(testu1B, (testu1_rect.x+3,testu1_rect.y))
        window.blit(testu1B, (testu1_rect.x-3,testu1_rect.y))
        window.blit(testu1B, (testu1_rect.x,testu1_rect.y+3))
        window.blit(testu1B, (testu1_rect.x,testu1_rect.y-3))
        window.blit(testu1, testu1_rect)
        
        window.blit(zenb1B,(283,400))
        window.blit(zenb1B,(277,400))
        window.blit(zenb1B,(280,403))
        window.blit(zenb1B,(280,397))
        window.blit(zenb1,(280,400))
        
        i=zenbBerria
        if(i==zenb):
            color=(255,255,255)
        if(i>zenb):
            color=(0, 149, 63)
        if(i<zenb):
            color=(255, 0, 0)
            lag=1
        zenbakia = myfont3.render(f"{i}", True, color)
        zenbakiaB = myfont3.render(f"{i}", True, (0,0,0))
        window.blit(this_image2, (640,100))
        window.blit(zenbakiaB,(900,403))
        window.blit(zenbakiaB,(900,397))
        window.blit(zenbakiaB,(903,400))
        window.blit(zenbakiaB,(897,400))
        window.blit(zenbakia,(900,400))
        pygame.time.delay(10)
        
        pygame.display.update()
        
        window.blit(testu2B, (testu2_rect.x+3,testu2_rect.y))
        window.blit(testu2B, (testu2_rect.x-3,testu2_rect.y))
        window.blit(testu2B, (testu2_rect.x,testu2_rect.y+3))
        window.blit(testu2B, (testu2_rect.x,testu2_rect.y-3))
        window.blit(testu2, testu2_rect)
        zuzena= myfont2.render("ZUZENA", True, txuria)
        zuzenaB= myfont2.render("ZUZENA", True, beltza)
        okerra= myfont2.render("OKERRA", True, txuria)
        okerraB= myfont2.render("OKERRA", True, beltza)
        pygame.display.update()
        
        #Konprobatu ea erantzuna zuzena izan den
        if(erantzuna==1):
            if(zenbBerria>=zenb):
                puntuak+=1
                window.blit(zuzenaB,(553,650))
                window.blit(zuzenaB,(547,650))
                window.blit(zuzenaB,(550,647))
                window.blit(zuzenaB,(550,653))
                window.blit(zuzena,(550,650))
            else:
                window.blit(okerraB,(553,650))
                window.blit(okerraB,(547,650))
                window.blit(okerraB,(550,647))
                window.blit(okerraB,(550,653))
                window.blit(okerra,(550,650))
                bukatu=True
        else:
            if(zenbBerria<=zenb):
                puntuak+=1
                window.blit(zuzenaB,(553,650))
                window.blit(zuzenaB,(547,650))
                window.blit(zuzenaB,(550,647))
                window.blit(zuzenaB,(550,653))
                window.blit(zuzena,(550,650))
            else:
                window.blit(okerraB,(553,650))
                window.blit(okerraB,(547,650))
                window.blit(okerraB,(550,647))
                window.blit(okerraB,(550,653))
                window.blit(okerra,(550,650))
                bukatu=True
        pygame.display.update()
        #pygame.time.delay(3000)
        #Prestatu hurrengo pertsona eta irudia
        errenkada= lortuErrenkadaJokuan(fitx)
        izenaNext= errenkada[0] 
        zenbNext= int(errenkada[1])
        URL= errenkada[2]
        
        #Lortu irudia URL-tik
        response = requests.get(URL)
        with urllib.request.urlopen(URL) as url:
            with open('tempNext.png', 'wb') as f:
                f.write(url.read())
        hurrengoa_prest=True
        pygame.time.delay(500)
        
        izena=izenBerria
        zenb=zenbBerria
        this_image=this_image2
        window.fill(beltza)
        
        
        if(bukatu): #Erantzun okerra izan bada, erakutsi puntuazioa
            window.fill(beltza)
            window.blit(ixa,(1210,20))
            puntuazioa= myfont2.render(f"Lortutako puntuak: {puntuak}", True, berdea)
            window.blit(puntuazioa,(450,365))
            replay= myfont2.render("Berriz jolastu", True, txuria)
            window.blit(replay,(500,450))
            pygame.display.update()
            erantzuna=0
            bukatu=False
            while(not erantzuna):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        print(pos)
                        if(pos[0]>=500 and pos[0]<=825 and pos[1]>=445 and pos[1]<=507):
                            erantzuna=1 #jarraitu jolasten
                            puntuak=0
                        if(pos[0]>=1210 and pos[0]<=1245 and pos[1]>=40 and pos[1]<=80):
                            bukatu=True
                            break
                if bukatu:
                    break   
    pygame.display.quit()        

#Exekutatu beharrekoa
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#main("Random")
main("Aktoreak.txt")
