import { mood_prompts, stress_prompts, emotion_prompts, self_reflection_prompts } from "./journal_prompt.js";

window.showPrompt = showPrompt;

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.js-journal-form');
  if (!form) return;

  const inputCategory = ['date', 'mood-response', 'stress-response', 'emotion-response', 'reflection-response'];
  const inputs = {};

  inputCategory.forEach((name) => {
    const input = form.querySelector(`[name="${name}"]`);
    inputs[name] = input;

    if (!input) return;

    input.addEventListener('input', () => {
      const errorMessage = form.querySelector(`.js-${name}-error-message`);
      if (errorMessage) {
        errorMessage.innerHTML = '';
      }
    });
  });

  form.addEventListener('submit', (e) => {
    let isError = false;

    inputCategory.forEach((name) => {
      const inputField = inputs[name];
      const inputValue = inputField != null ? inputField.value.trim() : undefined;
      const errorText = form.querySelector(`.js-${name}-error-message`);

      if (inputValue === '') {
        isError = true;

        if (errorText) {
          errorText.textContent = 'Field is missing';
        }
      }
    });

    if (isError) {
      e.preventDefault();
    }
  });
});

function showPrompt(sectionId, category) {
  const section = document.getElementById(sectionId);

  // Determine which array to use
  let prompts;
  switch (category) {
    case 'mood':
      prompts = mood_prompts;
      break;
    case 'stress':
      prompts = stress_prompts;
      break;
    case 'emotion':
      prompts = emotion_prompts;
      break;
    case 'self-reflection':
      prompts = self_reflection_prompts;
      break;
  }
  
  // Generate random prompt
  const prompt = prompts[Math.floor(Math.random() * prompts.length)];
  const display = section.querySelector('.display-prompt');
  display.textContent = prompt;

  // Enables input box to show up and users can type
  const inputBox = section.querySelector('input');
  inputBox.style.display = "block";

  // Disable button once it has been clicked
  const button = section.querySelector('#prompt-btn');
  button.disabled = true;
  button.textContent = "Prompt shown";
}

