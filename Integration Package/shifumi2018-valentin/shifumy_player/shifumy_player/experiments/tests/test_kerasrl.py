import unittest

from shifumy_player.experiments.kearsrl_vs_agent \
    import game_to_obs, obs_to_game, gesture_to_action, action_to_gesture
from shifumy_player.base import Round, ROCK, PAPER, SCISSORS


class TestConversions(unittest.TestCase):
    def test_gesture_to_action(self):
        self.assertEqual(gesture_to_action(ROCK), 0)
        self.assertEqual(gesture_to_action(PAPER), 1)
        self.assertEqual(gesture_to_action(SCISSORS), 2)

    def test_action_to_gesture(self):
        self.assertEqual(action_to_gesture(0), ROCK)
        self.assertEqual(action_to_gesture(1), PAPER)
        self.assertEqual(action_to_gesture(2), SCISSORS)

    def test_obs_to_game_to_obs(self):
        for feature_size in range(1, 5):
            obs_list = []
            for obs in range(9**feature_size):
                game = obs_to_game(obs, feature_size=feature_size)
                obs_list.append(game_to_obs(game))
                self.assertEqual(obs, obs_list[-1])
            self.assertSetEqual(set(obs_list), set(range(9**feature_size)))



if __name__ == '__main__':
    unittest.main()
