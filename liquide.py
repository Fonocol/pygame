import pygame
import time
from math import pi, cos, sin
import random
from modbus import Modbus

import sys

# Initialisation de Pygame et de l'écran
pygame.init()
modbus = Modbus()
ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulation de Réservoir de Liquide")
clock = pygame.time.Clock()

# Couleurs
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0, 255)
LIQUIDE = (random.randint(1, 254),random.randint(1, 254), 255)
GREY = (169, 169, 169)
AMPOULE = [pygame.image.load('./Assetes/Aon.png'),pygame.image.load('./Assetes/Aoff.png')]


# Génération initiale des bulles
def generate_bubbles(num_bubbles):
    return [(random.randint(10, 90), random.randint(10, 90), random.randint(2, 5)) for _ in range(num_bubbles)]

# Génération initiale des water

# Initialisation des bulles
bubbles = generate_bubbles(15)

# Animation des bulles
def animate_bubbles(bubbles, height):
    for i in range(len(bubbles)):
        bubbles[i] = (bubbles[i][0], (bubbles[i][1] - 0.5) % 100, bubbles[i][2])


# Fonction pour dessiner un indicateur de niveau de liquide
def draw_level_indicator(surface, x, y, fill_level):
    font = pygame.font.Font(None, 36)
    level_text = font.render(f"{fill_level:.1f}%", True, BLACK)
    surface.blit(level_text, (x, y))

# Fonction pour dessiner le réservoir
def draw_tank(surface, x, y, width, height, fill_level):
    
    # Dessin du liquide
    liquid_height = fill_level / 100 * height
    pygame.draw.rect(surface, LIQUIDE, (x + 2, y + height - liquid_height, width, liquid_height),1)
    
    
    # Ajout d'un effet de dégradé pour le liquide
    for i in range(1, int(liquid_height), 2):
        alpha = 255 - int(255 * (i / liquid_height))
        s = pygame.Surface((width, 2), pygame.SRCALPHA)
        s.fill((LIQUIDE[0],LIQUIDE[1], 255, alpha))
        surface.blit(s, (x + 2, y + height - i))
        
    #tank
    pygame.draw.line(surface, BLACK, (x, y), (x, y+height), 3)
    pygame.draw.line(surface, BLACK, (x, y+height), (x+width, y+height), 3)
    pygame.draw.line(surface, BLACK, (x+width, y+height), (x+width, y), 3)
    
    # Dessiner et animer les bulles
    draw_bubbles(surface, x, y, width, height, fill_level, bubbles)
    animate_bubbles(bubbles, 10)
    
    #-------------------------------------------------------------------------------------------------
    
def draw_bateri(surface, x, y, width, height, fill_level):
    # Dessin du liquide
    col = LIQUIDE
    liquid_width = fill_level / 100 * width
    if liquid_width < width/2:
        col = RED
    else:
        col = LIQUIDE
    
    pygame.draw.rect(surface,col,(x, y , liquid_width, height))
    pygame.draw.rect(surface, BLACK, (x, y , width, height),2)
    
    draw_level_indicator(surface,x+width,y,fill_level)


def draw_indicator(surface,x,y,l1,l2,l3):
    draw_bateri(surface, x, y, 400, 20, l1)
    draw_bateri(surface, x, y+30, 400, 20, l2)
    draw_bateri(surface, x, y+60, 400, 20, l3)
    



# Fonction pour dessiner des cercles (bubbles) dans le liquide
def draw_bubbles(surface, x, y, width, height, fill_level, bubbles):
    liquid_height = fill_level / 100 * height
    for bubble in bubbles:
        bubble_y = y + height - bubble[1] * liquid_height / 100
        pygame.draw.circle(surface, BLUE, (x + bubble[0] * width / 100, int(bubble_y)), bubble[2])



def rotate_image(ecran,x,y,image, angle):
    rotated_image = pygame.transform.rotate(image,angle)
    rot_img_rect = rotated_image.get_rect(center=(x,y))
    ecran.blit(rotated_image,rot_img_rect)

def tapie(ecran,x,y,angle,img1,dir,stat,ampoule):
    ampouleRect = ampoule[stat].get_rect()
    ampouleRect.x = x-60
    ampouleRect.y = y-40
    if stat==0:
        ecran.blit(ampoule[stat],ampouleRect)
    else:
        angle=0
        ecran.blit(ampoule[stat],ampouleRect)
    
    rotate_image(ecran,x,y,img1,angle*dir)
    rotate_image(ecran,x+100,y,img1,angle*dir)

    ecart = (angle/360)*50
    pygame.draw.line(ecran, BLACK, (x+ecart*(dir), y-15), (x+ecart*(dir)+10, y-15), 3)
    pygame.draw.line(ecran, BLACK, (x+ecart*(dir)+50, y-15), (x+ecart*(dir)+10+50, y-15), 3)

    pygame.draw.line(ecran, BLACK, (x+ecart*(-dir)+90, y+15), (x+ecart*(-dir)+100, y+15), 3)
    pygame.draw.line(ecran, BLACK, (x+ecart*(-dir)+50, y+15), (x+ecart*(-dir)+10+50, y+15), 3)



def main():
   
    continuer = True

    # asset
    roue = pygame.image.load('Assetes/roue.png')
    angle = 0.0
    vetesse_roue = 3.0


    clock = pygame.time.Clock()

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    continuer = False
                elif event.key == pygame.K_UP:
                    print("K_UP")
                    #fill_level = min(100.0, fill_level + 1.0)
                elif event.key == pygame.K_DOWN:
                    print("K_DOWN")
                    #fill_level = max(0.0, fill_level - 1.0)

        ecran.fill((224, 224, 224))  # Couleur de fond
        fill_level = modbus.lireRegistre(30)# niv + vitesse.y
        print(fill_level)

        #conv
        SUP_CONV1 = modbus.lireBit(303)
        SUP_CONV2 = modbus.lireBit(304)
        SUP_CONV3 = modbus.lireBit(305)
        
        #menu
        draw_indicator(ecran,200,50,100,100,fill_level/100)

        # Dessiner le réservoir avec le niveau de liquide
        draw_tank(ecran, 200, 200, 100, 100, 100)
        draw_tank(ecran, 500, 200, 100, 100, 100)
        draw_tank(ecran, 350, 400, 100, 100, fill_level/100)


        angle += vetesse_roue
        if angle >=360:
            angle =0
        
        if SUP_CONV3==1:
            SUP_CONV3=0
        else:
            SUP_CONV3=1

        if SUP_CONV2==1:
            SUP_CONV2=0
        else:
            SUP_CONV2=1

        if SUP_CONV1==1:
            SUP_CONV1=0
        else:
            SUP_CONV1=1
        
        
        tapie(ecran,200,350,angle,roue,1,SUP_CONV1,AMPOULE)
        tapie(ecran,500,350,angle,roue,1,SUP_CONV2,AMPOULE)
        tapie(ecran,350,550,angle,roue,1,SUP_CONV3,AMPOULE)
        clock.tick(60)
       

        

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
