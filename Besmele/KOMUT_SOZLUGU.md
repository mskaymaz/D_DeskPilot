# KOMUT SOZLUGU

Amac: Sohbet tetiklerini tek sayfada toplamak; `list?` istendiginde hizli ve vitrin gibi ozet vermek.

## list? Ciktisi
- `bismillah`: giris ve baglam alma
- `eko`: ekonomik ve asiri kisa cevap modu
- `ozet`: en fazla 2-3 satirlik aciklamasiz cevap modu
- `banaver`: komutu bana ver, ben calistirayim
- `derle`: platforma uygun derleme ve paket ciktisi
- `mola` / `yedek`: guvenli teslim noktasi
- `temizle`: artefakt temizligi
- `optimize`: talimat ve `md` konsolidasyonu

## Giris Komutlari
- `bismillah`: Yalniz `CORE.md`, `STATE.md` ve bu dosya okunur; baglam alinip hedef sorulur.
- `eko`: Yalniz istenen kapsama inilir; kullanici acikca istemedikce cevap asamasinda aciklama yapilmaz ve sonuc en fazla 2-3 satir tutulur.
- `ozet`: Ozellikle cevap yuzeyini sikistiran moddur; sonuc aciklamasiz veya minimum aciklamali bicimde en fazla 2-3 satir verilir.
- `banaver`: Asistan ilgili dogrulama veya gelistirme komutlarini kendi calistirmak yerine kopyala-yapistir olarak verir ve cikti bekler.
- `list?`: Bu dosyadaki aktif tetikleri kategorik ve kisa ozetle listeler.

## Derleme Komutlari
- `derle`: Platforma uygun gercek build akisina gecer; kullanici adini zorunlu alir ve cikti adina `R.yymmdd_hhmm` etiketi ekler.
- `derle <uygulama_adi>`: Varsayilan kullanimdir; repo disi varsayilan dagitim yeri `../ciktilar/<repo_adi>/` altina yazilir.
- Windows/masaustu tarafinda destekleyen ekosistemlerde tek dosya `.exe` uretmeye calisir; ekosistem klasor tabanliysa dogal klasor ciktisini etiketli adla tasir.
- Mobil ve web tarafinda tek dosya dayatmaz; o platformun gercek build cikti tipini (ornegin `apk`, `aab`, web klasoru, masaustu bundle) uretir.
- Asistan tarafinda sohbet kisayolu `derle UygulamaAdi`; arac karsiligi `python Besmele/tools/derle.py --ad UygulamaAdi` seklindedir.

## Teslim Komutlari
- `mola`: Hizli guvenli teslim komutudur; basariliysa ara vermeye uygun nokta olusturur, basarisizsa aktif oturum diff kaydi birakir.
- `yedek`: `mola` ile ayni teslim noktasi akisina baglidir; ozet not, `STATE/HISTORY/TASK` kaydi, commit, push, bundle ve esitlik kontrolu uretir.
- `molaya gecelim`: `mola` ile ayni anlamdadir.
- `simdi mola zamani`: `mola` ile ayni anlamdadir.

## Bakim Komutlari
- `temizle`: Temizlik adaylarini listeler; gecmise, task hafizasina ve izlenen kaynak dosyalara dokunmadan guvenli artefakt temizligi icin ozet verir.
- `temizle liste`: Yalniz adaylari ve tahmini alan kazancini gosterir.
- `temizle uygula`: Guvenli artefakt adaylarini siler; tracked kaynak dosyalara ve hafiza dosyalarina dokunmaz.
- `temizle derin`: Daha genis cache/build/paket temizligi onerir veya uygular; yine kullanici onayi olmadan supheli dosya silmez.

## Konsolidasyon Komutlari
- `optimize`: Sislik yapan talimat ve `md` yapilarini analiz eder; mimari seviyeyi, kapsam gucunu veya etki alanini dusurmeden guvenli konsolidasyon adaylari uretir.
- `optimize uygula`: Onaylanan guvenli konsolidasyonu uygular; kaliteyi dusurecekse hicbir sey yapmaz.
- `optimize derin`: Daha ileri mimari konsolidasyon onerir; ama guc kaybi riski varsa yalniz raporla durur.

## Kisa Kullanim
- Varsayilan olarak komutlar tek kelime yazilarak tetiklenir.
- Mod kapatma gerekiyorsa ilgili komutun yanina `off` eklenir.
- Repo-ozel davranis gerekiyorsa bu dosya degil, ilgili repo profili veya entegrasyon notu genisletilir.
- Temizlik davranisi icin resmi referans: `Besmele/TEMIZLIK_POLITIKASI.md`
- Optimize davranisi icin resmi referans: `Besmele/OPTIMIZE_POLITIKASI.md`
- Derleme davranisi icin resmi arac: `Besmele/tools/derle.py`
- Oturum devri ve yari kalan is kaydi icin resmi referans: `Besmele/oturumlar/`

Ne zaman acilir?
- Kisa komutlarin ne yaptigi unutuldugunda veya `list?` davranisi gerektiginde.
