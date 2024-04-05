# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import warnings

import cv2 as cv
import numpy as np

DEFAULT_SCREEN_SIZE = (900, 1440)
DEFAULT_SCREEN_SIZE = (1080, 1920)
DEFAULT_SCREEN_SIZE = (1000, 1920)
DEFAULT_SCREEN_SIZE = (900, 1600)


class ImageFeatureExtractor:
    def __init__(self, must_crop=True, bb_ratio = 1.5, kernel_se_size=3,
                 must_convert_HLS=False, min_area_ratio=0.01):
        """
        Current version is suitable with a blue background!

        Parameters
        ----------
        must_crop
        bb_ratio
        kernel_se_size
        must_convert_HLS
        """
        self.must_crop = must_crop
        self.bb_ratio = bb_ratio
        self.kernel_se_size = kernel_se_size
        self.must_convert_HLS = must_convert_HLS
        self.min_area_ratio = min_area_ratio

        self.fgbg = cv.bgsegm.createBackgroundSubtractorCNT()
        # self.fgbg = cv.bgsegm.createBackgroundSubtractorGSOC()

        # self.fgbg = cv.bgsegm.createBackgroundSubtractorGMG()
        # self.fgbg = cv.bgsegm.createBackgroundSubtractorLSBP()
        # self.fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

        self.kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,
                                          (kernel_se_size, kernel_se_size))
        self.image_mosaic = ImageMosaic()

    def transform(self, frame):
        """
        Transform a captured frame into a feature vector

        Parameters
        ----------
        frame : ndarray
            Input frame

        Returns
        -------
        ndarray
            Feature vector
        """
        self.image_mosaic.reset()


        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # frameHLS = cv.cvtColor(frame, cv.COLOR_BGR2HLS);
        # median_color = np.median(frameHLS, axis=(0,1,))
        # print(median_color, np.std(frameHLS, axis=(0,1)))
        # # c_min = np.array((median_color[0]-10, 0, 0))
        # # c_max = np.array((median_color[0]+10, 255, 255))
        # err = np.array((40, 35, 27))
        # c_min = median_color - err * 2
        # c_max = median_color + err * 2
        # frameHLS = cv.inRange(frameHLS, c_min, c_max)
        #
        # frame *= (frameHLS < 127)[:, :, None]

        if self.must_crop:
            frame = crop_center(frame, ratio=self.bb_ratio)
        original_frame = frame
        self.image_mosaic.add_image(frame)

        for i in range(3):
            channel_i = np.zeros_like(frame)
            channel_i[:, :, i] = frame[:, :, i]
            self.image_mosaic.add_image(channel_i)
            self.image_mosaic.add_image(frame[:, :, i])

        if self.must_convert_HLS:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2HLS)
            self.image_mosaic.add_image(frame)

        frame_ = np.copy(frame)
        blue_screen = True
        if blue_screen:
            frame_[:, :, 0] = 255 - frame_[:, :, 0]
            frame_[:, :, 1] = 0
        else:
            frame_[:, :, 1] = 255 - frame_[:, :, 1]
            frame_[:, :, 0] = 0
        self.image_mosaic.add_image(frame_)
        for i in range(3):
            channel_i = np.zeros_like(frame_)
            channel_i[:, :, i] = frame_[:, :, i]
            self.image_mosaic.add_image(channel_i)
            self.image_mosaic.add_image(frame_[:, :, i])

        fgmask = self.fgbg.apply(frame_)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, self.kernel)

        self.image_mosaic.add_image(self.fgbg.getBackgroundImage())
        self.image_mosaic.add_image(fgmask)

        masked_frame = original_frame * (fgmask[:, :, None] > 127)
        self.image_mosaic.add_image(masked_frame)

        # Find contour of largest area
        _, contours, _ = cv.findContours(fgmask,
                                         cv.RETR_TREE,
                                         cv.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None

        contour = contours[np.argmax([cv.contourArea(c) for c in contours])]

        frame = np.copy(masked_frame)
        cv.drawContours(frame, [contour], 0, (0, 255, 0), 2)
        self.image_mosaic.add_image(frame)

        # Build contour mask
        contour_mask = np.zeros(masked_frame.shape[:2], np.uint8)
        cv.drawContours(contour_mask, [contour], 0, 255, cv.FILLED)

        self.image_mosaic.add_image(contour_mask)

        contour_masked_frame = original_frame * (
                    contour_mask[:, :, None] > 127)
        self.image_mosaic.add_image(contour_masked_frame)

        # Find bounding box
        bounding_box = cv.boundingRect(contour)

        bb_p1 = bounding_box[:2]
        bb_p2 = (bounding_box[0] + bounding_box[2],
                 bounding_box[1] + bounding_box[3])
        x_max = bounding_box[0] + min(bounding_box[2],
                                      int(self.bb_ratio * bounding_box[3]))
        bb_p3 = (x_max, bb_p2[1])

        frame = np.copy(contour_masked_frame)
        cv.rectangle(frame, bb_p1, bb_p2, (255, 0, 0), 3)
        cv.rectangle(frame, bb_p1, bb_p3, (255, 255, 0), 2)
        self.image_mosaic.add_image(frame)


        frame = np.copy(contour_mask)
        cv.rectangle(frame, bb_p1, bb_p2, (255, 0, 0), 3)
        cv.rectangle(frame, bb_p1, bb_p3, (255, 255, 0), 2)
        self.image_mosaic.add_image(frame)

        bb_area = bounding_box[2] * bounding_box[3]
        # print('Area: {} px ({:.0%})'
        #       .format(bb_area, bb_area/original_frame.size))
        if bb_area < self.min_area_ratio * original_frame.size:
            return None

        # Crop
        contour_mask[:, x_max:] = 0
        contour_masked_frame = original_frame * (
                    contour_mask[:, :, None] > 127)

        frame = np.copy(contour_masked_frame)
        cv.rectangle(frame, bb_p1, bb_p2, (255, 0, 0), 3)
        cv.rectangle(frame, bb_p1, bb_p3, (255, 255, 0), 2)
        self.image_mosaic.add_image(frame)

        frame = np.copy(contour_mask)
        cv.rectangle(frame, bb_p1, bb_p2, (255, 0, 0), 3)
        cv.rectangle(frame, bb_p1, bb_p3, (255, 255, 0), 2)
        self.image_mosaic.add_image(frame)

        # Crop and downsample mask
        cropped = contour_mask[bb_p1[1]:bb_p3[1], bb_p1[0]:bb_p3[0]]
        n_rows = 20
        n_cols = int(self.bb_ratio * n_rows)
        # sampling_ratio = 10 // contour_mask.shape[0]
        # print(cropped.shape, n_rows, n_cols)
        image = cv.resize(cropped, (n_cols, n_rows))
        self.image_mosaic.add_image(cv.resize(image,
                                         contour_mask.shape[::-1],
                                         interpolation=cv.INTER_NEAREST))

        # # Compute convex hull of contour
        # cvx_hull = cv.convexHull(contour)
        #
        # frame = np.copy(masked_frame)
        # cv.drawContours(frame, [contour], 0, (0, 255, 0), 2)
        # cv.drawContours(frame, [cvx_hull], 0, (0, 0, 255), 2)
        # image_mosaic.add_image(frame)

        return image

    def show(self):
        """
        Display the mosaic frame computed by method `transform`
        """
        self.image_mosaic.show()
        if cv.waitKey(1) & 0xFF == ord('q'):
            raise ValueError('This should never happen.')


class ColoredBackgroundImageFeatureExtractor:
    def __init__(self,
                 screen_size=DEFAULT_SCREEN_SIZE,
                 hls_lb=(65, 0, 0),
                 hls_ub=(90, 255, 255),
                 must_crop=True, bb_ratio=1.5,
                 kernel_se_size=3,
                 min_area_ratio=0.01):

        self.hls_lb = np.array(hls_lb)
        self.hls_ub = np.array(hls_ub)
        self.must_crop = must_crop
        self.bb_ratio = bb_ratio
        self.kernel_se_size = kernel_se_size
        self.min_area_ratio = min_area_ratio

        # self.fgbg = cv.bgsegm.createBackgroundSubtractorCNT()
        # self.fgbg = cv.bgsegm.createBackgroundSubtractorGSOC()

        # self.fgbg = cv.bgsegm.createBackgroundSubtractorGMG()
        # self.fgbg = cv.bgsegm.createBackgroundSubtractorLSBP()
        # self.fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

        self.kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,
                                          (kernel_se_size, kernel_se_size))
        self.image_mosaic = ImageMosaic(screen_size=screen_size,
                                        name='Mosaic')
        # self.image_mosaic_front = ImageMosaic(screen_size=screen_size,
        #                                       name='Front mosaic')

    def transform(self, frame):
        """
        Transform a captured frame into a feature vector

        Parameters
        ----------
        frame : ndarray
            Input frame

        Returns
        -------
        ndarray
            Feature vector
        """
        self.image_mosaic.reset()
        # self.image_mosaic_front.reset()

        if frame is None:
            return None

        if self.must_crop:
            frame = crop_center(frame, ratio=self.bb_ratio)
        original_frame = frame
        self.image_mosaic.add_image(frame)
        # self.image_mosaic_front.add_image(frame)

        # convert to HLS:
        frame_hls = cv.cvtColor(frame, cv.COLOR_BGR2HLS)
        self.image_mosaic.add_image(frame_hls)

        # Filter out background based on HLS range
        # the resulting mask is a 2D ndarray with 255 entries for in-range
        # pixels and 0 values for out-of-range pixels
        frame_mask = cv.inRange(frame_hls, self.hls_lb, self.hls_ub)
        # Permute values
        frame_mask = 255 - frame_mask
        # self.image_mosaic.add_image(frame_mask)

        fgmask = cv.morphologyEx(frame_mask,
                                 cv.MORPH_OPEN, self.kernel)
        self.image_mosaic.add_image(fgmask)

        masked_frame = original_frame * (fgmask[:, :, None] > 127)
        self.image_mosaic.add_image(masked_frame)

        # Find contour of largest area
        contours = cv.findContours(fgmask,
                                   cv.RETR_TREE,
                                   cv.CHAIN_APPROX_SIMPLE)
        contours = contours[-2]

        if len(contours) == 0:
            zim = np.zeros_like(original_frame)
            for i in range(4):
                self.image_mosaic.add_image(zim)
            # for i in range(3):
                # self.image_mosaic_front.add_image(zim)
            return None

        contour = contours[np.argmax([cv.contourArea(c) for c in contours])]

        frame = np.copy(masked_frame)
        cv.drawContours(frame, [contour], 0, (0, 255, 0), 2)
        self.image_mosaic.add_image(frame)

        # Build contour mask
        contour_mask = np.zeros(masked_frame.shape[:2], np.uint8)
        cv.drawContours(contour_mask, [contour], 0, 255, cv.FILLED)

        # self.image_mosaic.add_image(contour_mask)

        contour_masked_frame = original_frame * (
                    contour_mask[:, :, None] > 127)
        # self.image_mosaic.add_image(contour_masked_frame)


        # Find bounding box
        bounding_box = cv.boundingRect(contour)

        bb_p1 = bounding_box[:2]
        bb_p2 = (bounding_box[0] + bounding_box[2],
                 bounding_box[1] + bounding_box[3])
        x_max = bounding_box[0] + min(bounding_box[2],
                                      int(self.bb_ratio * bounding_box[3]))
        bb_p3 = (x_max, bb_p2[1])

        frame = np.copy(contour_masked_frame)
        cv.rectangle(frame, bb_p1, bb_p2, (255, 0, 0), 3)
        cv.rectangle(frame, bb_p1, bb_p3, (255, 255, 0), 2)
        self.image_mosaic.add_image(frame)


        bb_area = bounding_box[2] * bounding_box[3]
        # print('Area: {} px ({:.0%})'
        #       .format(bb_area, bb_area/original_frame.size))]
        res = -1
        if bb_area < self.min_area_ratio * original_frame.size:
            zim = np.zeros_like(original_frame)
            for i in range(2):
                self.image_mosaic.add_image(zim)
            return None

        # Crop
        contour_mask[:, x_max:] = 0
        contour_masked_frame = original_frame * (
                    contour_mask[:, :, None] > 127)

        frame = np.copy(contour_masked_frame)
        # cv.rectangle(frame, bb_p1, bb_p2, (255, 0, 0), 3)
        cv.rectangle(frame, bb_p1, bb_p3, (255, 255, 0), 2)
        self.image_mosaic.add_image(frame)
        # self.image_mosaic_front.add_image(frame)
        zim = np.zeros_like(original_frame)
        # for i in range(2):
            # self.image_mosaic_front.add_image(zim)

        # Crop and downsample mask
        cropped = contour_mask[bb_p1[1]:bb_p3[1], bb_p1[0]:bb_p3[0]]
        n_rows = 20
        n_cols = int(self.bb_ratio * n_rows)
        image = cv.resize(cropped, (n_cols, n_rows))
        self.image_mosaic.add_image(cv.resize(image,
                                         contour_mask.shape[::-1],
                                         interpolation=cv.INTER_NEAREST))
        return image

    def show(self):
        """
        Display the mosaic frame computed by method `transform`
        """
        self.image_mosaic.show()
        # self.image_mosaic_front.show()
        if cv.waitKey(1) & 0xFF == ord('q'):
            raise ValueError('This should never happen.')

class ImageMosaic():
    # TODO add label as text on images (not urgent)
    # TODO reshape mosaic to fit an arbitrary dimension ratio (not urgent)
    # TODO adjust to screen size
    def __init__(self, screen_size=DEFAULT_SCREEN_SIZE, name='Mosaic',
                 do_resample=True):
        self.image_list = []
        self.labels = []
        self.resample_ratio = None
        self.name = name
        self.do_resample = do_resample
        self.screen_size = screen_size
        self.reset()

    def reset(self):
        self.image_list.clear()
        self.labels.clear()

    def add_image(self, image, label=None):
        if self.resample_ratio is not None and self.do_resample:
            image = cv.resize(image, (0, 0),
                              fx=self.resample_ratio,
                              fy=self.resample_ratio)
        if image.ndim == 2:
            image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        self.image_list.append(image)
        self.labels.append(label)

    def compute_mosaic(self):
        n_images = len(self.image_list)
        if n_images == 0:
            return None
        n_cols = int(np.ceil(np.sqrt(n_images)))
        n_rows = int(np.ceil(n_images / n_cols))
        if self.resample_ratio is None and self.do_resample:

            self.resample_ratio = min(
                self.screen_size[0] / (n_rows * self.image_list[0].shape[0]),
                self.screen_size[1] / (n_cols * self.image_list[0].shape[1])
            )
            self.image_list = [cv.resize(image, (0, 0),
                                         fx=self.resample_ratio,
                                         fy=self.resample_ratio)
                               for image in self.image_list]
        for i in range(n_cols * n_rows - n_images):
            self.image_list.append(np.zeros_like(self.image_list[0]))
        if len({im.shape for im in self.image_list}) > 1:
            for im in self.image_list:
                print(im.shape)
        rows = []
        for i in range(n_rows):
            rows.append(np.hstack(self.image_list[i*n_cols:(i+1)*n_cols]))

        mosaic = np.vstack(rows)
        return mosaic

    def show(self):
        mosaic_image = self.compute_mosaic()
        if mosaic_image is None:
            warnings.warn('Empty mosaic.')
        else:
            cv.imshow(self.name, mosaic_image)


def crop_center(x, ratio=1):
    # TODO bug
    # n_rows = x.shape[0]
    # AttributeError: 'NoneType' object has no attribute 'shape'
    n_rows = x.shape[0]
    diameter = int(ratio * n_rows)
    j0 = x.shape[1] // 2 - diameter // 2
    if j0 >= 0:
        return x[:, j0:j0+diameter+1]
    else:
        return x


if __name__ == '__main__':
    cap = cv.VideoCapture(0)

    height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    print('FPS:', cap.get(cv.CAP_PROP_FPS))
    print('Height:', height)
    print('Width:', width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height * 1)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width * 1)
    cap.set(cv.CAP_PROP_FPS, 20)
    print('FPS:', cap.get(cv.CAP_PROP_FPS))
    print('Height:', cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print('Width:', cap.get(cv.CAP_PROP_FRAME_WIDTH))

    # Create the image extractor
    # feature_extractor = ImageFeatureExtractor()
    # feature_extractor = ColoredBackgroundImageFeatureExtractor(
    #     screen_size=(300, 400))
    feature_extractor = ColoredBackgroundImageFeatureExtractor(
        screen_size=DEFAULT_SCREEN_SIZE)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Extract features from current frame
        y = feature_extractor.transform(frame)
        # print('Gesture detected: ', y is not None)
        # Display mosaic
        feature_extractor.show()

    cap.release()
    cv.destroyAllWindows()
