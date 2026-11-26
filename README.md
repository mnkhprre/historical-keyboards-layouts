# Historical Keyboards

macOS keyboard layouts for ancient and historical languages, in one installable bundle.
*Tarihî diller için macOS klavye düzenleri, tek bir paket hâlinde. Türkçe açıklama aşağıda.*

| Layout | Script / purpose | Folder |
|---|---|---|
| **Old Turkic** | Old Turkic (Orkhon) runes | [`layouts/old-turkic`](layouts/old-turkic) |
| **Old Persian** | Old Persian cuneiform | [`layouts/old-persian`](layouts/old-persian) |
| **Ottoman (Latin)** | Latin transcription of Ottoman Turkish | [`layouts/ottoman-latin`](layouts/ottoman-latin) |
| **Bronze Age Transliteration** | Transliteration of Akkadian, Hittite, Egyptian and other Bronze Age languages | [`layouts/bronze-age-translit`](layouts/bronze-age-translit) |
| **Nesili** | Hittite (Nesili) layout with a custom icon | [`layouts/nesili`](layouts/nesili) |
| **Morse (Turkish Q)** | Morse code on the Turkish Q layout | [`layouts/morse-tr`](layouts/morse-tr) |

Each folder's README describes that layout's modifier layers.

## Install

**From a release:** download `HistoricalKeyboards.bundle.zip` from
[Releases](../../releases), unzip it, and copy `HistoricalKeyboards.bundle` into
`~/Library/Keyboard Layouts/` (current user) or `/Library/Keyboard Layouts/` (all users).

**From source:**

```bash
scripts/install.sh
```

Then log out and back in, open **System Settings → Keyboard → Input Sources → Edit → +**,
and pick the layouts under **Others**.

To remove: `scripts/install.sh --uninstall`.

To install a single layout only, copy its `.keylayout` and `.icns` from `layouts/<name>/`
into `~/Library/Keyboard Layouts/`.

## Development

Layouts are edited with [Ukelele](https://software.sil.org/ukelele/).

- `layouts.json` lists every layout in the bundle, with its language code and Turkish name.
- `scripts/validate.py` checks that files exist, XML parses, and ids/names are unique.
- `scripts/build_bundle.py` writes `dist/HistoricalKeyboards.bundle`.
- `scripts/make-icon.swift "<glyph>" "<font>" out.icns` renders a glyph icon.
- Pushing a tag `v*` builds the bundle in GitHub Actions and attaches it to a release.

To add a layout: create `layouts/<name>/<name>.keylayout` and `<name>.icns`, add an entry to
`layouts.json`, pick a unique negative `id`, and run `python3 scripts/validate.py`.

The full git history of each original repository is kept under its folder
(`git log -- layouts/<name>`).

## Türkçe

Bu depo, daha önce ayrı repolarda duran klavye düzenlerimi bir araya getirir:
Göktürkçe (Orhun), Eski Farsça, Osmanlıca (Latin transkripsiyon), Tunç Çağı transliterasyon,
Nesili (Hititçe) ve Mors (Türkçe Q).

**Kurulum:** [Releases](../../releases) sayfasından `HistoricalKeyboards.bundle.zip` dosyasını
indirin, açın ve `HistoricalKeyboards.bundle`'ı `~/Library/Keyboard Layouts/` klasörüne kopyalayın.
Oturumu kapatıp açın; ardından **Sistem Ayarları → Klavye → Giriş Kaynakları → Düzenle → +**
yolunu izleyip **Diğerleri** altından düzenleri seçin. Kaynaktan kurmak için `scripts/install.sh`.

## License and credits

GPL-3.0 (see [`LICENSE`](LICENSE)). Third-party work is listed in [`CREDITS.md`](CREDITS.md).
