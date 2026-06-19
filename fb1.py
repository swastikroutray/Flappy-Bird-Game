import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 608
screen_height = 500
flying = False
game_over = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# define game variables
ground_scroll = 0
scroll_speed = 4

# load images
bg = pygame.image.load('bg.png')
ground_img = pygame.image.load('gd.png')


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.index = 0
        self.counter = 0

        for num in range(1, 4):
            img = pygame.image.load(f'b{num}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        # gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            self.rect.y += int(self.vel)
            if self.rect.bottom >= 400:
                self.rect.bottom = 400

        if game_over == False:
            # animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            #rotate the bird

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)

    # draw background
    screen.blit(bg, (0, 0))

    # update and draw bird
    bird_group.update()
    bird_group.draw(screen)

    #check if bird has hit the ground
    if flappy.rect.bottom >= 400:
        game_over = True
        flying = False

    if game_over == False:
        ground_scroll -= scroll_speed

    if abs(ground_scroll) > 35:
        ground_scroll = 0

    # draw and scroll ground
    screen.blit(ground_img, (ground_scroll, 400))
    screen.blit(ground_img, (ground_scroll + 336, 400))


    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            flappy.vel = -10

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()