const alertPlaceholder = document.getElementById('liveAlertPlaceholder');

const alert = (message, type) => {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      <strong>${message}</strong>
    </div>
  `;
  alertPlaceholder.appendChild(wrapper);
  alertTrigger.disabled = false;
};

const alertTrigger = document.getElementById('liveAlertBtn');
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    alert('Correo enviado! Revisa tu correo', 'success');
    alertTrigger.disabled = true;
  });
}