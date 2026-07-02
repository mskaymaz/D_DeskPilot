# PROJECT_PHILOSOPHY

## Ana lke

Bu proje ve bağlantılı uygulamalar ücretsiz, sade, kaliteli ve insanlık hayrına geliştirilen uygulamalardır.

## Kesin Kurallar

- Ücretli servis yok.
- Ücretli API yok.
- Abonelik yok.
- Kota bağımlılığı yok.
- nternet zorunluluğu yok.
- Kullanıcıdan veri toplama yok.
- Gereksiz karmaşıklık yok.

## TTS lkesi

- Windows'un kendi offline ses sistemi kullanılacak.
- Erkek ses varsa tercih edilecek.
- Yoksa sistem varsayılan sesi kullanılacak.
- Bulut TTS kullanılmayacak.

## Tasarım lkesi

- Gri duvar görünümü olmayacak.
- Estetik, okunabilir ve sempatik arayüz hedeflenecek.
- Ayarlar penceresi gereksiz şişirilmeyecek.
- Panel içi hızlı tema/renk kontrolleri tercih edilecek.
- Resize yapıldığında içerik oranlı büyüyüp küçülecek.

## Kod lkesi

- Mümkünse her kaynak dosya 500 satır altında tutulacak.
- UTF-8 / Türkçe karakter temizliği korunacak.
- Gereksiz refactor yapılmayacak.
- Her değişiklikten sonra derleme/syntax kontrolü yapılacak.

## Globalization / i18n Architecture Rule
DeskPilot must be designed so Turkish, English, and Arabic can be supported without rewriting UI logic.
User-facing strings should gradually move from hardcoded text into a translation layer such as `translations/tr.json`, `translations/en.json`, and `translations/ar.json`.
Arabic support must be treated as RTL-aware: alignment, layout direction, icon/text order, and font readability must be checked separately.
