let questions = [];
let userAnswers = [];
let currentQuestionIndex = 0;
let timeLeft = 60;
let timerInterval;
const questionText = document.getElementById('question-text');
const answerInput = document.getElementById('answer-input');
const submitBtn = document.getElementById('submit-btn');
const timer = document.querySelector('.timer');

let Question_number = 0;
  // Fetch questions from server
  fetch('Questions')
    .then(response => response.json())
    .then(data => {
      questions = data;
      console.log(questions )
      resetTimer();
      startTimer();
      showQuestion();
    })
    .catch(error => console.error(error));

  // Start the timer
  function startTimer() {
    if (timerInterval) {
      clearInterval(timerInterval);
    }
  
    timerInterval = setInterval(() => {
      timeLeft--;
      timer.style.width = `${(timeLeft / 60) * 100}%`;
      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        userAnswers.push('timeout');
        checkAnswer()
        // currentQuestionIndex++;
        // if (currentQuestionIndex < questions.length) {
        //   resetTimer();
        //   startTimer();
        //   showQuestion();
        // } else {
        //   window.location.href = "/Text_Test_Results";
        // }
      }
    }, 1000);
  }

  // Reset the timer
  function resetTimer() {
    timeLeft = 60;
    timer.style.width = '100%';
  }

  // Handle form submission
  submitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    checkAnswer();
  });

  answerInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
      checkAnswer();
    }
  });

  function showQuestion() {
    questionText.innerText = questions[currentQuestionIndex];
    answerInput.value = '';
  }

  function checkAnswer() {
    const userAnswer = answerInput.value;
    answerInput.value = ''; // Clear the answer input field
    currentQuestionIndex++;
  
    // Send the user's answer to the server
    fetch('Text_Answers/' + Question_number, {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain'
      },
      body: userAnswer
    })
      .then(response => {
        if (response.ok) {
          
          console.log(response);
          Question_number += 1;
        } else {
          console.error('Failed to submit answer.');
        }
  
        // Check if there are more questions to show
        if (currentQuestionIndex < questions.length) {
          resetTimer();
          startTimer();
          showQuestion();
        } else {
          window.location.href = "/Text_Test_Results";
        }
      })
      .catch(error => console.error(error));
  }

