import numpy as np
from population import Voters, Voters_net 
from progressbar import progressbar


class VoterModel():
    def __init__(self, N: int, q: int, p: float, M: int, c: float) -> None:
        """
        Initializes a voter model object
        :param N: Number of voters
        :param q: Size of lobby
        :param p: Probability of independent voting
        :param M: Number of Monte Carlo steps
        :param c: Initial concentration of 1s
        """
        self.N = N
        self.q = q
        self.p = p
        self.M = M

        self.voters = Voters(N, c)
        self.network = Voters_net(self.voters, q, p)
        print(self.network)

    def run_simulation(self) -> None:
        """
        Runs the voter model simulation
        """
        print(f"Running simulation with N={self.N}, q={self.q}, p={self.p}, M={self.M}")
        for _ in range(self.M): #progressbar(range(self.M), redirect_stdout=True):
            rng = np.random.default_rng()
            random_indexes = rng.choice(
                self.N, 
                size = self.N , 
                replace = True)
            for i in random_indexes:
                self.voters.try_to_change_opinion_of(i, self.network)
                #print(self.voters)


test = VoterModel(10, 2, 0.1, 1, 0.5)
test.run_simulation()