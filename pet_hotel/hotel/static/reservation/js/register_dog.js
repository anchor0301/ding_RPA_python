console.log("register_dog.js loaded!");


document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('input#id_breed_autocomplete.form-control');
  const container = input.closest('.position-relative');
  const box = container.querySelector('.autocomplete-suggestions');

  let timer;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    const q = input.value;
    if (q.length < 2) { box.innerHTML = ''; return; }
    timer = setTimeout(() => {
    fetch(`/hotel/breeds/autocomplete/?q=${encodeURIComponent(q)}`)
        .then(res => res.json())
        .then(list => {
        box.innerHTML = list
          .map(n => `<div class="suggestion-item">${n}</div>`)
          .join('');
      });
    }, 300);
  });

  box.addEventListener('click', e => {
    if (e.target.matches('.suggestion-item')) {
      input.value = e.target.textContent;
      box.innerHTML = '';
    }
  });
});