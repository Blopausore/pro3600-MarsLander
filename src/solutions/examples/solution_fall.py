from environment.action import Action
from solutions.abstract_solution import AbstractSolution

class SolutionFall(AbstractSolution):
    
    def get_parameters(self) -> dict:
        return {}
    
    def use(self, **kargs) -> Action:
        return Action(
            rotate=0,
            power=0
        )