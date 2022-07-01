import pygame
pygame.init

#creer la fenetre du jeu
pygame.display.set_mode((800, 600)) #definit la taille de la fenetre en px
pygame.display.set_caption("Labyrinthe") #definit le titre de la fenetre

#Boucle de jeux permettant de maintenir la fenetre ouverte
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Si on appuie sur la croix pour quitter la page
            running = False
pygame.quit()
