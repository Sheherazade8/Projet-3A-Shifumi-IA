# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import cv2 as cv
from pathlib import Path
from os import mkdir
import numpy as np


def crop_center_square(x):
    """
    Crop an image by keeping the largest centered square area.

    Parameters
    ----------
    x : ndarray
        Input image

    Returns
    -------
    ndarray
    Output image
    """
    n_rows = x.shape[0]
    j0 = x.shape[1] // 2 - n_rows // 2
    return x[:, j0:j0+n_rows]


class CameraThread():
    def __init__(self, fps = 10, height = 1080 // 2, width = 1920 // 2,
                 device=0):
        self.cap = None
        self.current_frame = None
        cv.VideoCapture(0)
        self._height = height
        self._width = width
        self._fps = fps
        self.device = device
        self.must_show = False

    def start(self):
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self._height)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self._width)
        self.cap.set(cv.CAP_PROP_FPS, self._fps)

    def show(self):
        self.must_show = True

    def hide(self):
        self.must_show = False

    def run(self):
        while True:
            self.ret, self.frame = self.cap.read()

            if self.must_show:
                frame = crop_center_square(frame)
                cv.imshow('frame', frame)

    def stop(self):
        self.cap.release()
        cv.destroyAllWindows()
        self.cap = None


def record(g_name, cap, duration, outdir_name):
    print('record', g_name)
    if not Path(outdir_name).exists():
        mkdir(outdir_name)

    fps = cap.get(cv.CAP_PROP_FPS)
    height = cv.CAP_PROP_FRAME_HEIGHT
    width = cv.CAP_PROP_FRAME_WIDTH
    print('FPS:', fps)
    print('Height:', cap.get(height))
    print('Width:', cap.get(width))

    # fourcc = cv.VideoWriter_fourcc(*'XVID')
    # out_path = Path(outdir_name) / '{}.avi'.format(g_name)
    # out = cv.VideoWriter(str(out_path), fourcc, fps,
    #                      (width, height),
    #                      True)
    # print(out.isOpened())
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
    for i in range(n_frames):
        out_path = Path(outdir_name) / '{}_{}.png'.format(g_name, i)
        cv.imwrite(str(out_path), frame_list[i])
    print('Done!')

    # out.release()


def run_record_rps(duration=5, fps=10, height=720//2, width=1280//2,
                   outdir_name='rps_images'):
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FPS, fps)

    for g_name in ['rock', 'paper', 'scissor']:
        record(g_name=g_name, cap=cap, duration=duration, outdir_name=outdir_name)

    cap.release()
    cv.destroyAllWindows()


def replay(filename):
    cap = cv.VideoCapture(filename)
    while (cap.isOpened()):
        ret, frame = cap.read()
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    outdir_name = 'rps_images'
    duration = 5
    run_record_rps(duration=duration, outdir_name=outdir_name)
    # for file in Path(outdir_name).glob('*.avi'):
    #     replay(str(file))
