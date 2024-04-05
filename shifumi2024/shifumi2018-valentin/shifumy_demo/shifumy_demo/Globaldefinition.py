# from shifumy_player.base import *
# from shifumy_player.players.pst_player import PstAgent
# from shifumy_player.players.Rnn_player.code.Agent.Agent import TdnnPstAgent
# from shifumy_player.players.random_player import RandomPlayer
# from shifumy_player.players.hmm_player.Rps_HMM import Rps_HMM
# from shifumy_player.players.numberphile_player import NumberphilePlayer
# from shifumy_player.players.actuarial_player import ActuarialPlayer
# from shifumy_player.players.stratego_player import StrategoPlayer
from shifumy_player.players.kilias_player import KiliasPlayer
from shifumy_player.players.ve_players.ve_online_pst \
    import OnlinePstAgent, OnlinePstAgentNS
from shifumy_player.players.ve_players.sklearn_agents \
    import MultinomialNBAgent, SgdSvmAgent, SgdLogRegAgent, PerceptronAgent, \
    PassiveAggressiveClassifierAgent, MLPClassifierAgent
from shifumy_player.players.ve_players.bandits \
    import UcbMetaAgent, UpdateAllMetaAgent, UpdateAllNsMetaAgent


# dict_all_agent = {
#     "RandomPlayer"   : RandomPlayer      ,
#     "PstAgent"       : PstAgent          ,
#     "HMM"            : Rps_HMM           ,
#     "Neural NetWork" : TdnnPstAgent      ,
#     "Numberphile"    : NumberphilePlayer ,  # Vidéo internet, règles, Mathias
#     "Actuarial"      : ActuarialPlayer   ,  # Mathias
#     "Stratego"       : StrategoPlayer    ,  # Mathias, multi-stratégies
#     "Kilias"         : KiliasPlayer      ,  # HMM+Actuarial avec switch
#     "V-OPST": OnlinePstAgent,
#     "V-OPST-NS": OnlinePstAgentNS,
#     "MultinomialNBAgent": MultinomialNBAgent,
#     "SgdSvmAgent": SgdSvmAgent,
#     "SgdLogRegAgent": SgdLogRegAgent,
#     "PerceptronAgent": PerceptronAgent,
#     "PassiveAggressiveClassifierAgent": PassiveAggressiveClassifierAgent,
#     "MLPClassifierAgent": MLPClassifierAgent,
#     "Bandit-UCB": UcbMetaAgent,
#     "Bandit-UpdateAll": UpdateAllMetaAgent,
#     "Bandit-UpdateAll NS": UpdateAllNsMetaAgent,
# }

dict_all_agent = {
    "Kilias"         : KiliasPlayer      ,  # HMM+Actuarial avec switch
    "V-OPST-NS": OnlinePstAgentNS,
    "SgdLogRegAgent": SgdLogRegAgent,
    "Bandit-UpdateAll": UpdateAllMetaAgent,
    "Bandit-UpdateAll NS": UpdateAllNsMetaAgent,
}
