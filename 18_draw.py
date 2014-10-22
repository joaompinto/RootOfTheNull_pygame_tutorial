#!/usr/bin/python

import pygame

if __name__ == "__main__":
    pygame.init()

    size = window_width, window_height = 400, 200
    window = pygame.display.set_mode(size)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)

    window.fill(white)

    #rect = pygame.Rect((20, 50), (100, 120))
    points_list = [(20, 50), (3, 120), (150, 120)]
    #pygame.draw.rect(window, red, rect, 3)
    pygame.draw.polygon(window, red, points_list)

    pygame.display.update()

    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    pygame.quit()


