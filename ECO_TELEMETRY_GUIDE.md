# IST-017: Eco-SDK İstemci Entegrasyon Rehberi (Masaüstü, Mobil, Web)

> **Bağlı Mimari Kararlar:** [013 — Ekosistem Telemetri & Cihaz Kimliği (`IST-013`)](013-ekosistem-telemetri-cihaz-kimligi-ve-istatistik-mimarisi.md) | [016 — Melez Hızlı Dağıtım (`IST-016`)](016-melez-hizli-dagitim-r2-ve-worker-cache-mimarisi.md)  
> **Hedef Kitle:** Uygulama repolarında (`D_*`, `M_*`, Web, `PushPull`, `Avkat`) güncelleme yapan **AI Kod Ajanları**.

---

## 1. Bağlayıcı Genel Kurallar (Tüm Platformlar)

1. **Tek Uç Nokta:** `POST https://msklabsdesk-backend.msklabs-org.workers.dev/api/v1/telemetry/heartbeat` (`Content-Type: application/json`).
2. **Kapanış İsteği Yok & `+7 Gün` Doğal Dağıtım:**
   - Uygulama **kapanırken** asla ağ isteği atmaz.
   - Uygulama her açıldığında yerelde `pending_launches += 1` artırılır.
   - Yalnızca şu **3 durumda** (ve internet varsa, arka planda UI'ı bloklamadan) tek paket gönderilir:
     1. İlk kurulum veya yeniden kurulum (`eco_state` yok ama `eco_device_id` zaten varsa `reinstall_count = 1`),
     2. Sürüm değişimi (`current_version != last_sent_version`),
     3. Son başarılı gönderimden itibaren **7 gün** (`604800` sn) geçmiş olması.
   - Sunucu `200 OK` döndüğünde yerel `pending_launches = 0`, `last_heartbeat_at = now`, `last_sent_version = current_version` kaydedilir. Ağ yoksa veya hata alınırsa değerler korunur, bir sonraki açılışta tekrar denenir.
3. **Sessiz Çalışma & Mağaza Kuralı:**
   - Uygulama içi ayarlarda opt-out anahtarı veya izin pop-up'ı **konulmaz**.
   - **Google Play / App Store** uygulamalarında mağaza *Data Safety / App Privacy* formunda *"App Analytics & Diagnostics (anonim, PII içermez)"* işaretlenir ve webdeki `privacy.html` bağlantısı gösterilir.
4. **Resmi `app_id` & İsimlendirme Standardı (Tek Kaynak = `app_catalog.json`):**
   - **Görünen Ad (Vitrin):** `Haydi Namaza`, `RekatSay`, `Date Counter` (boşluklu).
   - **Teknik Kimlik (`app_id`, R2, `/dl/`, Telemetri — `snake_case`):** `haydi_namaza`, `rekatsay`, `date_counter` *(Mağaza paket adı: `org.msklabs.<app_id>`).* Kod içine asla repo adı (`D_...`, `M_...`) veya görünen ad yazılmaz.

### Ortak JSON İstek Gövdesi
```json
{
  "eco_device_id": "eco_d4a1b89c-3e2f-4c5a-90ab-123456789abc",
  "app_id": "haydi_namaza",
  "app_version": "2.4.1",
  "install_source": "direct",
  "platform": "windows",
  "os_name": "Windows",
  "os_release": "11",
  "launch_count": 14,
  "reinstall_count": 0,
  "crashes": []
}
```
*(Destek formu kullanan uygulamalarda `support.ts` isteğine opsiyonel `eco_device_id` ve `app_version` alanları da eklenir.)*

---

## 2. Masaüstü Entegrasyonu (Windows / Linux / macOS)

### A. Ortak Kimlik Dosyası (`eco_identity.json`)
- **Windows:** `%APPDATA%\MSKLabs\eco_identity.json`
- **Linux:** `~/.config/msklabs/eco_identity.json`
- **macOS:** `~/Library/Application Support/MSKLabs/eco_identity.json`
- **İçerik:** `{"eco_device_id": "eco_<UUIDv4>", "created_at": "2026-11-24T16:00:00Z"}`
- **Zorunlu Atomik Yazma:** Dosya yoksa önce `eco_identity.json.tmp` oluşturup sonra `rename` ile hedefe taşıyın (iki MSK uygulaması aynı anda açılırsa dosya bozulmaz). Yazma izni yoksa uygulama kendi yerel veri klasörüne fallback yapar.

### B. Uygulama İçi Durum & 7 Günlük Gönderim Mantığı (Örnek Akış)
```text
1. eco_device_id = readOrCreateAtomic(SHARED_DIR / "eco_identity.json")
2. state = readJson(APP_LOCAL_DIR / "eco_state.json", default={
     pending_launches: 0, last_heartbeat_at: 0, last_sent_version: ""
   })
3. state.pending_launches += 1
4. isReinstall = (!fileExists(APP_LOCAL_DIR / "eco_state.json") && identityAlreadyExisted)
5. shouldSend = isReinstall
             || (state.last_heartbeat_at == 0)
             || (APP_VERSION != state.last_sent_version)
             || (nowUnix() - state.last_heartbeat_at >= 7 * 86400)
6. writeJson(APP_LOCAL_DIR / "eco_state.json", state)
7. if shouldSend:
     asyncPostHeartbeat(...) -> on 200 OK:
       state.pending_launches = 0
       state.last_heartbeat_at = nowUnix()
       state.last_sent_version = APP_VERSION
       writeJson(APP_LOCAL_DIR / "eco_state.json", state)
```

---

## 3. Mobil Entegrasyonu (Android & iOS / Flutter)

### A. Android Zorunlu Kurallar
1. **Ortak İmza:** Tüm MSK Android uygulamaları Play Console / yerel build'de **aynı Keystore anahtarı** ile imzalanır.
2. **`Signature-Level ContentProvider`:** İlk açılan uygulama `eco_device_id` üretir ve `android:protectionLevel="signature"` korumalı `ContentProvider` (`authority: org.msklabs.eco.identity`) üzerinden paylaşır.
3. **Android 11+ `<queries>` Manifest Bloğu:** Her uygulamanın `AndroidManifest.xml` dosyasına diğer MSK paketlerini/provider'ı görebilmesi için `<queries>` bloğu eklenir:
   ```xml
   <queries>
     <provider android:authorities="org.msklabs.eco.identity" />
   </queries>
   ```
4. **Yerel Kopya Güvencesi:** İkinci uygulama `ContentProvider`'dan `eco_device_id` okuduğu anda **kendi `EncryptedSharedPreferences` deposuna kalıcı kopyasını** yazar (ilk uygulama silinse bile kimlik kaybolmaz).

### B. iOS Zorunlu Kurallar
- Tüm MSK iOS uygulamalarında Xcode `Keychain Sharing` + `App Groups` (`group.org.msklabs.shared`) aktif edilir; `eco_device_id` Keychain'e yazılır ve oradan okunur.

### C. Mobil Gönderim Döngüsü
- Masaüstü Bölüm 2.B'deki aynı 7 günlük `pending_launches` mantığı uygulanır (`SharedPreferences` / `UserDefaults` üzerinde tutulur, `initState` / `onCreate` aşamasında arka planda çalıştırılır).

---

## 4. Web Entegrasyonu (`*.msklabs.org`)

- **Kimlik:** `document.cookie` üzerinden `Domain=.msklabs.org; SameSite=Lax; Secure; max-age=31536000` çerezi + `localStorage.getItem('eco_device_id')` fallback'i kullanılır. Parmak izi (`FingerprintJS`, Canvas/Audio hash) **yasaktır**.
- **Gönderim:** Sayfa açılışında `localStorage` üzerindeki `eco_state_<app_id>` kontrol edilir; aynı 7 günlük kural geçerlidir. İstek `fetch(ENDPOINT, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload), keepalive: true })` ile atılır.
