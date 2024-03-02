import numpy as np


class Voters:
    def __init__(self, size: int, initial_c: float):
        self.voters = np.ones(size)
        rng = np.random.default_rng()
        random_indexes = rng.choice(
                    size, 
                    size = int(size * initial_c), 
                    replace = False) # Replace flag makes all numbers unique
        self.voters[random_indexes] = -1
        self.update_c()

    def get_size(self):
        return len(self.voters)

    def get_values(self, indexes):
        return self.voters[indexes]

    def update_c(self):
        self.c = self.voters[self.voters == 1].sum() / self.get_size()

    def get_c(self):
        self.update_c()
        return self.c

    def try_to_change_opinion_of(self, 
        index: int, 
        voters_net):
        if (voters_net.is_opinion_changed(index, self.voters[index])):
            self.voters[index] *= (-1)
            #print(str(index) + " was changed")

    def __str__(self):
        return "Voters: % s, c: % s" % (self.voters, self.get_c())


class Voters_net:
    def __init__(self, voters, q: int, p: float, connection_type: str = "all connected"):
        self.voters = voters
        self.q = q
        self.p = p
        size = voters.get_size()

        if connection_type == "all connected":
            self.network = np.ones([size, size], dtype=bool)
            for i in range(size):
                self.network[i,i] = None

    def lobby_consensus(self, voters_index: int):
        rng = np.random.default_rng()
        connections = np.arange(self.voters.get_size())[self.network[voters_index]]
        random_indexes = rng.choice(
                    connections, 
                    size = self.q, 
                    replace = False)
        lobby = self.voters.get_values(random_indexes)
        if np.all(lobby == 1):
            #print("In favor: " + str(lobby))
            return 1
        elif np.all(lobby == -1):
            #print("In against: " + str(lobby))
            return -1
        else:
            return None

    def is_opinion_changed(self, voters_index: int ,voters_opinion: int):
        #print("voters_opinion: " + str(voters_opinion))
        lobby_consensus = self.lobby_consensus(voters_index)
        result = False
        if np.random.random_sample() < self.p:
            if np.random.random_sample() < 0.5: # p/2 propability of fliping
                #print("Noise")
                result = True
        else: # 1-p propability of looking for consenus
            match voters_opinion:
                case -1:
                    if lobby_consensus == 1:
                        if np.random.random_sample() < (1 - self.p):
                            result = True
                case 1:
                    if lobby_consensus == -1:
                        if np.random.random_sample() < (1 - self.p):
                            result = True

        return result
            

    def __str__(self):
        output = str(self.voters)
        output += "\nNetwork:\n" + str(1*self.network)
        return(output)
