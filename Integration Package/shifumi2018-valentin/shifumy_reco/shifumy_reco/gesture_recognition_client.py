# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import socket
import time
from threading import Thread, Condition

import cv2 as cv
import numpy as np
from shifumy_player.base import str_rps, ROCK, PAPER, SCISSORS
from shifumy_reco.base import RECO_CLASSIFIER_FILE_PATH, RECO_TRAIN_IMAGES_WARMUP_DIR_PATH
from shifumy_reco.gesture_classifier import RpsGestureClassifier
from shifumy_reco.utils import str_id_generator


import mediapipe as mp
from sklearn.neighbors import KNeighborsClassifier
import csv

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 50000

class AbstractGestureRecognitionClient(Thread):
    def __init__(self, clf, host=DEFAULT_HOST, port=DEFAULT_PORT):
        Thread.__init__(self)
        # 1) création du socket :
        print('création du socket')
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.expected_gesture = None
        self.clf = clf  # type: GestureRecognitionMain
        self.lock_expected_gesture = Condition()

        while True:
            # 2) envoi d'une requête de connexion au serveur :
            print("envoi d'une requête de connexion au serveur {}"
                  .format((host, port)))
            try:
                self.mySocket.connect((host, port))
                break
            except socket.error:
                print("La connexion a échoué.")
                time.sleep(1)
                print('Retry')

        print("Connexion établie avec le serveur.")

    def get_gesture(self):
        raise NotImplementedError

    def get_eog(self):
        raise NotImplementedError

    def run(self):
        try:
            while 1:
                # 3) Dialogue avec le serveur :
                msgServeur = self.mySocket.recv(1024).decode("Utf8")
                print("Received", msgServeur, end="")
                if "Wait gesture" in msgServeur:
                    # le serveur a besoin d'un geste
                    split_msgServeur = msgServeur.split(":")
                    with self.lock_expected_gesture:
                        # si il y a le nom du geste demandé
                        if len(split_msgServeur) > 1:
                            self.expected_gesture = int(split_msgServeur[-1])
                            print("; {}:{}".format(self.expected_gesture, str_rps(self.expected_gesture)))
                        else:
                            self.expected_gesture = None
                            print("")
                        self.clf.reset_sequence_frames()

                    # self.lock_expected_gesture.notify_all() # todo verifier que ca ne fait pas planter ici
                    g = self.get_gesture()
                    msgClient = str_rps(g)
                    print("Send", msgClient)
                    self.mySocket.send(msgClient.encode("Utf8"))
                elif msgServeur == "Wait end":
                    print("")
                    # le serveur veut que le joueur enleve sa main
                    with self.lock_expected_gesture:
                        # a la fin d'un geste on ne veut plus enregistrer l'image
                        self.expected_gesture = None
                    self.get_eog()
                    msgClient = "EOG"
                    self.mySocket.send(msgClient.encode("Utf8"))
        finally:
            # 4) Fermeture de la connexion :
            print("Connexion interrompue.")
            self.mySocket.close()

class HandGestureRecognition(AbstractGestureRecognitionClient):
    def __init__(self, clf, host=DEFAULT_HOST, port=DEFAULT_PORT):
        AbstractGestureRecognitionClient.__init__(self, clf, host=host, port=port)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.8,
                                         min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.knn = KNeighborsClassifier(n_neighbors=2)
        self.data = []
        self.labels = []
        self.path = []
        self.history = []
        self.result = None
        self.lock = Condition()

    def load_data(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for row in reader:
                # Suppose the label is the first column and the rest are data
                self.data.append(np.array(row[3][1:-1].split()).astype(np.float64))
                self.labels.append(row[0])
                self.path.append(row[2])
        self.data = np.array(self.data)
        self.labels = np.array(self.labels).astype(int)
        self.path = np.array(self.path)

    def landmarkFormat(self, handLandmarks):
        def normalize(landmarks):
            x = np.array([landmark.x for landmark in landmarks])
            y = np.array([landmark.y for landmark in landmarks])
            z = np.array([landmark.z for landmark in landmarks])
            x = (x - np.min(x)) / (np.max(x) - np.min(x))
            y = (y - np.min(y)) / (np.max(y) - np.min(y))
            z = (z - np.min(z)) / (np.max(z) - np.min(z))
            return x, y, z

        def cartesian_to_polar(landmarks):
            x, y, z = normalize(landmarks)
            r = np.sqrt(x**2 + y**2 + z**2)
            theta = np.where(r != 0, np.arccos(z/r), 0)
            phi = np.where(x != 0, np.arctan2(y, x), 0)
            return np.array([r, theta, phi]).T

        return cartesian_to_polar(handLandmarks.landmark)

    def train_knn(self):
        self.knn.fit(self.data, self.labels)

    def draw_landmarks(self):
    
        nb_frame = 10
        label_names = ['Feuille', 'Pierre', 'Ciseaux']

        # cap = cv.VideoCapture(0)
        cap = self.cap
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Conversion de l'image de BGR à RGB
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            results = self.hands.process(image)
            history = self.history
            # Dessin des landmarks de la main
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Transformation et prédiction du cluster
                    x0, y0, z0 = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y, hand_landmarks.landmark[0].z
                    transformed_landmarks = self.landmarkFormat(hand_landmarks)
                    transformed_landmarks_flat = np.ravel(transformed_landmarks).reshape(1, -1)
                    cluster_label = self.knn.predict(transformed_landmarks_flat)
                    cluster_name = label_names[cluster_label[0]]
                    # Affichage la classe sur l'image
                    # cv.putText(image, "cluster_name", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
                    history.append([cluster_label[0], x0, y0, z0])
                    self.history = history
            # Affichage de l'image résultante
            cv.imshow('MediaPipe Hands', image)

            # result si 10 frames
            if len(self.history) >= nb_frame:
                self.get_gesture()
                self.history = self.history[-nb_frame:]

            # Arrêt avec la touche 'q'
            if cv.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()
    
    def get_gesture(self):
        """ Renvoie la classe prédite si la main est stable sur les 5 dernières frames"""

        nb_frame = 5
        bins = [ROCK, PAPER, SCISSORS]
        frames = self.history[-nb_frame:]
        labels = [frame[0] for frame in frames]
        positions = [frame[1:3] for frame in frames]
        # Calcul de la différence moyenne entre les positions (en pourcentage)
        diff = np.mean(np.abs(np.diff(positions, axis=0)), axis=0)*100 

        # Si une seule classe détecté et moins de 1% de mouvement
        if len(set(labels)) == 1 and diff[0] < 1 and diff[1] < 1:
            self.result = bins[labels[0]]
            print("  > Gesture detected:", self.result)
            self.get_eog()
            return self.result
        else: # sinon on réinitialise
            self.result = None
            self.history = []


    def get_eog(self):
        """ Attend la fin du geste : la main doit sortir du cadre """
        print('Wait end of gesture')

        self.lock.acquire()  # Acquérir le verrou avant de commencer les attentes
        try:
            # tant que le geste n'est pas détecté
            while self.result is None: 
                self.lock.wait()

            # Ré-acquérir le verrou pour la prochaine condition, car chaque wait() nécessite que le verrou soit détenu
            # Cette ré-acquisition n'est pas nécessaire avec l'utilisation de `try`, c'était pour démonstration.
            # tant que la main est dans le cadre
            x0, y0 = self.history[-1][1], self.history[-1][2]
            while x0 < 0.9 and x0 > 0.1 and y0 < 0.9 and y0 > 0.1:
                self.lock.wait()
                x0, y0 = self.history[-1][1], self.history[-1][2]
        finally:
            self.lock.release()  # Toujours libérer le verrou, même si une exception est levée

        self.result = None
        self.history = []
        print('  > End of gesture!')
        return


class GestureRecognitionClient(AbstractGestureRecognitionClient):
    def __init__(self, lock, clf, n_frames, ratio=0.9,
                 host=DEFAULT_HOST, port=DEFAULT_PORT):
        AbstractGestureRecognitionClient.__init__(self, clf, host=host, port=port)
        self.lock = lock
        self.n_frames = n_frames
        self.result = None
        self.ratio = ratio

    def get_gesture(self):
        bins = [ROCK, PAPER, SCISSORS]
        self.lock.acquire()
        try:
            while True:
                with self.lock:
                    while len(self.clf.sequence[-self.n_frames:]) < self.n_frames or \
                            any([x is None for x in self.clf.sequence[-self.n_frames:]]):
                        # print("Sequence not ready: {}".format(self.clf.sequence))
                        self.lock.wait()

                    print("sequence ready to get gesture: {}".format(self.clf.sequence[-self.n_frames * 2:]))

                    h, a = np.histogram(self.clf.sequence[-self.n_frames:],
                                        bins=np.arange(4) - 0.5)
                    h = h / np.sum(h)
                    i_max = np.argmax(h)
                    if h[i_max] > self.ratio:
                        self.result = bins[i_max]
                        break
                    self.clf.reset_sequence()
        finally:
            self.lock.release()
    

    def get_eog(self):
        print('Wait end of gesture')
        self.lock.acquire()
        try:
            while len(self.clf.sequence) < self.n_frames or not all([x is None for x in self.clf.sequence[-self.n_frames:]]):
                self.lock.release()
                time.sleep(0.1)  # Pause active de 100 ms
                self.lock.acquire()
            self.result = None
            print('  > End of gesture!')
        finally:
            self.lock.release()

    # def run(self):
    #     bins = [ROCK, PAPER, SCISSORS]
    #     while True:
    #         with self.lock:
    #             self.lock.wait()
    #             if len(self.clf.sequence) >= self.n_frames:
    #                 sub_seq = self.clf.sequence[-self.n_frames:]
    #                 if any([x is None for x in sub_seq]):
    #                     continue
    #                 h, a = np.histogram(self.clf.sequence[-self.n_frames:],
    #                                     bins=np.arange(4)-0.5)
    #                 h = h / np.sum(h)
    #                 i_max = np.argmax(h)
    #                 if h[i_max] > self.ratio:
    #                     self.result = bins[i_max]
    #                     return


class GestureRecognitionMain():
    def __init__(self, clf_filename=RECO_CLASSIFIER_FILE_PATH):
        cap = cv.VideoCapture(0) # 0: default camera

        win_name = 'Mosaic'
        cv.namedWindow(win_name, cv.WINDOW_FULLSCREEN)
        cv.setWindowProperty(win_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        # win_name = 'Front mosaic'
        # cv.namedWindow(win_name, cv.WINDOW_FULLSCREEN)
        # cv.setWindowProperty(win_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        # cv.moveWindow(win_name, 0, 800)

        height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        print('FPS:', cap.get(cv.CAP_PROP_FPS))
        print('Height:', height)
        print('Width:', width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, height // 2)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, width // 2)
        # cap.set(cv.CAP_PROP_FPS, 25)
        print('FPS:', cap.get(cv.CAP_PROP_FPS))
        print('Height:', cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        print('Width:', cap.get(cv.CAP_PROP_FRAME_WIDTH))

        fps = cap.get(cv.CAP_PROP_FPS)
        n_frames = int(fps // (15/3))
        print(n_frames)

        lock = Condition()

        self.lock = lock
        self.clf = RpsGestureClassifier.load(clf_filename)
        self.cap = cap
        self.sequence = None
        self.reset_sequence()
        self.sequence_frames = None
        self.sequence_expected_gesture = None
        self.reset_sequence_frames()
        self.result = None

    def reset_sequence(self):
        self.sequence = []

    def reset_sequence_frames(self):
        self.sequence_frames = []
        self.sequence_expected_gesture = []

    def main_loop(self):
        # state = 'wait_gesture'

        # n_frames = 5
        # client_thread = GestureRecognitionClient(
        #     lock=self.lock, clf=self, n_frames=n_frames)

        client_thread = HandGestureRecognition(clf=self)
        

        client_thread.start()
        global_timestamp = int(time.time())
        global_random_id = str_id_generator(size=6)
        global_idx_saved_frame = 0
        while True:
            # print('Running...')
            with self.lock:
                # print('    Read frame')
                ret, frame = self.cap.read()
                # print('    ', ret)
                # print('    Classify frame')
                
                # y = self.clf.predict(frame)

                # if y is not None:  # something is on the screen
                #     with client_thread.lock_expected_gesture:
                #         if client_thread.expected_gesture is not None:
                #             self.sequence_expected_gesture.append(str_rps(client_thread.expected_gesture, language='EN'))
                #             self.sequence_frames.append(frame)

                # with client_thread.lock_expected_gesture:
                #     if client_thread.expected_gesture is None and \
                #             len(self.sequence_frames) > 0:
                #         global_id = "{}_{}".format(global_timestamp, global_random_id)
                #         warmup_dir_this_execution = RECO_TRAIN_IMAGES_WARMUP_DIR_PATH / global_id
                #         warmup_dir_this_execution.mkdir(parents=True, exist_ok=True)
                #         for idx_img, img in enumerate(self.sequence_frames):
                #             img_name = "{}_{}.png".format(self.sequence_expected_gesture[idx_img], global_idx_saved_frame)
                #             out_path = warmup_dir_this_execution / img_name
                #             cv.imwrite(str(out_path), img)
                #             global_idx_saved_frame += 1

                #         self.reset_sequence_frames()

                y = self.result

                if y is not None:
                    self.sequence_expected_gesture.append(str_rps(client_thread.expected_gesture, language='EN'))
                    self.sequence_frames.append(frame)
                if y is None and len(self.sequence_frames) > 0:
                    global_id = "{}_{}".format(global_timestamp, global_random_id)
                    warmup_dir_this_execution = RECO_TRAIN_IMAGES_WARMUP_DIR_PATH / global_id
                    warmup_dir_this_execution.mkdir(parents=True, exist_ok=True)
                    for idx_img, img in enumerate(self.sequence_frames):
                        img_name = "{}_{}.png".format(self.sequence_expected_gesture[idx_img], global_idx_saved_frame)
                        out_path = warmup_dir_this_execution / img_name
                        cv.imwrite(str(out_path), img)
                        global_idx_saved_frame += 1

                    self.reset_sequence_frames()

                

                # if y is not None:
                #     print('    ', str_rps(y))
                self.sequence.append(y)
                # print('    Notify')
                self.lock.notify_all()
                # print('    Show')
            self.clf.feature_extractor.show()
            # print('    Ok')
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            # if state == 'wait_gesture':
            #     if not t.is_alive():
            #         res = t.result
            #         if res is None:
            #             print('res is None!?!')
            #         else:
            #             print('*' * 80)
            #             print(str_rps(res))
            #             print('*' * 80)
            #         t = WaitGestureEndThread(lock=self.lock, clf=self,
            #                                  n_frames=n_frames)
            #         t.start()
            #         state = 'wait_end'
            #         print('Please remove your hand.')
            # elif state == 'wait_end':
            #     if not t.is_alive():
            #         t = RpsGestureRecognizerThread(lock=self.lock,
            #                                        clf=self,
            #                                        n_frames=n_frames)
            #         t.start()
            #         state = 'wait_gesture'
            #         print('Play again')


if __name__ == '__main__':
    grm = GestureRecognitionMain()
    grm.main_loop()