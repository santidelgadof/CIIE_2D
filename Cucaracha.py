import pygame
import random
import sys

pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 200  # Tamaño de celda para la cuadrícula de agujeros
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE  # Número de filas y columnas para la cuadrícula
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa Cucarachas")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Cucaracha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cucaracha.png").convert_alpha()  # Cargar la imagen de la cucaracha
        self.image = pygame.transform.scale(self.image, (50, 50))  # Escalar la imagen si es necesario
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = 0

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time >= 1000:  # Desaparece después de un segundo
                self.active = False
                self.kill()  # Elimina el sprite del grupo

class Agujero(pygame.sprite.Sprite):
    def __init__(self, x, y, hole_image):
        super().__init__()
        self.image = hole_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass

# Crear matriz de agujeros
agujeros = pygame.sprite.Group()
hole_image = pygame.image.load("agujero.png").convert_alpha()  # Cargar la imagen del agujero
hole_image = pygame.transform.scale(hole_image, (CELL_SIZE - 10, CELL_SIZE - 10))  # Ajustar tamaño del agujero
for row in range(ROWS):
    for col in range(COLS):
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        agujero = Agujero(x, y, hole_image)
        agujeros.add(agujero)

# Grupo de cucarachas
cucarachas = pygame.sprite.Group()

# Cargar imagen del insecticida
ins_image = pygame.image.load("insecticida.png").convert_alpha()
ins_image = pygame.transform.scale(ins_image, (100, 100))  # Ajustar tamaño del insecticida

# Cargar imagen de fondo
background_image = pygame.image.load("back.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Variables para controlar el tiempo
spawn_timer = 0
next_spawn_time = random.randint(2000, 5000)  # Tiempo aleatorio hasta la próxima aparición de una cucaracha

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

score = 0  # Contador de puntos
cucarachas_mostradas = 0  # Contador de cucarachas mostradas

while running and cucarachas_mostradas < 11:
    window.blit(background_image, (0, 0))  # Dibujar fondo

    # Dibujar agujeros
    for agujero in agujeros:
        window.blit(agujero.image, agujero.rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica si el clic ocurrió dentro de la región de una cucaracha activa
            for cucaracha in cucarachas:
                if cucaracha.active and cucaracha.rect.collidepoint(event.pos):
                    score += 1  # Aumenta el contador de puntos
                    cucaracha.active = False  # Desactiva la cucaracha
                    cucaracha.kill()  # Elimina el sprite del grupo
                    # Mostrar animación de insecticida
                    cell_center = (cucaracha.rect.centerx // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2,
                                   cucaracha.rect.centery // CELL_SIZE * CELL_SIZE + CELL_SIZE // 2)
                    window.blit(ins_image, (cell_center[0] - ins_image.get_width() // 2,
                                                  cell_center[1] - ins_image.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.delay(300)  # Retraso para mostrar la animación del insecticida
                    break  # Sal del bucle una vez que se haya encontrado una cucaracha clickeada

    # Lógica del juego
    spawn_timer += clock.get_time()
    if spawn_timer >= next_spawn_time:
        spawn_timer = 0
        next_spawn_time = random.randint(2000, 5000)  # Establecer el tiempo aleatorio hasta la próxima aparición de una cucaracha
        random_hole = random.choice(agujeros.sprites())  # Elegir un agujero aleatorio para que aparezca la cucaracha
        cucaracha = Cucaracha()
        cucaracha.rect.center = random_hole.rect.center
        cucaracha.active = True
        cucaracha.spawn_time = pygame.time.get_ticks()  # Guardar el tiempo de aparición de la cucaracha
        cucarachas.add(cucaracha)  # Añadir la cucaracha al grupo de cucarachas
        cucarachas_mostradas += 1  # Incrementa el contador de cucarachas mostradas

    # Actualizar y dibujar cucarachas
    cucarachas.update()
    cucarachas.draw(window)

    pygame.display.flip()
    clock.tick(60)

# Mostrar la puntuación final
window.fill(WHITE)
font = pygame.font.Font(None, 36)
final_score_text = font.render("Puntuación final: " + str(score), True, BLACK)
text_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
window.blit(final_score_text, text_rect.topleft)
pygame.display.flip()

# Esperar un momento antes de salir del juego
pygame.time.delay(3000)

pygame.quit()
sys.exit()
