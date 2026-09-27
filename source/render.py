"""Komponen HTML murni: data -> string. Tidak ada I/O."""
import re
from html import escape as e

def fig(uri, cap, gid, wide=False, ui=None):
    tag = f'<span class="ui-tag">Antarmuka: {e(ui)}</span>' if ui else ""
    return (f'<figure class="shot{" wide" if wide else ""}">{tag}<button type="button" class="shot-btn" data-group="{gid}" aria-label="Perbesar: {e(cap)}">'
            f'<img src="{uri}" alt="{e(cap)}" loading="lazy"></button><figcaption>{e(cap)}</figcaption></figure>')

def credit(mine, ui):
    """Pembeda kontribusi: siapa mengerjakan apa pada screenshot aplikasi."""
    return (f"<dl class='credit'><div class='mine'><dt>Dikerjakan saya</dt><dd>{e(mine)}</dd></div>"
            f"<div class='ui'><dt>Tampilan/antarmuka</dt><dd>Bukan buatan saya, {e(ui)}</dd></div></dl>")

def docs(groups, gid, img):
    out = ""
    for t, s, *cr in groups:
        out += (f"<div class='doc'><h5>{e(t)}</h5>{credit(*cr) if cr else ''}<div class='shots{' one' if len(s) == 1 else ''}'>"
                + "".join(fig(img(k), c, gid, img.aspect(k) >= 1.7, cr[1] if cr else None) for k, c in s) + "</div></div>")
    return f"<div class='docs'><h4 class='lbl'>Dokumentasi</h4>{out}</div>"

def meta(x, img, n=None):
    logo = (f"<img class='logo' src='{img(x['logo'], 360)}' alt='Logo {e(x['org'])}'>" if x.get("logo")
            else f"<div class='mark'>{e(x.get('mono', x['org'][0]))}</div>")
    idx = f"<span class='idx'>{n}</span>" if n else ""
    note = f"<p class='note'>{e(x['note'])}</p>" if x.get("note") else ""
    tags = "".join(f"<li>{e(t)}</li>" for t in x.get("tags", []))
    tags = f"<ul class='tags'>{tags}</ul>" if tags else ""
    return (f"<header class='meta'>{idx}{logo}<h3>{e(x['org'])}</h3><p class='role'>{e(x['role'])}</p>"
            f"<p class='when'>{e(x['period'])}{'<br>' + e(x['place']) if x.get('place') else ''}</p>{note}{tags}</header>")

def experience(x, img, n, total, show_results=True):
    did = "".join(f"<li>{e(p)}</li>" for p in x["did"])
    res = "".join(f"<li>{e(r)}</li>" for r in x["results"])
    res = f"<h4 class='lbl'>Hasil</h4><ul class='results'>{res}</ul>" if res and show_results else ""
    return (f"<article class='exp' id='{x['id']}' data-disc='{x['disc']}' data-stop>{meta(x, img, f'{n} / {total}')}"
            f"<div class='body'><p class='context'>{e(x['context'])}</p><h4 class='lbl'>Yang saya kerjakan</h4>"
            f"<ul class='did'>{did}</ul>{res}{docs(x['docs'], x['id'], img)}</div></article>")

def gantt(rows, start=(2024, 6), end=(2026, 10)):
    """Posisi bar = (bulan - start) / rentang. Label di kolom kiri agar tidak pernah terpotong."""
    m = lambda ym: ym[0] * 12 + ym[1]
    pct = lambda ym: round(100 * (m(ym) - m(start)) / (m(end) - m(start)), 2)
    ticks = "".join(f"<span class='tick' style='left:{pct((y, 1))}%'>{y}</span>" for y in range(2025, 2027))
    body = "".join(
        f"<a class='g-row {k}' href='#{a}'><span class='g-lbl'>{e(l)}</span><span class='g-track'>"
        f"<span class='g-bar' style='left:{pct(s)}%;width:{max(pct(f) - pct(s), 1.2)}%'></span></span></a>"
        for l, s, f, a, k in rows)
    return (f"<div class='gantt'><div class='g-row g-axis'><span></span><span class='g-track'>{ticks}</span></div>{body}</div>")

def project(p, img, n):
    gid = "proj-" + re.sub(r"\W+", "-", p["title"].lower())
    badge = f"<p class='badge'>{e(p['badge'])}</p>" if p.get("badge") else ""
    meta_ = " / ".join(x for x in (p["period"], p["tools"]) if x)
    sub = f"<p class='kind'>{e(p['sub'])}</p>" if p.get("sub") else ""
    pm = (f"<dl class='pm'><div><dt>Masalah</dt><dd>{e(p['problem'])}</dd></div>"
          f"<div><dt>Metode</dt><dd>{e(p['method'])}</dd></div></dl>")
    if p.get("findings"):  # proyek unggulan: teks penuh, angka kunci, lalu galeri dua kolom
        finds = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in p["findings"])
        shots = "".join(fig(img(k), c, gid) for k, c in p["imgs"])
        return (f"<article class='proj featured'><span class='idx'>{n:02d}</span>{sub}<h3>{e(p['title'])}</h3>"
                f"<p class='when'>{e(meta_)}</p>{pm}<dl class='finds'>{finds}</dl><div class='shots two-col'>{shots}</div></article>")
    shots = "<div class='shots'>" + "".join(fig(img(k), c, gid) for k, c in p["imgs"]) + "</div>"
    return (f"<article class='proj'><div class='proj-body'><span class='idx'>{n:02d}</span><h3>{e(p['title'])}</h3>"
            f"<p class='when'>{e(meta_)}</p>{badge}{pm}</div>{shots}</article>")
