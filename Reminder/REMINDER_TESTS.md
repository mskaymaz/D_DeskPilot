# Reminder Tests

## Genel Test Komutları

```powershell
cd D:\Code\mskaymaz\D_DigitalSaat
python -m py_compile .\*.py
python .\digitalSaatV2.py
```

## Test Listesi

### T-001 Uygulama Açılışı

- [ ] Uygulama açılıyor
- [ ] Eski hatırlatmalar bozulmadan yükleniyor
- [ ] Konsolda hata yok

### T-002 Tek Hatırlatma

- [ ] Yeni hatırlatma ekleniyor
- [ ] Ana zamanda bildirim geliyor
- [ ] Başlık doğru
- [ ] Açıklama doğru

### T-003 Sesli Ön Uyarı

- [ ] 20 dakika önce uyarı çalışıyor
- [ ] 1 saat önce uyarı çalışıyor
- [ ] 1 gün önce uyarı çalışıyor
- [ ] TTS başlığı okuyor
- [ ] TTS açıklamayı okuyor
- [ ] TTS kalan süreyi okuyor

### T-004 Limit Kontrolü

- [ ] 10 ön uyarı eklenebiliyor
- [ ] 11. ön uyarı engelleniyor
- [ ] Aynı uyarı ikinci kez eklenemiyor
- [ ] Ana zamandan sonra uyarı eklenemiyor

### T-005 Tekrarlı Sesli Uyarı

- [ ] 1 gün kala 3 saatte bir çalışıyor
- [ ] Çakışan uyarılar tekilleştiriliyor
- [ ] Kapatıldığında çalışmıyor

### T-006 TTS Fallback

- [ ] Erkek ses varsa kullanılıyor
- [ ] Erkek ses yoksa varsayılan ses kullanılıyor
- [ ] TTS hata verirse uygulama çökmeden devam ediyor

### T-007 Popup

- [ ] Popup görünüyor
- [ ] Tamamlandı çalışıyor
- [ ] Ertele çalışıyor
- [ ] Aç çalışıyor
- [ ] Popup ana saat görünümünü kapatmıyor

### T-008 Geriye Uyumluluk

- [ ] Eski JSON kayıtları açılıyor
- [ ] Eksik alanlar varsayılanla tamamlanıyor
- [ ] Bozuk kayıt uygulamayı çökertmiyor
