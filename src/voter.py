import numpy as np
from population import Voters, Voters_net 
from progressbar import progressbar
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

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
        #print(self.network)

    def run_simulation(self) -> None:
        """
        Runs the voter model simulation
        """
        print(f"Running simulation with N={self.N}, q={self.q}, p={self.p}, M={self.M}")

        c_values = np.zeros(self.M)
        voters_evolution = np.zeros((self.M, self.N))

        for step in range(self.M): #progressbar(range(self.M), redirect_stdout=True):
            rng = np.random.default_rng()
            random_indexes = rng.choice(
                self.N, 
                size = self.N , 
                replace = True)
            for i in random_indexes:
                self.voters.try_to_change_opinion_of(i, self.network)
                #print(self.voters)
            
            c_values[step] = self.voters.get_c()
            voters_evolution[step] = self.voters.voters

        self.c_values = c_values
        self.voters_evolution = voters_evolution

    def draw_concentration(self) -> None:
        """
        Draws the concentration over time
        """
        plt.plot(self.c_values)
        plt.xlabel("Monte Carlo steps")
        plt.ylabel("Concentration")
        plt.title(f"Concentration over time (N={self.N}, q={self.q}, p={self.p}, M={self.M})")
        plt.savefig('results/concentration{}{}.png'.format(self.q, self.p))

    def get_final_concentration(self) -> float:
        """
        Returns the final concentration
        """
        return self.c_values[-1]
    
    def animate_voters_evolution(self) -> None:
        """
        Animates the evolution of voters
        """
        G = nx.Graph()
        G.add_nodes_from(np.arange(self.N))
        network = self.network.network
        edges = np.argwhere(network)
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots()
        ax.set_axis_off()

        def update(num, pos, G, ax):
            ax.clear()
            node_colors = self.voters_evolution[num]
            nx.draw(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.coolwarm, ax=ax)
            ax.set_title('Framed {}'.format(num))

        ani = animation.FuncAnimation(fig, update, frames=self.M, interval=1000, fargs=(pos, G, ax))
        ani.save('results/voter_model.gif')
        
