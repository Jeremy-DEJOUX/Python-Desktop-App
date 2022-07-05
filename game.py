import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):
        # creer la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 600))  # definit la taille de la fenetre en px
        pygame.display.set_caption("Labyrinthe")  # definit le titre de la fenetre

        # charger la carte au format TMX
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # generer un jouer
        self.player = Player(30, 40)

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)

    def run(self):
        # Boucle de jeux permettant de maintenir la fenetre ouverte
        running = True

        while running:
            self.group.update()
            self.group.draw(self.screen)
            pygame.display.flip()  # Permet de actualiser à chaque tour de boucle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si on appuie sur la croix pour quitter la page
                    running = False

        pygame.quit()
