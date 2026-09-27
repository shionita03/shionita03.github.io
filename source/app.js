// Modul independen: lightbox, navigasi aktif, kontrol presentasi.
(() => {
  const dlg = document.getElementById("lb");
  const img = dlg.querySelector("img"), cap = dlg.querySelector(".lb-cap"), cnt = dlg.querySelector(".lb-count");
  let list = [], i = 0;
  const show = () => {
    const im = list[i].querySelector("img");
    img.src = im.src; img.alt = im.alt; cap.textContent = im.alt;
    cnt.textContent = list.length > 1 ? `${i + 1} / ${list.length}` : "";
    dlg.querySelectorAll(".nav-btn").forEach(n => n.hidden = list.length < 2);
  };
  const step = d => { i = (i + d + list.length) % list.length; show(); };
  document.addEventListener("click", ev => {
    const b = ev.target.closest(".shot-btn"); if (!b) return;
    list = [...document.querySelectorAll(`.shot-btn[data-group="${b.dataset.group}"]`)];
    i = list.indexOf(b); show(); dlg.showModal();
  });
  dlg.querySelector(".prev").onclick = () => step(-1);
  dlg.querySelector(".next").onclick = () => step(1);
  dlg.querySelector(".close").onclick = () => dlg.close();
  dlg.addEventListener("click", ev => { if (ev.target === dlg) dlg.close(); });
  dlg.addEventListener("keydown", ev => { if (ev.key === "ArrowLeft") step(-1); if (ev.key === "ArrowRight") step(1); });
})();
(() => {
  // Navigasi: tandai seksi aktif.
  const links = new Map([...document.querySelectorAll(".nav ul a")].map(a => [a.hash.slice(1), a]));
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return;
    links.forEach(a => a.classList.remove("on")); links.get(en.target.id)?.classList.add("on");
  }), { rootMargin: "-40% 0px -55% 0px" });
  links.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
})();
(() => {
  // Mode presentasi: tombol panah kanan/kiri (atau tombol di pojok) melompat antar "stop".
  const stops = () => [...document.querySelectorAll("[data-stop]")].filter(el => !el.hidden && el.offsetParent !== null);
  const count = document.querySelector(".p-count"), dlg = document.getElementById("lb");
  const current = () => { const s = stops(), y = innerHeight * 0.3; let i = 0; s.forEach((el, k) => { if (el.getBoundingClientRect().top <= y) i = k; }); return [s, i]; };
  const go = d => { const [s, i] = current(); const t = s[Math.max(0, Math.min(s.length - 1, i + d))]; t.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" }); };
  const update = () => { const [s, i] = current(); count.textContent = `${i + 1} / ${s.length}`; };
  document.querySelector(".p-next").onclick = () => go(1);
  document.querySelector(".p-prev").onclick = () => go(-1);
  addEventListener("keydown", ev => {
    if (dlg.open || /INPUT|TEXTAREA|BUTTON/.test(document.activeElement.tagName) && ev.key === " ") return;
    if (ev.key === "ArrowRight") { ev.preventDefault(); go(1); }
    if (ev.key === "ArrowLeft") { ev.preventDefault(); go(-1); }
  });
  addEventListener("scroll", () => requestAnimationFrame(update), { passive: true }); update();
})();
