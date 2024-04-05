# -*- coding: utf-8 -*-

from shifumy_player.players.pst_player.defs \
    import path_alldata, path_misc
from shifumy_player.players.stratego_player \
    import StrategoPlayer
from shifumy_player.players.pst_player._cross_validation \
    import get_wld_agent_in_history, write_win_lose_draw_results_in_file
from shifumy_player.players.pst_player.module.History \
    import History


def valid_stratego(history, file, confidence, forget, scale):
    agent = StrategoPlayer(confidence, forget, scale)
    wld = get_wld_agent_in_history(agent, history)
    file.write("\nconfidence = %lf, forget = %lf, scale = %lf" % (confidence, forget, scale))
    write_win_lose_draw_results_in_file(wld, file)


data_file = open(path_alldata, "r")
history = History()
history.read_from_file(data_file)
data_file.close()

save_path = path_misc + "stratego_test.txt"
save_file = open(save_path, "a")
save_file.write("\n\n\n")

for confidence in range(10, 90, 5):
    for forget in range(1, 10, 1):
        for scale in range(1, 10, 1):
            valid_stratego(history, save_file, confidence, forget, scale)
            print("confidence = %lf, forget = %lf, scale = %lf" % (confidence, forget, scale))
save_file.close()
