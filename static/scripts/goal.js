document.addEventListener('DOMContentLoaded', () => {
  const goal_form = document.querySelector('.js-goal-form');
  if (!goal_form) return;

  const inputNames = ['set_goals', 'category', 'date', 'priority'];
  const fields = {};

  inputNames.forEach((name) => {
    const field = goal_form.querySelector(`[name="${name}"]`);
    const errorElement = goal_form.querySelector(`.js-error-${name}`);
    fields[name] = { field, errorElement };

    if (!field || !errorElement) return;

    const eventType = (field.tagName === 'SELECT') ? 'change' : 'input';

    field.addEventListener(eventType, () => {
      errorElement.innerHTML = '';
    });
  });

  goal_form.addEventListener('submit', (e) => {
    let isEmpty = false;

    inputNames.forEach((name) => {
      const { field, errorElement } = fields[name];

      if (!field || !errorElement) return;

      const value = field.value.trim();

      if (!value) {
        errorElement.innerHTML = 'Field is missing';
        isEmpty = true;
      }
    });

    if (isEmpty) {
      e.preventDefault();
    }
  });
});