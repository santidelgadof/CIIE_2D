import pygame

# Draws the belt of each level
def drawBelt(WINDOW, theme, level, organicContainer, plasticContainer, paperContainer, glassContainer, firstClasificator, secondClasificator):
        pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(350, -3, 100, 703), width=1)
        pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, 0, 1, 700), width=1)
        pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(370, 0, 1, 700), width=1)
        # Level 1
        if level == 1:
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position, 321, 100), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position + 20, 341, 1), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position + 80, 341, 1), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(449, firstClasificator.y_position, plasticContainer.get_x_position() - 349, 100), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, firstClasificator.y_position + 20, plasticContainer.get_x_position() - 330, 1), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, firstClasificator.y_position + 80, plasticContainer.get_x_position() - 330, 1), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position + 99, 100, ( organicContainer.get_y_position() - firstClasificator.y_position - 99)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position() + 20, firstClasificator.y_position + 80, 1, ( organicContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position() + 80, firstClasificator.y_position + 80, 1, ( organicContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(plasticContainer.get_x_position(), firstClasificator.y_position + 99,  100,  ( plasticContainer.get_y_position() - firstClasificator.y_position - 99)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(plasticContainer.get_x_position() + 20, firstClasificator.y_position + 80,  1,  ( plasticContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(plasticContainer.get_x_position() + 80, firstClasificator.y_position + 80,  1,  ( plasticContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)
        # Level 2
        if level == 2 or level == 3:
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position, 321, 100), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position + 20, 341, 1), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position + 80, 341, 1), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(449, firstClasificator.y_position, plasticContainer.get_x_position() - 349, 100), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, firstClasificator.y_position + 20, plasticContainer.get_x_position() - 330, 1), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, firstClasificator.y_position + 80, plasticContainer.get_x_position() - 330, 1), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(paperContainer.get_x_position(), secondClasificator.y_position, 181, 100), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(paperContainer.get_x_position(), secondClasificator.y_position + 20, 201, 1), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(paperContainer.get_x_position(), secondClasificator.y_position + 80, 201, 1), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(449, secondClasificator.y_position, glassContainer.get_x_position() - 349, 100), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, secondClasificator.y_position + 20, glassContainer.get_x_position() - 330, 1), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(430, secondClasificator.y_position + 80, glassContainer.get_x_position() - 330, 1), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position(), firstClasificator.y_position + 99, 100, ( organicContainer.get_y_position() - firstClasificator.y_position - 99)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position() + 20, firstClasificator.y_position + 80, 1, ( organicContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(organicContainer.get_x_position() + 80, firstClasificator.y_position + 80, 1, ( organicContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(plasticContainer.get_x_position(), firstClasificator.y_position + 99,  100,  ( plasticContainer.get_y_position() - firstClasificator.y_position - 99)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(plasticContainer.get_x_position() + 20, firstClasificator.y_position + 80,  1,  ( plasticContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(plasticContainer.get_x_position() + 80, firstClasificator.y_position + 80,  1,  ( plasticContainer.get_y_position() - firstClasificator.y_position - 80)), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(paperContainer.get_x_position(), secondClasificator.y_position + 99, 100, ( paperContainer.get_y_position() - secondClasificator.y_position - 99)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(paperContainer.get_x_position() + 20, secondClasificator.y_position + 80, 1, ( paperContainer.get_y_position() - secondClasificator.y_position - 80)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(paperContainer.get_x_position() + 80, secondClasificator.y_position + 80, 1, ( paperContainer.get_y_position() - secondClasificator.y_position - 80)), width=1)

            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(glassContainer.get_x_position(), secondClasificator.y_position + 99,  100,  ( glassContainer.get_y_position() - secondClasificator.y_position - 99)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(glassContainer.get_x_position() + 20, secondClasificator.y_position + 80,  1,  ( glassContainer.get_y_position() - secondClasificator.y_position - 80)), width=1)
            pygame.draw.rect(WINDOW, theme.beltColor, pygame.Rect(glassContainer.get_x_position() + 80, secondClasificator.y_position + 80,  1,  ( glassContainer.get_y_position() - secondClasificator.y_position - 80)), width=1)