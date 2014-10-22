#!/usr/bin/python

# Code based on RootOfTheNull's Youtube tutorials for Python [pygame]

import pygame
from pygame.color import THECOLORS


class Player(pygame.sprite.Sprite):

    def __init__(self, color=THECOLORS['blue'], width=32, height=48):
        super(Player, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.set_properties()
        self.hspeed = 0
        self.vspeed = 0
        self.level = None

    def set_properties(self):
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.speed = 5

    def set_position(self, x, y):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def set_level(self, level):
        self.level = level
        self.set_position(level.player_start_x, level.player_start_y)

    def set_image(self, filename=None):
        self.image = pygame.image.load(filename).convert()
        self.set_properties()

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
                    self.hspeed = -self.speed
                if event.key == pygame.K_RIGHT:
                    self.hspeed = self.speed
                if event.key == pygame.K_UP:
                    if len(collision_list) > 0:  # Only jump when hitting in the ground
                        self.vspeed = -self.speed*2

            if event.type == pygame.KEYUP:  # Reset current speed
                if event.key == pygame.K_LEFT:
                    if self.hspeed < 0:
                        self.hspeed = 0
                if event.key == pygame.K_RIGHT:
                    if self.hspeed > 0:
                        self.hspeed = 0

    def experience_gravity(self, gravity=.35):
        if self.vspeed == 0:  # Keep applying gravity
            self.vspeed = 1
        else:
            self.vspeed += gravity


class Block(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color=THECOLORS['blue']):
        super(Block, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level(object):

    def __init__(self, player_object):
        self.object_list = pygame.sprite.Group()
        self.player_object = player_object
        self.player_start = self.player_start_x, self.player_start_y = 0, 0
        self.world_shift_x = self.world_shift_y = 0
        self.left_viewbox = window_width/2 - window_width/8
        self.right_viewbox = window_width/2 + window_width/10
        self.up_viewbox = window_height/5
        self.down_viewbox = window_height/2 +window_height/12


    def update(self):
        self.object_list.update()

    def draw(self, window):
        window.fill(THECOLORS['white'])
        self.object_list.draw(window)

    def shift_world(self, shift_x, shift_y):
        self.world_shift_x += shift_x
        self.world_shift_y += shift_y

        # Shift objects "in-screen" position
        for each_object in self.object_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y

    def run_viewbox(self):

        if self.player_object.rect.x <= self.left_viewbox:
            view_difference = self.left_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.left_viewbox  # Stop the player movement
            self.shift_world(view_difference, 0)

        if self.player_object.rect.x >= self.right_viewbox:
            view_difference = self.right_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.right_viewbox  # Stop the player movement
            self.shift_world(view_difference, 0)

        if self.player_object.rect.y <= self.up_viewbox:
            view_difference = self.up_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.up_viewbox  # Stop the player movement
            self.shift_world(0, view_difference)

        if self.player_object.rect.y >= self.down_viewbox:
            view_difference = self.down_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.down_viewbox  # Stop the player movement
            self.shift_world(0, view_difference)


class Level_01(Level):


    def __init__(self, player_object):
        super(Level_01, self).__init__(player_object)

        self.player_start = self.player_start_x, self.player_start_y = 100, 0

        level = [
            # [x, y, width, height, color ]
            [2, 124, 365, 47, THECOLORS['black']]
            , [200, 424, 280, 47, THECOLORS['black']]
        ]

        for block in level:
            print block
            new_block = Block(*block)
            self.object_list.add(new_block)


def set_message(text):
    global message, previous_message
    message = font.render(text, True, THECOLORS['black'],THECOLORS['white'])
    previous_message = message

if __name__ == "__main__":
    pygame.init()

    window_size = window_width, window_height = 640, 480
    window = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    pygame.display.set_caption("Platform!")

    white = (255, 255, 255)


    clock = pygame.time.Clock()
    frames_per_second = 60

    active_object_list = pygame.sprite.Group()
    player = Player()
    active_object_list.add(player)

    level_list = []
    level_list.append(Level_01(player))
    current_level_number = 0
    current_level = level_list[current_level_number]
    player.set_level(current_level)


    font = pygame.font.SysFont("Times New Roman", 30)
    message = previous_message = None
    set_message("Use the arrow keys to move the block")
    running = True

    while running:
        event = pygame.event.poll()  # We handle one event per frame
        if event.type == pygame.MOUSEMOTION:  # Ignore mouse events
            continue

        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Update functions
        player.update(current_level.object_list, event)
        event = None

        current_level.update()

        # Logic Testing
        current_level.run_viewbox()

        # Draw everything
        current_level.draw(window)
        active_object_list.draw(window)

        # Delay Framerate
        clock.tick(frames_per_second)

        # Update the screen
        pygame.display.update()

    pygame.quit()