import pygame
import random
import tkinter as tk
from tkinter import messagebox

width = 500
rows = 20


class cube(object):
    w = 500
    r = 20

    def __init__(self, start, dir_x = 1, dir_y = 0, color=(179, 255, 153)):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface, eyes=False):
        dif = self.w // self.r
        i = self.pos[0]
        j = self.pos[1]

        # +1 y -2 para que se vean las lineas
        pygame.draw.rect(surface, self.color, (i * dif + 1, j * dif + 1, dif - 2, dif - 2))

        if eyes:
            center = dif // 2
            radius = 3
            circleMiddle = (i * dif + center - radius, j * dif + 8)
            circleMiddle2 = (i * dif + dif - radius * 2, j * dif + 8)
            pygame.draw.circle(surface, (77, 77, 77), circleMiddle, radius)
            pygame.draw.circle(surface, (77, 77, 77), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}  # marca en que punto tiene que moverse el cuerpo

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)  # agrega cubo a la cabeza
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()  # ajusta si apretas mas de uno o presiona

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]  # agrega la pos de la cabeza

                if keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                if keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                if keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        for i, c in enumerate(self.body):
            p = c.pos[:]

            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])

                if i == len(self.body) - 1:  # si estoy en el ultimo cubo borro de turn
                    self.turns.pop(p)

            else:  # deja mover de izq a der de la pantalla
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.r - 1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.r - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == 1 and c.pos[1] >= c.r - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.r - 1)
                else:  # sino esta yendo a los bordes, solo mover
                    c.move(c.dir_x, c.dir_y)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # ojos
            else:
                c.draw(surface)

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_x = 0
        self.dir_y = 1


def draw_grid(w, r, surface):
    gap = w // r
    x = 0
    y = 0

    for l in range(rows):
        x += gap
        y += gap

        pygame.draw.line(surface, (102, 102, 102), (x, 0), (x, w))
        pygame.draw.line(surface, (102, 102, 102), (0, y), (w, y))


def redraw_window(surface):
    surface.fill((77, 77, 77))
    draw_grid(width, rows, surface)
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()


def random_snack(snak):
    positions = snak.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # no ponerlo encima de la snake
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes = ('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global s, snack
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption('una pitón hecha en pitón')
    s = snake((179, 255, 153), (10, 10))
    snack = cube(random_snack(s), color=(255, 102, 102))
    clock = pygame.time.Clock()
    flag = True

    while flag:
        clock.tick(12) # a no mas de 10 fps
        s.move()

        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = cube(random_snack(s), color=(255, 102, 102))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('Perdiste', 'Jugar de nuevo')
                s.reset((10, 10))
                break

        redraw_window(win)

main()
