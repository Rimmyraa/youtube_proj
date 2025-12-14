import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artificial life")

clock = pygame.time.Clock()


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 50, 50)


food = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]

class Creature:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.energy = 100
        self.speed = random.uniform(1, 2)

    def move(self):
        angle = random.uniform(0, math.pi * 2)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        self.x %= WIDTH
        self.y %= HEIGHT
        self.energy -= 0.1

    def eat(self):
        for f in food[:]:
            if math.dist((self.x, self.y), f) < 10:
                food.remove(f)
                self.energy += 30

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

creatures = [Creature() for _ in range(10)]

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Еда появляется
    if random.random() < 0.05:
        food.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    for c in creatures[:]:
        c.move()
        c.eat()
        if c.energy <= 0:
            creatures.remove(c)
        elif c.energy > 200:
            c.energy -= 100
            creatures.append(Creature())

        c.draw()

    for f in food:
        pygame.draw.circle(screen, GREEN, f, 3)

    pygame.display.flip()

pygame.quit()
