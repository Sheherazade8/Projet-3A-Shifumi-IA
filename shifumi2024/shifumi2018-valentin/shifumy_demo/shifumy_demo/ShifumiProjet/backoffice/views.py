from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from .data import Data
from .models import humans
from .models import humansRobot

###############################################################
#   Module Importation                                        #
##############################################################

from shifumy_player.base import *
from shifumy_demo.Globaldefinition import dict_all_agent
from collections import Counter

from django.contrib.staticfiles.templatetags.staticfiles import static

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from shifumy_demo.ShifumiProjet.shifumiIA.settings import BASE_DIR

import matplotlib.pyplot as plt


global Instance
global model_name
global pseudo

global Node_static
global gain_op
global gain_ag

global agent
global joeur
global Barret_max
global Barret_min


global list_start

import sqlite3
import time
import random
import string

from math import floor




    ################################################################################################
    #                                                                                              #
    #                 After that all function is the function used URL Django                      #
    #                                                                                              #
    ################################################################################################

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
         return ''.join(random.choice(chars) for _ in range(size))


def file_saved(pathfile,modelecture):
    with open(os.path.join(RESOURCES_PATH, pathfile), modelecture) as write_file:
        # open a file to write to
        conn = sqlite3.connect(os.path.join(RESOURCES_PATH, os.path.join("DB", "db.sqlite3")))
        # connect to your database
        cursor = conn.cursor()
        # create a cursor object (which lets you address the table results individually)
        data = humansRobot.objects.all()

        ligne = "Game,"+"Round,"+"Player_oppement,"+"Player_agent,"+"Model_Agent,"+"Pseudo"
        write_file.writelines(ligne + '\n')

        for row in data:
            # use the cursor as an iterable
            ligne =  str(row.game) + "," + str(row.round) + "," + str(
                row.opponent) + "," + str(row.agent)+","+str(row.Model_Used)+","+str(row.Pseudo_player)
            write_file.writelines(ligne + '\n')


def analysis(request):

    data = humansRobot.objects.all()
    datarangetab = humansRobot.objects.raw("select *, ((Gain/round)*100) as nb_gain  from backoffice_humansrobot group by Pseudo_player order by  nb_gain desc Limit 10")

    url = static('images')
    path = os.path.join(BASE_DIR, "static")
    pathfile = os.path.join(path, os.path.join("images", "TableauBord"))

    pathfilename = os.path.join(pathfile, "stat_all_agent.png")

    if os.path.isfile(pathfilename):
        os.remove(pathfilename)

    datafig = humansRobot.objects.raw("select id,Model_Used,sum(round) as total_round,sum(gain) as total_gain from backoffice_humansrobot where id in (select id from backoffice_humansrobot group by game ) group by Model_Used ")

    x = []
    y = []

    pseudo = ""
    for dat in datafig:
        pourcentage = (int(dat.total_gain) / int(dat.total_round)) * 100
        x.append(dat.Model_Used)
        y.append(pourcentage)
        pseudo = dat.Pseudo_player

    plt.bar(x, y)
    # plt.([1, 2, 1], bins=[0, 1, 2, 3])
    # plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
    # plt.yticks(np.arange(min(y), max(y) + 1, 1.0))

    plt.xlabel("Jouer Artificiel")
    plt.ylabel("Pourcentage de gain")

    plt.savefig(pathfilename)
    plt.clf()



    if request.POST.get('Download') == "All":

        filename = time.strftime("%Y_%m_%d_%H_%M_%S_")+id_generator()+".csv"
        pathfile = os.path.join("data",os.path.join("datasets",os.path.join("FromDb",filename)))
        file_saved(pathfile,"w+")





    return render(request, 'Pages/AnalysisData.html', {'data': data,'len':len(data),'dataOrderGain':datarangetab})




def boardGame(request):
    url = static('images')
    path = os.path.join(BASE_DIR, "static")
    pathfile = os.path.join(path, os.path.join("images", "TableauBord"))

    pathfilename = os.path.join(pathfile, "stat_this_game.png")

    if os.path.isfile(pathfilename):
        os.remove(pathfilename)


    data = humansRobot.objects.all()
    try:
       id_last_game = humansRobot.objects.all().last().game
    except Exception:
        return redirect("/")

    datarange = humansRobot.objects.filter(game = id_last_game)

    x = []
    y = []

    pseudo = ""
    for dat in datarange:
        gain = get_gain_op_game( int(dat.opponent) , int(dat.agent) )
        x.append(dat.round)
        y.append(gain)
        pseudo = dat.Pseudo_player

    # plt.figure(figsize=(len(x),4 ))

    plt.plot(x, y,)
    plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
    plt.yticks(np.arange(min(y), max(y) + 1, 1.0))
    plt.xlabel("Nombres de Round")
    plt.ylabel("Gain")

    plt.savefig(pathfilename)
    plt.clf()



    if request.POST.get('Download') == "All":

        filename = time.strftime("%Y_%m_%d_%H_%M_%S_")+id_generator()+".csv"
        #pathfile = os.path.join("data",os.path.join("datasets",os.path.join("FromDb",filename)))
        pathfile = os.path.join("DB", filename)
        file_saved(pathfile,"w+")





    return render(request, 'Pages/TableauBord/ThisGame.html', {'pseudo':pseudo})


def get_gain_op_game(op,ag):
    if(op == ag):
        return 0
    elif(mov_beat(op) == ag):
        return -1
    elif(mov_beat(ag) == op):
        return 1



def boardAllGame(request):

    data = humansRobot.objects.all()
    datarange = humansRobot.objects.raw("select *, (Gain/round) as nb_gain from backoffice_humansrobot group by Pseudo_player order by  nb_gain desc")

    if request.POST.get('Download') == "All":

        filename = time.strftime("%Y_%m_%d_%H_%M_%S_")+id_generator()+".csv"
        #pathfile = os.path.join("data",os.path.join("datasets",os.path.join("FromDb",filename)))
        pathfile = os.path.join("DB", filename)
        file_saved(pathfile,"w+")





    return render(request, 'Pages/AnalysisData.html', {'data': data,'len':len(data),'dataOrderGain':datarange})












def home(request):
    clean_session(request, ["begin", "actual_part", "load_tree"])
    reinitialize_var(request, ["winhr", "tiehr", "losthr"])


    data = Data()  # this function return

    # node = Load_Model(request)  # load tree
    # set_Node(node)

    if request.POST.get('choiceModel') != None:
        clean_session(request, ["begin", "actual_part"])
        reset_oppenent_gain(request)
        reset_agent_gain(request)
        object = dict_all_agent[request.POST.get('choiceModel')].load()
        set_Model_instance(object)
        object_model = get_Model_instance()
        set_pseudo(request.POST.get("pseudo"))
        set_Model_name(request.POST.get('choiceModel'))
        set_next_move(object.predict_agent_gesture())

        return redirect('/Game')

    return render(request, 'Pages/index.html',{"All_agent_name":dict_all_agent})





def show(request):
    actual, nexts, begin, actual_part, gain_op, gain_ag  = init_var_resquest_humanVsMariana(request)


    try:
        object_model = get_Model_instance()  # does a exist in the current namespace
    except NameError:
        return redirect('/')


    data = Data()  # this function return

    if request.POST.get('choiceModel') != None:
        clean_session(request, ["begin", "actual_part"])
        reset_oppenent_gain(request)
        reset_agent_gain(request)
        object_model.reset_game()
        object = dict_all_agent[request.POST.get('choiceModel')].load()
        set_Model_instance(object)
        object_model = get_Model_instance()
        set_pseudo(request.POST.get("pseudo"))
        set_Model_name(request.POST.get('choiceModel'))





    if request.POST.get('MoveChoice') != None:
        next = get_next_move()

        model = humansRobot()



        object_model.record(Round(transform_rps_123(request.POST.get("MoveChoice")),next))
        actual_part = request.session.get("actual_part")
        predict_move = object_model.predict_agent_gesture()

        actual, next = update_next_move(predict_move, next)

        gain = get_gain(request,transform_rps_123(request.POST.get("MoveChoice")), actual)

        game = insert_new_game(request, model, begin, "begin",
                              transform_rps_123(request.POST.get("MoveChoice")), next, get_pseudo(), get_Model_name(), "mouse_version",float(get_oppenent_gain(request)))


        taux_joeur,taux_agent = getPourcentage_Progress_Bar(request)

        all_start = get_all_start(get_list_start())

        return render(request, 'Pages/show.html',
                      {"agent_gesture": transform_123_rps(actual),
                       "agent_gesture_next": transform_123_rps(next),
                       "oppenement_gesture": request.POST.get("MoveChoice"), "agent_gain": get_agent_gain(request),"oppenement_gain": get_oppenent_gain(request),
                       "oppenent_gain_actuel": object_model.game[-1].get_opponent_gain(), "agent_gain_actuel": object_model.game[-1].get_agent_gain(),"All_agent_name":dict_all_agent,"Choiced_model":get_Model_name(),"Pseudo":get_pseudo(),"start_op":range(floor(int(get_oppenent_gain(request))/5)),"start_ag":range(floor(int(get_agent_gain(request))/5)),"taux_joeur":taux_joeur,"taux_agent":taux_agent,"list_start":get_list_start(),
                       "start_jaune_pl":range(all_start[0][0]),
                       "start_orange_pl": range(all_start[0][1]),
                       "start_vert_pl": range(all_start[0][2]),
                       "start_bleu_pl": range(all_start[0][3]),
                       "start_rouge_pl": range(all_start[0][4]),
                       "start_jaune_ag": range(all_start[1][0]),
                       "start_orange_ag": range(all_start[1][1]),
                       "start_vert_ag": range(all_start[1][2]),
                       "start_bleu_ag": range(all_start[1][3]),
                       "start_rouge_ag": range(all_start[1][4]),

                       })

    if request.POST.get('submit') == 'restartgame':
        clean_session(request, ["begin", "actual_part"])
        object_model.reset_game()
        reset_oppenent_gain(request)
        reset_agent_gain(request)

        set_Barret_min(0)
        set_Barret_max(5)
        set_gain_joeur_barret(0)
        set_gain_agent_barret(0)
        init_list_start()

        predict_move = object_model.predict_agent_gesture()

    if request.POST.get('submit') == 'visualiseMesResultat':
        return redirect("/thisGame")

        # predict_move = Random().get_random()


        set_actual_move(None)
        set_next_move(predict_move)
        # actual, next = update_next_move(predict_move, next)
        # actual, next = update_next_var(request, predict_move, next)

        tampon = min(int(get_oppenent_gain(request)), int(get_oppenent_gain(request))) // 5 * 5

        all_start = get_all_start(get_list_start())

        return render(request, 'Pages/show.html',
                      {"agent_gesture": transform_123_rps(get_actual_move()),
                       "agent_gesture_next": transform_123_rps(get_next_move()),
                       "oppenement_gesture": request.POST.get("MoveChoice"), "agent_gain": get_agent_gain(request),
                       "oppenement_gain": get_oppenent_gain(request),"All_agent_name":dict_all_agent,"Choiced_model":get_Model_name(),"Pseudo":get_pseudo(),"start_op":range(floor(int(get_oppenent_gain(request))/5)),"start_ag":range(floor(int(get_agent_gain(request))/5)),"tampon":tampon,"all_start":all_start}
                      )

    # return HttpResponse(get_Node().nb_RPS)
    #predict_move = get_predict(request, node_static, data)

    predict_move = object_model.predict_agent_gesture()

    # predict_move = Random().get_random()


    set_actual_move(None)
    set_next_move(predict_move)

    set_Barret_min(0)
    set_Barret_max(5)
    set_gain_joeur_barret(0)
    set_gain_agent_barret(0)
    init_list_start()

    all_start = get_all_start(get_list_start())



    return render(request, 'Pages/show.html',
                  {"agent_gesture": transform_123_rps(get_actual_move()),
                   "agent_gesture_next": transform_123_rps(get_next_move()),
                   "oppenement_gesture": request.POST.get("MoveChoice"), "agent_gain": get_agent_gain(request),
                   "oppenement_gain": get_oppenent_gain(request),"All_agent_name":dict_all_agent,"Choiced_model":get_Model_name(),"Pseudo":get_pseudo(),"start_op":range(floor(int(get_oppenent_gain(request))/5)),"start_ag":range(floor(int(get_agent_gain(request))/5)),"all_start":all_start}
                  )


def getPourcentage_Progress_Bar(request):
    agent = get_gain_agent_barret()
    joeur =get_gain_joeur_barret()
    agent_ab =  get_agent_gain(request)
    joeur_ab =  get_oppenent_gain(request)
    pourcentage = get_Barret_max() - get_Barret_min()

    if( (max(agent_ab,joeur_ab) == get_Barret_max()) and joeur_ab!= agent_ab  ):
        tampon = (min(joeur_ab,agent_ab) // 5)*5
        set_gain_joeur_barret(joeur_ab-tampon)
        set_gain_agent_barret(agent_ab-tampon)
        set_Barret_max(get_Barret_max()+5)
        set_Barret_min(tampon)
        agent = get_gain_agent_barret()
        joeur = get_gain_joeur_barret()

        pourcentage = get_Barret_max() - get_Barret_min()
        taux_joeur = (joeur / pourcentage) * 100
        taux_agent = (agent / pourcentage) * 100

        if(agent > joeur):
            if (agent % 5 == 0):
               add_list_start("agent")
        elif (agent < joeur):
             if (joeur % 5 == 0):
                add_list_start("joeur")

        return taux_joeur, taux_agent

    else:
        taux_joeur = (joeur / pourcentage) * 100
        taux_agent = (agent / pourcentage) * 100

        return taux_joeur,taux_agent

def get_all_start(list_start):
    dict_compteur = Counter(list_start)
    nb_gain_agent = dict_compteur["agent"]
    nb_gain_joeur = dict_compteur["joeur"]


    nb_start_jaune_ag = 0 # gain 5
    nb_start_orange_ag = 0 # 20
    nb_start_vert_ag = 0 # 80
    nb_start_bleu_ag = 0 # 320
    nb_start_rouge_ag = 0 # 1280

    nb_start_jaune_pl = 0  # gain 5
    nb_start_orange_pl = 0  # 20
    nb_start_vert_pl = 0  # 80
    nb_start_bleu_pl = 0  # 320
    nb_start_rouge_pl = 0  # 1280

    if(nb_gain_agent >= 256):
        while((nb_gain_agent - 256) >= 0 ):
            nb_gain_agent  -= 256
            nb_start_rouge_ag += 1

    if (nb_gain_agent >= 64):
        while ((nb_gain_agent - 64) > 0):
            nb_gain_agent -= 64
            nb_start_bleu_ag += 1

    if (nb_gain_agent >= 16):
        while ((nb_gain_agent - 16) >= 0):
            nb_gain_agent -= 16
            nb_start_vert_ag += 1
    if (nb_gain_agent >= 4):
        while ((nb_gain_agent - 4) >= 0):
            nb_gain_agent -= 4
            nb_start_orange_ag += 1
    if (nb_gain_agent >= 1):
        while ((nb_gain_agent - 1) >= 0):
            nb_gain_agent -= 1
            nb_start_jaune_ag += 1


    #


    if (nb_gain_joeur >= 256):
        while ((nb_gain_joeur - 256) >= 0):
            nb_gain_joeur -= 256
            nb_start_rouge_pl += 1
    if (nb_gain_joeur >= 64):
        while ((nb_gain_joeur - 64) >= 0):
            nb_gain_joeur -= 64
            nb_start_bleu_pl += 1

    if (nb_gain_joeur >= 16):
        while ((nb_gain_joeur - 16) >= 0):
            nb_gain_joeur -= 16
            nb_start_vert_pl += 1
    if (nb_gain_joeur >= 4):
        while ((nb_gain_joeur - 4) >= 0):
            nb_gain_joeur -= 4
            nb_start_orange_pl += 1
    if (nb_gain_joeur >= 1):
        while ((nb_gain_joeur - 1) >= 0):
            nb_gain_joeur -= 1
            nb_start_jaune_pl += 1

    return [[nb_start_jaune_pl ,
             nb_start_orange_pl ,
             nb_start_vert_pl ,
             nb_start_bleu_pl ,
             nb_start_rouge_pl ]
            ,[ nb_start_jaune_ag,
              nb_start_orange_ag ,
              nb_start_vert_ag ,
              nb_start_bleu_ag,
              nb_start_rouge_ag ]
            ]





####################################################################################################
#
#           All function to used
#
####################################################################################################


def insert_new_game(request, model, begin, beginreq, moveOne, moveTwo,pseudo,modelused,systeme,gain):
    if begin == 1:

        model.round = humansRobot.objects.all().last().round + 1
        model.game = humansRobot.objects.all().last().game
        request.session["actual_part"] = humansRobot.objects.all().last().game


    elif begin == 0:
        model.round = 1
        begin = 1
        request.session[beginreq] = begin
        try :
            model.game = humansRobot.objects.all().last().game + 1
            request.session["actual_part"] = humansRobot.objects.all().last().game + 1

        except Exception:
            model.game = 1
            request.session["actual_part"] = 1

    model.opponent = moveOne
    model.agent = moveTwo
    model.Model_Used = str(modelused)
    model.System = systeme
    model.Pseudo_player = str(pseudo)
    model.Gain = gain
    model.save()

    return model


def transform_123_rps(number):
    if (number == None):
        return "None"
    elif (number == ROCK):
        return "Rock"
    elif (number == SCISSORS):
        return "Scissors"
    elif (number == PAPER):
        return "Paper"


def transform_rps_123(rps):
    if (rps == None):
        return None
    elif (rps == "Rock"):
        return ROCK
    elif (rps == "Paper"):
        return PAPER
    elif (rps == "Scissors"):
        return SCISSORS


def init_var_resquest_humanVsMariana(request):
    # variable
    actual = request.session.get('actual_move')

    # next saved the new move of computer (int) 1-R 2-P- 3-S
    next = request.session.get('next_move')

    # begin is boolean variable , it's used tho initilized the round
    begin = request.session.get('begin', 0)

    # begin is boolean variable , it's used tho initilized the round
    actual_part = request.session.get('actual_part', 0)

    # tiehr,losthr,winhr is counter and return how much the user win,lost ,tie (int)
    gain_op = request.session.get('gainOp', 0)

    gain_ag = request.session.get('gainAg', 0)



    return actual, next, begin, actual_part, gain_op,gain_ag


def init_var_resquest_humanVsHuman(request):
    tiep1 = request.session.get('tiep1', 0)

    lostp1 = request.session.get('lostp1', 0)

    winp1 = request.session.get('winp1', 0)

    tiep2 = request.session.get('tiep2', 0)

    lostp2 = request.session.get('lostp2', 0)

    winp2 = request.session.get('winp2', 0)

    # with _counter_lock:
    beginround = request.session.get('beginround')

    return beginround, tiep1, lostp1, winp1, tiep2, lostp2, winp2


def update_next_var(request, model, next):
    request.session['actual_move'] = next
    actual = request.session['actual_move']

    request.session['next_move'] = model
    next = request.session['next_move']

    return actual, next


def update_next_move(model, next):
    # request.session['actual'] = next
    # actual = request.session['actual']
    set_actual_move(next)
    set_next_move(model)

    # request.session['next'] = model
    # next = request.session['next']

    return get_actual_move(), get_next_move()


def get_gain(request,playerOponement, playerAgent):

    if(playerOponement == playerAgent):
        return
    if mov_beat(playerOponement) == playerAgent:
        gain_ag = request.session.get('gainAg')
        request.session['gainAg'] = int(gain_ag) + 1
        set_gain_agent_barret(get_gain_agent_barret()+1)

        gain = get_gain_agent_barret()




    elif mov_beat(playerOponement) != playerAgent:
        gain_op = request.session.get('gainOp')
        request.session['gainOp'] = int(gain_op) + 1
        set_gain_joeur_barret(get_gain_joeur_barret()+1)
        gain = get_gain_joeur_barret()








def get_agent_gain(request):
    return request.session.get('gainAg')
def get_oppenent_gain(request):
    return request.session.get('gainOp')

def reset_agent_gain(request):
    request.session['gainOp'] = 0
def reset_oppenent_gain(request):
    request.session['gainAg'] = 0


def clean_session(request, listeVarSession):
    for liste in listeVarSession:
        try:
            del request.session[liste]
        except KeyError:
            pass


def reinitialize_var(request, listeVar):
    for liste in listeVar:
        try:
            request.session[liste] = 0
        except KeyError:
            pass


def mov_beat(move):
    if move == 0:
        return 1

    elif move == 1:
        return 2

    elif move == 2:
        return 0

########################################"
def set_Model_instance(object):
    global Instance
    Instance = object


def get_Model_instance():
    return Instance


def set_gain_joeur_barret(gain):
    global joeur
    joeur = gain


def get_gain_joeur_barret():
    return joeur

def set_gain_agent_barret(gain):
    global agent
    agent = gain


def get_gain_agent_barret():
    return agent



def set_Barret_max(num):
    global Barret_max
    Barret_max = num


def get_Barret_max():
    return Barret_max


def set_Barret_min(gain):
    global Barret_min
    Barret_min = gain


def get_Barret_min():
    return Barret_min



def init_list_start():
    global list_start
    list_start = []

def add_list_start(player):
    global list_start
    list_start.append(player)


def get_list_start():
    return list_start













def set_Model_name(name):
    global model_name
    model_name = name


def get_Model_name():
    return model_name


def set_pseudo(name):
    global pseudo
    pseudo = name


def get_pseudo():
    return pseudo

#######################################


def set_gain_op(gain):
    gain_op += gain


def get_gain_op():
    return gain_op

def reset_gain_op():
    gain_op = 0


def set_gain_ag(gain):
    gain_ag += gain


def get_gain_ag():
    return gain_ag
def reset_gain_ag():
    gain_ag = 0



def set_actual_move(actual):
    global actual_move
    actual_move = actual

def get_actual_move():
    return actual_move

def set_next_move(next):
    global next_move
    next_move = next

def get_next_move():
    return next_move

def set_partie(actual):
    global actual_partie
    actual_partie = actual

def get_partie():
    return actual_partie

    ################################################################################################
    #                                                                                              #
    #                 After that all function is the function used URL Django                      #
    #                                                                                              #
    ################################################################################################
