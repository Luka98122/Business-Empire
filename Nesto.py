import pygame


class player:
    def __init__(self, x, y, w, h, speed) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, window):
        pygame.draw.rect(
            window, pygame.Color("Blue"), pygame.Rect(self.x, self.y, self.w, self.h)
        )


window = pygame.display.set_mode((800, 800))
igrac = player(5, 5, 100, 100, 15)
clock = pygame.time.Clock()

while True == True:
    dx = 0
    dy = 0
    window.fill("Red")
    igrac.draw(window)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_s]:
        dy = 1
    if keys[pygame.K_a]:
        dx = -1

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    igrac.move(dx, dy)
    pygame.display.flip()
    clock.tick(60)
