#-*- coding: utf-8 -*-

# Mac Donald  Kilian
# HMM_fonctions 2
# crée le 04/06/2018

from shifumy_player.players.hmm_player.classe2 import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import random
import sys

def chaines_to_tuple(chaine1, chaine2):
    chaine = ()
    if len(chaine1) == 0 or len(chaine2) == 0:
        raise ValueError('Les chaines ne doivent pas etre vides')
    elif len(chaine1) != 1:
        if len(chaine1) != len(chaine2):
            raise ValueError('Les chaines doivent etre de la meme longueur')
        for i in range(len(chaine1)):
            chaine += (HMM.change_double(chaine1[i], chaine2[i]),)
    else:
        if len(chaine1[0]) != len(chaine2[0]):
            raise ValueError('Les chaines doivent etre de la meme longueur')
        for i in range(len(chaine1[0])):
            chaine += (HMM.change_double(chaine1[0][i], chaine2[0][i]),)
    return [chaine]

def xval(nbFolds, S, nbL, nbSMin, nbSMax, nbIter, nbInit):
    n = len(S)
    l = np.random.permutation(n)
    lvOpt = -float("inf")
    for nbS in range(nbSMin, nbSMax + 1):
        lv = 0
        for i in range(1, nbFolds + 1):
            f1 = int((i - 1) * n / nbFolds)
            f2 = int(i * n / nbFolds)
            learn = [S[l[j]] for j in range(f1)]
            learn += [S[l[j]] for j in range(f2, n)]
            test = [S[l[j]] for j in range(f1, f2)]
            h = HMM.bw3(nbS, nbL, learn, nbIter, nbInit)
            lv += h.logV(test)
        if lv > lvOpt:
            lvOpt = lv
            nbSOpt = nbS
    return lvOpt, nbSOpt


def func(x, a, b, c):  # fonction utilisee pour le fitting de certaines courbes
    return - a * np.exp(-x / b) - 25580 + c


def logV_vs_nb_iteration_bw1(nb_iter_max, nbS, S,
                             nbL=9):  # trace la log vraisemblance en fonction du nombre d'iteration de bw1
    """
    :param nb_iter_max: nombre d'iterations de bw1 a realiser
    :param nbS: nb d'etats
    :param S: liste de mots sur laquelle on entraine notre HMM
    :param nbL: nombre de lettres
    """

    hmm = HMM.gen_HMM(nbL, nbS)
    nb_iter = [0]
    logV = [hmm.logV(S)]
    for i in range(1, nb_iter_max + 1):
        try:
            hmm.bw1(S)
            nb_iter.append(i)
            logV.append(hmm.logV(S))
        except KeyboardInterrupt:
            break
    plt.plot(nb_iter, logV, '.', c='blue', label='logV en fonction du nombre d\'iteration de bw1')
    plt.xlabel('nb d\'iteration')
    plt.ylabel('logV')
    titre = 'anglais2000' + ' / nombre d\'etat = ' + str(nbS)
    plt.title(titre)
    optimizedParameters, pcov = opt.curve_fit(func, nb_iter, logV)

    # Use the optimized parameters to plot the best fit
    plt.plot(nb_iter,
             [func(x, optimizedParameters[0], optimizedParameters[1], optimizedParameters[2]) for x in nb_iter],
             label='-' + str(optimizedParameters[0]) + 'exp(-x/' + str(optimizedParameters[1]) + ') + ' + str(
                 -25580 + optimizedParameters[2]))

    plt.legend()
    plt.show()

def logV_vs_intialisation(nb_init_max, nb_iter, nbS, S,
                          nbL=9):  # trace la logvraisemblance optimale en fonction de differentes initialisations
    """
    :param nb_init_max: nombre d'initialisations differentes a realiser
    :param nb_iter: nombre d'iteration dans bw2
    :param nbS: nombre d'etats
    :param S: liste de mots sur laquelle on entraine nos HMM
    :param nbL: nombre de lettres
    """

    nb_init = []
    logV = []
    for i in range(1, nb_init_max + 1):
        print("init", i)
        try:
            h = HMM.bw2(nbS, nbL, S, nb_iter)
            nb_init.append(i)
            logV.append(h.logV(S))
            print("###################################")
            print(logV[-1])
            print("###################################")
        except KeyboardInterrupt:
            break
    plt.plot(nb_init, logV)
    plt.show()


def logV_vs_initialisation_variante(nb_init_max, limite, nbS, S,
                                    nbL=9):  # trace la logvraisemblance optimale en fonction de differentes
                                                # initialisations
    """
    :param nb_init_max: nombre d'initialisations differentes a realiser
    :param limite: limite pour bw2_variante
    :param nbS: nombre d'etats
    :param S: liste de mots sur laquelle on entraine nos HMM
    :param nbL: nombre de lettres
    """

    nb_init = []
    logV = []
    for i in range(1, nb_init_max + 1):
        try:
            h = HMM.bw2_variante(nbS, nbL, S, limite)
            nb_init.append(i)
            logV.append(h.logV(S))
        except KeyboardInterrupt:
            break
    plt.plot(nb_init, logV)
    plt.show()


def efficiency_vs_nb_state(nbFolds, S, nbSMin, nbSMax, nbIter, nbInit,
                           nbL=9):  # trace la log vraisemblance moyenne sur les echantillons tests en fonction du
                                    # nombre d'etat
    """
    :param nbFolds: cardinal de la partition de S
    :param S: liste de mots sur laquelle on entraine notre HMM
    :param nbSMin: nombre d'etat minimum
    :param nbSMax: nombre d'etat maximum
    :param nbIter: nombre d'iterations pour bw3
    :param nbInit: nbombre d'initialisations pour bw3
    :param nbL: nombre de lettres pour le HMM
    """

    n = len(S)
    l = np.random.permutation(n)
    nb_state = []
    logV = []
    for nbS in range(nbSMin, nbSMax + 1):
        #print('nbS:', nbS)
        try:
            lv = 0
            for i in range(1, nbFolds + 1):
                f1 = int((i - 1) * n / nbFolds)
                f2 = int(i * n / nbFolds)
                learn = [S[l[j]] for j in range(f1)]
                learn += [S[l[j]] for j in range(f2, n)]
                test = [S[l[j]] for j in range(f1, f2)]
                #print('bw3:',i)
                h = HMM.bw3(nbS, nbL, learn, nbIter, nbInit)
                lv += h.logV2(test)
            logV.append(lv / nbFolds)
            nb_state.append(nbS)
        except KeyboardInterrupt:
            break
    plt.plot(nb_state, logV)
    plt.show()

def efficiency_vs_nb_state2(nFolds, S, nbS, nbIter, nbInit, nbL=9):
    n = len(S)
    l = np.random.permutation(n)
    lv = 0
    f1 = int((nFolds - 1) * n / 10)
    f2 = int(nFolds * n / 10)
    learn = [S[l[j]] for j in range(f1)]
    learn += [S[l[j]] for j in range(f2, n)]
    test = [S[l[j]] for j in range(f1, f2)]
    # print('bw3:',i)
    h = HMM.bw3(nbS, nbL, learn, nbIter, nbInit)
    lv += h.logV2(test)
    print(nbS, nFolds, lv/10)

def efficiency_vs_nb_state_variante(nbFolds, S, nbSMin, nbSMax, limite, nbInit,
                                    nbL=9):  # trace la log vraisemblance moyenne sur les echantillons tests en
                                                # fonction du nombre d'etat
    """
    :param nbFolds: cardinal de la partition de S
    :param S: liste de mots sur laquelle on entraine notre HMM
    :param nbSMin: nombre d'etat minimum
    :param nbSMax: nombre d'etat maximum
    :param limite: limite pour bw3_variante
    :param nbInit: nbombre d'initialisations pour bw3
    :param nbL: nombre de lettres pour le HMM
    """

    n = len(S)
    l = np.random.permutation(n)
    nb_state = []
    logV = []
    for nbS in range(nbSMin, nbSMax + 1):
        try:
            lv = 0
            for i in range(1, nbFolds + 1):
                f1 = int((i - 1) * n / nbFolds)
                f2 = int(i * n / nbFolds)
                learn = [S[l[j]] for j in range(f1)]
                learn += [S[l[j]] for j in range(f2, n)]
                test = [S[l[j]] for j in range(f1, f2)]
                h = HMM.bw3_variante(nbS, nbL, learn, nbInit, limite)
                lv += h.logV(test)
            logV.append(lv / nbFolds)
            nb_state.append(nbS)
        except KeyboardInterrupt:
            break
    plt.plot(nb_state, logV)
    plt.show()

def parties_to_donnees(adr):
    if type(adr) != str:
        raise TypeError("adr doit etre une chaine de caracteres")
    if adr == "":
        raise ValueError("adr ne doit pas etre une chaine de caracteres vide")

    data = open(adr, 'r')
    line = data.readline()
    J1 = []
    J2 = []
    liste = []
    while line != '':
        e1 = 0
        while line[e1] != ':':
            e1 += 1
        prec = int(line[e1 - 1])
        while line != '' and line[e1] == ':' and int(line[e1 - 1]) == prec:
            e2 = e1 + 1
            while line[e2] != ':':
                e2 += 1
            J1 += [HMM.change_simple(int(line[e2 + 1]) - 1)]
            J2 += [HMM.change_simple(int(line[e2 + 3]) - 1)]
            line = data.readline()
        liste += chaines_to_tuple(J1, J2)
        J1 = []
        J2 = []
    data.close()
    return liste

def epuration(S):
    S2 = []
    for i in S:
        if len(i) != 1:
            S2 += [i]
    return S2



#parties_to_donnees('test1', 'test1ep')

# L = text_to_list('anglais2000')
# print('toc', xval(20, L, 26, 2, 10, 5, 5))

# logV_vs_nb_iteration_bw1(1000, 30, text_to_list('anglais2000'))


# efficiency_vs_nb_state(10, text_to_list('anglais2000'), 53, 1000, 100, 1)

# efficiency_vs_nb_state(10, text_to_list('allemand2000'), 2, 1000, 100, 1)


# logV_vs_nb_iteration_bw1(1000, 45, text_to_list('anglais2000'))

# HMM.bw3(45, 26, text_to_list('espagnol2000'), 55, 12).save("hmm_espagnol")
# HMM.bw3(45, 26, text_to_list('suedois2000'), 55, 12).save("hmm_suedois")
# HMM.bw3(45, 26, text_to_list('neerlandais2000'), 55, 12).save("hmm_neerlandais")
# HMM.bw3(45, 26, text_to_list('neerlandais2000'), 55, 12).save("hmm_neerlandais")
# HMM.bw3(45, 26, text_to_list('elfique'), 55, 12).save("hmm_elfique")
# HMM.bw3(100, 26, text_to_list('anglais2000'), 55, 15).save("hmm_anglais_v2")
# HMM.bw3(100, 26, text_to_list('allemand2000'), 55, 15).save("hmm_allemand_v2")
# HMM.bw3(100, 26, text_to_list('suedois2000'), 55, 15).save("hmm_suedois_v2")
# HMM.bw3(100, 26, text_to_list('neerlandais2000'), 55, 15).save("hmm_neerlandais_v2")

# HMM.bw3(45, 26, text_to_list('anglais2000'), 200, 20).save("hmm_anglais_parfait")

# logV_vs_intialisation(100, 400, 45, text_to_list('anglais2000'))

"""
def chaine_to_tuple(mot):
    w = ()
    for i in range(len(mot)):
        w += (HMM.lettre_to_num(mot[i]),)
    return w

def text_to_list(adr):  # transforme un document texte contenant des mot en liste de mots comprehensibles par le HMM
    :param adr: addresse du fichier texte a convertir
    :return: liste de tuples correspondant aux mots se trouvant dans le fichier texte
    data = open(adr, 'r')
    texte = data.read()
    L = texte.split('\n')
    data.close()
    L2 = []
    for w in L:
        L2 += [chaine_to_tuple(w)]
    return L2[:-1]
"""

#print(len(S))
#print(S)
#efficiency_vs_nb_state(10, S, 2, 1000, 50, 1)
#HMM.bw3(2, 9, S, 50, 2)
#a = int(input('debut')) + 1
#b = int(input('fin')) + 1
#b = sys.argv[1]
#a = sys.argv[2]
#efficiency_vs_nb_state(1, S, 1, 2, 2, 1)