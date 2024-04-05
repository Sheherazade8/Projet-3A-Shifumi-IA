# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

import cv2 as cv
import numpy as np

print(np.__version__)
cap = cv.VideoCapture(1)

setup = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ratio = 0.25
    format = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH) * ratio),
              int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) * ratio))
    frame = cv.resize(frame, format)
    if setup is None:
        setup = 0

        win_name = 'frame'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 0 * format[0], 0 * format[1])

        win_name = 'hsv'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 1 * format[0], 0 * format[1])

        win_name = 'H'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 0 * format[0], 1 * format[1])

        win_name = 'S'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 1 * format[0], 1 * format[1])

        win_name = 'V'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 2 * format[0], 1 * format[1])

        win_name = 'InRange_HV'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 0 * format[0], 2 * format[1])

        win_name = 'InRange_H'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 1 * format[0], 2 * format[1])

        win_name = 'InRange_H_mask'
        cv.namedWindow(win_name)
        cv.moveWindow(win_name, 2 * format[0], 2 * format[1])

    # Our operations on the frame come here
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    q = np.quantile(hsv, (0, 0.05, 0.1, 0.5, 0.9, 0.95, 1), axis=(0, 1))
    # m, s = np.mean(hsv, axis=(0, 1)), np.std(hsv, axis=(0, 1))
    # hsv_min = m - s
    # hsv_max = m + s
    # print(('({:03.0f}, {:03.0f}) ' * 3).format(
    #     hsv_min[0], hsv_max[0],
    #     hsv_min[1], hsv_max[1],
    #     hsv_min[2], hsv_max[2]))
    for c in range(hsv.shape[2]):
        print(q[:, c], end=' ')
    print('')

    lowerb5 = np.array((q[1, 0], 0, 0))
    upperb5 = np.array((q[-2, 0], 255, 255))
    filtered_frame5 = cv.inRange(hsv, lowerb5, upperb5)
    lowerb_h = np.array((75, 0, 0))
    upperb_h = np.array((95, 255, 255))
    filtered_frame_hard_h = cv.inRange(hsv, lowerb_h, upperb_h)
    lowerb_hv = np.array((75, 0, 50))
    upperb_hv = np.array((95, 255, 255))
    filtered_frame_hard_hv = cv.inRange(hsv, lowerb_hv, upperb_hv)

    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.imshow('hsv', hsv)
    cv.imshow('H', hsv[:, :, 0])
    cv.imshow('S', hsv[:, :, 1])
    cv.imshow('V', hsv[:, :, 2])
    cv.imshow('InRange_HV', filtered_frame_hard_hv)
    cv.imshow('InRange_H',
              (filtered_frame_hard_h[:, :, None]==0) * frame)
    cv.imshow('InRange_H_mask', filtered_frame_hard_h)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
