# Resize System

## Amaç

Panel büyüdüğünde sadece boşluk büyümeyecek.

çerik de oranlı büyüyecek.

## Ölçeklenecek Öğeler

- Yazı boyutu
- Checkbox boyutu
- Kart iç boşluğu
- Butonlar
- konlar
- Rozetler
- Kenar boşlukları
- Köşe yuvarlaklığı

## Temel Formül

base_width = 360
scale = current_width / base_width
scale = clamp(scale, 0.75, 1.60)

## Okunurluk

- Yazı minimum 10 px altına düşmemeli.
- Checkbox tıklama alanı minimum 22 px olmalı.
- Panel küçülürse kompakt moda geçilebilir.
