import pygame
from moviepy.editor import VideoFileClip
from PIL import Image

def main():
    # Inicializar Pygame
    pygame.init()

    # Definir dimensiones de la pantalla
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paso de nivel")

    # Cargar el GIF animado usando moviepy
    gif_path = "Animations/map1.gif"  # Ruta del archivo GIF
    clip = VideoFileClip(gif_path)

    # Loop de reproducción
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener el fotograma actual del GIF
        current_frame = clip.get_frame(pygame.time.get_ticks() / 1000)

        # Convertir el fotograma de numpy.ndarray a una imagen de PIL
        pil_image = Image.fromarray(current_frame)

        # Convertir la imagen de PIL a una superficie de Pygame
        frame_surface = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

        # Escalar el fotograma al tamaño de la pantalla
        frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Limpiar pantalla
        screen.fill((255, 255, 255))

        # Mostrar el fotograma en la pantalla
        screen.blit(frame_surface, (0, 0))

        # Actualizar la pantalla
        pygame.display.flip()

    # Salir de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
