"""
This module contains a Flask server implementation for handling text and video-based questions and answers.
"""

import pickle
import numpy as np
import os
import time
import json
import sys
import cv2
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import spacy
import librosa
import soundfile as sf
import speech_recognition as sr
from deepface import DeepFace

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Load the face cascade file
from cv2 import CascadeClassifier
faceCascade = CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables
Questions_Arr = []
Correct_Answer_Arr = []
User_Answers = []
All_Video_Details = []
emotion_counts = {"angry": 0, "disgust": 0, "fear": 0, "happy": 0, "sad": 0, "surprise": 0, "neutral": 0}


def sentences_similarity(sentence1, sentence2):
    """
    Calculate the similarity between two sentences using spaCy.

    Args:
        sentence1: The first sentence.
        sentence2: The second sentence.

    Returns:
        The similarity score between the sentences.
    """
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    return doc1.similarity(doc2)


@app.route('/Questions')
def text_questions():
    """
    Retrieve a list of random questions.

    Returns:
        A JSON response containing the list of questions.
    """
    global Questions_Arr, Correct_Answer_Arr
    random_rows = df.sample(n=10)  # Replace 'df' with your DataFrame or modify as needed
    Questions_Arr = random_rows['Questions'].tolist()
    Correct_Answer_Arr = random_rows['Answers'].tolist()
    return jsonify(Questions_Arr)


@app.route('/Text_Answers/<int:QuestionIndex>', methods=['POST'])
def text_answers(QuestionIndex):
    """
    Submit text answers to the questions.

    Args:
        QuestionIndex: The index of the current question.

    Returns:
        If the last question is submitted, returns the score as a JSON response.
        Otherwise, returns 'success' as a JSON response.
    """
    global User_Answers, Correct_Answer_Arr, Questions_Arr
    User_Answers.append(request.form['userAnswer'])
    if QuestionIndex == 9:
        score = 0
        for i in range(10):
            similarity = sentences_similarity(User_Answers[i], Correct_Answer_Arr[i])
            if similarity >= 0.5:
                score += 1
        return jsonify(score)
    return jsonify('success')


@app.route('/Video_Answers', methods=['POST'])
def video_answers():
    """
    Submit video answers with emotion analysis.

    Returns:
        A JSON response indicating the success or error status.
    """
    global All_Video_Details, emotion_counts
    video_file = request.files['videoFile']
    video_filename = secure_filename(video_file.filename)
    video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

    try:
        cap = cv2.VideoCapture(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
        if not cap.isOpened():
            return jsonify('error')

        frames_processed = 0
        face_detected = False
        emotion_detected = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) > 0:
                face_detected = True

                for (x, y, w, h) in faces:
                    face = frame[y:y + h, x:x + w]
                    emotion = DeepFace.analyze(face, actions=['emotion'])
                    emotion_counts[emotion['dominant_emotion']] += 1
                    emotion_detected = True

            frames_processed += 1

        cap.release()
        cv2.destroyAllWindows()

        if frames_processed > 0 and face_detected and emotion_detected:
            emotion_ratios = {emotion: count / frames_processed for emotion, count in emotion_counts.items()}
            All_Video_Details.append(emotion_ratios)
            return jsonify('success')
        else:
            return jsonify('error')
    except Exception as e:
        print(str(e))
        return jsonify('error')


if __name__ == '__main__':
    app.run(debug=True)
