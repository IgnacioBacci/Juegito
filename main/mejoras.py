import threading
import pygame
import random
import math
import time
import os
from PIL import Image
mejoras_normales = []
mejoras_raras = []
mejoras_legendarias=[]
planetas = ["Mercurio", "Venus", "Tierra", "Marte", "Jupiter", "Saturno", "Urano", "Neptuno"]


def critico(bala,jugador):
    if bala.critico==False:
        multiplicador = 0.5
        if bala.prob_critica > 1:
            bala.prob_critica -=1
            bala.critico=True
            bala.daño *= 1+ multiplicador
        for suerte in range(jugador.suerte):
            if random.random() <= bala.prob_critica:
                bala.critico=True
                bala.daño *= 1 + multiplicador
                break
def encontrar_enemigo_mas_cercano(enemigos_sprites, origen):
    distancia_maxima = 500
    objetivo = None
    distancia_objetivo = float('inf')
    for enemigo in enemigos_sprites:
        if hasattr(origen, 'base'):
            dx = enemigo.rect.x - origen.base.rect.x
            dy = enemigo.rect.y - origen.base.rect.y
            distancia = math.sqrt(dx ** 2 + dy ** 2)
        else:
            dx = enemigo.rect.x - origen.rect.x
            dy = enemigo.rect.y - origen.rect.y
            distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia <= distancia_maxima and distancia < distancia_objetivo and enemigo != origen:
            objetivo = enemigo
            distancia_objetivo = distancia
    return objetivo
def congelamiento(enemigo,congelamiento):
    if not enemigo.boss:
        if enemigo.velocidad <= 0.70:
            enemigo.velocidad = 0
        else:
            # Reducir la velocidad del enemigo
            enemigo.velocidad -= congelamiento

            # Guardar la imagen original del enemigo temporalmente
            enemigo_image_original = enemigo.image
            # Guardar la imagen modificada temporalmente
            enemigo_image_modificada = "enemigo_modificado.png"

            # Guardar la imagen original en un archivo temporal
            pygame.image.save(enemigo.image, "enemigo_original.png")

            # Cargar la imagen original como una imagen PIL
            img_enemigo = Image.open("enemigo_original.png")

            # Convertir la imagen a modo RGBA
            img_enemigo = img_enemigo.convert("RGBA")
            # Obtener los datos de la imagen
            data = img_enemigo.getdata()
            # Crear una lista para los nuevos datos modificados
            new_data = []
            color_objetivo = (162, 240, 217)
            for item in data:
                # Mezclar los componentes de color del píxel con los del color objetivo
                new_color = []
                for i in range(3):  # Para los componentes RGB
                    new_color.append(int(item[i] * 1 + color_objetivo[i] * (congelamiento+0.1)))

                # Mantener el canal alfa original
                new_data.append((*new_color, item[3]))

                # Actualizar los datos de la imagen con los nuevos datos modificados
            img_enemigo.putdata(new_data)

            # Guardar la imagen modificada
            img_enemigo.save(enemigo_image_modificada)

            # Cargar la imagen modificada en pygame
            enemigo.image = pygame.image.load(enemigo_image_modificada)

            # Eliminar los archivos temporales
            os.remove("enemigo_original.png")
            os.remove(enemigo_image_modificada)
def calcular_direccion(objetivo, origen):
    # Obtener las coordenadas del origen
    if hasattr(origen, 'arma_primaria'):
        x_origen = origen.arma_primaria.rect.centerx
        y_origen = origen.arma_primaria.rect.centery
    else:
        x_origen = origen.rect.centerx
        y_origen = origen.rect.centery

    if hasattr(objetivo, "base"):
        x_objetivo = objetivo.base.rect.centerx
        y_objetivo = objetivo.base.rect.centery
    # Obtener las coordenadas del objetivo
    else:
        x_objetivo = objetivo.rect.centerx
        y_objetivo = objetivo.rect.centery

    # Calcular el vector de dirección
    dx = x_objetivo - x_origen
    dy = y_objetivo - y_origen

    # Calcular la distancia
    distancia = math.sqrt(dx ** 2 + dy ** 2)

    # Normalizar el vector de dirección
    if distancia > 0:
        return (dx / distancia, dy / distancia)
    else:
        return (0, 0)
def actualizar_orbital(jugador,tipo):
    from main import balas_sprites
    orbital = [bala for bala in balas_sprites if bala.tipo == str(tipo)]
    num_orbitales = len(orbital)
    if num_orbitales == 0:
        return

    # Calcula el ángulo entre cada bala "Orbital"
    angulo_entre_balas = 360 / num_orbitales

    for i, bala in enumerate(orbital):
        # Incrementa el ángulo de la bala para hacerla girar
        bala.angulo = (i * angulo_entre_balas + pygame.time.get_ticks() / bala.velocidadProyectil) % 360
        angulo_rad = math.radians(bala.angulo)
        dist = bala.distancia_maxima # Ajustar el radio del círculo
        bala.rect.centerx = jugador.base.rect.centerx + math.cos(angulo_rad) * bala.distancia_maxima
        bala.rect.centery = jugador.base.rect.centery + math.sin(angulo_rad) * bala.distancia_maxima
        bala.direccion = (math.cos(angulo_rad), math.sin(angulo_rad))

def agregar_planeta(jugador):
    from main import balas_sprites,Bala
    planeta = random.choice(planetas)
    if planeta=="Mercurio":
        direccion = (0, -1)
        nueva_bala = Bala(10, 50,
                          pygame.image.load('Sprites/Armas/Balas/Mercury.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=20)
    elif planeta=="Venus":
        direccion = (0, -1)
        nueva_bala = Bala(15, 49,
                          pygame.image.load('Sprites/Armas/Balas/Venus.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=60)
    elif planeta=="Tierra":
        direccion = (0, -1)
        nueva_bala = Bala(20, 48,
                          pygame.image.load('Sprites/Armas/Balas/Earth.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=100)
    elif planeta=="Marte":
        direccion = (0, -1)
        nueva_bala = Bala(25, 47,
                          pygame.image.load('Sprites/Armas/Balas/Mars.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=140)
    elif planeta=="Jupiter":
        direccion = (0, -1)
        nueva_bala = Bala(30, 46,
                          pygame.image.load('Sprites/Armas/Balas/Jupiter.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=180)
    elif planeta=="Saturno":
        direccion = (0, -1)
        nueva_bala = Bala(35, 45,
                          pygame.image.load('Sprites/Armas/Balas/Saturn.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=220)
    elif planeta=="Urano":
        direccion = (0, -1)
        nueva_bala = Bala(40, 44,
                          pygame.image.load('Sprites/Armas/Balas/Uranus.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=260)
    elif planeta=="Neptuno":
        direccion = (0, -1)
        nueva_bala = Bala(45, 43,
                          pygame.image.load('Sprites/Armas/Balas/Neptune.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=300)
    else:
        return None
    planetas.remove(planeta)
    if len(planetas) ==0:
        if Expansion in mejoras_raras:
            mejoras_raras.remove(Expansion)
    balas_sprites.add(nueva_bala)
    print(len(mejoras_raras))

def hermite_spline(t, p0, p1, m0, m1):
    """Calcula un hermite spline."""
    h00 = (2 * t ** 3) - (3 * t ** 2) + 1
    h10 = t ** 3 - (2 * t ** 2) + t
    h01 = (-2 * t ** 3) + (3 * t ** 2)
    h11 = t ** 3 - t ** 2

    x = h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1
    return x
class Mejora:
    def __init__(self,nombre, efecto, rareza, sprite):
        self.valor = 0
        self.nombre = nombre
        self.efecto = efecto
        self.rareza = rareza
        self.sprite = sprite

class Autoreparacion(Mejora):
    def __init__(self, valor=0):
        self.valor = valor
        self.tiempo_ultima_reparacion = 0
        efecto = f"Heal {1 * (self.valor + 1)} per second"
        super().__init__("Self-repair", efecto, "Normal", "Sprites\\Recursos\\Mejoras\\Autoreparacion.png")
    def actualizar_efecto(self):
        self.efecto= f"Heal {1 * (self.valor + 1)} per second"
    def aplicar(self, jugador):
        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 1000
        if tiempo_segundos > self.tiempo_ultima_reparacion:
            jugador.base.vida_actual += self.valor * (tiempo_segundos - self.tiempo_ultima_reparacion)
            if jugador.base.vida_actual > jugador.base.vida_maxima:
                jugador.base.vida_actual = jugador.base.vida_maxima

        self.tiempo_ultima_reparacion = tiempo_segundos
Autoreparacion=Autoreparacion()
mejoras_normales.append(Autoreparacion)
class CorazaReforzada(Mejora):
    def __init__(self, valor=0):
        self.valor = valor
        efecto=f"Gain {25*(self.valor+1)} maximum health"
        super().__init__("reinforced armor", efecto, "Normal",
                         "Sprites\\Recursos\\Mejoras\\Coraza_Reforzada.png")
    def actualizar_efecto(self):
        self.efecto= f"Gain {25*(self.valor+1)} maximum health"
    def aplicar_primera(self, jugador):
        jugador.base.vida_maxima += 25


CorazaReforzada=CorazaReforzada()
mejoras_normales.append(CorazaReforzada)
class CalorCurativo(Mejora):
        def __init__(self, valor=0):
            self.valor = valor
            efecto=f"Heal for {10*(self.valor+1)}% of the heat generated"
            super().__init__("Healing heat", efecto, "Normal",
                             "Sprites\\Recursos\\Mejoras\\Calor_Curativo.png")

        def actualizar_efecto(self):
            self.efecto = f"Heal for {10*(self.valor+1)}% of the heat generated"
        def aplicar(self, jugador):
            valor = self.valor / 10
            if jugador.base.calor_actual > getattr(jugador, 'calor_anterior', jugador.base.calor_actual):
                Curacion= round((jugador.base.calor_actual - getattr(jugador, 'calor_anterior',jugador.base.calor_actual * valor)))
                jugador.base.vida_actual += Curacion
                if jugador.base.vida_actual > jugador.base.vida_maxima:
                    jugador.base.vida_actual = jugador.base.vida_maxima

            jugador.calor_anterior = jugador.base.calor_actual

CalorCurativo=CalorCurativo()
mejoras_normales.append(CalorCurativo)

class DisparoRafaga(Mejora):
    def __init__(self,valor=0):
        self.valor=valor
        efecto=f"After not shooting for 3 seconds, your rate of fire increases by {100*(self.valor+1)} for 5 seconds (Stackable)"
        super().__init__("Burst Shot", efecto, "Normal",
                         "Sprites/Recursos/Mejoras/Disparo_Rafaga.png")
        self.tiempo_primaria = 0
        self.tiempo_secundaria = 0
        self.duracion = 5
        self.activo_primaria=False
        self.activo_secundaria = False

    def actualizar_efecto(self):
        self.efecto = f"After not shooting for 3 seconds, your rate of fire increases by {100*(self.valor+1)} for 5 seconds"
    def realizar_accion(self, jugador, arma):
        if arma.tipo=="Primaria":
            while not jugador.disparando:
                time.sleep(0.1)
            arma.velocidad += arma.velocidad_base * (self.valor)
            print(f"AUMENTO {arma.velocidad}")
            time.sleep(self.duracion)
            arma.velocidad -= arma.velocidad_base * (self.valor)
            print(arma.velocidad)
        else:
            while not jugador.disparando_secundaria:
                time.sleep(0.1)
            arma.velocidad += arma.velocidad_base * (self.valor)
            print(f"AUMENTO {arma.velocidad}")
            time.sleep(self.duracion)
            arma.velocidad -= arma.velocidad_base * (self.valor)
            print(arma.velocidad)

    def aplicar(self, jugador):
        tiempo_actual = pygame.time.get_ticks()

        if jugador.arma_primaria is not None and not jugador.disparando:
            if not jugador.disparando:
                if not self.activo_primaria:
                    if tiempo_actual - self.tiempo_primaria >= 3000:
                        self.tiempo_primaria = tiempo_actual

                        # Utilizamos threading para ejecutar la acción concurrentemente
                        accion_thread = threading.Thread(target=self.realizar_accion, args=(jugador, jugador.arma_primaria))
                        accion_thread.start()
            elif self.activo_primaria:
                self.tiempo_primaria = 0
                self.activo_primaria = False
                print(jugador.arma_primaria.velocidad)

        if jugador.arma_secundaria is not None and not jugador.disparando_secundaria:
            if not jugador.disparando_secundaria:
                if not self.activo_secundaria:
                    if tiempo_actual - self.tiempo_secundaria >= 3000:
                        self.tiempo_secundaria = tiempo_actual

                        # Utilizamos threading para ejecutar la acción concurrentemente
                        accion_thread = threading.Thread(target=self.realizar_accion, args=(jugador, jugador.arma_secundaria))
                        accion_thread.start()
            elif self.activo_secundaria:
                self.tiempo_secundaria = 0
                self.activo_secundaria = False
                print(jugador.arma_secundaria.velocidad)

DisparoRafaga=DisparoRafaga()
mejoras_normales.append(DisparoRafaga)

class AprenderErrores(Mejora):
    def __init__(self,valor=0):
        self.valor=valor
        efecto=f"Increases the invulnerability time when receiving damage by {15*(valor+1)}%"
        super().__init__("Learn from mistakes", efecto, "Normal",
                         "Sprites/Recursos/Mejoras/Aprender_Errores.png")

    def actualizar_efecto(self):
        self.efecto =f"Increases the invulnerability time when receiving damage by {15*(self.valor+1)}%"
    def aplicar_primera(self, jugador):
        jugador.tiempo_invulnerabilidad += 150


AprenderErrores=AprenderErrores()
mejoras_normales.append(AprenderErrores)

class DisparoCertero(Mejora):
    def __init__(self):
        self.valor=0
        efecto=f"Increases the critical hit rate by {10*(self.valor+1)}%"
        super().__init__("Accurate shot", efecto,"Normal","Sprites\\Recursos\\Mejoras\\Disparo_certero.png")

    def actualizar_efecto(self):
        self.efecto = f"Increases the critical hit rate by {10*(self.valor+1)}%"
    def aplicar_primera(self,jugador):
        jugador.arma_primaria.prob_critica += 0.1
        jugador.arma_secundaria.prob_critica +=0.1

DisparoCertero=DisparoCertero()
mejoras_normales.append(DisparoCertero)
class SoltarAceite(Mejora):
    def __init__(self):
        self.cd=0
        self.duracion=2
        self.valor=0
        efecto=f"Upon receiving damage, release oil that deal {4*(self.valor+1)} damage per second to enemies"
        super().__init__("Oil leak", efecto,"Normal","Sprites\\Recursos\\Mejoras\\Aceite.png")

    def actualizar_efecto(self):
        self.efecto =f"Upon receiving damage, release oil that deal {4*(self.valor+1)} damage per second to enemies"
    def aplicar_recibir(self,jugador,daño):
        from main import enemigos_sprites, balas_sprites, Bala_temporal
        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 10000
        if tiempo_segundos > self.cd:
            objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, jugador)
            if objetivo:
                direccion = calcular_direccion(objetivo, jugador)
                nueva_bala = Bala_temporal(4*self.valor, 0,
                                      pygame.image.load("Sprites\\Recursos\\Mejoras\\Aceite2.png",).convert_alpha(),
                                      jugador.base.rect.x, jugador.base.rect.y + 20, direccion, 5000, tipo="Aceite")
                balas_sprites.add(nueva_bala)
                self.cd = tiempo_segundos
                return daño
        return daño
SoltarAceite=SoltarAceite()
mejoras_normales.append(SoltarAceite)
class MisilesRastreadores(Mejora):
    def __init__(self):
        self.tiempo_ultimo_misil=0
        self.valor=0
        efecto=f"Fire a missile that deals {15*(self.valor+1)} damage to a nearby enemy"
        super().__init__("Guided missiles", efecto, "Normal",
                         "Sprites\\Recursos\\Mejoras\\Misiles.png")

    def actualizar_efecto(self):
        self.efecto =f"Fire a missile that deals {15*(self.valor+1)} damage to a nearby enemy"
    def aplicar(self, jugador):
        from main import enemigos_sprites, balas_sprites, Bala

        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 3000
        if tiempo_segundos > self.tiempo_ultimo_misil:
                nueva_bala = Bala(15 * self.valor, 1,
                                      pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha(),
                                      jugador.base.rect.centerx, jugador.base.rect.y - 10, (jugador.base.rect.centerx,-1), 1, tipo="misil")
                for mejora in jugador.mejoras:
                    if hasattr(mejora, 'aplicar_dis'):
                        mejora.aplicar_dis(jugador, nueva_bala)
                balas_sprites.add(nueva_bala)
                self.tiempo_ultimo_misil = tiempo_segundos
                return None

        return None

MisilesRastreadores = MisilesRastreadores()
mejoras_normales.append(MisilesRastreadores)

class Overclock(Mejora):
    def __init__(self):
        self.ultima_activacion = 0
        self.duracion = 3  # Duración de la mejora en segundos
        self.cooldown = 10  # Tiempo de recarga en segundos
        self.timer = None
        self.valor=0
        efecto=f"When reaching 75% heat, core cooling increases by {75*(self.valor+1)}% for 3 seconds"
        super().__init__("Overclock",efecto, "Normal", "Sprites\\Recursos\\Mejoras\\Overclock.png")

    def actualizar_efecto(self):
        self.efecto =f"When reaching 75% heat, core cooling increases by {75*(self.valor+1)}% for 3 seconds"
    def aplicar(self, jugador):
        tiempo_actual = time.time()

        if jugador.base.calor_actual / jugador.base.calor_maximo >= 0.75:
            # Verificar si la mejora está en tiempo de recarga
            if tiempo_actual - self.ultima_activacion < self.cooldown:
                return
            jugador.nucleo.regCalor *= 1 + (0.75 * self.valor)

            # Actualizar el tiempo de última activación
            self.ultima_activacion = tiempo_actual

            # Configurar un temporizador para la duración de la mejora
            self.timer = threading.Timer(self.duracion, self.desactivar_mejora, args=[jugador])
            self.timer.start()

    def desactivar_mejora(self, jugador):
        jugador.nucleo.regCalor /= 1 + (0.75 * self.valor)
        self.timer = None
Overclock=Overclock()
mejoras_normales.append(Overclock)

class SaltoFase(Mejora):
    def __init__(self):
        self.valor=0
        self.valor2=self.valor
        if self.valor+1>=10:
            self.valor2=9
        efecto=f"When taking damage, {5*(self.valor2+1)}% chance to ignore it"
        super().__init__("Phase change",efecto,"Normal","Sprites\\Recursos\\Mejoras\\Salto_fase.png")

    def actualizar_efecto(self):
        self.valor2 = self.valor
        if self.valor + 1 >= 10:
            self.valor2 = 9
        self.efecto =f"When taking damage, {5*(self.valor2+1)}% chance to ignore it"
    def aplicar_recibir(self,jugador,daño):
        valor=self.valor
        if valor > 10:
            valor = 10
        if random.random() <(0.05*valor):
            daño =0
        return daño
SaltoFase=SaltoFase()
mejoras_normales.append(SaltoFase)

class CicloVida(Mejora):
    def __init__(self):
        self.valor=0
        efecto=f"Gain {1*(self.valor+1)} energy per kill"
        super().__init__("Life cycle",efecto,"Normal","Sprites\\Recursos\\Mejoras\\Ciclo_vida.png")
    def actualizar_efecto(self):
        self.efecto =f"Gain {1*(self.valor+1)} energy per kill"
    def aplicar_matar(self,jugador,enemigo):
        jugador.base.energia_actual += 1 * self.valor

CicloVida=CicloVida()
mejoras_normales.append(CicloVida)

class TormentaEstrellas(Mejora):
    def __init__(self):
        self.valor = 0
        self.cantidad=5
        super().__init__("Star storm", f"After using the core ability, creates 5 stars that rotate around and deal {10 * (self.valor + 1)} damage", "Normal", "Sprites\\Recursos\\Mejoras\\Star.png")


    def actualizar_efecto(self):
        self.efecto =f"After using the core ability, creates 3 stars that rotate around and deal {10 * (self.valor + 1)} damage"

    def aplicar_nucleo(self,jugador):
        from main import Bala,balas_sprites
        for num in range(self.cantidad):
            direccion = (0, -1)  # Dirección inicial hacia arriba
            nueva_bala = Bala(10*(self.valor), 5,
                              pygame.image.load('Sprites/Armas/Balas/Star.png').convert_alpha(),
                              jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                              1, tipo="Orbital Estelar", distancia=80)
            nueva_bala.angulo = 0
            balas_sprites.add(nueva_bala)
    def aplicar(self,jugador):
            actualizar_orbital(jugador,"Orbital Estelar")


TormentaEstrellas=TormentaEstrellas()
mejoras_normales.append(TormentaEstrellas)

class Boomerang(Mejora):
    def __init__(self):
        self.valor = 0
        self.cd=8
        self.incremento_angulo=20
        self.angulo_rotacion=0
        super().__init__("Boomerang", f"Every {self.cd} seconds throw a boomerang to a random direction that deal {25+ (10*(self.valor+1))}", "Normal", "Sprites\\Recursos\\Mejoras\\Rang.png")

        self.ultima_activacion = pygame.time.get_ticks()

    def actualizar_efecto(self):
        self.efecto = f"Every {self.cd} seconds throw a boomerang to a random direction that deals {25 + (10 * (self.valor + 1))} damage"
        if self.valor % 3 == 0 and self.cd > 2:
            self.cd -= 1

    def aplicar(self, jugador):
        from main import Bala, balas_sprites
        for bala in balas_sprites:
            if bala.tipo =="Boomerang":
                self.angulo_rotacion += self.incremento_angulo  # Incrementa el ángulo de rotación
                bala.image = pygame.transform.rotate(bala.original_image, self.angulo_rotacion)
                bala.rect = bala.image.get_rect(center=bala.rect.center)
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultima_activacion >= self.cd * 1000:
            self.ultima_activacion = tiempo_actual

            # Crear un boomerang
            direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            while direccion == (0, 0):
                direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            direccion_normalizada = pygame.math.Vector2(direccion).normalize()

            nueva_bala = Bala(
                25 + (10 * (self.valor)),
                7,
                pygame.image.load('Sprites/Armas/Balas/Rang.png').convert_alpha(),
                jugador.base.rect.centerx,
                jugador.base.rect.centery,
                direccion_normalizada,
                -1,
                tipo="Boomerang", distancia=1200
            )
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)
        for bala in balas_sprites:
            if bala.tipo=="Boomerang":
                bala.velocidadProyectil += 0.2
                if bala.distancia_recorrida > bala.distancia_maxima / 3:
                    dx = jugador.base.rect.centerx - bala.rect.centerx
                    dy = jugador.base.rect.centery - bala.rect.centery
                    distancia = math.sqrt(dx ** 2 + dy ** 2)
                    if distancia != 0:
                        direccion_hacia_jugador = (dx / distancia, dy / distancia)
                        bala.direccion = direccion_hacia_jugador

Boomerang=Boomerang()
mejoras_normales.append(Boomerang)
#Raros
class Acero(Mejora):
    def __init__(self):
        self.valor=0
        efecto=f"Reduce taken damage by {3*(self.valor+1)}"
        super().__init__("Steel+",efecto,"Rare","Sprites\\Recursos\\Mejoras\\Acero+.png")

    def actualizar_efecto(self):
        self.efecto =f"Reduce taken damage by {3*(self.valor+1)}"
    def aplicar_recibir(self,jugador,daño):
        print(daño)
        daño -= 3*self.valor
        if daño<0:
            daño=0
        print(daño)
        return(daño)

Acero=Acero()
mejoras_raras.append(Acero)
class CalorConstante(Mejora):
    def __init__(self):
        self.valor = 0
        self.aplicado = False
        self.activo = False
        efecto = f"Weapons generate 10% more heat. Above 50% heat, weapons deal {20 * (self.valor+1)}% more damage"
        super().__init__("Constant Heat", efecto, "Rare", "Sprites\\Recursos\\Mejoras\\Calor_constante.png")

    def actualizar_efecto(self):
        self.efecto =f"Weapons generate 10% more heat. Above 50% heat, weapons deal {20 * (self.valor+1)}% more damage"
    def aplicar(self, jugador):
        aumento= 0.2 * self.valor
        if self.aplicado==False:
            jugador.arma_primaria.calentamiento *=1.1
            jugador.arma_secundaria.calentamiento *= 1.1
            self.aplicado = True

        if jugador.base.calor_actual > 0.5 * jugador.base.calor_maximo:
            if self.activo ==False:
                jugador.arma_primaria.daño *= 1 + aumento
                jugador.arma_secundaria.daño *= 1 + aumento
            self.activo=True
        else:
            if self.activo == True:
                jugador.arma_primaria.daño /= (1+aumento)
                jugador.arma_secundaria.daño /= (1+aumento)
            self.activo=False
CalorConstante=CalorConstante()
mejoras_raras.append(CalorConstante)
class EngranajesPulidos(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Polished Gears", f"Increases movement speed by {5 * (self.valor+1)}%", "Rare", "Sprites\\Recursos\\Mejoras\\Engranajes.png")
    def actualizar_efecto(self):
        self.efecto =f"Increases movement speed by {5 * (self.valor+1)}%"
    def aplicar_primera(self,jugador):
        jugador.base.velocidad += jugador.base.velocidad_base * 0.05
EngranajesPulidos=EngranajesPulidos()
mejoras_raras.append(EngranajesPulidos)

class DisparoGemelo(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Twin Shot", f"You have {10 * (self.valor+1)}% chance to fire an additional bullet", "Rare", "Sprites\\Recursos\\Mejoras\\Disparo_gemelo.png")
    def actualizar_efecto(self):
        self.efecto =f"You have {10 * (self.valor+1)}% chance to fire an additional bullet"
    def aplicar_dis(self,jugador, arma):
        from main import calcular_direccion, balas_sprites
        disparos = 0
        disparos_realizados = 1
        valor=self.valor
        while valor > 10:
            disparos += 1
            valor -= 10
        for suerte in range(jugador.suerte):
            if random.random() <= (0.10 * valor):
                disparos += 1
                break
        from main import Bala
        for i in range(disparos):
            arma.velocidadProyectil -= disparos_realizados
            arma.daño *= 0.50
            nueva_bala = Bala(arma.daño, arma.velocidadProyectil, arma.image,
                              arma.rect.x, arma.rect.y, arma.direccion, arma.perforacion, distancia=arma.distancia_maxima, tipo=arma.tipo, eficiencia=0.1)

            if nueva_bala.velocidadProyectil <= 2:
                nueva_bala.velocidadProyectil += 1
                disparos_realizados -= 1

            balas_sprites.add(nueva_bala)

            disparos_realizados += 1
            arma.daño *= 2
            arma.velocidadProyectil += disparos_realizados

DisparoGemelo=DisparoGemelo()
mejoras_raras.append(DisparoGemelo)

class BalaDispercion(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Scatter Bullet", "Upon killing enemies, they explode into a shower of bullets", "Rare", "Sprites\\Recursos\\Mejoras\\Dispercion.png")

    def actualizar_efecto(self):
        self.efecto ="Upon killing enemies, they explode into a shower of bullets"
    def aplicar_matar(self, jugador, enemigo):
        from main import Bala, balas_sprites

        posicion_final_enemigo = (enemigo.rect.x, enemigo.rect.y)
        num_balas = 3 + self.valor
        separacion_angulo = 360 / num_balas

        for i in range(num_balas):
            # Calcular la dirección utilizando trigonometría
            angulo_rad = math.radians(i * separacion_angulo)
            direccion = (math.cos(angulo_rad), math.sin(angulo_rad))

            nueva_bala = Bala(3, 8,
                              pygame.image.load("Sprites\\Armas\\Balas\\Bala-1.png").convert_alpha(),
                              posicion_final_enemigo[0], posicion_final_enemigo[1] + 20, direccion, 1, eficiencia=0.15)

            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)
BalaDispercion=BalaDispercion()
mejoras_raras.append(BalaDispercion)

class Rebote(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Ricochet", f"When a bullet hits an enemy, it has a {10 * (self.valor + 1)}% chance to change its trajectory towards another one", "Rare", "Sprites\\Recursos\\Mejoras\\Rebote.png")

    def actualizar_efecto(self):
        self.efecto =f"When a bullet hits an enemy, it has a {10 * (self.valor + 1)}% chance to change its trajectory towards another one"
    def aplicar_imp(self,jugador,bala,enemigo):
        from main import enemigos_sprites, balas_sprites
        for suerte in range(jugador.suerte):
            if random.random() <= (0.10 * self.valor):
                objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, enemigo)
                if objetivo:
                    direccion = calcular_direccion(objetivo, enemigo)
                    bala.direccion=direccion
                    bala.daño *= 0.75
                break
Rebote=Rebote()
mejoras_raras.append(Rebote)

class PuntaAero(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Aerodynamic Tip", f"Increases projectile speed by {10 * (self.valor + 1)}%, every 3 upgrades increases penetration", "Rare", "Sprites\\Recursos\\Mejoras\\Aero.png")

    def actualizar_efecto(self):
        self.efecto =f"Increases projectile speed by {10 * (self.valor + 1)}%, every 3 upgrades increases penetration"
    def aplicar_primera(self,jugador):
        if self.valor < 10:
            jugador.arma_primaria.velocidadProyectil *=1.10
            jugador.arma_secundaria.velocidadProyectil *= 1.10
        if self.valor % 3==0:
            jugador.arma_primaria.perforacion +=1
            jugador.arma_secundaria.perforacion +=1

PuntaAero=PuntaAero()
mejoras_raras.append(PuntaAero)

class CriticoRestaurativo(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Restorative Critical", f"Critical hits restore {3 * (self.valor + 1)} health, {1 * (self.valor + 1)} energy, or reduce heat by {2 * (self.valor + 1)}", "Rare", "Sprites\\Recursos\\Mejoras\\Critico_restaurativo.png")
        self.num=0
    def actualizar_efecto(self):
        self.efecto =f"Critical hits restore {3 * (self.valor + 1)} health, {1 * (self.valor + 1)} energy, or reduce heat by {2 * (self.valor + 1)}"
    def aplicar_imp(self,jugador,bala,enemigo):
        if bala.critico==True:
            if self.num==0:
                jugador.base.vida_actual+=3*self.valor
                self.num+=1
                if jugador.base.vida_actual > jugador.base.vida_maxima:
                    jugador.base.vida_actual = jugador.base.vida_maxima
            elif self.num==1:
                jugador.base.energia_actual+=1*self.valor
                self.num+=1
            elif self.num==2:
                jugador.base.calor_actual -=2*self.valor
                self.num=0

    def aplicar_primera(self,jugador):
        print(self.valor)
        jugador.arma_primaria.prob_critica +=0.1
        jugador.arma_secundaria.prob_critica +=0.1
CriticoRestaurativo=CriticoRestaurativo()
mejoras_raras.append(CriticoRestaurativo)

class ExplosionHelada(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Frost Explosion", f"Every 7 seconds, slows down and inflicts {15 * (self.valor + 1)} damage to nearby enemies", "Rare", "Sprites\\Recursos\\Mejoras\\Ice_wave.png")
        self.cd = 7000
        self.ultima_activacion = 0
        self.animacion = [
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png",
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png",
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png"
        ]

    def actualizar_efecto(self):
        self.efecto = f"Every 7 seconds, slows down and inflicts {15 * (self.valor + 1)} damage to nearby enemies"

    def aplicar(self, jugador):
        from main import enemigos_sprites, animaciones
        from Enemigos import Animacion
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultima_activacion >= self.cd:
            radio = 150

            # Redimensionar los sprites de la animación
            animacion_redimensionada = self.redimensionar_animacion(self.animacion, radio * 2, radio * 2)
            animacion = Animacion(jugador.base.rect.center, animacion_redimensionada, True, desaparecer=True)
            animaciones.add(animacion)

            for enemigo in enemigos_sprites:
                distancia = math.sqrt(
                    (enemigo.rect.centerx - jugador.base.rect.centerx) ** 2 +
                    (enemigo.rect.centery - jugador.base.rect.centery) ** 2
                )
                if distancia <= radio:
                    enemigo.danio(15 * self.valor,(136,245,234))  # Inflige el daño al enemigo
                    congelamiento(enemigo, 0.20)

            self.ultima_activacion = tiempo_actual

    def redimensionar_animacion(self, animacion_paths, nuevo_ancho, nuevo_alto):
        sprites_redimensionados = []
        for sprite_path in animacion_paths:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite_redimensionado = pygame.transform.scale(sprite, (nuevo_ancho, nuevo_alto))
            sprites_redimensionados.append(sprite_redimensionado)
        return sprites_redimensionados

ExplosionHelada=ExplosionHelada()
mejoras_raras.append(ExplosionHelada)

class Sierra(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Saw", f"A spinning saw that deals {20*(self.valor + 1)} damage to enemies", "Rare", "Sprites\\Recursos\\Mejoras\\Saw.png")

        self.ultima_activacion = pygame.time.get_ticks()

    def actualizar_efecto(self):
        self.efecto =f"A spinning saw that deals {25*(self.valor + 1)} damage to enemies"
    def aplicar_primera(self, jugador):
        from main import Bala, balas_sprites
        for bala in balas_sprites:
            if bala.tipo == "Orbital Sierra":
                bala.daño = 25 *(self.valor)
        if self.valor % 3 == 0 or self.valor == 1:
            print(self.valor)
            direccion = (0, -1)  # Dirección inicial hacia arriba
            nueva_bala = Bala(25, 30,
                              pygame.image.load('Sprites/Armas/Balas/Saw.png').convert_alpha(),
                              jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                              -1, tipo="Orbital Sierra",distancia=175)
            nueva_bala.angulo = 0  # Añadimos el atributo de ángulo
            balas_sprites.add(nueva_bala)
            self.actualizar_sierra(jugador, balas_sprites)

    def aplicar(self, jugador):
        from main import balas_sprites
        self.actualizar_sierra(jugador, balas_sprites)

    def actualizar_sierra(self, jugador, balas_sprites):
        # Filtra las balas tipo "Sierra"
        sierras = [bala for bala in balas_sprites if bala.tipo == "Orbital Sierra"]
        num_sierra = len(sierras)
        if num_sierra == 0:
            return
        actualizar_orbital(jugador,"Orbital Sierra")


Sierra=Sierra()
mejoras_raras.append(Sierra)

#Legendarias
class CañonPrimario(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Primary Cannon", "Greatly enhances the primary weapon", "Legendary", "Sprites\\Recursos\\Mejoras\\Primario.png")

    def actualizar_efecto(self):
        self.efecto ="Greatly enhances the primary weapon"
    def aplicar_primera(self,jugador):
        jugador.arma_primaria.daño *= 1.5
        jugador.arma_primaria.velocidad *= 1.5
        jugador.arma_primaria.perforacion += 2

CañonPrimario=CañonPrimario()
mejoras_legendarias.append(CañonPrimario)

class DecoracionDados(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Dice Decoration", "Increases your luck", "Legendary", "Sprites\\Recursos\\Mejoras\\Dado.png")

    def actualizar_efecto(self):
        self.efecto ="Increases your luck"
    def aplicar_primera(self,jugador):
        jugador.suerte +=1

DecoracionDados=DecoracionDados()
mejoras_legendarias.append(DecoracionDados)

class EspirituVengativo(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Vengeful Spirits", "Upon killing an enemy, releases its spirit to torment another enemy", "Legendary", "Sprites\\Recursos\\Mejoras\\Espiritu_Vengativo.png")

    def actualizar_efecto(self):
        self.efecto ="Upon killing an enemy, releases its spirit to torment another enemy"
    def aplicar_matar(self, jugador, enemigo):
        from main import enemigos_sprites, balas_sprites, Bala
        objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, enemigo)
        if objetivo:
            posicion_final_enemigo = (enemigo.rect.x, enemigo.rect.y)
            nueva_bala = Bala(round((enemigo.vida_maxima) * (0.5 * self.valor)), 1,
                              pygame.image.load("Sprites\\Recursos\\Mejoras\\Espiritu_Vengativo2.png").convert_alpha(),
                              posicion_final_enemigo[0], posicion_final_enemigo[1] + 20, (0,-1), 1, tipo="Fantasmal")
            balas_sprites.add(nueva_bala)

            # Llama a encontrar_enemigo_mas_cercano para actualizar el objetivo del espiritu
            objetivo_espiritu = encontrar_enemigo_mas_cercano(enemigos_sprites, nueva_bala)
            nueva_bala.objetivo = objetivo_espiritu

            return nueva_bala
        else:
            return None
EspirituVengativo=EspirituVengativo()
mejoras_legendarias.append(EspirituVengativo)

class JugandoFuego(Mejora):
    def __init__(self):
        self.valor = 0
        self.activado = False
        super().__init__("Playing with Fire", f"When overheating, increases your weapons' damage by {10 * (self.valor + 1)}%, up to a maximum of {100 * (self.valor + 1)}%", "Legendary", "Sprites\\Recursos\\Mejoras\\Fuego.png")

    def actualizar_efecto(self):
        self.efecto =f"When overheating, increases your weapons' damage by {10 * (self.valor + 1)}%, up to a maximum of {100 * (self.valor + 1)}%"
    def aplicar(self,jugador):

        if jugador.sobrecalentado == True and self.activado==False:
            if not jugador.arma_primaria.daño / jugador.arma_primaria.daño_base > 1 + self.valor:
                jugador.arma_primaria.daño *= 1 + (0.1 * self.valor)
            if not jugador.arma_secundaria.daño / jugador.arma_secundaria.daño_base > 1 + self.valor:
                jugador.arma_secundaria.daño *= 1 +(0.1 * self.valor)
            self.activado=True
        elif jugador.sobrecalentado == False:
            self.activado=False

JugandoFuego=JugandoFuego()
mejoras_legendarias.append(JugandoFuego)

class Milicia(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Militia", f"Increases missile damage by {50 * (self.valor + 1)}%, sometimes when firing, you launch 3 missiles to nearby enemies", "Legendary", "Sprites\\Recursos\\Mejoras\\Milicia.png")

    def actualizar_efecto(self):
        self.efecto =f"Increases missile damage by {50 * (self.valor + 1)}%, sometimes when firing, you launch 3 missiles in a random direction"
    def aplicar_imp(self,jugador,bala,enemigo):
        from main import Bala,balas_sprites
        if bala.tipo == "misil":
            bala.daño *= 1 + (0.5*self.valor)
        angulo_rad = random.uniform(0, 2 * math.pi)
        for suerte in range(jugador.suerte):
            if random.random() <= 0.08:
                velocidad= 3
                for i in range(3):
                    angulo_rad += math.radians(10)
                    direccion = (math.cos(angulo_rad), math.sin(angulo_rad))
                    nueva_bala = Bala(30 * self.valor, velocidad,
                                      pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha(),
                                      jugador.base.rect.x, jugador.base.rect.y + 20, direccion,
                                      1,tipo="misil", eficiencia=0.1)
                    velocidad -=1
                    for mejora in jugador.mejoras:
                        if hasattr(mejora, 'aplicar_dis'):
                            mejora.aplicar_dis(jugador, nueva_bala)
                    balas_sprites.add(nueva_bala)
                break

Milicia=Milicia()
mejoras_legendarias.append(Milicia)

class Random(Mejora):
    def __init__(self):
        self.valor = 0
        self.misiles = 0
        super().__init__("Random", "Obtain a random effect", "Legendary", "Sprites\\Recursos\\Mejoras\\Random.png")

    def actualizar_efecto(self):
        self.efecto = "Obtain a random effect"
    def aplicar_primera(self,jugador):
        numero = random.random()
        if numero < 0.30:
            for mejora in jugador.mejoras.copy():
                if mejora in mejoras_normales:
                    while mejora in jugador.mejoras:
                        mejora_random = random.choice(mejoras_raras)
                        jugador.recolectar_mejora(mejora_random)
                        jugador.mejoras.remove(mejora)
        elif numero < 0.60:
            num = 0
            for mejora in jugador.mejoras.copy():
                if mejora in mejoras_raras:
                    while mejora in jugador.mejoras:
                        num += mejora.valor
                        mejora.valor=0
                        jugador.mejoras.remove(mejora)
            mejora_random = random.choice(mejoras_normales)
            num *=1.5
            for i in range(round(num)):
                jugador.recolectar_mejora(mejora_random)
        elif numero < 0.80:
            jugador.base.vida_maxima += 100
            jugador.base.calor_maximo +=100
            jugador.arma_primaria.daño += 4
            jugador.arma_secundaria.daño += 4
        elif numero < 0.99:
            print("Misiles")
            self.misiles +=1
        elif numero >= 0.99:
            jugador.arma_primaria.calentamiento =0
            jugador.arma_secundaria.calentamiento=0
            jugador.arma_secundaria.daño *=0.25
            jugador.arma_primaria.daño *=0.25
            jugador.arma_primaria.velocidad *=8
            jugador.arma_secundaria.velocidad *=8


    def aplicar_dis(self,jugador,arma):
        from main import balas_sprites
        if self.misiles >= 1:
            for bala in balas_sprites:
                if not bala.tipo:
                    bala.original_image = pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha()
                    bala.tipo = "misil"
                    bala.daño *= 1 + (0.2*self.misiles)
Random=Random()
mejoras_legendarias.append(Random)

class CriticoCongelante(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Freezing Critical", f"Critical hits reduce enemy speed. Increases damage by {50 * (self.valor + 1)}% against frozen enemies", "Legendary", "Sprites\\Recursos\\Mejoras\\Crit_cong.png")

    def actualizar_efecto(self):
        self.efecto = f"Critical hits reduce enemy speed. Increases damage by {50 * (self.valor + 1)}% against frozen enemies"
    def aplicar_imp(self, jugador, bala, enemigo):
        if enemigo.velocidad < enemigo.velocidad_base:
            bala.daño *= 1.5*self.valor
        if bala.critico:
           congelamiento(enemigo, 0.10*self.valor)


    def aplicar_primera(self,jugador,valor):
        jugador.arma_primaria.prob_critica +=0.2
        jugador.arma_secundaria.prob_critica +=0.2
CriticoCongelante=CriticoCongelante()
mejoras_legendarias.append(CriticoCongelante)

class CriticoMejorado(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Improved Critical", f"Bullets not from your weapons have a {50 * (self.valor + 1)}% chance of being critical based on your primary weapon's critical chance", "Legendary", "Sprites\\Recursos\\Mejoras\\Critico_mejorado.png")

    def actualizar_efecto(self):
        self.efecto =f"Bullets not from your weapons have a {50 * (self.valor + 1)}% chance of being critical based on your primary weapon's critical chance"
    def aplicar_primera(self,jugador):
        jugador.arma_primaria.prob_critica += 0.2
        jugador.arma_secundaria.prob_critica +=0.2
    def aplicar_imp(self,jugador,bala,enemigo):
        if bala.prob_critica == 0 and not bala.critico:
            bala.prob_critica += jugador.arma_primaria.prob_critica * (0.5 * self.valor)
            critico(bala,jugador)

CriticoMejorado=CriticoMejorado()
mejoras_legendarias.append(CriticoMejorado)

class Expansion(Mejora):
    def __init__(self):
        super().__init__("Expansion",f"Gain a planet",
                    "Rare", "Sprites\\Recursos\\Mejoras\\Expansion.png")
    def aplicar_primera(self,jugador):
        agregar_planeta(jugador)
Expansion=Expansion()
class CentroUniverso(Mejora):
    def __init__(self):
        self.valor = 0
        self.aumento=0.50
        super().__init__("Center of the universe", f"Orbitals are {50 * (self.valor + 1)}% bigger and deal {50 * (self.valor + 1)}% more damage, gain a planet", "Legendary", "Sprites\\Recursos\\Mejoras\\Universe.png")

    def actualizar_efecto(self):
        self.efecto =f"Orbitals are {50 * (self.valor + 1)}% bigger and deal {50 * (self.valor + 1)}% more damage, gain a planet"
        self.aumento= 0.50 * self.valor

    def aplicar_primera(self,jugador):
        agregar_planeta(jugador)
        if not Expansion in mejoras_raras:
            mejoras_raras.append(Expansion)

    def aplicar(self,jugador):
        actualizar_orbital(jugador,"Orbital Planeta")
        from main import balas_sprites
        for bala in balas_sprites:
            if "Orbital" in str(bala.tipo):
                nuevo_tamaño = (int(bala.tamaño_base[0] * (1+self.aumento)), int(bala.tamaño_base[0] * (1+self.aumento)))
                sprite_redimensionado = pygame.transform.scale(bala.original_image, nuevo_tamaño)
                bala.actual_image=sprite_redimensionado
                bala.daño = bala.daño_base * (1+(self.valor/2))

CentroUniverso=CentroUniverso()
mejoras_legendarias.append(CentroUniverso)

class Explosivos(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Hidden Explosives", f"Bullets explote, dealing {30 * (self.valor + 1)}% damage to nearby enemies", "Legendary", "Sprites\\Recursos\\Mejoras\\Universe.png")

    def actualizar_efecto(self):
        self.efecto =f"Bullets explote, dealing {30 * (self.valor + 1)}% damage to nearby enemies"

    def aplicar_imp(self, jugador, bala, enemigo):
        # Daño adicional de la explosión
        from main import enemigos_sprites,animaciones
        from Enemigos import Animacion
        daño_explosion = 2 + (bala.daño * (0.30 * self.valor))

        # Radio de la explosión
        radio_explosion = (daño_explosion * 5) + 100

        for enemigo_cercano in enemigos_sprites:
            if enemigo_cercano != enemigo and self.distancia(enemigo.rect.center,
                                                             enemigo_cercano.rect.center) <= radio_explosion:
                enemigo_cercano.danio(daño_explosion,(163, 33, 16, 64))
        anima=[
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom1.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom2.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom3.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom4.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom5.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom6.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom7.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom8.png")
        ]
        anima_redimensionada = [pygame.transform.scale(imagen, (radio_explosion, radio_explosion)) for imagen in anima]
        animacion=Animacion(enemigo.rect.center,anima_redimensionada,False, duracion_frame=25)
        animaciones.add(animacion)
    def distancia(self, punto1, punto2):
        return math.sqrt((punto1[0] - punto2[0]) ** 2 + (punto1[1] - punto2[1]) ** 2)
Explosivos=Explosivos()
mejoras_legendarias.append(Explosivos)

print(len(mejoras_normales))
print(len(mejoras_raras))
print(len(mejoras_legendarias))