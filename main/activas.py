import random
import threading
import pygame
import time
import math
LstNucleos= []
class Nucleo:
    def __init__(self, nombre, habilidad, regEner, regCalor,costo):
        self.nombre = nombre
        self.habilidad = habilidad
        self.regEner = regEner
        self.regCalor = regCalor
        self.costo= costo
        self.regCalor_base= regCalor
        self.regEner_base=regEner
        self.costo_base=costo
        self.activo= False
    def activar(self,jugador):
        pass
    def persistir(self,jugador):
        pass
class Iman(Nucleo):
    def activar(self, jugador):
        jugador.base.calor_actual -= 20
        if jugador.base.calor_actual < 0:
            jugador.base.calor_actual = 0
        self.activo = True
        self.timer = threading.Timer(3, self.desactivar, args=[jugador])
        self.timer.start()

    def desactivar(self, jugador):
        self.activo = False

    def persistir(self, jugador):
        from main import exp_sprites
        if self.activo:
            for exp in exp_sprites:
                desplazamiento_x = (jugador.base.rect.x - exp.rect.x) // 15
                desplazamiento_y = (jugador.base.rect.y - exp.rect.y) // 15

                exp.rect.x += desplazamiento_x
                exp.rect.y += desplazamiento_y

NucleoImantado= Iman("Nucleo Imantado", "Iman", 1, 1.5, 30)
LstNucleos.append(NucleoImantado)

class Ardiente(Nucleo):
    def activar(self,jugador):
        jugador.arma_primaria.velocidad *= 4
        jugador.arma_secundaria.velocidad *=4
        jugador.arma_primaria.calentamiento *=2
        jugador.arma_secundaria.calentamiento *=2
        self.timer = threading.Timer(5, self.desactivar, args=[jugador])
        self.timer.start()

    def desactivar(self,jugador):
        jugador.arma_primaria.velocidad /= 4
        jugador.arma_secundaria.velocidad /=4
        jugador.arma_primaria.calentamiento /=2
        jugador.arma_secundaria.calentamiento /=2

NucleoArdiente = Ardiente("Nucleo Ardiente","Calentamiento Forzado",1, 3, 50)
LstNucleos.append(NucleoArdiente)


class Tormenta(Nucleo):
    def __init__(self, nombre, habilidad, regEner, regCalor, costo):
        super().__init__(nombre, habilidad, regEner, regCalor, costo)
        self.cantRayos=0
        self.activo=False
        self.sprite =0
        self.a = 0
    def activar(self, jugador):
        self.activo = True
        self.cantRayos=0
        self.sprite = pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha()
        self.timer = threading.Timer(4, self.desactivar, args=[jugador])
        self.timer.start()
    def persistir(self,jugador):
        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 500
        if tiempo_segundos > self.a and self.activo==True:
            self.lanzar_rayo(jugador)
            self.a=tiempo_segundos
    def desactivar(self,jugador):
        self.activo=False
    def lanzar_rayo(self, jugador):
        from main import enemigos_sprites, Bala, balas_sprites, pygame
        lista_enemigos = list(enemigos_sprites)
        distancia = 651
        intentos = 0
        # Si la lista de enemigos está vacía, imprime un mensaje y sal de la función
        if not lista_enemigos:
            print("No hay enemigos disponibles para lanzar el rayo")
            return

        while distancia > 650:
            objetivo = random.choice(lista_enemigos)
            distancia_x = abs(jugador.base.rect.x - objetivo.rect.x)
            distancia_y = abs(jugador.base.rect.y - objetivo.rect.y)
            distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)
            intentos +=1
            if intentos >= 3:
                return


        # Si el enemigo está lo suficientemente cerca, lanzar el rayo
        direccion = (0, 1)
        sprite = pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha()
        nueva_bala = Bala(15, 40,
                          sprite,
                          objetivo.rect.x, objetivo.rect.y - 120, direccion, 1)
        balas_sprites.add(nueva_bala)
        print("Rayo lanzado hacia el enemigo")
        print("Cantidad de balas:", len(balas_sprites))

NucleoTormentoso=Tormenta("Nucleo Tormentoso","Tormenta Electrica", 2, 1, 40)
LstNucleos.append(NucleoTormentoso)