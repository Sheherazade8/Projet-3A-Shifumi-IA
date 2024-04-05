# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

from ...base import RpsAgent
from ..random_player import RandomPlayer
from ..pst_player.module.Node import Node, NodeNS


class OnlinePstAgent(RpsAgent):
    """ A prediction suffix tree agent that learns online from scratch

    Parameters
    ----------
    max_depth : int
        Maximum depth of the prediction suffix tree
    """
    def __init__(self, max_depth=3, root = Node()):
        """

        """
        RpsAgent.__init__(self)
        self.root = root
        self.max_depth = max_depth

    def reset_game(self):
        RpsAgent.reset_game(self)
        self.root = Node()

    def record(self, last_round):
        """
        Record last played round and update the tree.

        Parameters
        ----------
        last_round : Round
            Last round to be recorded
        """
        RpsAgent.record(self, last_round)
        self.root.learn_sequence(self.game[-self.max_depth - 1:])

    def predict_agent_gesture(self):
        """
        Play rediction by descending in the tree (or at random if less than 2
        rounds have been played).

        Returns
        -------
        {ROCK, PAPER, SCISSORS}
        """
        if len(self.game) < 2:
            rp = RandomPlayer()
            return rp.predict_agent_gesture()

        online_gesture = self.root.predict_gesture_online(
            self.game[-self.max_depth - 1:])
        return online_gesture

    def __repr__(self):
        return 'OnlinePstAgent(max_depth={})'.format(self.max_depth)

    @staticmethod
    def load(max_depth=3):
        from ..pst_player.defs import path_pst
        root = Node.load_tree(path_pst)
        return OnlinePstAgent(root=root, max_depth=max_depth)

class OnlinePstAgentNS(RpsAgent):
    """ A prediction suffix tree agent that learns online from scratch

    Parameters
    ----------
    max_depth : int
        Maximum depth of the prediction suffix tree
    """
    def __init__(self, max_depth=3, root = None, alpha=0.123):
        """

        """
        RpsAgent.__init__(self)
        if root is None:
            root = NodeNS(alpha=alpha)
        self.root = root
        self.max_depth = max_depth
        self.alpha = root.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.root.set_alpha(alpha)

    def reset_game(self):
        RpsAgent.reset_game(self)
        self.root = NodeNS(alpha=self.alpha)

    def record(self, last_round):
        """
        Record last played round and update the tree.

        Parameters
        ----------
        last_round : Round
            Last round to be recorded
        """
        RpsAgent.record(self, last_round)
        self.root.learn_sequence(self.game[-self.max_depth - 1:])

    def predict_agent_gesture(self):
        """
        Play rediction by descending in the tree (or at random if less than 2
        rounds have been played).

        Returns
        -------
        {ROCK, PAPER, SCISSORS}
        """
        if len(self.game) < 2:
            rp = RandomPlayer()
            return rp.predict_agent_gesture()

        online_gesture = self.root.predict_gesture_online(
            self.game[-self.max_depth - 1:])
        return online_gesture

    def __repr__(self):
        return 'OnlinePstAgentNS(max_depth={}, alpha={})'\
            .format(self.max_depth, self.alpha)

    @staticmethod
    def load():
        from ..pst_player.defs import path_pst_ns
        root = NodeNS.load_tree(path_pst_ns)
        return OnlinePstAgentNS(root=root)