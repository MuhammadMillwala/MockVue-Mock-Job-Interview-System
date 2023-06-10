let start_button = document.querySelector("#start-record");
const timer = document.getElementById('timer');
const question = document.getElementById('question');
const nextBtn = document.getElementById('next');
nextBtn.disabled=true;

let timer_duration = 10 * 60 * 1000; // 10 minutes in milliseconds
let questions = ['QUESTIONS'];
let timeLeft = 600;
let timerInterval;

let question_number = 0;

let recorder;
let chunks = [];


async function startCamera() {
  fetch('start')
  .then(response => response.text())
  .then(message => console.log(message));
  document.getElementById('video-stream').src = "videofeed";
}


function stopCamera() {
  fetch('stop')
  .then(response => response.text())
  .then(message => console.log(message));
  document.getElementById('video-stream').src = "";
}


function startRecording() {
  navigator.mediaDevices.getUserMedia({ 
    audio: {
      volume: 1.0 // set the audio volume to maximum
    }
  })
    .then(stream => {
      recorder = new MediaRecorder(stream);
      recorder.addEventListener('dataavailable', event => {
        chunks.push(event.data);
      });
      recorder.start();
    })
    .catch(error => {
      console.error(error);
    });
}

function stopRecording() {
  return new Promise(resolve => {
    recorder.addEventListener('stop', () => {
      const blob = new Blob(chunks);
      const formData = new FormData();
      formData.append('file', blob, 'audio'+ question_number +'.mp3');
      fetch('/upload-audio/' + question_number, { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          question_number += 1;
          resolve();
        })
        .catch(error => {
          console.error(error);
          resolve();
        });
    });
  });
}

function startTimer() {
  timerInterval = setInterval(() => {
    timeLeft--;
    timer.style.width = `${(timeLeft / 600) * 100}%`;
    if (timeLeft <= 0) 
    {
      stopCamera();
      window.location.href = "/Video_Test_Results";
    }
  }, 1000);
}


fetch('Questions')
  .then(response => response.json())
  .then(data => 
  {
    questions = questions.concat(data);
    showQuestion(0);
  });

async function showQuestion(index) 
{
  if (index < questions.length) 
  {
    question.textContent = questions[index];
    currentQuestionIndex = index;
  } else {
    stopCamera();
    question.textContent = "Processing"
    await new Promise(r => setTimeout(r, 10000));
    window.location.href = "/Video_Test_Results";
  }
}

nextBtn.addEventListener('click', async () => {
  stopRecording();
  recorder.stop();
  chunks = [];
  showQuestion(currentQuestionIndex + 1);
  startRecording();
});

start_button.addEventListener('click', async function() {
  await startCamera();
  startTimer();
  showQuestion(1);
  startRecording();
  nextBtn.disabled = false;
  start_button.disabled = true;
});