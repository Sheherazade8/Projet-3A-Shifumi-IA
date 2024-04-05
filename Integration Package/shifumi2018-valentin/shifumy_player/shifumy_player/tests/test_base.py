import unittest
from ..base import ROCK, PAPER, SCISSORS, Round, RpsAgent


class TestRpsConstants(unittest.TestCase):
    def test_differences(self):
        self.assertNotEqual(ROCK, PAPER)
        self.assertNotEqual(PAPER, SCISSORS)
        self.assertNotEqual(SCISSORS, ROCK)


class TestRound(unittest.TestCase):
    def test_init(self):
        for go in {ROCK, PAPER, SCISSORS}:
            for ga in {ROCK, PAPER, SCISSORS}:
                # Correct initiatization
                r = Round(opponent=go, agent=ga)
                self.assertEqual(r.opponent, go)
                self.assertEqual(r.agent, ga)
                # Wrong initiatizations should raise an error
                with self.assertRaises(AssertionError):
                    Round(opponent=go, agent='rock')
                with self.assertRaises(AssertionError):
                    Round(opponent=go, agent=None)
                with self.assertRaises(AssertionError):
                    Round(opponent='paper', agent=ga)
                with self.assertRaises(AssertionError):
                    Round(opponent=None, agent=ga)

    def test_agent_gain(self):
        self.assertEqual(Round(opponent=ROCK, agent=ROCK).get_agent_gain(),
                         0)
        self.assertEqual(Round(opponent=ROCK, agent=PAPER).get_agent_gain(),
                         1)
        self.assertEqual(Round(opponent=ROCK, agent=SCISSORS).get_agent_gain(),
                         -1)
        self.assertEqual(Round(opponent=PAPER, agent=ROCK).get_agent_gain(),
                         -1)
        self.assertEqual(Round(opponent=PAPER, agent=PAPER).get_agent_gain(),
                         0)
        self.assertEqual(Round(opponent=PAPER, agent=SCISSORS).get_agent_gain(),
                         1)
        self.assertEqual(Round(opponent=SCISSORS, agent=ROCK).get_agent_gain(),
                         1)
        self.assertEqual(Round(opponent=SCISSORS, agent=PAPER).get_agent_gain(),
                         -1)
        self.assertEqual(Round(opponent=SCISSORS, agent=SCISSORS).get_agent_gain(),
                         0)

    def test_opponent_gain(self):
        for go in {ROCK, PAPER, SCISSORS}:
            for ga in {ROCK, PAPER, SCISSORS}:
                self.assertEqual(
                    Round(opponent=go, agent=ga).get_opponent_gain(),
                    Round(opponent=ga, agent=go).get_agent_gain())

class TestRpsAgent(unittest.TestCase):
    def test_record_and_reset(self):
        r0 = Round(opponent=ROCK, agent=ROCK)
        r1 = Round(opponent=ROCK, agent=PAPER)
        r2 = Round(opponent=SCISSORS, agent=SCISSORS)

        a = RpsAgent()
        self.assertIsInstance(a.game, list)
        self.assertEqual(len(a.game), 0)

        a.record(r0)
        self.assertIsInstance(a.game, list)
        self.assertEqual(len(a.game), 1)
        self.assertEqual(a.game[0], r0)

        a.record(r1)
        a.record(r2)
        self.assertIsInstance(a.game, list)
        self.assertEqual(len(a.game), 3)
        self.assertEqual(a.game[0], r0)
        self.assertEqual(a.game[1], r1)
        self.assertEqual(a.game[2], r2)

        a.reset_game()
        self.assertIsInstance(a.game, list)
        self.assertEqual(len(a.game), 0)

    def test_predict_not_implemented(self):
        a = RpsAgent()
        with self.assertRaises(NotImplementedError):
            a.predict_agent_gesture()

    def test_load(self):
        with self.assertRaises(NotImplementedError):
            RpsAgent.load()

if __name__ == '__main__':
    unittest.main()
