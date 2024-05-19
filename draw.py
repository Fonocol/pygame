import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR = 800
HAUTEUR = 600
TAILLE_CELLULE = 10

# Couleurs
COULEUR_FOND = (30, 30, 30)
COULEUR_LIQUIDE = (0, 0, 255)

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Simulation de Liquide")

# Fonction pour dessiner le liquide
def dessiner_liquide(liquide):
    fenetre.fill(COULEUR_FOND)
    for cellule in liquide:
        pygame.draw.rect(fenetre, COULEUR_LIQUIDE, (cellule[0] * TAILLE_CELLULE, cellule[1] * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE))
    pygame.display.flip()

# Fonction pour mettre à jour la position du liquide
def mettre_a_jour_liquide(liquide):
    nouvelles_cellules = []
    for cellule in liquide:
        x, y = cellule
        if y < HAUTEUR // TAILLE_CELLULE - 1 and (x, y + 1) not in liquide:
            nouvelles_cellules.append((x, y + 1))
        else:
            nouvelles_cellules.append(cellule)
    return nouvelles_cellules

# Initialisation du liquide
liquide = [(LARGEUR // (2 * TAILLE_CELLULE), HAUTEUR // (2 * TAILLE_CELLULE))]

# Boucle principale
continuer = True
horloge = pygame.time.Clock()

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    liquide = mettre_a_jour_liquide(liquide)
    if len(liquide) < (LARGEUR // TAILLE_CELLULE) * (HAUTEUR // TAILLE_CELLULE):
        liquide.append((random.randint(0, LARGEUR // TAILLE_CELLULE - 1), 0))

    dessiner_liquide(liquide)
    horloge.tick(30)

pygame.quit()
