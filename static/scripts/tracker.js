document.addEventListener('DOMContentLoaded', () => {
  const tracker_form = document.querySelector('.js-mood-form');
  if (!tracker_form) return;

  const inputNames = ['date', 'mood_feeling', 'mood_sleep', 'mood_diet', 'mood_energy', 'mood_stress'];
  const inputs = {};

  inputNames.forEach((name) => {
    if (name === 'date') {
      const input = tracker_form.querySelector(`input[name="${name}"]`);
      inputs[name] = input;  // ✅ Save the date input

      if (input) {
        input.addEventListener('input', () => {
          const errorDateMessage = document.querySelector(`.js-error-${name}`);
          if (errorDateMessage) {
            errorDateMessage.innerHTML = '';
          }
        });
      }

    } else {
      const inputGroup = tracker_form.querySelectorAll(`input[name="${name}"]`);
      inputs[name] = inputGroup;  // ✅ Save the radio group

      inputGroup.forEach((radio) => {
        radio.addEventListener('change', () => {
          const errorMessage = document.querySelector(`.js-error-${name}`);
          if (errorMessage) {
            errorMessage.innerHTML = '';
          }
        });
      });
    }
  });

  tracker_form.addEventListener('submit', (e) => {
    let validForm = true;

    inputNames.forEach((name) => {
      let isFilled = false;

      if (name === 'date') {
        isFilled = inputs[name] && inputs[name].value;
      } else {
        inputs[name].forEach((radio) => {
          if (radio.checked) {
            isFilled = true;
          }
        });
      }

      if (!isFilled) {
        e.preventDefault();
        validForm = false;

        const errorMessage = document.querySelector(`.js-error-${name}`);
        if (errorMessage) {
          errorMessage.innerHTML = 'Field is missing';
        }
      }
    });
  });
});
