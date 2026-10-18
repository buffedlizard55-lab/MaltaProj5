'use strict';
// Progressive enhancement only: all rows and links are present in static HTML.
const search = document.querySelector('#search');
if (search) {
  const controls = ['kind', 'temporal', 'publication'].map(id => document.getElementById(id));
  const rows = [...document.querySelectorAll('#events tbody tr')];
  const count = document.getElementById('count');
  const empty = document.getElementById('empty');
  const text = new Map(rows.map(row => [row, row.textContent.toLocaleLowerCase()]));
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const row of rows) {
      const matches = text.get(row).includes(query) && controls.every(control => !control.value || row.dataset[control.id] === control.value);
      row.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = `${visible} of ${rows.length} entries`;
    empty.hidden = visible !== 0;
  }
  search.addEventListener('input', filter);
  controls.forEach(control => control.addEventListener('change', filter));
  document.getElementById('reset').addEventListener('click', () => {
    search.value = '';
    controls.forEach(control => { control.value = ''; });
    filter();
    search.focus();
  });
  document.getElementById('table-tools').hidden = false;
  filter();
}
