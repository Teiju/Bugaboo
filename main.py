#Kerää kaikki kentän kolikot ja siirry ovesta seuraavaan kenttään. Muista varoa kummitusta!

import pygame
import random
import sys

class Bugaboo:
    def __init__(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.tilanne = [["Kenttä: ", 1], ["Pisteet: ", 0], ["Elämiä jäljellä: ", 3], ["Liikuta roboa nuolinäppäimin!", ""]]
        self.leveys, self.korkeus, self.alareuna, self.reuna = 800, 500, 80, 30
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.fontti = pygame.font.SysFont("Arial", 20)
        self.ohjeRivi = self.fontti.render("Kerää kaikki kentän kolikot ja siirry ovesta seuraavaan kenttään.", True, (255,255,200))
    
        pygame.display.set_caption("BUGABOO!")
        self.uusi_peli()


    def uusi_peli(self):
        self.tilanne = [["Kentta: ", 1], ["Pisteet: ", 0], ["Elämiä jäljellä: ", 3], ["Liikuta roboa nuolinäppäimin!", ""]]
        self.lataa_kuvat()
        self.uusi_kentta()
        self.pelaa()


    def pelaa(self):
        oikealle = False
        vasemmalle = False
        alas = False
        ylos = False
        while True:
            for tapahtuma in pygame.event.get():
                if self.tilanne[2][1] <= 0:
                    tapahtuma.type == self.lopetus()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = True
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = True
                    if tapahtuma.key == pygame.K_UP:
                        ylos = True
                    if tapahtuma.key == pygame.K_ESCAPE or tapahtuma.key == pygame.K_e:
                        tapahtuma.type = pygame.QUIT
 
                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = False
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = False
                    if tapahtuma.key == pygame.K_UP:
                        ylos = False                  
 
                if tapahtuma.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            #LIIKUTETAAN ROBOA
            if oikealle: 
                if self.oliot[2][0] <= (self.leveys - self.kuvat[2].get_width() - self.reuna):
                    self.oliot[2][0] += 2
            if vasemmalle: 
                if self.oliot[2][0] >= self.reuna +2:
                    self.oliot[2][0] -= 2
            if alas: 
                if self.oliot[2][1] <= (self.korkeus - self.alareuna - self.kuvat[2].get_height()):
                    self.oliot[2][1] += 2
            if ylos: 
                if self.oliot[2][1] >= self.reuna +2:
                    self.oliot[2][1] -= 2

            self.liikuta_hirvio()
            self.osuma()
            self.paivita()
            self.kello.tick(60)


    def osuma(self):
        robo_keskiX = self.oliot[2][0] + (self.kuvat[2].get_width()/2)
        robo_keskiY = self.oliot[2][1] + (self.kuvat[2].get_height()/2)
        #TARKISTETAAN OSUIKO ROBO self.oliot[2]  KOLIKKOON self.oliot[3] ->
        for i in range(3, len(self.oliot)):
            kolikon_keskiX = self.oliot[i][0]+(self.kuvat[3].get_width()/2)
            kolikon_keskiY = self.oliot[i][1]+(self.kuvat[3].get_height()/2)
            if robo_keskiX+self.kuvat[3].get_width() >= kolikon_keskiX and robo_keskiX-self.kuvat[3].get_width() <= kolikon_keskiX:
                if robo_keskiY+self.kuvat[3].get_height() >=kolikon_keskiY and robo_keskiY-self.kuvat[3].get_height() <= kolikon_keskiY:
                    self.oliot.pop(i)
                    self.tilanne[1][1] += 1
                    break
        #TARKISTETAAN OSUIKO ROBO self.oliot[2]  HIRVIÖÖN self.oliot[1]
        hirvio_keskiX = self.oliot[1][0]+(self.kuvat[1].get_width()/2)
        hirvio_keskiY = self.oliot[1][1]+(self.kuvat[1].get_height()/2)
        if robo_keskiX+self.kuvat[1].get_width() >= hirvio_keskiX and robo_keskiX-self.kuvat[1].get_width() <= hirvio_keskiX:
            if robo_keskiY+self.kuvat[1].get_height() >=hirvio_keskiY and robo_keskiY-self.kuvat[1].get_height() <= hirvio_keskiY:
                self.tilanne[2][1] -= 1
                self.check_monsterXY()      
                return
        #TARKISTETAAN OSUIKO ROBO self.oliot[2]  OVEEN self.oliot[0] -> OVESTA VOI KÄYDÄ VAIN, JOS KAIKKI KOLIKOT ON KERÄTTY
        if len(self.oliot) <= 3:
            ovi_keskiX = self.oliot[0][0]+(self.kuvat[0].get_width()/2)
            ovi_keskiY = self.oliot[0][1]+(self.kuvat[0].get_height()/2)
            if robo_keskiX+self.kuvat[0].get_width() >= ovi_keskiX and robo_keskiX-self.kuvat[0].get_width() <= ovi_keskiX:
                if robo_keskiY+self.kuvat[0].get_height() >=ovi_keskiY and robo_keskiY-self.kuvat[0].get_height() <= ovi_keskiY:
                    self.tilanne[0][1] += 1
                    self.uusi_kentta()
                    return


    def paivita(self):
        self.naytto.fill((0, 0, 255))
        pygame.draw.rect(self.naytto, (100, 100, 100), (self.reuna, self.reuna, (self.leveys-(self.reuna*2)), (self.korkeus - self.reuna - self.alareuna))) 
        if self.tilanne[0][1] == 1:
            self.naytto.blit(self.ohjeRivi, (self.reuna, 1))
        #PÄIVITETÄÄN TILANNETAULU
        x, y = self.reuna, (self.korkeus-self.alareuna+(self.reuna/2))
        for i in range(len(self.tilanne)):
            teksti1, teksti2 = self.fontti.render(self.tilanne[i][0], True, (255,255,200)), self.fontti.render(str(self.tilanne[i][1]), True, (255,255,200))
            self.naytto.blit(teksti1, (x, y))
            self.naytto.blit(teksti2, (x + teksti1.get_width()+ 5, y))
            x += teksti1.get_width() + teksti2.get_width() +40
        #PÄIVITETÄÄN OLIOT KENTÄLLE
        for i in range(len(self.kuvat) -1):
            self.naytto.blit(self.kuvat[i], (self.oliot[i][0], self.oliot[i][1]))
        if len(self.kuvat) <= len(self.oliot):
            for i in range(len(self.kuvat) -1, len(self.oliot)):
                self.naytto.blit(self.kuvat[3], (self.oliot[i][0], self.oliot[i][1]))
        pygame.display.flip()


    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["ovi", "hirvio", "robo", "kolikko"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))


    def uusi_kentta(self):
        self.oliot = []
        #LUODAAN OVEN, HIRVIÖN JA ROBON ALOITUSKOORDINAATIT
        for olio in range(len(self.kuvat)-1):
            x, y = random.randint(self.reuna, (self.leveys-self.kuvat[olio].get_width() - self.reuna)), random.randint(self.reuna, (self.korkeus-self.kuvat[olio].get_height() - self.alareuna))
            self.oliot.append([x, y])
        self.check_monsterXY()
        #LUODAAN KOLIKOITA 2 + KENTÄN NUMERO
        for i in range(self.tilanne[0][1] + 2):
            kX, kY = random.randint(self.reuna, (self.leveys-self.kuvat[3].get_width() - self.reuna)), random.randint(self.reuna, (self.korkeus - self.kuvat[3].get_height() - self.alareuna))
            self.oliot.append([kX, kY])
            i += 1

    def check_monsterXY(self):
        x, y = self.oliot[1][0], self.oliot[1][1]
        #HIRVIÖ EI SAA ILMESTYÄ ROBON SEKTORILLE
        if self.oliot[2][0] <= self.leveys/2:
            if self.oliot[2][1] <= self.korkeus/2:
                x, y = random.randint(self.leveys/2, (self.leveys - self.kuvat[1].get_width() - self.reuna)), random.randint(self.korkeus/2, (self.korkeus - self.kuvat[1].get_height() - self.alareuna))
            if self.oliot[2][1] > self.korkeus/2:                        
                x, y = random.randint(self.leveys/2, (self.leveys - self.kuvat[1].get_width() - self.reuna)), random.randint(self.reuna, (self.korkeus/2 - self.kuvat[1].get_height()))
        if self.oliot[2][0] > self.leveys/2:
            if self.oliot[2][1] <= self.korkeus/2:
                x, y = random.randint(self.reuna, (self.leveys/2 - self.kuvat[1].get_width())), random.randint(self.korkeus/2, (self.korkeus - self.kuvat[1].get_height() - self.alareuna))
            if self.oliot[2][1] > self.korkeus/2:                        
                x, y = random.randint(self.reuna, (self.leveys/2 - self.kuvat[1].get_width())), random.randint(self.reuna, (self.korkeus/2 - self.kuvat[1].get_height()))
        self.oliot[1][0] = x
        self.oliot[1][1] = y        

    def liikuta_hirvio(self):
        #HIRVIÖ LIIKKUU EPÄTASAISIN LIIKKEIN JA PELIN EDETESSÄ SE LISÄÄ VAUHTIA
        nopeus = self.tilanne[0][1]
        if nopeus > random.randint(0, 20):
            robo_keskiX = self.oliot[2][0] + (self.kuvat[2].get_width()/2)
            robo_keskiY = self.oliot[2][1] + (self.kuvat[2].get_height()/2)
            hirvio_keskiX = self.oliot[1][0] + (self.kuvat[1].get_width()/2)
            hirvio_keskiY = self.oliot[1][1] + (self.kuvat[1].get_height()/2)
            if robo_keskiX < hirvio_keskiX:
                self.oliot[1][0] -= 1 +(nopeus/2)
            if robo_keskiX > hirvio_keskiX:
                self.oliot[1][0] += 1 + (nopeus/2)
            if robo_keskiY < hirvio_keskiY: 
                self.oliot[1][1] -= 1 + (nopeus/3)
            if robo_keskiY > hirvio_keskiY: 
                self.oliot[1][1] += 1 + (nopeus/3)


    def lopetus(self):
        self.lopetusFontti = pygame.font.SysFont("Arial", 40)
        self.naytto.fill((0,0,255))
        #PÄIVITETÄÄN TILANNETAULU
        y = 36
        for i in range(len(self.tilanne) -2):
            teksti1, teksti2 = self.lopetusFontti.render(self.tilanne[i][0], True, (255,255,255)), self.lopetusFontti.render(str(self.tilanne[i][1]), True, (255,255,255))
            x = self.leveys/2 - ((teksti1.get_width()+teksti2.get_width()+10)/2)
            self.naytto.blit(teksti1, (x, y))
            self.naytto.blit(teksti2, (x + teksti1.get_width()+10, y))
            y += 50
        self.lopetusFontti2 = pygame.font.SysFont("Arial", 80)
        teksti = self.lopetusFontti2.render("GAME OVER", True, (255,255,0))
        self.naytto.blit(teksti, ((self.leveys/2 - teksti.get_width()/2), y+30))
        kysymys = self.lopetusFontti.render("Jatketaanko?  k / e", True, (255,255,255))
        self.naytto.blit(kysymys, ((self.leveys/2 - kysymys.get_width()/2), y+160))        
        pygame.display.flip()
        
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_k:
                        self.uusi_peli()                    
                    if tapahtuma.key == pygame.K_e or tapahtuma.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    Bugaboo()
