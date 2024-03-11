import pygame
from ResourceManager import ResourceManager

resource_manager = ResourceManager()

def main():
    # Initialize Pygame
    pygame.init()

    # Define screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level transition")

    # Load a list of images
    image_surfaces = [
        pygame.transform.scale(resource_manager.A5.get(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(resource_manager.A6.get(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(resource_manager.A7.get(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(resource_manager.A8.get(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    ]
    num_images = len(image_surfaces)
    current_image_index = 0

    # Display each image once
    while current_image_index < num_images:
        # Get the current image
        current_image_surface = image_surfaces[current_image_index]

        # Clear the screen
        screen.fill((255, 255, 255))

        # Display the current image on the screen
        screen.blit(current_image_surface, (0, 0))

        # Update the screen
        pygame.display.flip()

        # Wait for a moment between each image (500 ms)
        pygame.time.delay(500)

        # Switch to the next image
        current_image_index += 1

    # Quit Pygame
    return True

if __name__ == "__main__":
    main()
