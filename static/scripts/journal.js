const prompts = [
  "What is one thing I did well today?",
  "What is something I learned about myself today?",
  "What emotion stands out the most right now?",
  "What is one kind thing I can do for myself tomorrow?",
  "What is one thing that went well today?",
  "Did anything make me smile or laugh today?"
];

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.js-journal-form');
  if (!form) return;

  const dateField = form.querySelector('input[name="date"]');
  const contentField = form.querySelector('textarea[name="content"]');
  const errorDateMessage = document.querySelector('.js-date-error-message');
  const errorContentMessage = document.querySelector('.js-error-message2')

  // Clear error message when date is changed
  dateField.addEventListener('input', () => {
    if (dateField.value) {
      errorDateMessage.innerHTML = '';
    }
  });

  // Clear error message when content is not empty
  contentField.addEventListener('input', () => {
    if (contentField.value) {
      errorContentMessage.innerHTML = '';
    }
  });

  form.addEventListener('submit', (e) => {
    if (!dateField.value && !contentField.value) {
      e.preventDefault();
      alert('Please fill out all fields');
    } else if (!dateField.value) {
      e.preventDefault();
      errorDateMessage.innerHTML = 'Date field is missing';
    } else if (!contentField.value) {
      e.preventDefault();
      errorContentMessage.innerHTML = 'Content field is missing';
    }
  });
});

function showPrompt() {
  // Generate random prompt
  const prompt = prompts[Math.floor(Math.random() * prompts.length)];
  document.querySelector('.display-prompt').innerHTML = prompt;

  // Enables input box to show up and users can type
  const inputBox = document.querySelector('input[name="prompt_response"]');
  inputBox.style.display = "block";

  // Disable button once it has been clicked
  const button = document.querySelector('#prompt-btn');
  button.disabled = true;

  // Change button text
  button.textContent = "Prompt shown";
}