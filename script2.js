let currentQuestionIndex = 0;

function nextQuestion() {
  const questionContainers = document.querySelectorAll('.questionContainer');

  // Hide the current question
  questionContainers[currentQuestionIndex].style.display = 'none';

  // Display the next question
  currentQuestionIndex++;
  if (currentQuestionIndex < questionContainers.length) {
      questionContainers[currentQuestionIndex].style.display = 'block';
  } else {
      // If all questions are answered, show the result container and buttons
      document.getElementById('resultContainer').style.display = 'block';
      document.getElementById('buttonsContainer').style.display = 'block';
  }
}

function submitForm() {
    const currentMood = document.querySelector('input[name="currentMood"]:checked');
    const desiredMood = document.querySelector('input[name="desiredMood"]:checked');

    if (currentMood && desiredMood) {
      // Display the loading message and spinner
      document.getElementById('loadingMessage').style.display = 'block';
      document.getElementById('loadingSpinner').style.display = 'block';

      // Simulating a delay before showing the result
      setTimeout(() => {
          const currentMoodResult = currentMood.value;
          const desiredMoodResult = desiredMood.value;

          // Display the selected moods
          document.getElementById('currentMoodResult').textContent = `Current Mood: ${currentMoodResult}`;
          document.getElementById('desiredMoodResult').textContent = `Desired Mood: ${desiredMoodResult}`;

          // Show the result container and hide the loading elements
          document.getElementById('resultContainer').style.display = 'block';
          document.getElementById('loadingMessage').style.display = 'none';
          document.getElementById('loadingSpinner').style.display = 'none';
      }, 2000); // Simulating a delay, you can replace this with your actual playlist curation logic
  } else {
      alert('Please select both current and desired moods.');
  }
}
