#!/usr/bin/python

# Code based on RootOfTheNull's Youtube tutorials for Python [pygame]

import pygame
from pygame.color import THECOLORS


class Block(pygame.sprite.Sprite):

    def __init__(self, color=THECOLORS['blue'], width=64, height=64):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.set_properties()
        self.sound = pygame.mixer.Sound("data/metal_gong.wav")
        self.hspeed = 0
        self.vspeed = 0

    def change_speed(self, hspeed, vspeed):
        self.hspeed += hspeed
        self.vspeed += vspeed

    def set_properties(self):
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.speed = 5

    def set_position(self, x, y):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def set_image(self, filename=None):
        self.image = pygame.image.load(filename)
        self.set_properties()

    def play_sound(self):
        self.sound.play()

    def update(self, collidable = pygame.sprite.Group(), event=None):
        self.rect.x += self.hspeed
        self.experience_gravity()

        # Check horizontal collisions
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if self.hspeed > 0:
                self.rect.right = collided_object.rect.left
            if self.hspeed < 0:
                self.rect.left = collided_object.rect.right

        self.rect.y += self.vspeed

        # Check vertical collisions
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if self.vspeed > 0:
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            if self.vspeed < 0:
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                        self.change_speed(-self.speed, 0)
                if event.key == pygame.K_RIGHT:
                    self.change_speed(self.speed, 0)
                if event.key == pygame.K_UP:
                    if len(collision_list) > 0:  # Only jump when hitting in the ground
                        self.change_speed(0, -self.speed*2)
                if event.key == pygame.K_DOWN:
                    #self.change_speed(0, self.speed)
                    pass
            if event.type == pygame.KEYUP:  # Reset current speed
                if event.key == pygame.K_LEFT:
                    if self.hspeed != 0:
                        self.hspeed = 0
                if event.key == pygame.K_RIGHT:
                    if self.hspeed != 0:
                        self.hspeed = 0
                if event.key == pygame.K_UP:
                    #if self.vspeed != 0:
                    #    self.vspeed = 0
                    pass
                if event.key == pygame.K_DOWN:
                    #if self.vspeed != 0:
                    #    self.vspeed = 0
                    pass

    def experience_gravity(self, gravity=.35):
        if self.vspeed == 0:  # Colliding vertically
            self.vspeed = 1   # Keep gravity in effect
        else:
            self.vspeed += gravity


def set_message(text):
    global message, previous_message
    message = font.render(text, True, THECOLORS['black'],THECOLORS['white'])
    previous_message = message

if __name__ == "__main__":
    pygame.init()

    window_size = window_width, window_height = 640, 480
    window = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    pygame.display.set_caption("Game!")

    white = (255, 255, 255)


    clock = pygame.time.Clock()
    frames_per_second = 60

    block_group = pygame.sprite.Group()
    a_block = Block()
    a_block.set_image('data/brick.png')
    a_block.set_position(window_width/2-150, window_height/2-100)

    another_block = Block(THECOLORS['red'])
    another_block.set_position(window_width/2, window_height/2+80)

    more_block = Block(THECOLORS['blue'], 300, 20)
    more_block.set_position(window_width/2, window_height/2+200)
    block_group.add(more_block, another_block, a_block)
    #a_block.play_sound()

    font = pygame.font.SysFont("Times New Roman", 30)
    message = previous_message = None
    set_message("Use the arrow keys to move the block")
    collidable_objects = pygame.sprite.Group()
    collidable_objects.add(more_block, another_block)
    running = True

    while running:
        event = pygame.event.poll()  # We handle one event per frame
        if event.type == pygame.MOUSEMOTION:  # Ignore mouse events
            continue

        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        clock.tick(frames_per_second)
        window.fill(white)
        a_block.update(collidable_objects, event)
        event = None
        if message != previous_message:
            set_message(message)
        window.blit(message, (window_width/2 - message.get_rect().width/2,
                           0))
        block_group.draw(window)
        pygame.display.update()

pygame.quit()