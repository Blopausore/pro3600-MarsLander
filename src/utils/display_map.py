##
#%%
import pygame
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.utils.constants import X_SCALE, Y_SCALE
from environment.surface import Surface
from gui.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FRAMES_PER_SECOND, WHITE, BLACK, BLUE, RED, GREEN, LANDERS_PATH

fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)

RED = (255, 0, 0)
LANDERS_PATH = 'data/lander'
print(os.listdir("."))
MAP_PATH = "./data/maps/"
map_list = []
for map_json_name in os.listdir(MAP_PATH):
    map_path = os.path.join(MAP_PATH, map_json_name)
    with open(map_path, "r") as json_file:
        map_dict = json.load(json_file)
        map_list.append(map_dict)

def draw_surface(surface : Surface, display : pygame.display):
    """Draw all the segments that composed the surface"""
    for line in surface.lands:
        pygame.draw.line(
            display, 
            RED, 
            [fx(line.point_a.x), fy(line.point_a.y)],
            [fx(line.point_b.x), fy(line.point_b.y)],
            width=4
        )


map = map_list[1]

log = """
Display map
    - Press 's' to take a screenshot
    - Press 'q' to quit
"""

def main():
    pygame.init()
    
    points, initial_state = map.get('points'), map.get('lander_state')
    surface = Surface(points)   
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    pygame.image.save(display, "./data/images/screenshot_{}.jpeg".format(map.get('name')))        
        draw_surface(surface, display)
        pygame.display.update()
        pygame.time.Clock().tick(FRAMES_PER_SECOND)
    



if __name__ == "__main__":
    main()
# %%


