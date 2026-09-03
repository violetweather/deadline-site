"use strict";
/* Shared chrome for every Deadline page: ticker, countdown, nav effects. */

const REPO_URL = "https://github.com/violetweather/deadline-site";
const SUBMIT_ISSUE_URL = REPO_URL + "/issues/new?template=submission.yml";

/* marquee ticker */
(function () {
  const track = document.getElementById("ticker-track");
  if (!track) return;
  const phrases = ["Every model meets its deadline", "27 machine-generated tasks", "Every task has a token deadline",
    "No judge model", "Hidden tests", "Scores out of 100", "Submit before midnight", "Python, JavaScript, and SQL"];
  const half = phrases.map(p => `<span>${p}</span>`).join("");
  track.innerHTML = half + half;
})();

/* countdown to local midnight: nav clock, flap cells, day ruler */
(function () {
  const navClock = document.getElementById("nav-clock");
  const fc = document.getElementById("fc-cells");
  let cells = null;
  if (fc) {
    fc.innerHTML = `<span class="cell"></span><span class="cell"></span><span class="sep">:</span>
<span class="cell"></span><span class="cell"></span><span class="sep">:</span>
<span class="cell"></span><span class="cell"></span>`;
    cells = fc.querySelectorAll(".cell");
  }
  const dlFill = document.getElementById("dl-fill");
  const dlNow = document.getElementById("dl-now");

  function tick() {
    const now = new Date();
    const mid = new Date(now);
    mid.setHours(24, 0, 0, 0);
    const s = Math.floor((mid - now) / 1000);
    const h = String(Math.floor(s / 3600)).padStart(2, "0");
    const m = String(Math.floor(s / 60) % 60).padStart(2, "0");
    const ss = String(s % 60).padStart(2, "0");
    if (navClock) navClock.textContent = `T−${h}:${m}:${ss}`;
    if (cells) {
      const digits = h + m + ss;
      cells.forEach((c, i) => { if (c.textContent !== digits[i]) c.textContent = digits[i]; });
    }
    if (dlFill && dlNow) {
      const pctNum = (now - new Date(now.getFullYear(), now.getMonth(), now.getDate())) /
                     86400000 * 100;
      const pct = pctNum.toFixed(2) + "%";
      dlFill.style.width = pct;
      dlNow.style.left = pct;
      const clock = document.getElementById("dl-clock");
      if (clock) {
        clock.textContent =
          `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
        // near either end of the strip the marker clock crashes into the
        // head labels (title on the left, LEFT counter on the right)
        clock.style.visibility = (pctNum > 86 || pctNum < 16) ? "hidden" : "visible";
      }
      const flag = document.querySelector(".dl-flag");
      if (flag) flag.style.opacity = pctNum > 78 ? "0" : "1";
      const left = document.getElementById("dl-left");
      if (left) left.textContent = `${h}:${m} LEFT`;
    }
  }
  tick();
  setInterval(tick, 1000);
})();

/* nav link decode-scramble on hover */
(function () {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const GLYPHS = "#%@$0123456789XKWM";
  document.querySelectorAll(".nav-links a span").forEach(el => {
    const orig = el.textContent;
    let iv = null;
    el.parentElement.addEventListener("mouseenter", () => {
      if (iv) clearInterval(iv);
      let settled = 0;
      iv = setInterval(() => {
        el.textContent = orig.split("").map((ch, j) =>
          ch === " " ? " " : (j < settled ? ch : GLYPHS[Math.random() * GLYPHS.length | 0])
        ).join("");
        settled++;
        if (settled > orig.length) {
          clearInterval(iv);
          iv = null;
          el.textContent = orig;
        }
      }, 26);
    });
    el.parentElement.addEventListener("mouseleave", () => {
      if (iv) { clearInterval(iv); iv = null; }
      el.textContent = orig;
    });
  });
})();
