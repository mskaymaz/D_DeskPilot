# Todo UI / UX Design

## Vizyon

To-do paneli sadece yapılacaklar listesi olmayacak.

Kullanıcının baktığında hoşuna giden, göz yormayan, sempatik ve işlevsel bir günlük çalışma paneli olacak.

## İstemediğimiz Şey

```text
Düz gri pencere
Ruhsuz liste
Sıkıcı checkbox dizisi
Ayarlar içinde onlarca karmaşık renk satırı
Okunması zor küçük metinler
```

## İstediğimiz Şey

```text
Estetik
Canlı ama göz yormayan
Kullanıcıya sıcak gelen
Bay/bayan fark etmeksizin genel beğeniye uygun
Okunabilir
Kişiselleştirilebilir
Panel içinde hızlı ayarlanabilir
```

## Ana Panel Taslağı

```text
┌────────────────────────────────────┐
│ Bugünün İşleri              🎨 ⚙  │
├────────────────────────────────────┤
│ [+ Hızlı görev ekle...]            │
│                                    │
│ Bugün                              │
│ ┌────────────────────────────────┐ │
│ │ ☐ Kod kontrolü          Yüksek │ │
│ │   Release öncesi bakılacak     │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ ☐ Market alışverişi     Normal │ │
│ └────────────────────────────────┘ │
│                                    │
│ Tamamlananlar                      │
│ ✓ Eski notları temizle             │
└────────────────────────────────────┘
```

## Panel Üst Araçları

Ayarlar penceresini büyütmemek için panelin üstünde küçük ve kibar kontroller olacak.

Örnek:

```text
🎨 Tema
▣ Panel rengi
A Yazı rengi
□ Çerçeve rengi
Aa Yazı ölçeği
↔ Resize
```

Bu kontroller:

- Panelin üst kısmında küçük ikonlar halinde olabilir.
- Hover ile açıklama gösterebilir.
- Açılır mini renk paleti sunabilir.
- Ayarlar penceresine onlarca yeni satır eklemez.

## Renk Yaklaşımı

Hazır tema paletleri:

- Sade Gece
- Açık Ferah
- Kahve Tonu
- Mavi Odak
- Yeşil Sakin
- Mor Yumuşak
- Pembe Zarif
- Kontrast Okunur

Kullanıcı isterse ayrıca:

- Panel zemin rengi
- Kart rengi
- Yazı rengi
- Çerçeve rengi
- Vurgu rengi

seçebilir.

## Görev Kartı

Görevler düz satır değil, kart olmalı.

Kart içinde:

- Checkbox
- Başlık
- Açıklama özeti
- Öncelik rozeti
- Tarih etiketi
- Alt görev ilerleme çubuğu
- Hızlı işlem butonları

Örnek:

```text
┌─────────────────────────────────┐
│ ☐ Ödev taslağını hazırla  Acil  │
│   Giriş ve sonuç kısmı yazılacak │
│   Alt görev: 2/5                │
└─────────────────────────────────┘
```

## Öncelik Görünümü

Öncelikler görsel olarak ayrılmalı ama rahatsız edici olmamalı.

- Düşük
- Normal
- Yüksek
- Acil

Her öncelik için:

- Yumuşak arka plan
- Küçük rozet
- Okunabilir metin

## Durumlar

- Bekliyor
- Devam ediyor
- Tamamlandı
- İptal
- Gecikmiş

Tamamlanan görevler soluklaşabilir ama tamamen kaybolmaz.

## Resize Davranışı

Panel köşelerinden büyütülüp küçültülebilir.

Panel büyüdükçe oranlı büyüyecekler:

- Yazılar
- Checkboxlar
- Kart iç boşlukları
- Butonlar
- Rozetler
- İkonlar
- Arama kutusu
- Filtreler

Panel küçüldükçe:

- Metinler kırpılmadan mümkün olduğunca ölçeklenir.
- Kartlar sıkışır ama okunurluk korunur.
- Çok küçük boyutta kompakt moda geçilebilir.

## Oranlı Ölçekleme İlkesi

```text
base_width = 360
current_width = panel.width
scale = current_width / base_width
scale = clamp(scale, 0.75, 1.60)
```

Ölçeklenen değerler:

```text
font_size
checkbox_size
icon_size
padding
margin
border_radius
card_spacing
```

## Okunurluk Kuralı

- Yazı boyutu minimum 10 px altına düşmemeli.
- Checkbox tıklama alanı minimum 22 px olmalı.
- Kartlar arasında yeterli boşluk kalmalı.
- Renk kontrastı okunabilir olmalı.
- Kullanıcının seçtiği renk kötü kontrast üretiyorsa otomatik uyarı veya düzeltme yapılmalı.

## Panel İçi Mini Tema Editörü

Önerilen yapı:

```text
🎨
  Tema Seç:
    Sade Gece
    Açık Ferah
    Mavi Odak
    Yeşil Sakin

  Renkler:
    Panel
    Kart
    Yazı
    Çerçeve
    Vurgu

  [Varsayılana Dön]
```

## Neden Ayarlar Penceresine Koymuyoruz?

Çünkü:

- Ayarlar penceresi kalabalıklaşır.
- Kullanıcı paneli görmeden renk seçer.
- Deneme/yanılma zorlaşır.
- Panel estetiği panel üzerinde ayarlanmalıdır.

Bu nedenle görsel ayarlar panel üzerinde, genel davranış ayarları ana ayarlar içinde kalmalıdır.
