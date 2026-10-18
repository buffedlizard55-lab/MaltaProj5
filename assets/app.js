'use strict';
// Progressive enhancement only: all rows and links are present in static HTML.
// Every filter bar is wired to the event table that follows it, so a page can
// carry more than one table (the Upcoming page groups entries by date horizon).
function wire(bar) {
  const search = bar.querySelector('input[type="search"]');
  if (!search) return;
  const id = search.id.replace(/^search-?/, '');
  const suffix = id ? '-' + id : '';
  let node = bar.nextElementSibling;
  let table = null;
  while (node && !table) {
    table = node.matches && node.matches('table.events') ? node : node.querySelector('table.events');
    node = node.nextElementSibling;
  }
  if (!table) return;
  const controls = ['kind', 'temporal', 'cost', 'publication']
    .map(name => ({ element: document.getElementById(name + suffix), key: name }))
    .filter(control => control.element);
  const rows = [...table.tBodies[0].rows];
  const count = document.getElementById('count' + suffix);
  const empty = document.getElementById('empty' + suffix);
  const text = new Map(rows.map(row => [row, row.textContent.toLocaleLowerCase()]));
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const row of rows) {
      const matches = text.get(row).includes(query) && controls.every(control => !control.element.value || row.dataset[control.key] === control.element.value);
      row.hidden = !matches;
      if (matches) visible++;
    }
    if (count) count.textContent = `${visible} of ${rows.length} entries`;
    if (empty) empty.hidden = visible !== 0;
  }
  search.addEventListener('input', filter);
  controls.forEach(control => control.element.addEventListener('change', filter));
  const reset = document.getElementById('reset' + suffix);
  if (reset) {
    reset.addEventListener('click', () => {
      search.value = '';
      controls.forEach(control => { control.element.value = ''; });
      filter();
      search.focus();
    });
  }
  bar.hidden = false;
  filter();
}

[...document.querySelectorAll('.tools')].forEach(wire);
