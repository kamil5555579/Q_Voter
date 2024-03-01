import numpy as np

class VoterModel():
    def __init__(self, N: int, q: int, p: float, M: int) -> None:
        """
        Initializes a voter model object
        :param N: Number of voters
        :param q: Size of lobby
        :param p: Probability of independent voting
        :param M: Number of Monte Carlo steps
        """
        self.N = N
        self.q = q
        self.p = p
        self.M = M

    def run_simulation(self) -> None:
        """
        Runs the voter model simulation
        """
        print(f"Running simulation with N={self.N}, q={self.q}, p={self.p}, M={self.M}")



