import pygame
from player import Player
from map import MapManager


class Game:

    def __init__(self):

        # creer la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 600))  # definit la taille de la fenetre en px
        pygame.display.set_caption("Labyrinthe")  # definit le titre de la fenetre

        # generer un jouer
        self.player = Player("player", 0, 0)
        self.map_manager = MapManager(self.screen, self.player)


    def handle_input(self):
        pressed = pygame.key.get_pressed()  # recupère les touches pressé

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')


    def update(self):
        self.map_manager.update()


    def run(self):

        clock = pygame.time.Clock()

        # Boucle de jeux permettant de maintenir la fenetre ouverte
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()  # Permet de actualiser à chaque tour de boucle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si on appuie sur la croix pour quitter la page
                    running = False

            clock.tick(60)

        pygame.quit()
