

# %%
import pygame
import sys

import os
import json

from gui.utils.constants import (
    WHITE, BLACK, RED, GREEN,
    MENUE_WIDTH, CHOICE_HEIGHT,
    SOLUTION_X, MAP_X, RUN_X, RUN_Y, RUN_WIDTH, RUN_HEIGHT,
    MENUE_WINDOW_WIDTH, MENUE_WINDOW_HEIGHT
)


# Initialisation de Pygame
pygame.init()

# Police
pygame.font.init()
font = pygame.font.SysFont(None, 30)



# Solutions menue

sol_selected = 0  # Élément sélectionné par défaut


# Maps menue

map_selected = 0  # Élément sélectionné par défaut




def menue(map_list, verbose=False):
    """
    Display the menue and return the selected solution and map
    """
    if verbose: print("Displaying menue : start")
    sol_selected = 0  
    map_selected = 0
    pygame.init()
    # Créer la fenêtre
    fenetre = pygame.display.set_mode((MENUE_WINDOW_WIDTH, MENUE_WINDOW_HEIGHT))
    pygame.display.set_caption("Mars Lander")
    if verbose: print("Displaying menue : pygame window created")
    def menue_display(solutions, maps):
        fenetre.fill(WHITE)

        # Afficher les éléments du menu
        for i, element in enumerate(solutions):
            texte = font.render(element, True, BLACK if i != sol_selected else RED)
            y = CHOICE_HEIGHT + i * CHOICE_HEIGHT
            fenetre.blit(texte, (SOLUTION_X, y))

        # Afficher les éléments du menu
        for i, element in enumerate(maps):
            texte = font.render(element, True, BLACK if i != map_selected else RED)
            y = CHOICE_HEIGHT + i * CHOICE_HEIGHT
            fenetre.blit(texte, (MAP_X, y))

        pygame.draw.rect(fenetre, GREEN, (RUN_X, RUN_Y, RUN_WIDTH, RUN_HEIGHT))
        texte_run = font.render("Run", True, WHITE)
        fenetre.blit(texte_run, (RUN_X+10, RUN_Y + RUN_HEIGHT//2))

        pygame.display.flip()

    solutions = ["Manual", "Genetic"]
    maps = list(map(lambda m: m['name'], map_list))
    # Boucle principale du programme
    if verbose: print("Displaying menue : main loop")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche de la souris
                    if 350 <= event.pos[0] <= 450 :
                        print(f"Run MarsLander on map {maps[map_selected]} by {solutions[sol_selected]}")
                        if verbose: 
                            print("Displaying menue : end")
                        pygame.quit()

                        return map_list[map_selected], solutions[sol_selected]
                    else:
                        # Vérifier quel élément a été sélectionné
                        x_mouse, y_mouse = event.pos
                        if 50<= x_mouse <= 150:
                            sol_selected = (y_mouse - 50) // 50
                        elif 200<= x_mouse <=300:
                            map_selected = (y_mouse - 50) // 50



        menue_display(solutions, maps)

if __name__ == "__main__":
    menue()

# %%
