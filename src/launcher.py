import json
import os
import sys
import cProfile
from environment.environment import Environment
from environment.surface import Surface
from utils.utils import load_map

from gui.menue import menue
from gui.gui_sr import Gui
from gui.gui_trajectory import GuiTrajectory

from solutions.examples.solution_fall import SolutionFall
from solutions.genetic.genetic_solution import GeneticSolution
from solutions.manual.manual_solution import ManualSolution

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MAP_PATH = "./data/maps/"
map_list = []
for map_json_name in os.listdir(MAP_PATH):
    map_path = os.path.join(MAP_PATH, map_json_name)
    with open(map_path, "r") as json_file:
        map_dict = json.load(json_file)
        map_list.append(map_dict)


def main():
    """main function
    Launch menue, simulation, ... 
    """
    if sys.argv[1] in {"-v", "--verbose"}:
        print("Verbose mode")
        verbose = True
    else:
        verbose = False

    if verbose:
        print("Map list : ", map_list)

    map, solution = menue(map_list, verbose=verbose)

    points, initial_state = map.get('points'), map.get('lander_state')
    surface = Surface(points)   
    environment = Environment(surface, initial_state)

    if solution == "Manual":
        solution_algorithm = ManualSolution()
        gui = Gui(environment, solution_algorithm)
    else:
        solution_algorithm = GeneticSolution(environment)
        gui = GuiTrajectory(environment, solution_algorithm)
    gui.run()

if __name__ == "__main__":
    cp = cProfile.Profile()
    cp.enable()
    main()
    cp.disable()
    cp.print_stats(sort='cumulative')
    cp.dump_stats('profile.cprof')
