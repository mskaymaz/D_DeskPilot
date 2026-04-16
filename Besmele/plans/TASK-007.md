# TASK-007

status: review
owner: UNASSIGNED
updated: 2026-04-16 17:10 +03:00
scope: `eko` ve `ozet` cevap disiplini, tum pencerelerde topmost guclendirmesi, `derle` akisinin canli exe ciktisi ve bu exe'nin repo icinde versiyonlanmasi

goal:
- Ekonomik cevap komutlarini resmi hale getirmek ve uygulamanin gorev cubugu ustunde kalma davranisini daha dayanikli yapmak

in_scope:
- `eko` ve `ozet` komut vitrini kayitlari
- Ana ve serbest pencerelerde `her zaman ustte` pekistirmesi
- `derle` araci ile R etiketli exe uretimi
- Uretilen `exe` ciktisinin repo icindeki dagitim klasorunde push edilmesi

out_of_scope:
- Yeni UI tasarimi
- Gorev cubugu icin derin Win32 shell kancalari

plan:
- [x] `eko` ve `ozet` komutlarini resmi kayitlara isle
- [x] Tum gorunur pencerelerde topmost zorlamasini ortaklastir
- [x] `derle` akisiyla canli Windows exe ciktisi al
- [x] Yedek teslimi icin `STATE/HISTORY` ve git kayitlarini tamamla
- [x] Uretilen `exe` dosyasini repo icine al ve push et

log:
- 2026-04-16 12:48 +03:00 | `eko` ve `ozet` resmi cevap komutlari olarak eklendi.
- 2026-04-16 17:01 +03:00 | Tum pencerelerde `her zaman ustte` davranisi gorev cubugu kosulundan bagimsiz guclendirildi.
- 2026-04-16 17:03 +03:00 | `derle` ile `DigitalSaat_R.260416_1703.exe` canli olarak uretildi.
- 2026-04-16 17:06 +03:00 | Yedek teslimi icin plan, state ve history kayitlari guncellendi.
- 2026-04-16 17:10 +03:00 | Kullanici talebiyle `exe` artefaktini repo icindeki `dagitim/` klasorunde de versiyonlama karari alindi.

verification:
- [x] `python -m py_compile core_window.py`
- [x] `python Besmele/tools/derle.py --ad DigitalSaat --giris digitalSaatV2.py`
- [ ] Repo icindeki `dagitim/` binary dosyasi icin uzaktan indirme/dogrulama yapilmadi

handover:
- next: Binary dagitimin repo boyutuna etkisini izle; gerekirse GitHub Release akisina gec.
- risk: Binary dosyalari git gecmisini hizla buyutebilir.
