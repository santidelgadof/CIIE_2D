import pygame
import sys
from gui import Button

def inicializar_juego():
    pygame.init()
    return pygame.display.set_mode((800, 800)), pygame.time.Clock()

def cargar_fondo():
    return pygame.image.load("Animacion.jpg").convert()

def play_music():
    pygame.mixer.music.load("pantalla_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

def dibujar_rectangulo_redondeado(pantalla):
    x = 200  # Posición x del rectángulo (ajusta según sea necesario)
    y = 355  # Posición y del rectángulo (ajusta según sea necesario)
    ancho = 400  # Ancho del rectángulo
    alto = 200  # Alto del rectángulo
    radio = 50  # Radio de las esquinas redondeadas
    color = (218, 255, 252)  # Color del rectángulo (rojo en este caso)
    pygame.draw.rect(pantalla, color, (x + radio, y, ancho - 2 * radio, alto))
    pygame.draw.rect(pantalla, color, (x, y + radio, ancho, alto - 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x, y, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x + ancho - 2 * radio, y, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x, y + alto - 2 * radio, 2 * radio, 2 * radio))
    pygame.draw.ellipse(pantalla, color, (x + ancho - 2 * radio, y + alto - 2 * radio, 2 * radio, 2 * radio))

def main():
    pantalla, reloj = inicializar_juego()
    fondo = cargar_fondo()
    x, y = 0, 0

    play_music()
    boton1 = Button(300, 375, "JUGAR")  # Crear instancia de Button
    boton2 = Button(300, 475, "CREDITOS")  # Crear instancia de Button

    tiempo_transcurrido = 0
    tiempo_aparicion_botones = 2000  # Tiempo en milisegundos (2 segundos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton1.top_rect.collidepoint(event.pos):
                    print("Ruta 1")
                    # Agrega aquí la lógica para redirigir al jugador a la Ruta 1
                elif boton2.top_rect.collidepoint(event.pos):
                    print("Ruta 2")
                    # Agrega aquí la lógica para redirigir al jugador a la Ruta 2

        x_relativa = x % fondo.get_rect().height
        pantalla.blit(fondo, (x_relativa - fondo.get_rect().height, y))
        if x_relativa < 800:
            pantalla.blit(fondo, (x_relativa, 0))
        x += 1

        tiempo_transcurrido += reloj.get_time()

        if tiempo_transcurrido >= tiempo_aparicion_botones:
            dibujar_rectangulo_redondeado(pantalla)  # Dibujar el rectángulo redondeado
            boton1.update()  # Actualizar el estado del botón
            boton2.update()  # Actualizar el estado del botón
            boton1.draw(pantalla)  # Dibujar el botón en la pantalla
            boton2.draw(pantalla)  # Dibujar el botón en la pantalla

        pygame.display.update()
        reloj.tick(60)

if __name__ == "__main__":
    main()
