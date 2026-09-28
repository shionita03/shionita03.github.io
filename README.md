# Portofolio Shionita Dwilani Nainggolan

## Cara membuka

Klik dua kali `index.html`. Halaman langsung terbuka di browser (Chrome, Edge, Firefox, atau Safari).
Tidak perlu server atau instalasi apa pun: semua gambar, CSS, dan JavaScript sudah ada di dalam satu file itu.

Untuk presentasi interview, tekan **→ / ←** di keyboard atau pakai tombol ↑ ↓ di pojok kanan bawah untuk pindah bagian.
Klik gambar mana pun untuk memperbesar.

Tombol bulat di kanan atas mengganti tema terang/gelap (pilihan diingat browser; bawaannya mengikuti pengaturan sistem).

Catatan: jenis huruf (Space Grotesk, DM Sans, dan Instrument Serif) diambil dari Google Fonts. Tanpa internet,
halaman tetap berjalan normal dengan huruf cadangan dari sistem.

## Cara mengubah isi

Semua teks ada di satu file: `source/content.py`. Tampilan tidak perlu disentuh.

```bash
cd source
pip install -r requirements.txt   # sekali saja (Pillow, untuk memproses gambar)
python build.py                   # menulis ulang ../index.html
```

Lalu refresh browser.

## Isi folder source

| File | Fungsi |
|---|---|
| `content.py` | Semua isi: profil, pendidikan, pengalaman, proyek, lomba, kegiatan |
| `render.py` | Komponen HTML (kartu pengalaman, lini masa, galeri) |
| `build.py` | Menyusun urutan bagian dan menulis `index.html` |
| `assets.py` | Mengompres gambar ke WebP dan menanamkannya ke HTML |
| `style.css` | Warna, huruf, dan tata letak |
| `app.js` | Pembesar gambar, navigasi aktif, dan mode presentasi |
| `img/` | Gambar sumber. Kode gambar di `content.py`: `p12` = `img/port/p-012.png`, `d3` = `img/doc/d-003.png`, `t26` = `img/ta/t-026.png` |

Untuk menambah gambar baru, simpan misalnya sebagai `img/doc/d-008.png`, lalu pakai kode `d8` di `content.py`.
