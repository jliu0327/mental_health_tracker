document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.js-journal-form');
  if (!form) {
    return;
  }

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