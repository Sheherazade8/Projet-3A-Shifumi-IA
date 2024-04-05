# Integration Package

## Overview
This integration package contains the modifications and enhancements made to the existing project. Our contributions aim to improve the performance of the Shifumi game with a better gesture recognizer. These changes have been added to the specific folder named Shifumi2018-Valentin

## Objective
The objective is to integrate the new gesture recognition model into the Shifumi game. The modifications aim to incorporate the gesture recognition functionality into the existing game framework.

## Changes
1. **shifumi2018-valentin/shifumi_reco/shifumi_reco/gesture_recognizer_client**:
    - Added a new class called `HandGestureRecognition` to replace the previous class `GestureRecognitionClient`.
    - Modified GestureRecognitionMain class to call the new class `HandGestureRecognition` instead of the previous one.

2. **shifumi2018-valentin/shifumy_demo_cv/shifumy_demo_cv/main.py**:
    - Various improvements have been made to enhance the integration.

## Additional Improvements for Complete Integration
1. **Linking Recognition with Gameplay**:
    - Updated the file that links the recognition part of the project with the gameplay part.

2. **Bug Fixes**:
    - Addressed issues and made necessary changes to ensure smooth functionality.
