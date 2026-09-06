"use strict";
(() => {
  let theme = "light";
  try { if (localStorage.getItem("deadline-theme") === "dark") theme = "dark"; } catch (_) { /* Storage is optional. */ }
  document.documentElement.dataset.theme = theme;
  document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("theme-toggle");
    if (!button) return;
    function label() {
      const dark = document.documentElement.dataset.theme === "dark";
      button.setAttribute("aria-label", `Switch to ${dark ? "light" : "dark"} theme`);
      button.setAttribute("aria-pressed", String(dark));
    }
    button.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("deadline-theme", next); } catch (_) { /* Still works without persistence. */ }
      label();
    });
    label();
  });
})();
