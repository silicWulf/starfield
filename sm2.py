import os
import glob
# import pygame
try:
    import pyjsdl as pygame
except:
    try:
        import pygame
    except ImportError:
        import pyjsdl as pygame
import random
import ctypes


u32 = ctypes.windll.user32

WIN_WIDTH  = u32.GetSystemMetrics(0)
WIN_HEIGHT = u32.GetSystemMetrics(1)
REALWIN_WIDTH  = WIN_WIDTH
REALWIN_HEIGHT = WIN_HEIGHT

dummy_PLANETSLIST = glob.glob('assets/planet*.png')
PLANETSLIST = []
for foobar in dummy_PLANETSLIST:
    PLANETSLIST.append(pygame.image.load(foobar))
dummy_ASTEROIDLIST = glob.glob('assets/asteroid*.png')
ASTEROIDLIST = []
for lol in dummy_ASTEROIDLIST:
    ASTEROIDLIST.append(pygame.image.load(lol))

STARSURF = pygame.image.load('assets/star.png')


class main:
    def __init__(self):
        global REALWIN_WIDTH
        global REALWIN_HEIGHT
        pygame.init()
        self.window = pygame.display.set_mode((REALWIN_WIDTH, REALWIN_HEIGHT))
        # self.window = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        # self.screen = pygame.display.set_mode((REALWIN_WIDTH, REALWIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.stars = []
        self.planets = []
        self.asteroids = []
        self.spaceship = glob.glob('assets/spaceship*.gif')
        sdum = []
        for xyzzy in self.spaceship:
            sdum.append(pygame.image.load(xyzzy))
        self.spaceship = sdum
        self.ss_sprite = self.spaceship[0]
        self.ss_currtick = 0
        self.ss_index = 0
        self.ss_maxticks = 4
        self.ss_size = self.ss_sprite.get_size()
        self.ss_pos_index = 0
        self.ss_pos_currtick = 0
        self.ss_pos_maxticks = 43
        self.spaceship_pos = [(int((WIN_WIDTH / 2) - (self.ss_size[0] / 2)), int((WIN_HEIGHT / 2) - (self.ss_size[1] / 2)))]
        temp1 = self.spaceship_pos[0][0]
        temp2 = self.spaceship_pos[0][1]
        self.spaceship_pos.append((temp1, temp2 - 1))
        self.spaceship_pos.append((temp1, temp2))
        self.spaceship_pos.append((temp1, temp2 + 1))

        for x in range(0, 100):
            newstar = Star('dasd',
                      random.randint(0, WIN_HEIGHT),
                      random.randint(1, 7))
            for x in range(0, random.randint(0, WIN_WIDTH * 5)):
                newstar.tick()
            self.stars.append(newstar)

        for x in range(0, random.randint(1, 3)):
            newast = Asteroid('lol',
                              random.randint(0, WIN_HEIGHT))
            for x in range(0, random.randint(0, WIN_WIDTH * 5)):
                newast.tick()
            self.asteroids.append(newast)

        newplan = Planet('kek', random.randint(0, WIN_HEIGHT))
        for x in range(0, random.randint(0, WIN_WIDTH * 5)):
            newplan.tick()
        self.planets.append(newplan)


        while True:
            self.clock.tick(60)

            self.window.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os._exit(0)
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    REALWIN_WIDTH, REALWIN_HEIGHT = event.size

            for planet in self.planets:
                planet.tick()
                planetpos = planet.x, planet.y
                self.window.blit(planet.surface, planetpos)

            for asteroid in self.asteroids:
                asteroid.tick()
                asteroidpos = asteroid.x, asteroid.y
                self.window.blit(asteroid.surface, asteroidpos)

            for star in self.stars:
                star.tick()
                starpos = star.x, star.y
                # print(starpos)
                self.window.blit(star.surface, starpos)

            self.ss_pos_currtick += 1
            self.ss_currtick += 1
            if self.ss_currtick == self.ss_maxticks:
                self.ss_currtick = 0
                self.ss_index += 1
                try:
                    self.ss_sprite = self.spaceship[self.ss_index]
                except IndexError:
                    self.ss_index = 0
            if self.ss_pos_currtick == self.ss_pos_maxticks:
                self.ss_pos_currtick = 0
                self.ss_pos_index += 1
                try:
                    self.spaceship_pos[self.ss_pos_index]
                except IndexError:
                    self.ss_pos_index = 0

            # print(self.spaceship_pos[self.ss_pos_index])

            self.window.blit(self.ss_sprite, self.spaceship_pos[self.ss_pos_index])

            # pygame.transform.scale(self.window, (REALWIN_WIDTH, REALWIN_HEIGHT), self.screen)

            pygame.display.update()


class Star:
    def __init__(self, name, y_location, layer, imgpath='assets/star.png', planet_backtick=0):
        if imgpath != 'assets/star.png':
            self.surface = pygame.image.load(imgpath)
        else:
            self.surface = STARSURF
        self.size = self.surface.get_size()

        self.layer = layer

        set_x = int(round(self.size[0] - layer))
        set_y = int(round(self.size[1] - layer))

        self.x = WIN_WIDTH
        self.y = y_location
        self.currx = WIN_WIDTH

        try:
            self.surface = pygame.transform.scale(self.surface, (set_x, set_y))
        except ValueError as e:
            if planet_backtick == 0:
                raise e

        self.index = -1
        self.plot = []
        self.currenttick = 0
        for foo in range(((WIN_WIDTH + set_x) * layer) + planet_backtick):
            self.pretick()
        # print(self.plot)


    def pretick(self):
        self.currenttick += 1
        if self.currenttick >= self.layer:
            self.currenttick = 0
            self.currx -= 1

        self.plot.append(self.currx)

    def tick(self):
        self.index += 1
        try:
            bar = self.plot[self.index]
        except IndexError:
            self.y = random.randint(0, WIN_HEIGHT)
            self.index = 0
            bar = self.plot[0]
        self.x = bar


class Asteroid(Star):
    def __init__(self, name, y_location):
        xx = random.randint(8, 12)
        super().__init__(name, y_location, xx, imgpath=random.choice(dummy_ASTEROIDLIST), planet_backtick=random.randint(100, 300))

        self.surface = pygame.transform.scale(pygame.transform.rotate(self.surface, random.randint(0, 361)), (int(111 / 2), int(90 / 2)))  # CHANGE THE IMAGE SIZE IF YOU EVER CHANGE THE ASTEROID PICTURE, THIS IS PROBABLY WHY IT'S NOT WORKING YOU KLUTZ


class Planet(Star):
    def __init__(self, name, y_location):
        super().__init__(name, y_location, random.randint(20, 28), planet_backtick=random.randint(200, 800))

        self.surface = random.choice(PLANETSLIST)


if __name__ == '__main__':
    main()
