from abc import ABC, abstractmethod
import pygame
import os
import sys
import time

from environment.environment import Environment
from environment.surface import Surface
from environment.entities.lander import Lander
from environment.utils.constants import X_SCALE, Y_SCALE

from solutions.abstract_solution import AbstractSolution
from solutions.manual.manual_solution import ManualSolution 
from solutions.genetic.genetic_solution import GeneticSolution

from utils.point import Point
from utils.segment import Segment

from gui.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FRAMES_PER_SECOND, WHITE, BLACK, BLUE, RED, GREEN, LANDERS_PATH
from gui.log import manual_gui_log, trajectory_gui_log

fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)

lander_image_path = os.path.join(LANDERS_PATH, 'lander_0.png')

LINE_WIDTH = 3

class GuiAbstract(ABC):

    def __init__(self, environment: Environment, solution : AbstractSolution):
        """Graphic User Interface
        Manage the graphics of the simulation
        
        Fields :
            * environment : Environment
            * solution : Solution
            * display : pygame.display
            * font : pygame.Font
        
        """
        self.environment = environment
        self.solution = solution
        self.env_iterator = 0
        if isinstance(solution, ManualSolution):
            print(manual_gui_log, file=sys.stderr)
        elif isinstance(solution, GeneticSolution):
            print(trajectory_gui_log, file=sys.stderr)
        # PYGAME INITIALIZER
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.lander_image = pygame.image.load(lander_image_path)

    def screen_reset(self):
        """Draw the environment"""
        self.display.fill(BLACK)
        self.draw_surface()
        
    def reset(self):
        """Reset all the environments"""
        self.environment.reset()
        self.trajectory = []

    def display_text(self, text, position):
        """Draw text on the screen at the position position."""
        id_text = self.font.render(text, True, (255, 255, 255))
        self.display.blit(id_text, position)

    def render_reset(self):  
        """Reset the render"""
        self.env_iterator +=1
        self.screen_reset()

    def draw_surface(self):
        """Draw all the segments that composed the surface"""
        surface : Surface= self.environment.surface
        for line in surface.lands:
            pygame.draw.line(
                self.display, 
                RED, 
                [fx(line.point_a.x), fy(line.point_a.y)],
                [fx(line.point_b.x), fy(line.point_b.y)],
                width=LINE_WIDTH
            )

    def exit(self):
        """Exit the simulation"""
        pygame.quit()
        return True
        

    @abstractmethod
    def write_parameters(self, lander: Lander):
        """Draw the states of the lander"""
        ...

    @abstractmethod
    def step(self, dt=1):    
        """Compute an environment step"""    
        ...
      
    @abstractmethod
    def pygame_step(self, success):
        """Compute the pygame step"""
        ...

    @abstractmethod
    def run(self):
        """Run the simulation"""
        ...
