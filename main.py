import sys
import pygame
from pygame import *

pygame.init()

fensterX = 600
fensterY = 400
fenster = pygame.display.set_mode((fensterX, fensterY))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

appRun = True

fps = 59

weiß = (255,255,255)
schwarz = (0,0,0)
rot = (255,0,0)

spielerX = 250
spielerY = 360
spielerBreite = 32
spielerHoehe = 32

gegnerX = 20
gegnerY = 20

spielerLinks = False
spielerRechts = False

schuesse = []

counter = 0
counterGegner = 0

reihen = 3
level = 0
bewRichtung = 2
gegnerSchiffe = []


class schuss():

    def __init__(self, posx = spielerX, posy = spielerY, x = 2, y = 5, getroffen = False):
        self.posx = posx + int(spielerBreite/2)
        self.posy = posy
        self.x = x
        self.y = y
        self.getroffen = getroffen

class GeneriereGegner():

    def __init__(self, posx = gegnerX, posy = gegnerY,z = bewRichtung, x = 32, y = 32, getroffen = False ):
        self.posx = posx
        self.posy = posy
        self.x = x
        self.y = y
        self.bewRichtung = z
        self.getroffen = getroffen

def schussBew():
    global schuesse
    schuesseEntfernen = []
    for i in range(len(schuesse)):
        j = schuesse[i]
        if j.getroffen == True:
            schuesseEntfernen.append(i)
        pygame.draw.rect(fenster,rot,(j.posx, j.posy, j.x, j.y))
        j.posy -= 5
        if j.posy <= 0:
            schuesseEntfernen.append(i)
    for i in range(len(schuesseEntfernen),0,-1):
        schuesse.pop(i-1)


def spielerZeichnen():
    pygame.draw.rect(fenster,rot,(spielerX, spielerY, spielerBreite, spielerHoehe))

def gegnerZeichnen():
    for i in gegnerSchiffe:
        for j in i:
            if j.getroffen == False:
                pygame.draw.rect(fenster, rot,(j.posx, j.posy,j.x,j.y))

def spielerBew():
    global spielerX

    if spielerLinks:
        spielerX -= 3
    if spielerRechts:
        spielerX += 3

def gegnerBew():
    for i in gegnerSchiffe:
        for j in i:
            j.posx += j.bewRichtung

def bewRichtungAendern():
    bewändern = False
    for i in gegnerSchiffe:
        anzahl = len(i)
        if anzahl > 0 and (i[0].posx < 20 or i[anzahl-1].posx > 545):
            bewändern = True
    if bewändern == True:
        for i in gegnerSchiffe:
            for j in i:
                j.bewRichtung *= -1
                j.posy += 20
                if j.bewRichtung < 0:
                    j.posx -= 1
                else:
                    j.posx += 1


def trefferAuswerten():
    schiffeEntfernen = []
    for i in schuesse:
        """
        for j in gegnerSchiffe:
            for k in j:
                  if i.posx <= k.posx+32 and i.posy <= k.posy + 32 and i.posx >= k.posx and i.posy >= k.posy and k.getroffen == False:
                    k.getroffen = True
                    i.getroffen = True
                    #schiffeEntfernen.append()
                    print(schiffeEntfernen)"""
        for j in range(len(gegnerSchiffe)):
            schiffe = gegnerSchiffe[j-1]
            for k in range(len(schiffe)):
                schiff = schiffe[k-1]
                if i.posx <= schiff.posx + 32 and i.posy <= schiff.posy + 32 and i.posx >= schiff.posx and i.posy >= schiff.posy and schiff.getroffen == False:
                    schiff.getroffen = True
                    i.getroffen = True
                    schiffe.remove(schiff)
            if len(schiffe) == 0:
                gegnerSchiffe.pop(j-1)

while appRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                spielerLinks = True
            if event.key == K_RIGHT:
                spielerRechts = True
            if event.key == K_SPACE:
                if len(schuesse) < 3:
                    schuss1 = schuss(spielerX,spielerY)
                    schuesse.append(schuss1)
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                spielerLinks = False
            if event.key == K_RIGHT:
                spielerRechts = False

    if len(gegnerSchiffe) == 0:
        gegnerY = 20
        gegnerX = 20
        level += 1
        bewRichtung = level
        richtung = bewRichtung
        for i in range(reihen):
            schiffe = []
            if i % 2 == 1:
                gegnerX = 55
            if i % 2 == 0:
                gegnerX = 20
            for j in range(8):
                gegner = GeneriereGegner(gegnerX,gegnerY,richtung)
                schiffe.append(gegner)
                gegnerX += 70
            gegnerSchiffe.append(schiffe)
            richtung *= -1
            gegnerY += 60

    fenster.fill(schwarz)
    spielerBew()
    spielerZeichnen()
    trefferAuswerten()

    bewRichtungAendern()

    if counter == 3:
        gegnerBew()
        counter = 0
    else:
        counter += 1
    gegnerZeichnen()
    schussBew()
    pygame.display.flip()
    clock.tick(fps)
    print(len(gegnerSchiffe))

pygame.quit()
sys.exit()