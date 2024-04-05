import cv2
import mediapipe as mp
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import csv

class HandGestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.8,
                                         min_tracking_confidence=0.9)
        self.mp_drawing = mp.solutions.drawing_utils
        self.knn = KNeighborsClassifier(n_neighbors=2)
        self.data = []
        self.labels = []
        self.path = []

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

    def detect_gesture(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Conversion de l'image de BGR à RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            # Dessin des landmarks de la main
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Transformation et prédiction du cluster
                    x0, y0, z0 = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y, hand_landmarks.landmark[0].z
                    transformed_landmarks = self.landmarkFormat(hand_landmarks)
                    transformed_landmarks_flat = np.ravel(transformed_landmarks).reshape(1, -1)
                    cluster_label = self.knn.predict(transformed_landmarks_flat)

                    # Affichage du cluster sur l'image
                    if cluster_label == 0:
                        cv2.putText(image, 'Feuille', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    elif cluster_label == 1:
                        cv2.putText(image, 'Pierre', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    elif cluster_label == 2:
                        cv2.putText(image, 'Ciseaux', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    else:
                        cv2.putText(image, 'Inconnu', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    # Afficher la plus proche distance
                    #nearest_neighbors = self.knn.kneighbors(transformed_landmarks_flat, 5)
                    #mean_distance = np.mean(nearest_neighbors[0][0])

            # Affichage de l'image résultante
            cv2.imshow('MediaPipe Hands', image)

            # Arrêt avec la touche 'q'
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


gesture_recognition = HandGestureRecognition()
gesture_recognition.load_data('shifumi2024/shifumi2018-valentin/shifumy_demo_cv/shifumy_demo_cv/landmarks.csv')
gesture_recognition.train_knn()
gesture_recognition.detect_gesture()
