# BESMELE

Amac: Buyuk-kucuk tum projelerde ekonomik token odakli, kisa ve profesyonel calisma omurgasi saglamak.

Ortak kurallar: `Besmele/KURAL_KAYNAGI.md`
Hedef mimari: `Besmele/HEDEF_MIMARI.md`

Yapi ayrimi:
- KOK tetikleyiciler: AGENTS.md, CORE.md, STATE.md
- Operasyon dosyalari: Besmele/ klasoru

Hizli kullanim:
1. Yeni projeye kopyala: koke AGENTS/CORE/STATE, kokte Besmele/ klasoru.
2. bismillah de; yalniz kokteki CORE ve STATE okunur.
3. Ardindan `Besmele/KOMUT_SOZLUGU.md` ile aktif tetikler baglama alinir.
4. Operasyon gerektiginde Besmele/ altindaki ilgili dosyaya inilir.
5. `eko` ve `ozet`, cevap asamasinda yuzeyi en fazla 2-3 satira indirir; kullanici istemedikce aciklama yazilmaz.

Besmele/ icerigi:
- README.md
- BASLANGIC_OZETI.md
- EKIP_EL_KITABI.md
- KURAL_KAYNAGI.md
- HEDEF_MIMARI.md
- KOMUT_SOZLUGU.md
- TEMIZLIK_POLITIKASI.md
- OPTIMIZE_POLITIKASI.md
- PROFIL_REHBERI.md
- ENTEGRASYON_REHBERI.md
- WORKBOARD.md
- HISTORY.md
- FAZ_YOL_HARITASI.md
- oturumlar/AKTIF_OTURUM.md
- optional/CIHAZ_TESTI.md
- hooks/pre-commit
- hooks/pre-commit.cmd
- plans/TASK-xxx.md
- plans/TASK-SABLON.md
- tools/validate_besmele.py
- tools/ci_dogrula.sh
- tools/ci_dogrula.cmd
- tools/ci_github_actions_ornek.yml
- tools/r_etiketi_uret.py
- tools/history_ekle.py
- tools/oturum_arsivle.py
- tools/teslim_noktasi.py
- tools/derle.py
- tools/bootstrap_besmele.py

Operasyon akisi:
1. `KURAL_KAYNAGI`: ust ilkeleri belirler.
2. `KOMUT_SOZLUGU`: sohbet tetiklerini listeler.
3. `BASLANGIC_OZETI`: 1 sayfalik hizli giris ozetidir.
4. `EKIP_EL_KITABI`: ekip ici hizli kullanim ve devralma rehberidir.
5. `TEMIZLIK_POLITIKASI`: guvenli artefakt temizliginin sinirlarini belirler.
6. `OPTIMIZE_POLITIKASI`: kaliteyi dusurmeyen guvenli konsolidasyon sinirlarini belirler.
7. `PROFIL_REHBERI`: repo seviyesi ve teknoloji yonunu daraltir.
8. `ENTEGRASYON_REHBERI`: yeni veya mevcut repoya kurulum yolunu verir.
9. `WORKBOARD` + `HISTORY` + `FAZ_YOL_HARITASI`: canli hafizayi tutar.
10. `oturumlar/`: yari kalan islerde devri hassaslastiran aktif oturum kaydini tutar.

R etiketi:
- Format: R.yymmdd_hhmm
- Kullanim: commit/push notu, HISTORY tag, bundle ve exe/paket adlari

Temel araclar:
- Hook etkinlestirme: `git config core.hooksPath Besmele/hooks`
- Yerel/CI dogrulama (Windows): `Besmele\\tools\\ci_dogrula.cmd`
- Yerel/CI dogrulama (Linux/macOS): `sh Besmele/tools/ci_dogrula.sh`
- GitHub Actions ornek akis: `Besmele/tools/ci_github_actions_ornek.yml`
- R etiketi uretimi: `python Besmele/tools/r_etiketi_uret.py --kip etiket`
- Commit notu kalibi: `python Besmele/tools/r_etiketi_uret.py --kip commit --ozet "Kisa ozet"`
- Bundle adi kalibi: `python Besmele/tools/r_etiketi_uret.py --kip bundle --proje Besmele`
- Release adi kalibi: `python Besmele/tools/r_etiketi_uret.py --kip release --proje Besmele --uzanti zip`
- HISTORY append (tek komut): `python Besmele/tools/history_ekle.py --tip snapshot --ref TASK-003 --ozet "Kisa ozet"`
- Aktif oturum kaydi: `python Besmele/tools/oturum_arsivle.py --ozet "Kisa ozet"`
- Mola/yedek teslim noktasi: `python Besmele/tools/teslim_noktasi.py --kip yedek --ozet "Kisa ozet"`
- Derle araci: `python Besmele/tools/derle.py --ad UygulamaAdi`
- Yeni repo bootstrap (tek komut): `python Besmele/tools/bootstrap_besmele.py <hedef_repo_yolu>`

Derle davranisi:
- Varsayilan cikti konumu repo disinda `../ciktilar/<repo_adi>/` klasorudur.
- Windows/masaustu tarafinda destekleyen ekosistemlerde tek dosya `.exe` hedeflenir.
- Flutter/web gibi klasor tabanli ekosistemlerde dogal build ciktisi etiketli adla repo disina kopyalanir.
- Her cikti adinda zorunlu `R.yymmdd_hhmm` etiketi vardir.

Not: Varsayilan teknoloji listesi sinirlayici degildir; asistan gerekceyle farkli dil/cati onerebilir. Son karar her zaman kullanicidadir.
