// Progressive enhancement for components/range_calendar.py: roving focus and range choice.
document.querySelectorAll('[data-component="range-calendar"]').forEach((root) => {
  const buttons = Array.from(root.querySelectorAll('button[data-date]'));
  const start = root.querySelector('input[name="start"]');
  const end = root.querySelector('input[name="end"]');
  const move = (from, step) => {
    const next = buttons[buttons.indexOf(from) + step];
    if (!next) return;
    from.tabIndex = -1;
    next.tabIndex = 0;
    next.focus();
  };
  root.addEventListener('keydown', (event) => {
    const current = event.target.closest('button[data-date]');
    if (!current) return;
    const steps = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 };
    if (event.key in steps) {
      event.preventDefault();
      move(current, steps[event.key]);
    }
  });
  root.addEventListener('click', (event) => {
    const chosen = event.target.closest('button[data-date]');
    if (!chosen || chosen.getAttribute('aria-disabled') === 'true') return;
    if (!start.value || end.value) {
      start.value = chosen.dataset.date;
      end.value = '';
    } else {
      end.value = chosen.dataset.date;
    }
  });
});
