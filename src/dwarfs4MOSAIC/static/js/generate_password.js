
window.addEventListener('DOMContentLoaded', function () {
  const pwLabel = document.querySelector('label[for="id_password1"]');
  if (pwLabel) {
      const container = pwLabel.parentElement;
      const button = document.createElement('button');
      button.textContent = 'Generate password';
      button.type = 'button';
      button.className = 'button';
      button.style.display = 'block';
      button.style.marginBottom = '10px';
      button.style.padding = '10px 20px';

      // Insert button before the container
      container.parentElement.insertBefore(button, container);

      button.addEventListener('click', function () {
          const pw1 = document.getElementById('id_password1');
          const pw2 = document.getElementById('id_password2');
          new_password = generatePassword(12);

          if (pw1 && pw2) {
            pw1.type = 'text';  // mostrar texto en claro
            pw2.type = 'text';
            pw1.value = new_password;
            pw2.value = new_password;
          }
      });
  }
});

function generatePassword(length = 12) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}:"<>?|[];\',./`~';
  let password = '';
  const array = new Uint32Array(length);
  window.crypto.getRandomValues(array);

  for (let i = 0; i < length; i++) {
    password += chars[array[i] % chars.length];
  }
  return password;
}

