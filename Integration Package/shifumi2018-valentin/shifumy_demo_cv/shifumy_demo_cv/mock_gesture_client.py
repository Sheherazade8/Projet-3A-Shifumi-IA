# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

import time
import random


from shifumy_player.base import \
    str_rps
from shifumy_player.players.random_player import RandomPlayer

from shifumy_reco.gesture_recognition_client import \
    AbstractGestureRecognitionClient


class MockGestureRecognitionThread(AbstractGestureRecognitionClient):
    def __init__(self, host='0.0.0.0', port=50000):
        AbstractGestureRecognitionClient.__init__(self, host=host, port=port)
        self.mock_player = RandomPlayer()

    def get_gesture(self):
        g = self.mock_player.predict_agent_gesture()
        t = random.randint(200, 1000) / 1000
        print('Wait {}ms before sending {}'.format(t, str_rps(g)))
        time.sleep(t)
        print('Send gesture!')
        return g

    def get_eog(self):
        t = random.randint(200, 1000) / 1000
        print('Wait {}ms before ending gesture'.format(t))
        time.sleep(t)
        print('End gesture!')



if __name__ == '__main__':
    c = MockGestureRecognitionThread()
    c.start()
    c.join()