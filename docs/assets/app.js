/* SF Events — client-side table search & filters (vanilla JS, no dependencies). */
(function () {
  "use strict";
  var table = document.getElementById("evt-table");
  if (!table) return;
  var toolbar = document.querySelector(".toolbar");
  var kind = toolbar ? toolbar.getAttribute("data-page") : "";

  var search = document.getElementById("f-search");
  var status = document.getElementById("f-status");
  var month = document.getElementById("f-month");
  var upcoming = document.getElementById("f-upcoming");
  var countEl = document.getElementById("row-count");

  var groups = Array.prototype.slice.call(table.querySelectorAll("tbody.mgroup"));
  var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr")).filter(function (r) {
    return !r.classList.contains("monthrow") && r.closest("tbody.mgroup") === null || r.closest("tbody.mgroup") !== null;
  });

  function rowText(r) { return (r.getAttribute("data-name") || "") + " " + r.textContent.toLowerCase(); }

  function apply() {
    var q = search ? search.value.trim().toLowerCase() : "";
    var st = status ? status.value : "";
    var mo = month ? month.value : "";
    var up = upcoming && upcoming.checked;
    var shown = 0, total = 0;

    if (groups.length) {
      groups.forEach(function (g) {
        var gmonth = g.getAttribute("data-month");
        var anyVisible = false;
        g.querySelectorAll("tr").forEach(function (r) {
          if (r.classList.contains("monthrow")) return;
          total++;
          var ok = true;
          if (q && rowText(r).indexOf(q) === -1) ok = false;
          if (st && r.getAttribute("data-status") !== st) ok = false;
          if (mo && gmonth !== mo) ok = false;
          if (up && r.querySelector(".badge-up") === null) ok = false;
          r.style.display = ok ? "" : "none";
          if (ok) { shown++; anyVisible = true; }
        });
        g.style.display = anyVisible ? "" : "none";
        var mr = g.querySelector(".monthrow");
        if (mr && mo) mr.style.display = "none"; else if (mr) mr.style.display = "";
      });
    } else {
      table.querySelectorAll("tbody tr").forEach(function (r) {
        total++;
        var ok = true;
        if (q && rowText(r).indexOf(q) === -1) ok = false;
        if (st && r.getAttribute("data-status") !== st) ok = false;
        if (up && r.querySelector(".badge-up") === null) ok = false;
        r.style.display = ok ? "" : "none";
        if (ok) shown++;
      });
    }
    if (countEl) countEl.textContent = "Showing " + shown + " of " + total + " events";
  }

  if (search) search.addEventListener("input", apply);
  if (status) status.addEventListener("change", apply);
  if (month) month.addEventListener("change", apply);
  if (upcoming) upcoming.addEventListener("change", apply);
  apply();
})();
