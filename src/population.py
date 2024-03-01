import numpy as np


class Voters:
    def __init__(self, size):
        self.voters = np.zeros(size, dtype=bool)
        rng = np.random.default_rng()
        random_indexes = rng.choice(
                    size, 
                    size = int(size/2), 
                    replace = False) # Replace flag makes all numbers unique
        self.voters[random_indexes] = 1

    def get_size(self):
        return len(self.voters)

    def get_values(self, indexes):
        return self.voters[indexes]

    def __str__(self):
        return "Voters: % s\n" % (1*self.voters)


class Voters_net:
    def __init__(self, voters, connection_type = "all connected"):
        self.voters = voters
        size = voters.get_size()

        if connection_type == "all connected":
            self.network = np.ones([size, size], dtype=bool)
            for i in range(size):
                self.network[i,i] = None

    def lobby_consensus(self, q):
        rng = np.random.default_rng()
        random_indexes = rng.choice(
                    self.voters.get_size(), 
                    size = q, 
                    replace = False)
        lobby = self.voters.get_values(random_indexes)
        if lobby.all():
            print("In favor: " + str(lobby))
            return True
        elif (~lobby).all():
            print("In against: " + str(lobby))
            return False
        else:
            return None

    def __str__(self):
        output = str(self.voters)
        output += "Network:\n" + str(1*self.network)
        return(output)

# Main tmp

voters1 = Voters(10)
net1 = Voters_net(voters1)
for _ in range(10):
    net1.lobby_consensus(3)
print(net1)