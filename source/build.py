"""Rakit halaman presentasi: content + render + assets -> satu HTML mandiri."""
from functools import lru_cache
import os
import content as C, render as R, assets
HERE = os.path.dirname(os.path.abspath(__file__))
from icons import ICON

img = lru_cache(None)(lambda k, w=2000: assets.data_uri(k, w))
img.aspect = assets.aspect  # dipakai render untuk menentukan gambar lebar (satu baris penuh)
e = R.e
P = C.PROFILE

SECTIONS = [("pendidikan", "Pendidikan & pelatihan"), ("linimasa", "Lini masa"), ("pengalaman", "Pengalaman kerja"),
            ("proyek", "Proyek"), ("lomba", "Lomba"), ("kegiatan", "Kegiatan lain")]
NUM = {sid: f"{i + 1:02d}" for i, (sid, _) in enumerate(SECTIONS)}
TITLE = dict(SECTIONS)

def contact():
    return (f"<div class='cta'><a class='btn primary' href='mailto:{P['email']}'>{ICON['mail']}{P['email']}</a>"
            f"<a class='btn' href='https://wa.me/{P['wa']}' target='_blank' rel='noopener'>{ICON['wa']}{P['phone']}</a>"
            f"<a class='btn' href='https://{P['linkedin']}' target='_blank' rel='noopener'>{ICON['in']}LinkedIn</a>"
            f"<a class='btn' href='https://{P['github']}' target='_blank' rel='noopener'>{ICON['gh']}GitHub</a></div>")

def sec(sid, body, sub="", alt=False):
    s = f"<p class='sub'>{e(sub)}</p>" if sub else ""
    return (f"<section class='block{' alt' if alt else ''}' id='{sid}' data-stop><div class='wrap'>"
            f"<div class='sec-h'><span class='num'>{NUM[sid]}</span><h2>{TITLE[sid]}</h2>{s}</div>{body}</div></section>")

def hero():
    roles = "".join(f"<li>{r}</li>" for r in P["roles"])
    facts = "".join(f"<div class='tile'><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in C.KEYFACTS)
    agenda = "".join(f"<li><a href='#{s}'><span>{NUM[s]}</span>{t}{ICON['arrow']}</a></li>" for s, t in SECTIONS)
    return f"""<header class="hero" id="top" data-stop><div class="wrap"><div class="bento">
<div class="tile intro"><p class="eyebrow">{ICON['pin']}Portofolio · {e(P['location'])}</p>
<h1>{e(P['first'])} <em>{e(P['last'])}</em></h1><ul class="roles">{roles}</ul><p class="lead">{e(P['summary'])}</p>{contact()}</div>
<figure class="tile photo"><img src="{img('photo0', 700)}" alt="Foto {e(P['first'])} {e(P['last'])}"></figure>
<dl class="facts">{facts}</dl>
{skills()}</div>
<nav class="agenda" aria-label="Agenda presentasi"><p>Agenda</p><ol>{agenda}</ol></nav></div></header>"""

def education():
    d = C.EDU
    focus = "".join(f"<li>{e(x)}</li>" for x in d["focus"])
    act = "".join(f"<li>{e(x)}</li>" for x in d["activity"])
    n = len(C.TRAININGS)
    trains = "".join(R.experience(x, img, i + 1, n) for i, x in enumerate(C.TRAININGS))
    return f"""<article class="edu-card"><div><p class="kind">Pendidikan formal</p><h3>{e(d['school'])}</h3>
<p class="role">{e(d['degree'])}, {e(d['faculty'])}</p><p class="when">{e(d['period'])}</p><div class="gpa"><span>IPK</span>{e(d['gpa'])}</div></div>
<div><h4 class="lbl">Tugas akhir</h4><p class="thesis"><a href="#proyek">{e(d['thesis'].replace('Tugas akhir: ', '').replace(' (lihat bagian Proyek)', ''))}</a></p><h4 class="lbl">Fokus studi</h4><ul class="chips">{focus}</ul><h4 class="lbl">Kegiatan</h4><ul class="did">{act}</ul></div></article>
<h3 class="subh">Pelatihan</h3><div class="trainings">{trains}</div>"""

def timeline():
    legend = "<div class='legend'><span class='work'>Pekerjaan & magang</span><span class='now'>Saat ini</span></div>"
    return f"{legend}<div class='g-scroll'>{R.gantt(C.TIMELINE)}</div><p class='hint'>Klik baris untuk membuka detail.</p>"

NOTE = (f"<aside class='scope-note'>{ICON['info']}<div><strong>Catatan tentang screenshot aplikasi.</strong> "
        "Beberapa dokumentasi menampilkan aplikasi yang dibangun bersama tim. Tampilan (frontend) aplikasi tersebut "
        "<em>bukan</em> buatan saya. Kontribusi saya ada di sisi model AI, data, dan backend, dan dijelaskan di kotak "
        "\"Dikerjakan saya\" pada setiap dokumentasi.</div></aside>")

def experiences():
    n = len(C.EXPERIENCES)
    return "".join(R.experience(x, img, i + 1, n, show_results=False) for i, x in enumerate(C.EXPERIENCES))

def projects():
    return "<div class='proj-list'>" + "".join(R.project(p, img, i + 1) for i, p in enumerate(C.PROJECTS)) + "</div>"

def competition():
    k = C.COMPETITION
    finds = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in k["findings"])
    shots = "".join(R.fig(img(p), c, "lomba") for p, c in k["docs"])
    return f"""<article class="comp"><div class="comp-head"><div><h3>{e(k['name'])}</h3><p class="when">{e(k['period'])} / {e(k['tools'])}</p></div>
<p class="rank">{ICON['trophy']}{e(k['rank'])}</p></div><h4 class="comp-title">{e(k['title'])}</h4><p class="comp-method">{e(k['method_short'])}</p>
<dl class="finds">{finds}</dl></article><div class="shots comp-shots">{shots}</div>"""

def activities():
    cards = []
    for i, t in enumerate(C.TEACHING):
        logos = "".join(f"<img src='{img(k, 300)}' alt=''>" for k in t["logos"])
        pts = "".join(f"<li>{e(p)}</li>" for p in t["points"])
        shots = "".join(R.fig(img(k), c, f"teach{i}") for k, c in t["imgs"])
        w = f" / {e(t['period'])}" if t["period"] else ""
        cards.append(f"<article class='card'><div class='logos'>{logos}</div><h3>{e(t['title'])}</h3><p class='when'>{e(t['org'])}{w}</p>"
                     f"<ul class='did'>{pts}</ul>{'<div class=\"shots one\">' + shots + '</div>' if shots else ''}</article>")
    orgs = "".join(f"<div class='org'><img src='{img(k, 240)}' alt='Logo {e(n)}'><div><strong>{e(n)}</strong><span>{e(d)}</span></div></div>" for k, n, d in C.ORGS)
    photos = "".join(R.fig(img(k, 900), c, "org") for k, c in C.ORG_PHOTOS)
    return (f"<h3 class='subh'>Mengajar & asisten</h3><div class='two'>{''.join(cards)}</div>"
            f"<h3 class='subh'>Organisasi kampus</h3><div class='orgs'>{orgs}</div><div class='shots four'>{photos}</div>")

def skills():
    chips = lambda xs: "<ul class='chips'>" + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
    cols = "".join(f"<div class='tile sk'><h3><span class='ico'>{ICON[k]}</span>{e(t)}</h3>{chips(sk)}</div>"
                   for k, t, sk, _ids in C.SKILL_GROUPS)
    return f"{cols}<div class='tile sk tools'><h3><span class='ico'>{ICON['tools']}</span>Tools</h3>{chips(C.TOOLS.split(', '))}</div>"

def page():
    nav = "".join(f"<li><a href='#{s}'>{t}</a></li>" for s, t in SECTIONS)
    css, js = (open(os.path.join(HERE, f), encoding="utf-8").read() for f in ("style.css", "app.js"))
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Portofolio | {e(P['first'])} {e(P['last'])}</title>
<meta name="description" content="Portofolio {e(P['first'])} {e(P['last'])}: AI Engineer, Data Scientist, Data Analyst.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<script>try{{const t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(_){{}}</script>
<style>{css}</style></head><body>
<nav class="nav" aria-label="Navigasi"><div class="wrap"><a class="brand" href="#top"><span class="mono">SN</span><span class="brand-name">Shionita D. Nainggolan</span></a>
<ul>{nav}</ul><button type="button" class="theme" aria-label="Mode gelap" aria-pressed="false">{ICON['theme']}</button></div></nav>
{hero()}
<main>
{sec('pendidikan', education())}
{sec('linimasa', timeline(), 'Riwayat pekerjaan dan magang.', alt=True)}
{sec('pengalaman', NOTE + experiences(), 'Diurutkan dari yang terbaru.')}
{sec('proyek', projects(), alt=True)}
{sec('lomba', competition(), 'Satria Data (Statistika Ria dan Festival Sains Data), kompetisi data tingkat nasional.')}
{sec('kegiatan', activities(), alt=True)}
</main>
<footer id="kontak" data-stop><div class="wrap"><div class="outro"><p class="eyebrow">Kontak</p><h2>Terima <em>kasih</em></h2><p>{e(P['first'])} {e(P['last'])}</p>{contact()}</div></div></footer>
<div class="presenter" aria-label="Kontrol presentasi"><button type="button" class="p-prev" aria-label="Bagian sebelumnya">{ICON['up']}</button>
<span class="p-count">1</span><button type="button" class="p-next" aria-label="Bagian berikutnya">{ICON['down']}</button></div>
<dialog class="lb" id="lb" aria-label="Pratinjau dokumentasi"><button class="close" type="button" aria-label="Tutup">{ICON['x']}</button>
<div class="lb-inner"><img alt=""><div class="lb-bar"><button class="nav-btn prev" type="button" aria-label="Sebelumnya">{ICON['left']}</button>
<div><p class="lb-cap"></p><p class="lb-count"></p></div><button class="nav-btn next" type="button" aria-label="Berikutnya">{ICON['right']}</button></div></div></dialog>
<script>{js}</script></body></html>"""

if __name__ == "__main__":
    html = page()
    out = os.path.join(HERE, "..", "index.html")
    open(out, "w", encoding="utf-8").write(html)
    s = assets.stats()
    print(f"[build] {s['count']} gambar, {s['bytes'] / 1e6:.2f} MB, HTML {len(html) / 1e6:.2f} MB -> {out}")
