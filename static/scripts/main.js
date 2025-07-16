window.onload = () => {
  const alertBox = document.querySelector('.js-alert');
  if (alertBox) {
    setTimeout(() => {
      alertBox.style.display = 'none';
    }, 3000);
  }
};