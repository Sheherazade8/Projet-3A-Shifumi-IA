# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
from os import mkdir
from pathlib import Path

from shifumy_player.base import RESOURCES_PATH

RECO_DIR_PATH = Path(RESOURCES_PATH) / 'reco'
if not RECO_DIR_PATH.exists():
    mkdir(str(RECO_DIR_PATH))

RECO_TRAIN_IMAGES_DIR_PATH = RECO_DIR_PATH / 'rps_images'
RECO_TRAIN_IMAGES_RECORD_DIR_PATH = RECO_TRAIN_IMAGES_DIR_PATH / 'record'
RECO_TRAIN_IMAGES_RECORD_DIR_PATH.mkdir(parents=True, exist_ok=True)

RECO_TRAIN_IMAGES_WARMUP_DIR_PATH = RECO_TRAIN_IMAGES_DIR_PATH / 'player_warmup'
RECO_TRAIN_IMAGES_WARMUP_DIR_PATH.mkdir(parents=True, exist_ok=True)

RECO_TRAIN_CLF_DIR_PATH = RECO_DIR_PATH / 'train'
if not RECO_TRAIN_CLF_DIR_PATH.exists():
    mkdir(str(RECO_TRAIN_CLF_DIR_PATH))

RECO_CLASSIFIER_FILE_PATH = RECO_DIR_PATH / 'classifier.pickle'

RECO_EPISODE_FILE_PATH = RECO_DIR_PATH / 'training_episodes.pickle'

RECO_MOSAIC_TRAIN_FILE_PATH = RECO_TRAIN_CLF_DIR_PATH / 'Mosaic_train.png'
