'use strict';
const search = document.querySelector('#search');
if (search) {
  const kind = document.querySelector('#kind');
  const rows = [...document.querySelectorAll('#events tbody tr')];
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const row of rows) {
      row.hidden = !(row.textContent.toLocaleLowerCase().includes(query) && (!kind.value || row.dataset.kind === kind.value));
      if (!row.hidden) count++;
    }
    document.querySelector('#count').textContent = `${count} of ${rows.length} entries`;
    document.querySelector('#empty').hidden = count !== 0;
  }
  search.addEventListener('input', filter);
  kind.addEventListener('change', filter);
  document.querySelector('#reset').addEventListener('click', () => { search.value = ''; kind.value = ''; filter(); search.focus(); });
}
