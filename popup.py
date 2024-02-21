import pygame
import sys


# Pantalla
ANCHO, ALTO = 800, 800
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
FPS = 60
RELOJ = pygame.time.Clock()

# Fondo del juego
fondo = pygame.image.load("ejemplo.jpg").convert()
x = 0
y = 0
PANTALLA.blit(fondo, (y, x))


# Bucle de juego.
while True:
	# Cerrar Juego
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	# Movimiento del fondo
	y_relativa = y % fondo.get_rect().height
	PANTALLA.blit(fondo, (y_relativa - fondo.get_rect().height, x ))
	if y_relativa < ALTO:
		PANTALLA.blit(fondo, (y_relativa, 0))
	y += 1
	# Control de FPS
	RELOJ.tick(FPS)
	# Actualización de la ventana
	pygame.display.update()