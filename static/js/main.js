/* =========================================================
   Найкраща Кава — клієнтський JavaScript (ES6+)
   1. Бургер-меню з блокуванням скролу
   2. Заглушки для відсутніх фото
   3. Автовідправка сортування в каталозі
   4. Валідація форм (бронювання, вхід, реєстрація)
   5. Лічильник гостей
   6. Таби «Вхід / Реєстрація» і показ пароля
   7. Модальне вікно підтвердження видалення
   ========================================================= */

const lockScroll = (lock) => document.body.classList.toggle('no-scroll', lock);

/* ---------- 1. Бургер-меню ---------- */
const burger = document.querySelector('.burger');
const nav = document.querySelector('#main-nav');

if (burger && nav) {
  const setMenu = (open) => {
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Закрити меню' : 'Відкрити меню');
    lockScroll(open);
  };

  burger.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  window.matchMedia('(min-width: 1025px)').addEventListener('change', (e) => { if (e.matches) setMenu(false); });
}

/* ---------- 2. Заглушки для фото ---------- */
document.querySelectorAll('.photo img').forEach((img) => {
  const markMissing = () => img.classList.add('is-missing');
  if (img.complete && img.naturalWidth === 0) markMissing();
  img.addEventListener('error', markMissing);
});

/* ---------- 3. Автовідправка сортування ---------- */
document.querySelectorAll('[data-autosubmit]').forEach((select) => {
  select.addEventListener('change', () => select.form.submit());
});

/* ---------- 4. Валідація форм ---------- */
const rules = {
  name: (v) => (v.trim().length >= 2 && v.trim().length <= 50) || "Вкажіть ім'я (від 2 до 50 символів)",
  phone: (v) => /^\+380\d{9}$/.test(v.replace(/\s/g, '')) || 'Введіть номер у форматі +380XXXXXXXXX',
  email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) || 'Введіть коректну електронну пошту',
  password: (v) => v.length >= 6 || 'Пароль має містити щонайменше 6 символів',
  date: (v, input) => {
    if (!v) return 'Оберіть дату';
    return v >= input.min || 'Дата не може бути в минулому';
  },
  time: (v) => v !== '' || 'Оберіть час зі списку',
  guests: (v) => (Number.isInteger(+v) && +v >= 1 && +v <= 10) || 'Від 1 до 10 гостей',
  comment: (v) => v.length <= 300 || 'Не більше 300 символів',
};

const showError = (input, message) => {
  const field = input.closest('.field');
  const error = document.getElementById(input.getAttribute('aria-describedby'));
  field.classList.toggle('has-error', Boolean(message));
  input.setAttribute('aria-invalid', message ? 'true' : 'false');
  if (error) {
    error.textContent = message || '';
    error.hidden = !message;
  }
};

const validateInput = (input) => {
  const rule = rules[input.name];
  if (!rule) return true;
  const result = rule(input.value, input);
  showError(input, result === true ? '' : result);
  return result === true;
};

document.querySelectorAll('#booking-form, form[data-validate]').forEach((form) => {
  const inputs = [...form.querySelectorAll('input, select, textarea')].filter((i) => rules[i.name]);

  inputs.forEach((input) => {
    input.addEventListener('blur', () => validateInput(input));
    input.addEventListener('input', () => {
      if (input.closest('.field').classList.contains('has-error')) validateInput(input);
    });
  });

  form.addEventListener('submit', (e) => {
    const results = inputs.map(validateInput);
    if (results.includes(false)) {
      e.preventDefault();
      form.querySelector('[aria-invalid="true"]')?.focus();
    }
  });
});

/* ---------- 5. Лічильник гостей ---------- */
document.querySelectorAll('.stepper').forEach((stepper) => {
  const input = stepper.querySelector('input');
  stepper.querySelectorAll('[data-step]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const next = (parseInt(input.value, 10) || 0) + Number(btn.dataset.step);
      input.value = Math.min(Number(input.max), Math.max(Number(input.min), next));
      validateInput(input);
    });
  });
});

/* ---------- 6. Таби і показ пароля ---------- */
const tabs = document.querySelectorAll('.auth__tab');
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((t) => {
      const active = t === tab;
      t.classList.toggle('is-active', active);
      t.setAttribute('aria-selected', String(active));
      document.getElementById(t.getAttribute('aria-controls')).hidden = !active;
    });
  });
});

document.querySelectorAll('[data-toggle-password]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const input = btn.previousElementSibling;
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    btn.setAttribute('aria-label', show ? 'Сховати пароль' : 'Показати пароль');
  });
});

/* ---------- 7. Модальне вікно підтвердження видалення ---------- */
const modal = document.getElementById('confirm-modal');

if (modal) {
  const text = modal.querySelector('#modal-text');
  const confirmBtn = modal.querySelector('#modal-confirm');
  let pendingForm = null;
  let lastFocused = null;

  const openModal = (form, name) => {
    pendingForm = form;
    lastFocused = document.activeElement;
    text.textContent = `Позицію «${name}» буде видалено з меню без можливості відновлення.`;
    modal.hidden = false;
    lockScroll(true);
    confirmBtn.focus();
  };

  const closeModal = () => {
    modal.hidden = true;
    lockScroll(false);
    pendingForm = null;
    lastFocused?.focus();
  };

  document.querySelectorAll('[data-confirm]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openModal(btn.form, btn.dataset.confirm);
    });
  });

  modal.querySelectorAll('[data-close]').forEach((el) => el.addEventListener('click', closeModal));
  confirmBtn.addEventListener('click', () => pendingForm?.submit());
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !modal.hidden) closeModal();
  });
}
