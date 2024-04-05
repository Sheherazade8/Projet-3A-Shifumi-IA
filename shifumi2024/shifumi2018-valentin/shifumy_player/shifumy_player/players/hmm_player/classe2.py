#-*- coding: utf-8 -*-

# Mac Donald  Kilian
# classe 2
# cree le 20/06/2018

import numpy as np
import random
import time
import copy
from math import *

def verif_crois(w):
    var = int(int(w[-1])/3)
    l = ()
    for i in range(len(w) - 1):
        l += (w[i],)
    wr = l + (int(0 + 3 * var),)
    wp = l + (int(1 + 3 * var),)
    ws = l + (int(2 + 3 * var),)
    return wr, wp, ws

def esp(p):
    new = [p[0] + p[1] + p[2], p[3] + p[4] + p[5], p[6] + p[7] + p[8]]
    esper = [new[2] - new[1], new[0] - new[2], new[1] - new[0]]
    return esper


class HMM:
    # Defint un HMM

    valeurs  = {'R':0, 'P':1, 'S':2, 0:'R', 1:'P', 2:'S'}
    paires = {'RR':0, 'RP':1, 'RS':2, 'PR':3, 'PP':4, 'PS':5, 'SR':6, 'SP':7, 'SS':8,
              0:'RR', 1:'RP', 2:'RS', 3:'PR', 4:'PP', 5:'PS', 6:'SR', 7:'SP', 8:'SS'}

    def __init__(self, letters_number, states_number, initial, transitions, emissions):

        # The number of letters
        if type(letters_number) != int or letters_number <= 0:
            raise ValueError("The letters number should be a positive integer")
        self.__letters_number = letters_number

        # The number of states
        if type(states_number) != int or states_number <= 0:
            raise ValueError("The states number should be a positive integer")
        self.__states_number = states_number

        # The vector defining the initial weights
        self.check_initial(initial)
        self.__initial = initial

        # The array defining the transitions
        self.check_transitions(transitions)
        self.__transitions = transitions

        # The list of vectors defining the emissions
        self.check_emissions(emissions)
        self.__emissions = emissions

    @property
    def letters_number(self):
        return self.__letters_number

    @property
    def states_number(self):
        return self.__states_number

    @property
    def initial(self):
        return self.__initial

    @property
    def transitions(self):
        return self.__transitions

    @property
    def emissions(self):
        return self.__emissions

    @initial.setter
    def initial(self, values):
        self.check_initial(values)
        self.__initial = values

    @staticmethod
    def check_initial(value):
        """
        :param value: Vecteur d'initial
        :return: Renvoie une erreur si le tableau n'est pas de dimension 1, e une valeur negative ou e une somme de
        valeurs differente de 1.
        """
        HMM.check_probability_array(value)
        if value.ndim != 1:
            raise ValueError("The parameter value should be a one dimension array")

    @staticmethod
    def check_probability_array(array):
        """
        :param array: Tableau numpy
        :return: Renvoie une erreur si la somme des valeurs sur une ligne ne vaut pas 1 et si'il y a des valeurs
        negatives
        """
        if not isinstance(array, np.ndarray):
            raise TypeError("The parameter array should be a np.ndarray")
        if array.ndim == 1:
            sum = 0
            for value in array:
                if value < 0:
                    raise ValueError("The probabilities should be positive numbers")
                sum += value
            if not np.isclose([sum], [1]):
                raise ValueError("The probabilities sum should be equal to 1 for each lign")
        elif array.ndim == 2:
            for i in range(array.shape[0]):
                sum = 0
                for j in range(array.shape[1]):
                    if array[i, j] < 0:
                        raise ValueError("The probabilities should be positive numbers")
                    sum += array[i, j]
                if not np.isclose([sum], [1]):
                    raise ValueError("The probabilities sum should be equal to 1 for each lign")
        else:
            raise ValueError("The dimension of the parameter array should be 1 or 2")

    def check_transitions(self, value):
        """
        :param value: Matrice de transitions
        :return: Renvoie une erreur si la somme des valeurs sur une ligne ne vaut pas 1 et si'il y a des valeurs
        negatives
        """
        self.check_dim(value, self.states_number, self.states_number)
        self.check_probability_array(value)

    def check_emissions(self, value):
        """
        :param value: Matrice d'emissions
        :return: Renvoie une erreur si la somme des valeurs sur une ligne ne vaut pas 1 et si'il y a des valeurs
        negatives
        """
        self.check_dim(value, self.states_number, self.letters_number)
        self.check_probability_array(value)

    @staticmethod
    def check_dim(tableau, nb_lignes, nb_colonnes):
        """
        :param tableau: Tableau numpy
        :param nb_lignes: Nombre de lignes attendues
        :param nb_colonnes: Nombre de colonnes attendues
        :return: Renvoie une erreur si les dimensions du tableau ne sont pas celles attendues
        """
        if type(nb_lignes) != int:
            raise TypeError('nb_lignes doit etre un entier')
        if type(nb_colonnes) != int:
            raise TypeError('nb_colonnes doit etre un entier')
        if nb_lignes < 0:
            raise ValueError("nb_lignes doit etre positif")
        if nb_colonnes < 0:
            raise ValueError("nb_colonnes doit etre positif")
        if tableau.ndim != 2:
            raise ValueError("The parameter tableau should be a 2D array")
        if tableau.shape[0] != nb_lignes or tableau.shape[1] != nb_colonnes:
            raise ValueError("Le tableau est de mauvaises dimensions")

    def check_w(self, w):
        """
        :param w: Tuple
        :return: Renvoie une erreur si w n'est pas un tuple ou s'il contient des elements qui ne sont pas des
        observables
        """
        if type(w) != tuple:
            raise TypeError("w doit etre un tuple")

        if len(w) == 0:
            raise ValueError("w ne doit pas etre vide")

        for x in w:
            if type(x) != int:
                raise TypeError('Les lettres d\'un mot doivent etre des entiers')
            if x >= self.letters_number:
                raise ValueError("Tous les elements doivent appartenir aux observables")

    @transitions.setter
    def transitions(self, value):
        self.check_transitions(value)
        self.__transitions = value

    @emissions.setter
    def emissions(self, value):
        self.check_emissions(value)
        self.__emissions = value

    @staticmethod
    def load(adr):
        # Charge un HMM depuis une adresse donnee
        """
        :param adr: Nom d"un fichier texte contenant les donnees d'un HMM
        :return: Un HMM
        """
        if type(adr) != str:
            raise TypeError("adr doit etre une chaine de caracteres")
        if adr == "":
            raise ValueError("adr ne doit pas etre une chaine de caracteres vide")

        data = open(adr, 'r')
        line = data.readline()
        hash_count = 0
        while hash_count <= 4:
            if line[0] == '#':
                if hash_count == 0:
                    letters_number = int(data.readline())
                if hash_count == 1:
                    states_number = int(data.readline())
                if hash_count == 2:
                    initial = np.zeros((states_number))
                    for i in range(states_number):
                        initial[i] = float(data.readline())
                if hash_count == 3:
                    transitions = np.zeros((states_number, states_number))
                    for i in range(states_number):
                        ligne = data.readline().split()
                        for j in range(len(ligne)):
                            transitions[i, j] = float(ligne[j])
                if hash_count == 4:
                    emissions = np.zeros((states_number, letters_number))
                    for i in range(states_number):
                        ligne = data.readline().split()
                        for j in range(len(ligne)):
                            emissions[i, j] = float(ligne[j])
                hash_count += 1
            line = data.readline()
        data.close()
        return HMM(letters_number, states_number, initial, transitions, emissions)

    def __str__(self):
        # Affiche le HMM
        """
        :return: Le HMM correspondant en affichant le nom des differentes entrees
        """
        return 'The number of letters : ' + str(self.__letters_number) + '\n' + ' The number of states : ' + str(
            self.__states_number) + '\n' + 'The initial vector : ' + str(
            self.__initial) + '\n' + 'The internal transitions : ' + '\n' + str(
            self.__transitions) + '\n' + 'The emissions : ' + '\n' + str(self.__emissions)

    @staticmethod
    def draw_multinomial(
            array):  # liste proba, sort indice en fonction 0,2;0,3.0,4 = il sprt 0 avec proba 0,2, 1 avec proba 0,3 ...
        """
        :param array: Tableau de probabilites dont la somme des vleurs vaut 1
        :return: Un indice du tableau avec une probabilite egale e la valeur correspondant e l'indice
        """
        if not isinstance(array, np.ndarray):
            raise TypeError("The parameter array should be a np.ndarray")
        if array.ndim != 1:
            raise ValueError("The parameter array should be a 1D array")
        HMM.check_probability_array(array)
        random.seed(time.clock())
        random_number = random.random()
        probability_sum = 0
        for i, probability in enumerate(array):
            probability_sum += probability
            if random_number <= probability_sum:
                return i
        return array.shape[1] - 1

    def generate_random(self, n):
        """
        :param n: Longueur souhaitee de la liste
        :return: Un tuple d'oservables de longueur n ou chaque observable est choisit avec une probabilite
        egale e sa probabilite correspondante
        """
        if type(n) != int:
            raise ValueError("n doit etre un entier")
        if n < 0:
            raise ValueError("n doit etre positif")
        sequence = ()
        actual_state = self.draw_multinomial(self.initial)
        for i in range(n):
            sequence += (self.draw_multinomial(self.emissions[actual_state]),)
            actual_state = self.draw_multinomial(self.transitions[actual_state])
        return sequence

    def save(self, address):
        """
        :param address: Nom du fichier
        :return: HMM sous fichier texte nomme par address
        """
        if type(address) != str:
            raise TypeError("adr doit etre une chaine de caracteres")
        if address == "":
            raise ValueError("adr ne doit pas etre une chaine de caracteres vide")

        nfile = open(address, "w")
        nfile.write("# The number of letters\n")
        nfile.write(str(self.letters_number) + "\n")
        nfile.write("# The number of states\n")
        nfile.write(str(self.states_number) + "\n")
        nfile.write("# The initial transitions\n")
        for p in self.initial:
            nfile.write(str(p) + "\n")
        nfile.write("# The internal transitions\n")
        for i in range(len(self.transitions)):
            for j in range(len(self.transitions[0])):
                nfile.write(str(self.transitions[i, j]) + " ")
            nfile.write("\n")
        nfile.write("# The emissions" + "\n")
        for i in range(len(self.emissions)):
            for j in range(len(self.emissions[0])):
                nfile.write(str(self.emissions[i, j]) + " ")
            nfile.write("\n")
        nfile.close()

    def __eq__(self, hmm2):
        # Definition de l'egalite entre 2 HMM
        if not isinstance(hmm2, HMM):
            raise TypeError("ne peut pas verifier une egalite entre un HMM et un objet qui n'est pas un HMM")
        if self.letters_number != hmm2.letters_number:
            return False
        if self.states_number != hmm2.states_number:
            return False
        if not np.isclose(self.initial, hmm2.initial):
            return False
        if not np.isclose(self.transitions, hmm2.transitions):
            return False
        if not np.isclose(self.emissions, hmm2.emissions):
            return False
        return True

    def pfw(self, w):  # liste d'observable 1 -N , prend un endroit , proba qu'il sort tou ce qui a eu avant
        """""
        :param w: tuple d'observables
        :return: Probabilite d'obtenir cette liste
        """
        self.check_w(w)
        f = self.initial * self.emissions[:, w[0]]
        for i in range(1, len(w)):
            f = np.dot(f, self.transitions) * self.emissions[:, w[i]]
        return np.sum(f)

    def pfw2(self, w):
        self.check_w(w)
        l = ((w[0]),)
        wr, wp, ws = verif_crois(l)
        somme = np.log(self.pfw(wr) + self.pfw(wp) + self.pfw(ws))
        for i in range(1, len(w)):
            l += (w[i],)
            wr, wp, ws = verif_crois(l)
            somme += np.log(self.pfw(wr) + self.pfw(wp) + self.pfw(ws))
        return somme

    def pbw(self, w):  # liste d'observable 1 -N , prend un endroit , proba qu'il sort tou ce qui a eu apres
        """
        :param w: tuple d'observables
        :return: Probabilite d'obtenir cette liste
        """
        self.check_w(w)
        b = np.array([1] * self.states_number)
        for i in range(len(w) - 2, -1, -1):
            b = np.dot(self.transitions, self.emissions[:, w[i + 1]] * b)
        return np.sum(self.initial * b * self.emissions[:, w[0]])

    def predit(self, w):  # sort la lettre qui a le plus de chance d'apparaitre apres une liste d'observable
        """
        :param w: tuple d'observables
        :return: L'observable ayant la plus grande probabilite d'apparaitre ensuite
        """
        self.check_w(w)
        h = self.initial
        for i in range(1, len(w)):
            h = np.dot(self.emissions[:, w[i]] * h, self.transitions)
        p = np.dot(h, self.emissions)
        new = [p[0] + p[1] + p[2], p[3] + p[4] + p[5], p[6] + p[7] + p[8]]
        val = new.index(max(new))
        return val

    def predit_bat(self, w):  # sort la lettre qui bat la lettre anticipée avec la meilleure espérence
        """
        :param w: tuple d'observables
        :return: L'observable ayant la plus grande probabilite d'apparaitre ensuite
        """
        self.check_w(w)
        h = self.initial
        for i in range(1, len(w)):
            h = np.dot(self.emissions[:, w[i]] * h, self.transitions)
        p = np.dot(h, self.emissions)
        esper = esp(p)
        val = esper.index(max(esper))
        return val

    def viterbi(self, w):  # le chemin le plus probable d'un mot
        """
        :param w: tuple d'observables
        :return: La liste d'etats la plus probable correspondant e ce chemin
        """
        self.check_w(w)
        chemin_1 = []
        chemin_2 = []
        liste_etats = []
        p_1 = self.initial * self.emissions[:, w[0]]
        p_2 = self.initial * self.emissions[:, w[0]]
        for i in range(self.states_number):
            chemin_1 += [[i]]
            chemin_2 += [[i]]
            liste_etats += [i]
        for i in range(1, len(w)):
            for k in range(self.states_number):
                m = 0
                j_retenu = 0
                for j in range(self.states_number):
                    a = m
                    b = p_1[j] * self.transitions[j, k]
                    m = max(a, b)
                    if m == b:
                        j_retenu = j
                chemin_2[k] = chemin_1[j_retenu] + [k]
                p_2[k] = m * self.emissions[k, w[i]]
            chemin_1 = copy.deepcopy(chemin_2)
            p_1 = copy.deepcopy(p_2)
        return chemin_2[np.argmax(p_2)], np.log(np.max(p_2))

    def f(self, w):  # proba de les t premiere lettre du mot pour finir dans l etat k
        """
        :param w: tuple d'observable
        :return: Matrice de dimension nb_d'etats * len(w) correspondant au f du polycopie 4.4
        """
        f = np.zeros((self.states_number, len(w)))
        f[:, 0] = self.initial * self.emissions[:, w[0]]
        for i in range(1, len(w)):
            f[:, i] = np.dot(f[:, i - 1], self.transitions) * self.emissions[:, w[i]]

        return f

    def b(self, w):  # proba en partant de k pour finir le mot
        """
        :param w: tuple d'observable
        :return: Matrice de dimension nb_d'etats * len(w) correspondant au b du polycopie 4.4
        """
        b = np.zeros((self.states_number, len(w)))
        b[:, len(w) - 1] = np.array([1] * self.states_number)
        for i in range(len(w) - 2, -1, -1):
            b[:, i] = np.dot(self.transitions, self.emissions[:, w[i + 1]] * b[:, i + 1])
        return b

    def gamma(self, w):
        """
        :param w: tuple d'observable
        :return: Matrice de dimension nb_d'etats * len(w) correspondant au gamma du polycopie 4.4
        """
        f = self.f(w)
        b = self.b(w)
        return (f * b) / np.einsum('kt,kt->t', b, f)

    def xi(self, w):
        """
        :param w: tuple d'observable
        :return: Matrice de dimension nb_d'etats * nb_d'etats * len(w) correspondant au xi du polycopie 4.4, sans boucle
        """
        f = self.f(w)[:, :-1]
        b = self.b(w)[:, 1:]
        emissions = self.emissions[:, w[1:]]
        xi = np.einsum('kt,kl,lt,lt->klt', f, self.transitions, emissions, b)
        v = np.einsum('kt,kl,lt,lt->t', f, self.transitions, emissions, b)
        somme = np.tile(v, (self.states_number, self.states_number, 1))
        xi = xi / somme
        return xi

    def xi2(self, w):
        """
        :param w: tuple d'observable
        :return: Matrice de dimension nb_d'etats * nb_d'etats * len(w) correspondant au xi du polycopie 4.4
        """
        f = self.f(w)[:, :-1]
        b = self.b(w)[:, 1:]
        emissions = self.emissions[:, w[1:]]
        xi = np.einsum('kt,kl,lt,lt->klt', f, self.transitions, emissions, b)
        for t in range(xi.shape[2]):
            xi[:, :, t] = xi[:, :, t] / np.sum(xi[:, :, t])
        return xi

    def bw1(self, S):  # modifie hmm pour augmenter la vraisemblance des mot entres
        """
        :param S: Liste de tuple d'observables
        :return: Modifie les valeurs des matrices du HMM pour augmenter la vraisemblance de S
        """
        if type(S) != list:
            raise TypeError("S doit etre une liste")
        if len(S) == 0:
            raise ValueError("S ne doit pas etre vide")
        for w in S:
            self.check_w(w)
        pi = np.zeros(self.states_number)
        T = np.zeros((self.states_number, self.states_number))
        O = np.zeros((self.states_number, self.letters_number))
        for j in range(len(S)):
            gamma = self.gamma(S[j])
            xi = self.xi(S[j])
            pi += np.array(gamma[:, 0])
            t = np.einsum('klt->kl', xi)
            T += t
            for t in range(len(S[j])):
                O[:, S[j][t]] += gamma[:, t]
        self.transitions = (T.T / T.sum(1)).T
        self.emissions = (O.T / O.sum(1)).T
        self.initial = pi / pi.sum()

    @staticmethod
    def bw2(nbS, nbL, S, N):  # creer un hmm , et avec bw1, l'ameliore
        """
        :param nbS: Nombre d'etats
        :param nbL: Nombre de sommets
        :param S: Liste de tuple d'observables
        :param N: nombre d iteration
        :return: Un HMM genere aleatoirement e nbS etats et nbL sommets mis e jour N fois grace e bw1 pour augmenter
        la vraisemblance
        """
        if type(N) != int or N < 0:
            raise ValueError("N doit etre un entier positif")
        hmm = HMM.gen_HMM(nbL, nbS)
        for i in range(N):
            hmm.bw1(S)
        return hmm

    @staticmethod
    def bw3(nbS, nbL, S, N, M):  # creer M hmm avec bw2, et prend le meilleur
        """
        :param nbS: Nombre d'etats
        :param nbL: Nombre de sommets
        :param S: Liste de tuple d'observables
        :param N: nombre d iterations == nombre de fois que bw1 est repeter pour tout les hmm
        :param M: nombre d initialisation differentes == nombre de hmm que l'on creer avec bW2
        :return: Le HHMi avec 0 <= i <= M-1 qui maximise la vraisemblance de S
        """
        if type(M) != int or M < 0:
            raise ValueError("M doit etre un entier positif")
        max_logV = -float('inf')
        hmm = None
        for i in range(M):
            h = HMM.bw2(nbS, nbL, S, N)
            logV = h.logV(S)
            if max_logV < logV:
                max_logV = logV
                hmm = h
        return hmm

    @staticmethod
    def bw2_variante(nbS, nbL, S, limite, n=10):
        # Meme fonction que bw2 mais s'arrete automatiquement lorsque la log vraisemblance
        # augmente d'une valeur inferieure
        # au parametre limite en N iterations

        if (type(n) != int or n <= 0):
            raise ValueError("n doit etre un entier strictement positif")
        if type(limite) != int and type(limite) != float or limite < 0:
            raise ValueError("le parametre limite doit etre un nombre positif")

        hmm = HMM.gen_HMM(nbL, nbS)
        res = [None] * (n - 1)
        res.append(hmm.logV(S))
        while res[0] is None or res[0] - res[-1] > limite:
            hmm.bw1(S)
            res.append(hmm.logV(S))
            del res[0]
        return hmm

    @staticmethod
    def bw3_variante(nbS, nbL, S, M, limite, n=10):
        # Meme fonction que bw2 mais s'arrete automatiquement lorsque la log vraisemblance
        # augmente d'une valeur inferieure
        # au parametre limite en 10 iterations

        if type(M) != int or M < 0:
            raise ValueError("M doit etre un entier positif")
        max_logV = -float('inf')
        hmm = None
        for i in range(M):
            h = HMM.bw2_variante(nbS, nbL, S, limite, n)
            logV = h.logV(S)
            if max_logV < logV:
                max_logV = logV
                hmm = h
        return hmm

    @staticmethod
    def gen_vect(n):  # vecteur de longueur n somme = 1
        if type(n) != int or n < 0:
            raise ValueError("M doit etre un entier strictement positif")
        if n == 1:
            return np.ones(1)
        else:
            L = [(i, np.random.random()) for i in range(n - 1)]
            L = sorted(L, key=lambda x: x[1])
            v = np.zeros(n)
            v[L[0][0]] = L[0][1]
            for i in range(1, n - 1):
                v[L[i][0]] = L[i][1] - L[i - 1][1]
            v[n - 1] = 1 - L[n - 2][1]
        return v

    @staticmethod
    def gen_HMM(nbL, nbS):  # creer hmm aleatoire
        initial = HMM.gen_vect(nbS)
        transitions = np.zeros((nbS, nbS))
        for i in range(nbS):
            transitions[i, :] = HMM.gen_vect(nbS)
        emissions = np.zeros((nbS, nbL))
        for i in range(nbS):
            emissions[i, :] = HMM.gen_vect(nbL)
        return HMM(nbL, nbS, initial, transitions, emissions)

    def logV(self, S):  # vraisemblance d'un mot
        """
        :param S: Liste de tuple d'observables
        :return: La log vraisemblance de S
        """
        somme = 0
        for w in S:
            self.check_w(w)
            somme += np.log(self.pfw(w))
        return somme

    def logV2(self, S):
        somme = 0
        for w in S:
            self.check_w(w)
            somme += self.pfw2(w)
        return somme

    @staticmethod
    def change_simple(x):
        return HMM.valeurs[x]

    @staticmethod
    def change_double(x, y = None):
        if y == None:
            return HMM.paires[x]
        return HMM.paires[x + y]

"""
    @staticmethod
    def num_to_lettre(n):
        :param n: Entier entre 0 et 25
        :return: La lettre de l'alphabet correspondant e n
        if type(n) != int:
            raise TypeError('le numero doit etre un entier')
        if n < 0 or n > 25:
            raise ValueError('le numero doit etre compris entre 0 et 25')
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        return alphabet[n]

    @staticmethod
    def lettre_to_num(lettre):
        :param lettre: Lettre de l'alphabet
        :return: L'indice de la lettre
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        if type(lettre) != str:
            raise TypeError('la lettre doit etre un caractere')
        if lettre not in alphabet:
            raise ValueError('la lettre doit etre dans l\'alphabet')
        return alphabet.index(lettre)

    def gen_mot_lettres(self, n):
        word = self.generate_random(n)
        mot = ""
        for l in word:
            mot += HMM.num_to_lettre(l)
        return mot

    def pfw2(self, w):
        self.check_w(w)
        l = (w[0],)
        wr, wp, ws = verif_crois(l)
        fr = self.initial * self.emissions[:, wr[0]]
        fp = self.initial * self.emissions[:, wp[0]]
        fs = self.initial * self.emissions[:, ws[0]]
        f = fr + fp + fs
        for i in range(1, len(w)):
            l += (w[i],)
            wr, wp, ws = verif_crois(l)
            fr = np.dot(f, self.transitions) * self.emissions[:, wr[i]]
            fp = np.dot(f, self.transitions) * self.emissions[:, wp[i]]
            fs = np.dot(f, self.transitions) * self.emissions[:, ws[i]]
            f = fr + fp + fs
        return np.sum(f)

    def pfw2(self, w):
        somme = 0
        l = (w[0],)
        wr, wp, ws = verif_crois(l)
        somme += np.log(self.pfw(wr) + self.pfw(wp) + self.pfw(ws))
        for i in range(1, len(w)):
            l = ()
            for j in range(i):
                l += (w[j],)
            wr, wp, ws = verif_crois(l)
            somme += np.log(self.pfw(wr) + self.pfw(wp) + self.pfw(ws))
        return somme
"""