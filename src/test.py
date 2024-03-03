import unittest
from population import Voters, Voters_net

class TestVoters(unittest.TestCase):

    def test_voters_net(self):
        voters = Voters(10, 0.5)
        voters_net = Voters_net(voters, 2, 0.1)
        self.assertEqual(voters_net.lobby_consensus(0), None)
        self.assertEqual(voters_net.is_opinion_changed(0, 1), False)

if __name__ == "__main__":
    unittest.main()