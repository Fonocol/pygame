from math import cos, sin, pi
import random
import time
import pygame
from modbus import Modbus

def drawpolygoneRegulier(surface,couleur,nombrepoints,origine,r=1,phi=0):
    points = []

    for i in range(nombrepoints):
        x= r*cos(2*i*pi/nombrepoints + phi) + origine[0]
        y= r*sin(2*i*pi/nombrepoints + phi) + origine[1]
        point =(x,y)
        points.append(point)

    pygame.draw.polygon(surface,couleur,points)
    
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
def drawRegul(surface,couleur,x,y,niv):
    points = [(x,y+100),(x+100,y+100)]

    p1 = (x,y+100+niv)
    p2 = (x+100,y+100+niv)
    points.append(p2)
    points.append(p1)
    

    pygame.draw.polygon(surface,couleur,points)
    
def drawBac(surface,couleur,x,y,niv):
    pygame.draw.line(surface, RED, (x, y+niv+100), (x+100, y+niv+100), 3)

    #niv
    drawRegul(surface,GREEN,x,y,niv)
    
    pygame.draw.line(surface, couleur, (x, y), (x, y+100), 3)
    pygame.draw.line(surface, couleur, (x, y+100), (x+50, y+120), 3)
    pygame.draw.line(surface, couleur, (x+50, y+120), (x+100, y+100), 3)
    pygame.draw.line(surface, couleur, (x+100, y+100), (x+100, y), 3)
    
def drawCircle(surface,couleur,x=0,y=0):
    pygame.draw.ellipse(surface, couleur, (x, y, 20, 20), 2)
    pygame.draw.ellipse(surface, couleur, (x+100, y, 20, 20), 2)
    pygame.draw.line(surface, couleur, (x+10, y), (x+110, y), 3)
    pygame.draw.line(surface, couleur, (x+10, y+19), (x+110, y+19), 3)

    
    



def main():
    pygame.init()
    modbus = Modbus()
    ecran = pygame.display.set_mode((800, 480))
    ecranRect = ecran.get_rect()

    # font = pygame.font.SysFont()
    fontName = pygame.font.get_default_font()
    font = pygame.font.Font(fontName, 32)
    monTexte = ""
    couleur = "0x000000"

    vitesse = pygame.Rect((10, 10), (0, 0))
    position = pygame.Rect((0, 0), (0, 0))
    phi = 0
    vitesseRotation = pi/128



    continuer = True
    ison = False
    color = ['0xFF0000',"0x00FF00"]
    cal = color[ison]
    niv =0.0
    
    ampoule = [pygame.image.load('off.png'),pygame.image.load('on.png')]
    rot = pygame.image.load('rot.png')
    engrenage = pygame.transform.scale_by(rot,0.4)
    
    ampoule[0] = pygame.transform.scale_by(ampoule[0],0.2)
    ampoule[1]=pygame.transform.scale_by(ampoule[1],0.2)
    SUP_CONV3 = modbus.lireBit(303)

    

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            elif event.type == pygame.KEYDOWN:
                if event.key < 256 and event.key >= 0:
                    # monTexte = "La touche '" + chr(event.key).upper() + "' a ete appuyer"
                    monTexte = chr(event.key).upper()
                    print(monTexte)
                if event.key == pygame.K_q:
                    print("A bientot")
                    continuer = False
                elif event.key == pygame.K_r:
                    couleur = "0xFF0000"
                elif event.key == pygame.K_g:
                    couleur = "0x00FF00"
                elif event.key == pygame.K_b:
                    couleur = "0x0000FF"
        
        ecran.fill("0xE4E4E4")
        
        surface = font.render(monTexte, True, couleur)
        surfaceRect = surface.get_rect()
        # surfaceRect.x = ecranRect.w/2 - surfaceRect.w/2 + vitesse.x
        # surfaceRect.y = ecranRect.h/2 - surfaceRect.h/2 + vitesse.y
        
        position.y = position.y + vitesse.y
        position.x = position.x + vitesse.x
        # surfaceRect.y = position.y
        
        niv = modbus.lireRegistre(30)# niv + vitesse.y
        print(niv)
        
        SUP_CONV1 = modbus.lireBit(303)
        SUP_CONV2 = modbus.lireBit(304)
        SUP_CONV3 = modbus.lireBit(305)
        

        surfaceRect.x = position.x
        surfaceRect.y = position.y
        time.sleep(0.1)
        # surfaceRect = pygame.Rect((100, 200), (32, len(monTexte)*32))

        # ecran.blit(, pygame.Rect(100, 200))

        #figure
        phi = phi + vitesseRotation*100
        phi = phi%(2*pi)

        ecran.blit(surface, surfaceRect)
        ampouleRect = ampoule[0].get_rect()
        ampouleRect.x = 300
        ampouleRect.y = 300
        
        if SUP_CONV3==1:
            SUP_CONV3=0
        else:
            SUP_CONV3=1
            
        ecran.blit(ampoule[SUP_CONV3],ampouleRect)
        
        drawBac(ecran,BLACK,100,100,-100)
        drawBac(ecran,BLACK,500,100,-100)
        drawBac(ecran,BLACK,300,300,-niv/100)
        
        rot = pygame.transform.rotate(engrenage,phi)
        
        #ecran.blit(rot,(10,10))
        #drawpolygoneRegulier(ecran,cal,50,(10,10),10,phi)
        drawCircle(ecran,BLACK,100,250)
        drawCircle(ecran,BLACK,500,250)
        drawCircle(ecran,BLACK,300,450)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()