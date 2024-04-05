# coding: utf8

from ....base import RpsAgent
from ..module.Node import Node
from ..defs import path_pst, beats

class PstAgent(RpsAgent):
    """
    This class is the class from which all the agent using a prediction suffix\
    tree will inherited.
    """
    def __init__(self, root = Node()):
        super().__init__()
        self.root = root

    @staticmethod
    def load():
        root = Node.load_tree(path_pst)
        return PstAgent(root)


class DeepestPstAgent(PstAgent):
    """
    This agent will predict_agent_gesture the next gesture using the data of the deepest
    node using the longest sequence possible and choose the gesture with the best
    gain expectation.
    """
    def __init__(self, root = Node()):
        super().__init__(root)

    def predict_agent_gesture(self):
        root = self.root
        assert (isinstance(root,Node))
        return root.predict_gesture_deepest(self.game)

    @staticmethod
    def load():
        p = PstAgent.load()
        return DeepestPstAgent(p.root)

class ConfidentPstAgent(PstAgent):
    """
    This agent will predict_agent_gesture the next gesture using the data from every node
    using the longest sequence possible and choose the gesture with the best
    gain expectation using a confident interval calculate with beta.
    """
    def __init__(self, beta = 0, root = Node()):
        super().__init__(root)
        self.beta = beta

    def predict_agent_gesture(self):
        root = self.root
        return root.predict_gesture_confident(self.game, self.beta)

    @staticmethod
    def load():
        p = PstAgent.load()
        return CondfidentPstAgent(p.root)

class UndecidedPstAgent(PstAgent):
    """
    This agent will predict_agent_gesture the next gesture using the data of the every
    node using a sequence of length depth at most and choose the gesture with
    the best gain expectation using a confident interval.
    """
    def __init__(self, beta = 0, root = Node(), depth = 0):
        super().__init__(root)
        self.depth = depth
        self.beta = beta

    def predict_agent_gesture(self):
        root = self.root
        return root.predict_gesture_undecided(self.game, self.depth, beta)

    @staticmethod
    def load():
        p = PstAgent.load()
        return UndecidedPstAgent(p.root)

class VariantPstAgent(PstAgent):
    """
    This agent will predict_agent_gesture the next gesture using the data of the deespest
    node using a sequence of length depth at most and choose the gesture with the
    best gain expectation.
    """
    def __init__(self, root = Node(), depth = 0):
        super().__init__(root)
        self.depth = depth

    def predict_agent_gesture(self):
        root = self.root
        return root.predict_gesture_variant(self.game, self.depth)

    @staticmethod
    def load():
        p = PstAgent.load()
        return VariantPstAgent(p.root)

class DoubleFacePstAgent(DeepestPstAgent):
    """
    This agent is a combination of two DeepestPstAgent, one using the bash
    tree and the other using an online tree.
    """
    def __init__(self, root = Node()):
        super().__init__(root)
        self.online_root = Node()

    def reset_game(self):
        super().reset_game()
        self.online_root = Node()

    def record(self, last_round):
        super().record(last_round)
        self.online_root.learn_sequence(self.game[-3:])

    def predict_agent_gesture(self):
        bash_gesture = super().predict_agent_gesture()
        online_root = self.online_root
        online_gesture = online_root.predict_gesture_online(self.game)
        if online_gesture == None:
            return bash_gesture
        return online_gesture
        """elif bash_gesture == online_gesture:
            return bash_gesture
        elif bash_gesture == beats[online_gesture]:
            return bash_gesture
        else:
            return online_gesture"""

    @staticmethod
    def load():
        p = PstAgent.load()
        return DoubleFacePstAgent(p.root)
