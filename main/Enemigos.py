import pygame
import math
import random
configuracion_enemigos=[]
class Animacion(pygame.sprite.Sprite):
    def __init__(self, posicion, frames, derecha, duracion_frame=100, desaparecer=False):
        super().__init__()
        if derecha:
            self.frames = [pygame.transform.flip(frame, True, False) for frame in frames]
        else:
            self.frames = frames
        self.frame_actual = 0
        self.image = self.frames[self.frame_actual]
        self.rect = self.image.get_rect(center=posicion)
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.duracion_frame = duracion_frame
        self.desaparecer = desaparecer
        self.total_frames = len(frames)
        self.alpha_values = [255 - int(255 * (i / (self.total_frames - 1))) for i in range(self.total_frames)]

    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_frame > self.duracion_frame:
            self.frame_actual += 1
            self.tiempo_ultimo_frame = ahora
            if self.frame_actual >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_actual]
                if self.desaparecer:
                    alpha = self.alpha_values[self.frame_actual]
                    self.image.set_alpha(alpha)

# Clase base Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, vida, velocidad, daño, sprite_path, objetivo, valor, boss=False, tipo="Enemigo", ):
        super().__init__()
        self.vida = vida
        self.velocidad = velocidad
        self.velocidad_base = velocidad
        self.daño = daño
        self.path=sprite_path
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.objetivo = objetivo
        self.valor = valor
        self.vida_maxima = vida
        self.mirando_derecha = False
        self.muriendo = False
        self.frame_actual = 0
        self.tiempo_ultimo_frame = 0
        self.duracion_frame = 100
        self.animacion_muerte_ice_slime = [
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death1.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death2.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death3.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death4.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death5.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death6.png")
        ]
        self.boss = boss
        self.barra = boss
        self.tipo = tipo
        self.angulo_actual=None
        self.actualizado=False
        self.colision=True

    def rotar1(self):
        if self.mirando_derecha:
            self.image = pygame.transform.flip(self.image, True, False)
            self.mirando_derecha = not self.mirando_derecha

    def rotar2(self):
        if not self.mirando_derecha:
            self.image = pygame.transform.flip(self.image, True, False)
            self.mirando_derecha = not self.mirando_derecha

    def mover_hacia_objetivo(self):
        dx = self.objetivo.base.rect.x - self.rect.x
        dy = self.objetivo.base.rect.y - self.rect.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        if self.velocidad <= 0:
            from main import animaciones, enemigos_sprites
            self.morir()
            animacion = Animacion(self.rect.center, self.animacion_muerte_ice_slime, self.mirando_derecha)
            animaciones.add(animacion)
        if distancia > 0:
            velocidad_x = (dx / distancia) * self.velocidad
            velocidad_y = (dy / distancia) * self.velocidad

            self.rect.x += velocidad_x
            self.rect.y += velocidad_y

            # Evitar la superposición con otros enemigos
            self.evitar_superposicion()

            # Rotar según la dirección de movimiento
            if velocidad_x > 0 and not self.mirando_derecha:
                self.rotar2()
            elif velocidad_x < 0 and self.mirando_derecha:
                self.rotar1()

    def rotar_en_circulos(self):
        if self.velocidad <= 0:
            from main import animaciones, enemigos_sprites
            self.morir()
            animacion = Animacion(self.rect.center, self.animacion_muerte_ice_slime, self.mirando_derecha)
            animaciones.add(animacion)
        dx = self.objetivo.base.rect.centerx - self.rect.centerx
        dy = self.objetivo.base.rect.centery - self.rect.centery
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if 297 <= distancia <= 300:
            centro_x = self.objetivo.base.rect.centerx
            centro_y = self.objetivo.base.rect.centery
            radio = 299

            # Calcular el ángulo actual basándose en la posición actual del enemigo
            self.angulo_actual = math.atan2(self.rect.centery - centro_y, self.rect.centerx - centro_x)

            # Incrementa el ángulo para mover el enemigo en un círculo
            self.angulo_actual += (self.velocidad * 0.75) / radio

            # Calcula la nueva posición en el círculo
            nueva_x = centro_x + radio * math.cos(self.angulo_actual)
            nueva_y = centro_y + radio * math.sin(self.angulo_actual)

            # Mueve el enemigo a la nueva posición
            self.rect.centerx = nueva_x
            self.rect.centery = nueva_y

            # Evitar la superposición con otros enemigos
            self.evitar_superposicion()

            angulo_grados = math.degrees(self.angulo_actual)
            if 90 <= angulo_grados <= 270 and not self.mirando_derecha:
                self.rotar1()
            elif (angulo_grados < 90 or angulo_grados > 270) and self.mirando_derecha:
                self.rotar2()

        elif distancia > 300:
            # Si está a más de 300 de distancia, dirígete hacia el jugador
            if distancia > 0:
                velocidad_x = (dx / distancia) * self.velocidad
                velocidad_y = (dy / distancia) * self.velocidad

                self.rect.centerx += velocidad_x
                self.rect.centery += velocidad_y

                # Evitar la superposición con otros enemigos
                self.evitar_superposicion()

                # Rotar según la dirección de movimiento
                if velocidad_x > 0 and not self.mirando_derecha:
                    self.rotar2()
                elif velocidad_x < 0 and self.mirando_derecha:
                    self.rotar1()
        elif distancia < 297:
            if distancia > 0:
                # Calcula las velocidades invertidas para dirigirse hacia el jugador
                velocidad_x = -(dx / distancia) * self.velocidad
                velocidad_y = -(dy / distancia) * self.velocidad

                self.rect.centerx += velocidad_x
                self.rect.centery += velocidad_y

                # Evitar la superposición con otros enemigos
                self.evitar_superposicion()

                # Rotar según la dirección de movimiento
                if velocidad_x > 0 and not self.mirando_derecha:
                    self.rotar2()
                elif velocidad_x < 0 and self.mirando_derecha:
                    self.rotar1()


    def evitar_superposicion(self):
        if self.colision:
            from main import enemigos_sprites
            colisiones = pygame.sprite.spritecollide(self, enemigos_sprites, False)
            for enemigo in colisiones:
                if enemigo != self:
                    # Calcula la distancia y dirección del otro enemigo
                    dx = self.rect.centerx - enemigo.rect.centerx
                    dy = self.rect.centery - enemigo.rect.centery
                    distancia = math.sqrt(dx ** 2 + dy ** 2)

                    if distancia > 0:
                        # Mueve el enemigo actual un poco lejos del enemigo colisionado
                        desvio_x = (dx / distancia) * 2
                        desvio_y = (dy / distancia) * 2
                        self.rect.x += desvio_x
                        self.rect.y += desvio_y

    def soltar_recurso(self):
        from main import exp_sprites,sprite_exp1,sprite_exp2,sprite_exp3,Exp
        coordenadas=self.rect.center
        if 1<self.valor < 150:
            nuevo_recurso = Exp(sprite_exp1, *coordenadas, nivel=1)
        elif 150<=self.valor < 500:
            nuevo_recurso = Exp(sprite_exp2, *coordenadas, nivel=2)
        elif 500 <= self.valor:
            nuevo_recurso = Exp(sprite_exp3, *coordenadas, nivel=3)
        elif self.valor==1:
            return None
        exp_sprites.add(nuevo_recurso)

    def danio(self,daño,color_daño):
        from main import numeros_de_dano,DamageNumber
        self.vida -= daño
        texto_daño = str(daño)
        coordenadas_enemigo = (self.rect.x, self.rect.y)
        nuevo_dano = DamageNumber(texto_daño, coordenadas_enemigo[0], coordenadas_enemigo[1], color_daño)
        numeros_de_dano.append(nuevo_dano)
        self.barra=True

    def morir(self):
        from main import enemigos_sprites
        self.soltar_recurso()
        enemigos_sprites.remove(self)

    def aumentar_danio_y_vida(self,presu):
        if not self.actualizado:
            self.daño *= round(1 + (presu/400))
            self.vida_maxima *= round(1+(presu/400))
            self.vida *= round(1 + (presu/400))
            self.velocidad_base += round(0.02 * (presu/800))
            self.actualizado=True

    def barra_vida(self):
        from main import pantalla
        if self.barra:
            # Obtener el ancho del sprite del enemigo
            sprite_ancho = self.rect.width

            # Calcular el ancho de la barra de vida basada en la salud actual y el ancho del sprite
            barra_ancho = int(sprite_ancho * (self.vida / self.vida_maxima))
            barra_fondo_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, sprite_ancho, 5)
            barra_vida_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, barra_ancho, 5)

            # Dibujar la barra de vida en la pantalla
            pygame.draw.rect(pantalla, (255, 0, 0), barra_fondo_rect)  # Fondo de la barra de vida (rojo)
            pygame.draw.rect(pantalla, (0, 255, 0), barra_vida_rect)  # Barra de vida actual (verde)

    def update(self):
        self.mover_hacia_objetivo()
        self.barra_vida()
        self.ataque()

    def ataque(self):
        pass
# Clase intermedia Slime
class Slime(Enemigo):
    def __init__(self, vida, velocidad, daño, sprite_path, valor, boss=False, objetivo=None):
        super().__init__(vida, velocidad, daño, sprite_path, objetivo, valor, boss, tipo="Slime")

    def ataque(self):
        # Método de ataque común para Slimes
        pass


# Clases específicas de enemigos
class Ugly_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=20, velocidad=1.2, daño=6, sprite_path='Sprites/Enemigos/Enemigo-1.png', valor=3,
                         objetivo=objetivo)

    def ataque(self):
        # Implementa el ataque específico de Ugly_Slime
        pass


class Angry_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=50, velocidad=1.4, daño=17, sprite_path='Sprites/Enemigos/Enemigo-2.png', valor=15,
                         objetivo=objetivo)

    def ataque(self):
        # Implementa el ataque específico de Angry_Slime
        pass


class Fast_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=80, velocidad=1.6, daño=17, sprite_path='Sprites/Enemigos/Enemigo-3.png', valor=60,
                         objetivo=objetivo)
        self.colision=False

    def ataque(self):
        # Implementa el ataque específico de Fast_Slime
        pass


class Tank_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=120, velocidad=0.9, daño=30, sprite_path='Sprites/Enemigos/Enemigo-4.png', valor=90,
                         objetivo=objetivo)

    def ataque(self):
        # Implementa el ataque específico de Tank_Slime
        pass


class Pink_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=100, velocidad=1.2, daño=20, sprite_path='Sprites/Enemigos/Enemigo-5.png', valor=76,
                         objetivo=objetivo)
        self.tiempo_entre_ataques = 3000
        self.tiempo_ultimo_ataque=0

    def ataque(self):
        if pygame.time.get_ticks() - self.tiempo_entre_ataques>=self.tiempo_ultimo_ataque:
            from main import Bala, balas_enemigos
            from mejoras import calcular_direccion
            direccion=calcular_direccion(self.objetivo,self)
            nueva_bala =Bala(self.daño / 2, 5+(self.velocidad/2),
                                    pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                    self.rect.x, self.rect.y, direccion, 1, distancia=550)
            balas_enemigos.add(nueva_bala)
            self.tiempo_ultimo_ataque=pygame.time.get_ticks()

    def update(self):

        self.ataque()
        self.rotar_en_circulos()
        self.barra_vida()

class Two_Headed_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=400, velocidad=1.4, daño=40, sprite_path='Sprites/Enemigos/Two-Headed-Slime/Two-Slime.png', valor=300,
                         boss=True, objetivo=objetivo)
        self.num = 0
        self.ultimo_ataque = 0
        self.timer = pygame.time.get_ticks()
        self.tiempo_entre_ataques = 5000
        self.intervalo = 500
        self.animacion_ataque=[
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack1.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack2.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack3.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack4.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack5.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack6.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack7.png")
        ]
        self.sprite_original = self.image
        self.animando = False
        self.tiempo_ultimo_frame = 0
        self.frame_actual = 0
        self.duracion_frame = 100


    def ataque(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
            self.ultimo_ataque = tiempo_actual
            self.num = random.randint(1, 3)
            if self.num == 1:
                print("Invocar")
                self.invocar_enemigos()
            elif self.num == 2:
                print("Disparando")
                self.tipo_ataque_2()
            elif self.num == 3:
                self.tipo_ataque_3()
        if not self.animando:
            if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
                self.animando = True
                self.frame_actual = 0
                self.image = self.animacion_ataque[self.frame_actual]
                self.tiempo_ultimo_frame = tiempo_actual
                self.ultimo_ataque = tiempo_actual  # Actualizar el tiempo del último ataque para el siguiente ciclo
        else:
            if tiempo_actual - self.tiempo_ultimo_frame >= self.duracion_frame:
                self.tiempo_ultimo_frame = tiempo_actual
                self.frame_actual += 1
                if self.frame_actual >= len(self.animacion_ataque):
                    self.frame_actual = 0
                    self.animando = False
                    self.image = self.sprite_original
                    self.tipo_ataque_2()
                else:
                    self.image = self.animacion_ataque[self.frame_actual]

    def invocar_enemigos(self):
        from main import enemigos_sprites
        for _ in range(4):
            nuevo_enemigo = Enemigo(vida=5, velocidad=(1.3+(_*0.1)), daño=self.daño/5, sprite_path='Sprites/Enemigos/Two-Headed-Slime/Slimy.png',
                                    objetivo=self.objetivo, valor=1, boss=False)
            nuevo_enemigo.rect.center = self.rect.center
            enemigos_sprites.add(nuevo_enemigo)

    def tipo_ataque_2(self):
        from main import balas_enemigos, Bala
        from mejoras import calcular_direccion

        # Calcular la dirección hacia el objetivo
        direccion_original = calcular_direccion(self.objetivo, self)

        # Convertir la dirección a un vector unitario
        distancia = math.sqrt(direccion_original[0] ** 2 + direccion_original[1] ** 2)
        if distancia != 0:
            direccion_unitaria = (direccion_original[0] / distancia, direccion_original[1] / distancia)
        else:

            direccion_unitaria = (0, 0)

        # Calcular el ángulo en radianes para desviar las balas
        angulo_desvio = math.radians(10)  # 15 grados de desviación

        # Calcular las direcciones desviadas usando rotación
        def rotar_vector(vector, angulo):
            x, y = vector
            cos_ang = math.cos(angulo)
            sin_ang = math.sin(angulo)
            return (x * cos_ang - y * sin_ang, x * sin_ang + y * cos_ang)

        direccion_izquierda = rotar_vector(direccion_unitaria, -angulo_desvio)
        direccion_derecha = rotar_vector(direccion_unitaria, angulo_desvio)

        # Crear las tres balas con las direcciones calculadas
        nueva_bala_centro = Bala(self.daño / 2, 6,
                                 pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                 self.rect.x, self.rect.y, direccion_unitaria, 1, distancia=1100)
        nueva_bala_izquierda = Bala(self.daño / 2, 6,
                                    pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                    self.rect.x, self.rect.y, direccion_izquierda, 1, distancia=1100)
        nueva_bala_derecha = Bala(self.daño / 2, 6,
                                  pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                  self.rect.x, self.rect.y, direccion_derecha, 1, distancia=1100)

        # Agregar las balas al grupo de sprites de balas enemigas
        balas_enemigos.add(nueva_bala_centro)
        balas_enemigos.add(nueva_bala_izquierda)
        balas_enemigos.add(nueva_bala_derecha)

    def tipo_ataque_3(self):
        pass
        from main import balas_enemigos, Bala_temporal
        from mejoras import calcular_direccion
        direccion=calcular_direccion(self.objetivo,self)
        nueva_bala=Bala_temporal(self.daño/4, 3,
                                      pygame.image.load("Sprites\\Enemigos\\Two-Headed-Slime\\Two-Slime-At2.png",).convert_alpha(),
                                      self.rect.x, self.rect.y, direccion, 3000, tipo="Rastreo")
        balas_enemigos.add(nueva_bala)

    def update(self):
        self.ataque()
        self.rotar_en_circulos()
        self.barra_vida()


def spawn_enemigos(enemigos_sprites, jugador):
    from main import presupuesto_invocacion
    if len(enemigos_sprites) <= 15:
        valor_total = 0
        enemigos_disponibles = configuracion_enemigos.copy()
        while presupuesto_invocacion >= 1 and enemigos_disponibles:
            enemigo_clase = random.choice(enemigos_disponibles)
            enemigo = enemigo_clase(objetivo=jugador)
            if enemigo.valor + valor_total <= presupuesto_invocacion:
                # Calcular un ángulo aleatorio en radianes
                angulo_rad = random.uniform(0, 2 * math.pi)

                 # Calcular la posición relativa en el círculo
                radio = random.uniform(750, 800)
                pos_x_rel = radio * math.cos(angulo_rad)
                pos_y_rel = radio * math.sin(angulo_rad)

                # Calcular las coordenadas absolutas en relación con la posición del jugador
                enemigo.rect.x = jugador.base.rect.x + pos_x_rel
                enemigo.rect.y = jugador.base.rect.y + pos_y_rel

                enemigos_sprites.add(enemigo)
                valor_total += enemigo.valor
            else:
                enemigos_disponibles.remove(enemigo_clase)
    presupuesto_invocacion += 1
    presupuesto_invocacion *= 1.005
    nuevo_tiempo_ultimo_spawn_enemigos = pygame.time.get_ticks()
    for enemigo in enemigos_sprites:
        enemigo.aumentar_danio_y_vida(presupuesto_invocacion)
    return presupuesto_invocacion, nuevo_tiempo_ultimo_spawn_enemigos


def spawn_boss(enemigos_sprites,jugador):
    boss_c= random.choice(boss_config)
    boss= boss_c(objetivo=jugador)
    angulo_rad = random.uniform(0, 2 * math.pi)

    # Calcular la posición relativa en el círculo
    radio = random.uniform(750, 800)
    pos_x_rel = radio * math.cos(angulo_rad)
    pos_y_rel = radio * math.sin(angulo_rad)

    # Calcular las coordenadas absolutas en relación con la posición del jugador
    boss.rect.x = jugador.base.rect.x + pos_x_rel
    boss.rect.y = jugador.base.rect.y + pos_y_rel

    enemigos_sprites.add(boss)


def crear_enemigos():
    enemigos_config = [
        Ugly_Slime,
        Angry_Slime,
        Pink_Slime,
        Tank_Slime,
        Fast_Slime,
        Two_Headed_Slime,
    ]
    boss_config=[
        Two_Headed_Slime
    ]
    return enemigos_config,boss_config

configuracion_enemigos,boss_config = crear_enemigos()


