// reservation.js

document.addEventListener('DOMContentLoaded', function(){
  const hoursText = document
    .getElementById('restaurant-hours')  // см. ниже: спрятанный блок в шаблоне
    .textContent
    .trim();

  // Парсим первое вхождение интервала HH:MM–HH:MM
  const matcher = hoursText.match(/(\d{2}:\d{2})\s*[-–]\s*(\d{2}:\d{2})/);
  const timeInput = document.getElementById('id_time');

  if (matcher && timeInput) {
    const [ , openTime, closeTime ] = matcher;

    // устанавливаем min/max на поле
    timeInput.min = openTime;
    timeInput.max = (closeTime > openTime ? closeTime : '23:59');

    // показываем подсказку
    const hint = document.createElement('div');
    hint.classList.add('form-text', 'text-muted');
    hint.textContent = `Выберите время с ${openTime} до ${closeTime}.`;
    timeInput.parentNode.append(hint);
  } else {
    console.warn('Не удалось извлечь расписание из строки:', hoursText);
  }
});
{% block extra_js %}
<script>
  function fmtDate(d) {
    const opts = { day:'numeric', month:'long' };
    return d.toLocaleDateString('ru', opts);
  }
  function updateSummary(){
    const guests = document.querySelector('[name="guests"]').value;
    const dateIn = document.querySelector('[name="date"]').value;
    const t0 = document.querySelector('[name="time"]').value;
    const t1 = document.querySelector('[name="end_time"]').value;
    if(!guests||!dateIn||!t0||!t1) {
      document.getElementById('reservation-summary').textContent = '';
      return;
    }
    const dt = new Date(dateIn);
    const dayLabel = ( (new Date()).toDateString()===dt.toDateString() )
      ? 'Сегодня'
      : ( (new Date(Date.now()+864e5)).toDateString()===dt.toDateString() )
        ? 'Завтра'
        : fmtDate(dt);
    document.getElementById('reservation-summary').textContent =
      `${guests} гость(ей)  >  ${dayLabel}, ${fmtDate(dt)}  >  ${t0} – ${t1}`;
  }

  document.querySelectorAll('input[name=guests],input[name=date],input[name=time],input[name=end_time]')
    .forEach(el => el.addEventListener('change', updateSummary));
</script>
{% endblock %}
