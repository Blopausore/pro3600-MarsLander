##
#%%  



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

from gui.gui_abstract import GuiAbstract
from gui.utils.constants import (
    WINDOW_HEIGHT, WINDOW_WIDTH, FRAMES_PER_SECOND,
    WHITE, BLACK, BLUE, RED, GREEN, LANDERS_PATH,
    MENUE_WINDOW_HEIGHT, MENUE_WINDOW_WIDTH)
from gui.log import manual_gui_log, trajectory_gui_log

fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)

lander_image_path = os.path.join(LANDERS_PATH, 'lander_0.png')

UNSUCCESFUL_TRAJCTORY_LINE_WIDTH = 3
SUCCESFUL_TRAJCTORY_LINE_WIDTH = 5

class Gui(GuiAbstract):
    # def draw_lander(self, lander: Lander):
    #     rotated_image = pygame.transform.rotate(self.lander_image, lander.rotate)
    #     new_rect = rotated_image.get_rect(center = self.lander_image.get_rect(center = (lander.x, lander.y)).center)
        
    #     self.display.blit(rotated_image, new_rect)

    # def draw_lander(self, lander: Lander):
    #     rotated_image = pygame.transform.rotate(self.lander_image, lander.rotate)
    #     new_rect = rotated_image.get_rect(center=self.lander_image.get_rect(center=(lander.x, lander.y)).center)

    #     surface = pygame.Surface((15 * 2, 15 * 2), pygame.SRCALPHA)
    #     surface.blit(rotated_image, new_rect)

    #     self.display.blit(surface, (lander.x - 15, lander.y - 15))

    def draw_lander(self, lander):
        """Draw the spaceship. It is represented here by a circle"""
        pygame.draw.circle(self.display, WHITE, (fx(int(lander.x)), fy(int(lander.y))), 15)
        

    def write_parameters(self, lander: Lander):
        """Draw the states of the lander"""
        self.display_text(
            "Parameters : ",
            (80, 100)
        )
        self.display_text(
            "Coordonates : ({}, {})".format(int(lander.x), int(lander.y)),
            (100, 130)
        )
        self.display_text(
            "Velocity : ({}, {})".format(int(lander.v_speed), int(lander.h_speed)),
            (100, 160)
        )
        self.display_text(
            "Power, angle : {}, {}".format(lander.power, lander.rotate),
            (100, 190)
        )
        self.display_text(
            "Fuel : {}".format(lander.fuel),
            (100, 220)
        )
        
    def step(self, dt=1):    
        """Compute an environment step"""    
        action = self.solution.use(environment = self.environment)
        done = self.environment.step(action, dt) or action.end
        lander_position = (fx(self.environment.lander.x), fy(self.environment.lander.y))
        self.trajectory.append(lander_position)
        #pygame.transform.rotate(self.lander_image,self.rotate)
        # pygame.draw.line(self.display, WHITE, lander_position, lander_position)
        if done :
            if self.environment.successful_landing():
                self.env_iterator -=1
                self.render_reset()
                color = GREEN
                width_ = SUCCESFUL_TRAJCTORY_LINE_WIDTH

            else:
                color = BLUE
                width_ = UNSUCCESFUL_TRAJCTORY_LINE_WIDTH
            start_point = self.trajectory[0]
            for end_point in self.trajectory[1:]:
                pygame.draw.line(
                    self.display, 
                    color, 
                    start_point,
                    end_point,
                    width=width_
                )
                start_point = end_point
            
        return done
    
      
    def pygame_step(self, done):
        """Compute the pygame step"""
        self.write_parameters(self.environment.lander)
        self.draw_lander(self.environment.lander)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if done:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        done = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return self.exit()()

        pygame.display.flip()
        self.render_reset()
        return done

    def run(self):
        """Run the simulation"""
        done = False
        self.reset()
        self.render_reset()
        while not done:
            done = self.step(1/FRAMES_PER_SECOND)
            self.pygame_step(done)
            time.sleep(1/FRAMES_PER_SECOND)
        
        while True:
            time.sleep(1/FRAMES_PER_SECOND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    return self.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.run()

