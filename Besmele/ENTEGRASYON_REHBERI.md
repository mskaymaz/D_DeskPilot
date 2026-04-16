# ENTEGRASYON REHBERI

Amac: Besmele'yi yeni veya mevcut bir repoya temiz, tekrar edilebilir ve dogrulanabilir sekilde kurmak.

## Uc Mod
- `ozetten_kur`: Yeni repo icin proje ozetinden hareketle Besmele omurgasi ve ilk mimariyi kurar.
- `repoyu_incele`: Mevcut repo yapisini, kodlarini, `md` talimatlarini ve ilerleme hafizasini okuyup baglama alir.
- `temizlik_oner`: Kaldirilabilir adaylari listeler; kesin silme yalniz kullanici onayi ile yapilir.

## Mod 1: ozetten_kur
1. Repo kokune `AGENTS.md`, `CORE.md`, `STATE.md` yerlestirilir.
2. `Besmele/` klasoru operasyon omurgasi olarak eklenir.
3. `PROFIL_REHBERI` uzerinden `mini`, `standart` veya `ileri` seviye secilir.
4. Ilk mimari yon, ilk task ve calisma hafizasi repo ozetiyle birlikte kurulur.
5. Hook yolu istenirse `git config core.hooksPath Besmele/hooks` ile etkinlestirilir.
6. Kurulum `python Besmele/tools/validate_besmele.py` ile dogrulanir.

## Mod 2: repoyu_incele
- Repo agaci, kodlar, mevcut `md` talimatlari ve varsa mevcut calisma kurallari okunur.
- `task`, `roadmap`, `todo`, `progress`, `handover` ve benzeri hafiza dosyalari yuksek oncelikle korunur.
- Besmele disi task sistemi otomatik silinmez; once anlamli bir esleme yapilip gerekiyorsa birlikte yasama modeli kurulur.
- Sonuc olarak `ENTEGRASYON_HARITASI` uretilir.

## ENTEGRASYON_HARITASI Icerigi
- `baglam_ozeti`: Repo ne yapiyor, nerede duruyor, aktif is nedir.
- `hafiza_kaynaklari`: Korunacak task, roadmap, handover ve benzeri dosyalar.
- `besmele_esleme`: Hangi mevcut yapilarin Besmele hangi dosyasi veya katmaniyla iliskilenecegi.
- `temizlik_adaylari`: Gereksiz, cakisan veya artik aktif olmayan dosyalar.
- `onay_bekleyenler`: Yalniz kullanici onayi ile silinecek veya arsivlenecek maddeler.

## Mod 3: temizlik_oner
- Temizlik daima liste olarak baslar; otomatik silme ile baslamaz.
- Ozellikle mevcut task ve ilerleme hafizasina dokunulmaz.
- Kullanici `hangileri haric` dedikten sonra kalan adaylar temizlenir.
- Temizlik deseni `TEMIZLIK_POLITIKASI.md` uzerinden yorumlanir.

## Temizlik Komut Ailesi
- `temizle`: Adaylari listeler ve risk durumunu ozetler.
- `temizle liste`: Yalniz temizlenebilir artefaktlari gosterir.
- `temizle uygula`: Guvenli adaylari siler.
- `temizle derin`: Daha genis artefakt/cikti/cache temizligi icin oneri veya uygulama akisina gecer.

## Optimize Komut Ailesi
- `optimize`: Talimat ve `md` yapilarinda guvenli konsolidasyon adaylarini listeler.
- `optimize uygula`: Onaylanan sadeleştirmeyi uygular; guc kaybi riski varsa durur.
- `optimize derin`: Daha ileri birlestirme onerir; gerekirse `uygun optimize yok` sonucuyla cikar.
- Resmi sinirlar: `OPTIMIZE_POLITIKASI.md`

## Tek Komut Kurulum
```powershell
python Besmele/tools/bootstrap_besmele.py <hedef_repo_yolu>
```

## Diger Kaynaktan Alma
```powershell
git clone https://github.com/mskaymaz/Besmele.git
cd Besmele
git checkout main
```

## Bundle Akisi
```powershell
for /f "delims=" %i in ('python Besmele\tools\r_etiketi_uret.py --kip bundle --proje Besmele') do set BUNDLE_ADI=%i
git bundle create "E:\\%BUNDLE_ADI%" --all
git clone "E:\\%BUNDLE_ADI%" Besmele
```

## Derle Akisi
```powershell
python Besmele/tools/derle.py --ad BenimUygulamam
```

- Varsayilan cikti klasoru repo disinda `../ciktilar/<repo_adi>/` altindadir.
- Python, .NET ve Go gibi destekleyen masaustu ekosistemlerinde tek dosya hedeflenir.
- Flutter masaustu/web/mobil ciktilari kendi dogal build bicimiyle uretilir; sonuc repo disina etiketli adla tasinir.
- Gerekirse hedef secimi `--hedef windows|web|android-apk|android-aab|ios|linux|macos` ile zorlanabilir.
- Python veya .NET gibi belirsiz girisli repolarda `--giris` ile ana dosya/proje dosyasi verilebilir.

## Kayit Araclari
- R etiketi: `python Besmele/tools/r_etiketi_uret.py --kip etiket`
- Commit metni: `python Besmele/tools/r_etiketi_uret.py --kip commit --ozet "Kisa ozet"`
- Release adi: `python Besmele/tools/r_etiketi_uret.py --kip release --proje Besmele --uzanti zip`
- HISTORY append: `python Besmele/tools/history_ekle.py --tip snapshot --ref TASK-xxx --ozet "Kisa ozet"`
- Aktif oturum arsivi: `python Besmele/tools/oturum_arsivle.py --ozet "Kisa ozet"`
- Yedek/mola teslim noktasi: `python Besmele/tools/teslim_noktasi.py --kip mola --ozet "Kisa ozet"`
- Derleme araci: `python Besmele/tools/derle.py --ad UygulamaAdi`

## Oturum Devri
- Yari kalan calisma varsa yeni oturumda once `STATE`, aktif `TASK`, son `HISTORY`, sonra `Besmele/oturumlar/AKTIF_OTURUM.md` okunur.
- Gerekirse `AKTIF_OTURUM.patch` ile teknik fark ayrintisi incelenir.
- `oturum_arsivle.py` aktif durumu kaydeder; `teslim_noktasi.py` basarisiz olursa bunu otomatik birakir.

Ne zaman acilir?
- Besmele yeni repoya kurulacaginda, mevcut repoya ekleneceginde, repo inceleme yapilacaginda veya teslim/bundle akisina gecileceginde.
