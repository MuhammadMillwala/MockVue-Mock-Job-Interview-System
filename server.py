from __future__ import print_function  # In python 2.7
import numpy as np
import pickle
import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, send_from_directory, Response
import time
import spacy
import cv2
from deepface import DeepFace
import pandas as pd
import json
import sys
from werkzeug.utils import secure_filename
import librosa
import soundfile as sf
import speech_recognition as sr

app = Flask(__name__)
df = pd.read_csv('data/normalized_dataset.csv')
similarities = []
Questions_Arr = []
Correct_Answer_Arr = []
User_Answers = []
All_Video_Details = []
All_Text_Details = []

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'ogg', 'wav', 'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

camera = cv2.VideoCapture(0)
emotion_counts = {
    'angry': 0,
    'disgust': 0,
    'fear': 0,
    'happy': 0,
    'sad': 0,
    'surprise': 0,
    'neutral': 0,
    'no_face': 0,
}
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def sentences_similarity(sentence1, sentence2):
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    similarity = doc1.similarity(doc2)
    return similarity

@app.route('/')
def index():
    global similarities, Questions_Arr, Correct_Answer_Arr, User_Answers, All_Text_Details, emotion_counts, All_Video_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    All_Video_Details = []
    emotion_counts = {
        'angry': 0,
        'disgust': 0,
        'fear': 0,
        'happy': 0,
        'sad': 0,
        'surprise': 0,
        'neutral': 0,
        'no_face': 0,
    }
    return render_template('Main_page.html')

@app.route('/home')
def home():
    return render_template('Main_page.html')

@app.route('/about')
def about():
    return render_template('Main_page.html')

@app.route('/text_test_instructions')
def text_test_instructions():
    return render_template('Instructions_text.html')

@app.route('/video_test_instructions')
def video_test_instructions():
    return render_template('Instructions_video.html')

@app.route('/Text_Test')
def Text_Test():
    return render_template('Text_Test.html')

@app.route('/Text_Test_Results')
def Text_Test_Results():
    return render_template('Text_Test_Results.html')

@app.route('/Video_Test')
def Video_Test():
    return render_template('Video_Test.html')

@app.route('/Video_Test_Results')
def Video_Test_Results():
    return render_template('Video_Test_Results.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/Questions')

@app.route('/Questions')
def Text_Questions():
    global Questions_Arr, Correct_Answer_Arr
    random_rows = df.sample(n=10)
    Questions_Arr = random_rows['Questions'].tolist()
    Correct_Answer_Arr = random_rows['Answers'].tolist()
    return jsonify(Questions_Arr)

@app.route('/Text_Answers/<int:QuestionIndex>', methods=['POST'])
def Text_Answers(QuestionIndex):
    global User_Answers, Correct_Answer_Arr, Questions_Arr
    User_Answers.append(request.form['userAnswer'])
    if QuestionIndex == 9:
        score = 0
        for i in range(10):
            similarity = sentences_similarity(User_Answers[i], Correct_Answer_Arr[i])
            similarities.append(similarity)
            if similarity >= 0.5:
                score += 1
        return jsonify(score)
    else:
        return jsonify('success')

@app.route('/Video_Answers', methods=['POST'])
def Video_Answers():
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

