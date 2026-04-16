# Chat Komut Kısaltmaları (Codex)

Bu dosya, bu sohbet içinde kullandığımız kısa komutların anlamını ve çalışma şeklini kayda almak içindir.

## Tetikleme

- Komutlar **tek kelime** yazılarak tetiklenir (case-insensitive): `eko`, `banaver`, `temizle`, `yedek`.
- Mod kapatma: `eko off`, `banaver off`.

## Komutlar

### `eko` (kalıcı mod)

- Yalnız açıkça istenen kapsamda çalışılır; alakasız dosya/arama yapılmaz.
- Varsayılan yanıt **tek satır** ve minimal tutulur (kullanıcı daha fazlasını istemedikçe).

### `bana ver` (kalıcı mod)

- Codex `dart format` / `flutter analyze` / `flutter test` komutlarını **kendi çalıştırmaz**.
- Gerektiğinde bu komutları **kopyala-yapıştır** şeklinde verir ve kullanıcının terminal çıktısını bekler.

Önerilen komut seti:

```powershell
dart format lib test
flutter analyze
flutter test
```

### `temizle` (eylem)

- `flutter clean` çalıştırır.
- Ardından `flutter pub get` çalıştırır.
- `public_release/staging` altında **24 saatten eski** dosyaları siler.
- Python build/cache artıklarını siler: `build/`, `_MEI*`, `__pycache__/`, `*.pyc`.
- Dağıtım artıklarını siler: `*.Windows.zip`.
- `dist/` içindeki EXE temizliği korumalıdır:
  - **En son oluşturulan EXE** korunur.
  - **Son 24 saat içinde oluşturulan EXE'ler** korunur.
  - Bunların dışındaki eski EXE'ler silinir.
- `yedekler/` içindeki `.bundle` temizliği korumalıdır:
  - **En son oluşturulan bundle** korunur.
  - **Son 24 saat içinde oluşturulan bundle'lar** korunur.
  - Bunların dışındaki eski bundle'lar silinir.

Not: Bu sürüm kaynak kod yerine üretim/artık dosyaları temizlemeyi hedefler; kod dosyaları etkilenmez.

### `yedek` (eylem)

- Zaman damgası: `R<yyMMdd-HHmm>` (örn. `R260408-1530`).
- “Her şeyi ekle” prensibi: `git add -A` (untracked dahil).
- Bundle üretimi: `yedekler/R<ts>.bundle`.
- Push: `origin main`.

Önemli notlar:

- Repo kuralı olarak `besmele/AGENTS.md` altında “`.bundle` depoya commit edilmez” denir; bu kısaltma ise kullanıcı isteğiyle **bundle’ı da commit/push** eder.
- Commit/push öncesi format/analyze/test kapısı gerekir. `banaver` açıksa Codex komutları verir ve çıktı bekler; değilse Codex çalıştırarak ilerler.
