# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

import threading
import random
import time


class Thread1(threading.Thread):
    def __init__(self, cv):
        threading.Thread.__init__(self)
        self.cv = cv

    def run(self):
        for i in range(100):
            with self.cv:
                # Choose to notify the other Thread or not
                if random.random() > 0.7:
                    print(' > notify', end='')
                    cv.notify_all()
                else:
                    print('continue', end='')
                # Sleep, keeping the lock, so ... will be printed on the
                # same line
                time.sleep(random.randint(1, 60) / 100 + 0.2)
                print('...')
            # Sleep in order to give time to the other Thread for getting awake
            time.sleep(random.randint(1, 60) / 100 + 0.2)


class Thread2(threading.Thread):
    def __init__(self, cv):
        threading.Thread.__init__(self)
        self.cv = cv

    def run(self):
        for i in range(100):
            with self.cv:
                # Wait until notified (lock is released while waiting)
                cv.wait()
                print(' > awake! ', end='')
                # Sleep, keeping the lock, so i will be printed on the
                # same line
                time.sleep(random.randint(1, 60) / 100 + 0.2)
                print(i)



if __name__ == '__main__':
    cv = threading.Condition()
    t1 = Thread1(cv=cv)
    t2 = Thread2(cv=cv)

    t1.start()
    t2.start()

    t1.join()
    t2.join()