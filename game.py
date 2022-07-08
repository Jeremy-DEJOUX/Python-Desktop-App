import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):
        self.map = "world"

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
            if list(obj.properties)[0] == 'Type' and

        #definir le rectangle de collision pour rentrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

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

    def switch_house(self):
        # charger la carte au format TMX
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir une liste qui stocke les rectangles de collison
        self.walls = []

        for obj in tmx_data.objects:
            print(obj.properties)
            if obj.properties == 'Type':
                if obj.properties['Type'] == "collision":
                    self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # definir le rectangle de collision pour rentrer dans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recuperer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        # charger la carte au format TMX
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir une liste qui stocke les rectangles de collison
        self.walls = []
        for obj in tmx_data.objects:
            if obj.properties == 'Type' and obj.properties['Type'] == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # definir le rectangle de collision pour rentrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #recuperer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20


    def update(self):
        self.group.update()

        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'world'

        #verifier l'entrer dans la maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()

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
