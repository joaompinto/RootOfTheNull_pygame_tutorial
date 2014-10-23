#!/usr/bin/python

import pygame

if __name__ == "__main__":
    pygame.init()

    size = window_width, window_height = 1200, 1000
    window = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    black= pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)

    window.fill(white)
    pygame.display.update()

    to_draw = []
    draw_start_box = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = mouse_pos
                draw_start_box = True
            if event.type == pygame.MOUSEBUTTONUP:
                final_pos = mouse_pos
                draw_start_box = False
                rect = pygame.Rect(pos, (final_pos[0] - pos[0], final_pos[1] - pos[1]))
                rect.normalize()
                to_draw += [rect]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for platform in to_draw:
                        print "[" + str(platform).split("(")[1].split(")")[0] + ", black],"
                if event.key == pygame.K_BACKSPACE:
                    to_draw.pop()

        window.fill(white)
        if draw_start_box:
            pygame.draw.rect(window, red, pygame.Rect(pos, (mouse_pos[0] - pos[0], mouse_pos[1] - pos[1])))

        for item in to_draw:
            pygame.draw.rect(window, black, item)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


