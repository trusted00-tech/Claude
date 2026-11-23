# ORORA Motion Engine

Video motion graphic 9:16 (TikTok/Reels) dari data produk. Format v1 di-approve Jhon 2026-11-23.
Stack: HTML template + Playwright (render frame) + ffmpeg. Tanpa After Effects, tanpa biaya per render.

## Struktur video (15.5 detik, default)
| Scene | Fungsi | Isi config |
|---|---|---|
| hook (2.3s) | Tahan swipe | foto close-up / klip Seedance + teks kinetik |
| benefit (3.0s) | 3 manfaat | foto full body + 3 chip |
| detail (2.9s) | Pembeda produk | zoom ke focal + lingkaran |
| proof (2.7s) | Bukti bahan | infografis listing + meter angka |
| sizes (2.0s) | Hilangkan ragu size | foto + chip size |
| cta (2.6s) | Konversi | "Klik keranjang kuning" + panah |

## Pakai
```bash
python3 prep_product.py <shopify-handle>            # ambil foto orora.co.id -> assets/<handle>/ (cleanN = teks listing dihapus)
cp configs/jaket-fullzip-coffee.json configs/<baru>.json   # edit teks, foto, focal
./build.sh configs/<baru>.json out.mp4 [vo.mp3]     # render; vo opsional (ElevenLabs), musik otomatis di-duck
```
Requirements: node + playwright (chromium), python3 + numpy + opencv-python-headless, ffmpeg, font Inter Display.

## Config
- `lines`: `*kata*` = kotak merah, `_kata_` = kotak kuning, `~teks~` = baris kecil.
- `img` + `focal:[x,y]` (koordinat di foto 1024px) + `zoom:[awal,akhir]` opsional.
- **Mode overlay Seedance**: ganti `img` dengan `"video": "/path/clip.mp4"` (+ `videoStart` detik). Teks/CTA ditempel di atas klip.
- `timing` opsional untuk ubah durasi per scene.

## Aturan konten (wajib)
1. Klaim hanya dari listing resmi (bahan, size chart, kebijakan tukar size). Tidak mengarang.
2. Harga TIDAK ditampilkan (harga promo TikTok bisa beda) -> CTA "Cek harga promo".
3. Teks di area aman: x 70–910, y 250–1560 (hindari ikon kanan & caption bawah TikTok).
4. Hook ≤ 6 kata, 1 kata di-highlight. CTA selalu keranjang kuning.
5. Positioning ORORA: effortless, nyaman, praktis. Bukan luxury.
6. Musik di file = placeholder; saat upload pakai trending sound.
