from __future__ import print_function # In python 2.7
import numpy as np
import pickle
import os
from flask import Flask,redirect,url_for,render_template,request,jsonify
from flask import Response
import time
import os
# !python -m spacy download en_core_web_md
import spacy
nlp = spacy.load("en_core_web_md")
import cv2
import subprocess
from deepface import DeepFace
import pandas as pd
import json
import sys
from werkzeug.utils import secure_filename
import librosa
import soundfile as sf
import speech_recognition as speechrecognizer
import speech_recognition as sr

import math



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

def sentences_similarity(sentence1,sentence2):
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    similarity = doc1.similarity(doc2)
    return similarity
        

@app.route('/')
def index():
    global similarities
    global Questions_Arr
    global Correct_Answer_Arr
    global User_Answers
    global All_Text_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    global emotion_counts
    global All_Video_Details


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
    global similarities
    global Questions_Arr
    global Correct_Answer_Arr
    global User_Answers
    global All_Text_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    global emotion_counts
    global All_Video_Details


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
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/Questions')
def Text_Questions():
    global Questions_Arr
    global Correct_Answer_Arr
    random_rows = df.sample(n=10)
    Questions_Arr = random_rows['Questions'].tolist()
    Correct_Answer_Arr = random_rows['Answers'].tolist()
    return Questions_Arr

@app.route('/Text_Answers/<int:Qindex>', methods=['POST'])
def text_answers(Qindex):
    global All_Text_Details
    global Questions_Arr
    global Correct_Answer_Arr

    answer = request.data.decode('utf-8')
    temp_list = []
    temp_list.append(Questions_Arr[Qindex])
    temp_list.append(Correct_Answer_Arr[Qindex])
    temp_list.append(answer)
    temp_list.append(sentences_similarity(str(answer),str(Correct_Answer_Arr[Qindex])))
    All_Text_Details.append(temp_list)
    return jsonify(answer)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-audio/<int:Qindex>', methods=['POST'])
def upload_audio(Qindex):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))        
        audio, speechrecognizer = librosa.load("uploads/audio"+str(Qindex)+".mp3")
        sf.write("uploads/audio"+str(Qindex)+".wav", audio, speechrecognizer)
        # open the audio file using the recognizer  
        r = sr.Recognizer()
        with sr.AudioFile("uploads/audio"+str(Qindex)+".wav") as source:
            # listen to the file and store the audio data in a variable
            audio_data = r.record(source)
        # use the recognizer to convert speech to text
        text = r.recognize_google(audio_data)
        os.remove("uploads/audio"+str(Qindex)+".mp3")
        os.remove("uploads/audio"+str(Qindex)+".wav")
        global Questions_Arr
        global Correct_Answer_Arr
        global All_Video_Details
        Similarity = sentences_similarity(str(text), str(Correct_Answer_Arr[Qindex]))
        temp_list = []
        temp_list.append(Questions_Arr[Qindex])
        temp_list.append(Correct_Answer_Arr[Qindex])
        temp_list.append(text)
        temp_list.append(Similarity)
        All_Video_Details.append(temp_list)
        return jsonify({'success': text}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@app.route('/video_results')
def video_results():
    temp_Emotion_Counts = emotion_counts
    temp_Results = All_Video_Details

    temp_Emotion_Counts['angry'] = emotion_counts['angry'] * 0.2
    temp_Emotion_Counts['disgust'] = emotion_counts['disgust'] * 0.2
    temp_Emotion_Counts['fear'] = emotion_counts['fear'] * 0.2
    temp_Emotion_Counts['happy'] = emotion_counts['happy'] * 1.3
    temp_Emotion_Counts['sad'] = emotion_counts['sad'] * 0.2
    temp_Emotion_Counts['neutral'] = emotion_counts['neutral'] * 1
    temp_Emotion_Counts['no_face'] = 0

    new_temp = [] 
    new_temp.append(temp_Results)
    new_temp.append(list(temp_Emotion_Counts.values()))
    return jsonify(new_temp)


@app.route('/text_results')
def text_results():
    # All_Text_Details_temp = []
    All_Text_Details_temp = All_Text_Details    
    return jsonify(All_Text_Details_temp)

def generate_frames():
    global camera
    while True:
        if camera is not None:
            success, frame = camera.read()
            if not success:
                break
        else:
            break
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_copy = frame
        frame = buffer.tobytes()
 
        # convert to grayscale
        gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)

        # detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # loop over faces
        for (x, y, w, h) in faces:
            # extract face
            face = frame_copy[y:y+h, x:x+w]
            # recognize emotion if a face is detected
            if len(face) > 0:
                try:
                    result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=True)
                    if result[0]['dominant_emotion'] is not None:
                        emotion_counts[result[0]['dominant_emotion']] += 1
                    else:
                        no_count['no_emotion'] += 1
                except ValueError as err:
                    emotion_counts['no_face'] += 1
            # update the no_face count if no face is detected
            else:
                emotion_counts['no_face'] += 1

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/videofeed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start')
def start():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return 'Camera started'

@app.route('/start_again')
def start_again():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    while not camera.isOpened():  # Wait until the camera is ready
        pass
    return 'Camera started'

@app.route('/stop')
def stop():
    global camera
    if camera is not None:
        camera.release()
        camera = None
        camera = cv2.VideoCapture(0)
    return 'Camera stopped'

if __name__=='__main__':
    app.run(debug=True,port=8000)