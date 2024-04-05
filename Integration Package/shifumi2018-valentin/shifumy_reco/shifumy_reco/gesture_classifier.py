# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import pickle
import time
from os import mkdir
from pathlib import Path
from threading import Thread, Condition

import cv2 as cv
import numpy as np
from shifumy_player.base import ROCK, PAPER, SCISSORS, str_rps
from shifumy_reco.base import RECO_TRAIN_IMAGES_DIR_PATH, \
    RECO_TRAIN_CLF_DIR_PATH, RECO_CLASSIFIER_FILE_PATH, \
    RECO_EPISODE_FILE_PATH, RECO_MOSAIC_TRAIN_FILE_PATH, RECO_TRAIN_IMAGES_RECORD_DIR_PATH
from shifumy_reco.image_processing import ColoredBackgroundImageFeatureExtractor, ImageMosaic
from shifumy_reco.utils import str_id_generator
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV


# TODO use data/model folder


def record(g_name, cap, duration, outdir_path=RECO_TRAIN_IMAGES_DIR_PATH):
    assert isinstance(outdir_path, Path)

    print('record', g_name)
    if not outdir_path.exists():
        mkdir(str(outdir_path))

    fps = cap.get(cv.CAP_PROP_FPS)
    height = cv.CAP_PROP_FRAME_HEIGHT
    width = cv.CAP_PROP_FRAME_WIDTH
    print('FPS:', fps)
    print('Height:', cap.get(height))
    print('Width:', cap.get(width))

    n_frames = int(duration*fps)
    frame_list = []
    print('Capturing...')
    for i in range(n_frames):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # frame = crop_center_square(frame)
        # out.write(frame)
        frame_list.append(frame)

        frame_text = np.copy(frame)
        cv.putText(frame_text,
                   g_name + '{:.0%}'.format((i+1)/n_frames),
                   (0, frame_text.shape[0]-1),
                   cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2)
        cv.imshow('frame', frame_text)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    print('Saving...')
    frame_text = np.copy(frame)
    cv.putText(frame_text,
               'Saving...',
               (0, frame_text.shape[0] - 1),
               cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2)
    # for i in range(10):
    cv.imshow('frame', frame_text)
    if cv.waitKey(1) & 0xFF == ord('q'):
        pass
    n_offset = len(list(outdir_path.glob('{}_*.png'.format(g_name, i))))
    for i in range(n_frames):
        out_path = outdir_path / '{}_{:09d}.png'.format(g_name, i+n_offset)
        cv.imwrite(str(out_path), frame_list[i])
    print('Done!')

    # out.release()


def run_record_rps(cap, duration=5, outdir_path=RECO_TRAIN_IMAGES_DIR_PATH):
    for g in {ROCK, PAPER, SCISSORS}:
        record(g_name=str_rps(g, language='EN'), cap=cap, duration=duration,
               outdir_path=outdir_path)


# def replay(filename):
#     """ deprecated ?"""
#     cap = cv.VideoCapture(filename)
#     while (cap.isOpened()):
#         ret, frame = cap.read()
#         cv.imshow('frame', frame)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv.destroyAllWindows()


def replay_images(dir_path=RECO_TRAIN_IMAGES_DIR_PATH, format='png'):
    for image_path in dir_path.glob('*.' + format):
        image = cv.imread(str(image_path), cv.IMREAD_COLOR)
        cv.imshow('image', image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


def extract_training_episodes(in_dir_path=RECO_TRAIN_IMAGES_DIR_PATH,
                              out_dir_path=RECO_TRAIN_CLF_DIR_PATH,
                              episode_file_path=RECO_EPISODE_FILE_PATH,
                              format='png'):
    if not out_dir_path.exists():
        mkdir(out_dir_path)
    training_episodes = []
    for g in {ROCK, PAPER, SCISSORS}:

        files = in_dir_path.glob(str_rps(g, language='EN') + '*.' + format)

        feature_extractor = ColoredBackgroundImageFeatureExtractor()
        episode = []
        for image_file in files:
            print('Process ', image_file)
            image = cv.imread(str(image_file), cv.IMREAD_COLOR)
            y = feature_extractor.transform(image)
            if y is not None:
                print('-> {} ({})'.format(str_rps(g, language='EN'), y.shape))
                episode.append((y, g))
                cv.imshow(str_rps(g, language='EN'), y)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if len(episode) == 0:
                    continue
                training_episodes.append(episode)
                episode = []
        if len(episode) > 0:
            training_episodes.append(episode)

    print('Number of episodes:', len(training_episodes))
    with open(str(episode_file_path), 'wb') as f:
        pickle.dump(training_episodes, f, pickle.HIGHEST_PROTOCOL)

    for i, e in enumerate(training_episodes):
        mosaic = ImageMosaic(do_resample=False)
        for y, g in e:
            mosaic.add_image(y)
        mosaic_image = mosaic.compute_mosaic()
        cv.imwrite(str(out_dir_path / 'Mosaic_{}_{}.png'.format(i, len(e))),
                   mosaic_image)
    return training_episodes


def extract_training_set_from_episodes(
        training_episodes, remove_inds=[], i_start=5, i_end=-5,
        mosaic_train_file_path=RECO_MOSAIC_TRAIN_FILE_PATH):
    training_set = []
    mosaic = ImageMosaic(do_resample=False)
    for i, e in enumerate(training_episodes):
        if i in remove_inds:
            continue
        training_set += e[i_start:i_end]

    for x, y in training_set:
        mosaic.add_image(x)
    mosaic_image = mosaic.compute_mosaic()
    cv.imwrite(str(mosaic_train_file_path), mosaic_image)
    return training_set


class RpsGestureClassifier():
    def __init__(self):
        self.feature_extractor = ColoredBackgroundImageFeatureExtractor()
        self.classifier = None
        self.sequence = []

    def predict(self, x):
        """
        Return the predicted gesture or None if no gesture has been detected.

        :param x: image from which to predict
        :return:
        """
        x = self.feature_extractor.transform(x)
        if x is None:
            return None
        return self.classifier.predict(x.reshape((1, -1,)))[0]

    def train(self, training_set):
        X = np.vstack((x.reshape((1, -1)) for x, y in training_set))
        y = np.array([y for x, y in training_set])
        # TODO find better classifier: more training data, select by cross-val
        # TODO cross-validation to tune parameters
        score = 'precision'
        tuned_parameters = [
            {
                'loss': ['hinge'],
                'alpha': [10**(-n) for n in range(10)],
            },
            {
                'loss': ['log'],
                'alpha': [10**(-n) for n in range(10)],
            },
        ]
        clf = GridSearchCV(SGDClassifier(),
                           tuned_parameters,
                           cv=3,
                           scoring='accuracy')
        clf.fit(X, y)
        print("Best parameters set found on development set:")
        print(clf.best_params_)
        print("Grid scores on development set:")
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))

        # self.classifier = SGDClassifier()
        # self.classifier.fit(X, y)
        self.classifier = clf

    def save(self, filepath=RECO_CLASSIFIER_FILE_PATH):
        with open(str(filepath), 'wb') as f:
            pickle.dump(self.classifier, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filepath=RECO_CLASSIFIER_FILE_PATH):
        with open(str(filepath), 'rb') as f:
            classifier = pickle.load(f)
        clf = RpsGestureClassifier()
        clf.classifier = classifier
        return clf


class RpsGestureClassifierThread(Thread):
    def __init__(self, cap, lock, clf_filepath=RECO_CLASSIFIER_FILE_PATH):
        Thread.__init__(self, name='RpsGestureClassifierThread')
        self.lock = lock
        self.clf = RpsGestureClassifier.load(clf_filepath)
        self.cap = cap
        self.sequence = None
        self.reset_sequence()

    def reset_sequence(self):
        self.sequence = []

    def run(self):
        cap = cv.VideoCapture(0)
        while True:
            print('Running...')
            with self.lock:
                print('    Read frame')
                ret, frame = self.cap.read()
                print('    ', ret)
                print('    Classify frame')
                y = self.clf.predict(frame)
                if y is not None:
                    print('    ', str_rps(y, language='EN'))
                self.sequence.append(y)
                print('    Notify')
                self.lock.notify_all()
                print('    Show')
                self.clf.feature_extractor.show()
                print('    Ok')
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                print('    Sleep')
                time.sleep(0.2)
                print('    Awake')


class RpsGestureClassifierPseudoThread():
    def __init__(self, cap, lock, clf_filepath=RECO_CLASSIFIER_FILE_PATH):
        self.lock = lock
        self.clf = RpsGestureClassifier.load(clf_filepath)
        self.cap = cap
        self.sequence = None
        self.reset_sequence()

    def reset_sequence(self):
        self.sequence = []

    def run(self):
        state = 'wait_gesture'
        n_frames = 5
        t = RpsGestureRecognizerThread(lock=self.lock, clf=self, n_frames=n_frames)
        t.start()
        while True:
            # print('Running...')
            with self.lock:
                # print('    Read frame')
                ret, frame = self.cap.read()
                # print('    ', ret)
                # print('    Classify frame')
                y = self.clf.predict(frame)
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

            if state == 'wait_gesture':
                if not t.is_alive():
                    res = t.result
                    if res is None:
                        print('res is None!?!')
                    else:
                        print('*' * 80)
                        print(str_rps(res, language='EN'))
                        print('*' * 80)
                    t = WaitGestureEndThread(lock=self.lock, clf=self, n_frames=n_frames)
                    t.start()
                    state = 'wait_end'
                    print('Please remove your hand.')
            elif state == 'wait_end':
                if not t.is_alive():
                    t = RpsGestureRecognizerThread(lock=self.lock, clf=self,
                                                   n_frames=n_frames)
                    t.start()
                    state = 'wait_gesture'
                    print('Play again')

            # print('    Sleep')
            # time.sleep(0.2)
            # print('    Awake')


class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        cap = cv.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            cv.imshow('frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()


class RpsGestureRecognizer():
    def __init__(self, cap, filepath=RECO_CLASSIFIER_FILE_PATH, n_frames=15, ratio=0.9):
        self.cap = cap
        self.clf = RpsGestureClassifier.load(filepath)
        self.n_frames = n_frames
        self.ratio = ratio
        self._sequence = None

        self.reset()

    def reset(self):
        self._sequence = []

    def wait_gesture(self):
        self.reset()
        bins = [ROCK, PAPER, SCISSORS]
        while True:
            ret, frame = cap.read()
            y = self.clf.predict(frame)
            if y is not None:
                self._sequence.append(y)
                if len(self._sequence) >= self.n_frames:
                    h, a = np.histogram(self._sequence[-self.n_frames:],
                                        bins=np.arange(4)-0.5)
                    h = h / np.sum(h)
                    i_max = np.argmax(h)
                    if h[i_max] > self.ratio:
                        return bins[i_max]
            else:
                self.reset()
            # cv.imshow('image', frame)
            self.clf.feature_extractor.show()
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    def wait_end_gesture(self):
        """ Wait end of the gesture, i.e., removing the hand

        End of gesture is decided when self.n_frames successive None values
        are detected.
        """
        none_counter = 0
        while True:
            ret, frame = cap.read()
            if self.clf.predict(frame) is None:
                none_counter += 1
                if none_counter > self.n_frames:
                    return
            else:
                none_counter = 0


class RpsGestureRecognizerThread(Thread):
    def __init__(self, lock, clf, n_frames):
        Thread.__init__(self)
        self.lock = lock
        self.clf = clf
        self.n_frames = n_frames
        self.result = None
        self.ratio = 0.9

    def run(self):
        bins = [ROCK, PAPER, SCISSORS]
        while True:
            with self.lock:
                self.lock.wait()
                if len(self.clf.sequence) >= self.n_frames:
                    sub_seq = self.clf.sequence[-self.n_frames:]
                    if any([x is None for x in sub_seq]):
                        continue
                    h, a = np.histogram(self.clf.sequence[-self.n_frames:],
                                        bins=np.arange(4)-0.5)
                    h = h / np.sum(h)
                    i_max = np.argmax(h)
                    if h[i_max] > self.ratio:
                        self.result = bins[i_max]
                        return


class WaitGestureEndThread(Thread):
    def __init__(self, lock, clf, n_frames):
        Thread.__init__(self)
        self.lock = lock
        self.clf = clf
        self.n_frames = n_frames
        self.result = None

    def run(self):
        while True:
            with self.lock:
                self.lock.wait()
                if len(self.clf.sequence) >= self.n_frames:
                    if all([x is None
                            for x in self.clf.sequence[-self.n_frames:]]):
                        return


if __name__ == '__main__':
    duration = 20

    cap = cv.VideoCapture(1)

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

    options = ['Record',
               'Replay',
               'Extract episodes',
               'Train',
               'Test frame prediction',
               'Test gesture recognition (OLD)',
               'Test gesture recognition/Treads (OLD)',
               'Test gesture recognition',
               ]
    s = '\n'.join(['{}: {}'.format(i, x) for i, x in enumerate(options)])
    answer = int(input(s + '\n' + ">"))
    answer = options[answer]
    if answer == 'Record':
        global_timestamp = int(time.time())
        global_random_id = str_id_generator(size=6)
        dir_record = RECO_TRAIN_IMAGES_RECORD_DIR_PATH / "{}_{}".format(global_timestamp, global_random_id)
        run_record_rps(cap=cap, duration=duration,
                       outdir_path=dir_record)
    elif answer == 'Replay':
        replay_images(dir_path=RECO_TRAIN_IMAGES_DIR_PATH, format='png')
    elif answer == 'Extract episodes':
        extract_training_episodes(in_dir_path=RECO_TRAIN_IMAGES_DIR_PATH,
                                  out_dir_path=RECO_TRAIN_CLF_DIR_PATH,
                                  episode_file_path=RECO_EPISODE_FILE_PATH,
                                  format='png')
    elif answer == 'Train':
        with open(str(RECO_EPISODE_FILE_PATH), 'rb') as f:
            training_episodes = pickle.load(f)
        training_set = extract_training_set_from_episodes(training_episodes)
        classifier = RpsGestureClassifier()
        classifier.train(training_set)
        classifier.save()
    elif answer == 'Test frame prediction':
        clf = RpsGestureClassifier.load()
        while True:
            ret, frame = cap.read()
            y = clf.predict(frame)
            if y is not None:
                print(str_rps(y))
            else:
                print(y)
            cv.imshow('image', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    elif answer == 'Test gesture recognition (OLD)':
        fps = cap.get(cv.CAP_PROP_FPS)
        n_frames = int(fps//3)
        print(n_frames)
        rec = RpsGestureRecognizer(cap=cap, n_frames=n_frames)
        while True:
            print('Just play now.')
            y = rec.wait_gesture()
            print('#' * 80)
            print(str_rps(y))
            print('#' * 80)
            print('Please remove your hand.')
            rec.wait_end_gesture()

    elif answer == 'Test gesture recognition/Treads (OLD)':
        fps = cap.get(cv.CAP_PROP_FPS)
        n_frames = int(fps//3)
        print(n_frames)

        print('Create threads')
        lock = Condition()
        clf_thread = RpsGestureClassifierThread(cap=cap, lock=lock)

        print('Start threads')
        clf_thread.start()

        print('Wait for end of threads')
        clf_thread.join()

    elif answer == 8:
        fps = cap.get(cv.CAP_PROP_FPS)
        n_frames = int(fps//3)
        print(n_frames)
        clf = RpsGestureClassifier.load(RECO_CLASSIFIER_FILE_PATH)
        lock = Condition()
        while True:
            print('Running...')
            with lock:
                print('    Read frame')
                ret, frame = cap.read()
                print('    ', ret)
                print('    Classify frame')
                y = clf.predict(frame)
                if y is not None:
                    print('    ', str_rps(y))
                # self.sequence.append(y)
                print('    Notify')
                lock.notify_all()
                print('    Show')
                clf.feature_extractor.show()
                print('    Ok')
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                print('    Sleep')
                time.sleep(0.2)
                print('    Awake')
    elif answer == 9:
        fps = cap.get(cv.CAP_PROP_FPS)
        n_frames = int(fps // 3)
        print(n_frames)
        clf = RpsGestureClassifier.load(RECO_CLASSIFIER_FILE_PATH)
        lock = Condition()
        win = cv.namedWindow('Frames!')
        thread = MyThread(cap=cap, win=win)
        thread.start()
        thread.join()
    elif answer == 10:
        win = cv.namedWindow('Frames!')

        while True:
            print('    Read frame')
            ret, frame = cap.read()
            cv.imshow(win, frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1)
    elif answer == 'Test gesture recognition':
        fps = cap.get(cv.CAP_PROP_FPS)
        n_frames = int(fps // 3)
        print(n_frames)

        print('Create threads')
        lock = Condition()
        pseudothread = RpsGestureClassifierPseudoThread(cap=cap, lock=lock)
        pseudothread.run()

    # while True:
        #     print('Running...')
        #     with lock:
        #         print('    Read frame')
        #         ret, frame = cap.read()
        #         print('    ', ret)
        #         print('    Classify frame')
        #         y = clf.predict(frame)
        #         if y is not None:
        #             print('    ', str_rps(y))
        #         # self.sequence.append(y)
        #         print('    Notify')
        #         lock.notify_all()
        #         print('    Show')
        #         clf.feature_extractor.show()
        #         print('    Ok')
        #         if cv.waitKey(1) & 0xFF == ord('q'):
        #             break
        #         print('    Sleep')
        #         time.sleep(0.2)
        #         print('    Awake')
        # rec = RpsGestureRecognizer(cap=cap, n_frames=n_frames)
        # while True:
        #     print('Just play now.')
        #     y = rec.wait_gesture()
        #     print('#' * 80)
        #     print(str_rps(y))
        #     print('#' * 80)
        #     print('Please remove your hand.')
        #     rec.wait_end_gesture()

    # for file in Path(outdir_name).glob('*.avi'):
    #     replay(cap, str(file))

    cap.release()
    cv.destroyAllWindows()

