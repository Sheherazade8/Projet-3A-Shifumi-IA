import sys
print(sys.path)

import unittest
from shifumy_player.base import Round, ROCK, PAPER, SCISSORS
from shifumy_player.players.random_player import RandomPlayer



class TestRandomPlayer(unittest.TestCase):
    def test_predict(self):
        p = RandomPlayer()
        for i in range(100):
            self.assertIn(p.predict_agent_gesture(), {ROCK, PAPER, SCISSORS})

    def test_load(self):
        with self.assertRaises(AssertionError):
            p = RandomPlayer.load('file.py')
        p = RandomPlayer.load(None)
        self.assertIsInstance(p, RandomPlayer)


if __name__ == '__main__':
    unittest.main()
