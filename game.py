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
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir une liste qui stocke les rectangles de collison
        self.walls = []
        for obj in tmx_data.objects:
            if obj.properties['Type'] == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

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
        self.group.update()

        # verification de la collison
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # Boucle de jeux permettant de maintenir la fenetre ouverte
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()  # Permet de actualiser à chaque tour de boucle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si on appuie sur la croix pour quitter la page
                    running = False

            clock.tick(60)

        pygame.quit()
