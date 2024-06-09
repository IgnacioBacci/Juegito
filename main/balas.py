import pygame
from main import pantalla_alto,pantalla_ancho
class Bala(pygame.sprite.Sprite):
    def __init__(self, daño, velocidadProyectil, sprite, origen_x, origen_y, direccion, perforacion, prob_critica=0):
        super().__init__()
        self.daño = daño
        self.velocidadProyectil = velocidadProyectil
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = origen_x
        self.rect.y = origen_y
        self.direccion = direccion
        self.perforacion = perforacion
        self.prob_critica = prob_critica
        self.critico=False

    def update(self):
        self.rect.x += self.velocidadProyectil * self.direccion[0]
        self.rect.y += self.velocidadProyectil * self.direccion[1]

        if self.rect.y < - 100 or self.rect.y > pantalla_alto + 100 or self.rect.x < - 100 or self.rect.x > pantalla_ancho + 100 or self.perforacion == 0:
            self.kill()