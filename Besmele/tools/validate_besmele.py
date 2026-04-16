from pathlib import Path
import sys

kok = Path(__file__).resolve().parents[2]
operasyon = Path(__file__).resolve().parents[1]

kok_zorunlu = ["AGENTS.md", "CORE.md", "STATE.md"]
operasyon_zorunlu = [
    "README.md",
    "KURAL_KAYNAGI.md",
    "HEDEF_MIMARI.md",
    "KOMUT_SOZLUGU.md",
    "TEMIZLIK_POLITIKASI.md",
    "OPTIMIZE_POLITIKASI.md",
    "PROFIL_REHBERI.md",
    "ENTEGRASYON_REHBERI.md",
    "WORKBOARD.md",
    "HISTORY.md",
    "FAZ_YOL_HARITASI.md",
]
opsiyonel_zorunlu = ["CIHAZ_TESTI.md"]
oturum_zorunlu = ["AKTIF_OTURUM.md", "README.md"]
hook_zorunlu = ["pre-commit", "pre-commit.cmd"]
arac_zorunlu = [
    "validate_besmele.py",
    "ci_dogrula.sh",
    "ci_dogrula.cmd",
    "ci_github_actions_ornek.yml",
    "r_etiketi_uret.py",
    "history_ekle.py",
    "oturum_arsivle.py",
    "teslim_noktasi.py",
    "derle.py",
    "bootstrap_besmele.py",
]
state_zorunlu = ["last_update:", "active_task:", "phase:", "next_step:", "blockers:", "active_owner:", "last_delivery:", "handover:"]

hata = []

for ad in kok_zorunlu:
    if not (kok / ad).exists():
        hata.append(f"Eksik kok dosyasi: {ad}")

for ad in operasyon_zorunlu:
    if not (operasyon / ad).exists():
        hata.append(f"Eksik operasyon dosyasi: Besmele/{ad}")

if not (operasyon / "plans").exists():
    hata.append("Eksik klasor: Besmele/plans")
if not (operasyon / "tools").exists():
    hata.append("Eksik klasor: Besmele/tools")
if not (operasyon / "hooks").exists():
    hata.append("Eksik klasor: Besmele/hooks")
if not (operasyon / "optional").exists():
    hata.append("Eksik klasor: Besmele/optional")
if not (operasyon / "oturumlar").exists():
    hata.append("Eksik klasor: Besmele/oturumlar")
if not (operasyon / "plans" / "TASK-SABLON.md").exists():
    hata.append("Eksik dosya: Besmele/plans/TASK-SABLON.md")
for ad in opsiyonel_zorunlu:
    if not (operasyon / "optional" / ad).exists():
        hata.append(f"Eksik dosya: Besmele/optional/{ad}")
for ad in oturum_zorunlu:
    if not (operasyon / "oturumlar" / ad).exists():
        hata.append(f"Eksik dosya: Besmele/oturumlar/{ad}")

for ad in hook_zorunlu:
    if not (operasyon / "hooks" / ad).exists():
        hata.append(f"Eksik dosya: Besmele/hooks/{ad}")

for ad in arac_zorunlu:
    if not (operasyon / "tools" / ad).exists():
        hata.append(f"Eksik dosya: Besmele/tools/{ad}")

if not hata:
    agents = (kok / "AGENTS.md").read_text(encoding="utf-8")
    core = (kok / "CORE.md").read_text(encoding="utf-8")
    readme = (operasyon / "README.md").read_text(encoding="utf-8")
    kural = (operasyon / "KURAL_KAYNAGI.md").read_text(encoding="utf-8")
    komut_sozlugu = (operasyon / "KOMUT_SOZLUGU.md").read_text(encoding="utf-8")
    entegrasyon = (operasyon / "ENTEGRASYON_REHBERI.md").read_text(encoding="utf-8")

    if "R.yymmdd_hhmm" not in agents or "R.yymmdd_hhmm" not in core or "R.yymmdd_hhmm" not in readme:
        hata.append("R format notu kok/operasyon dosyalarinda eksik")
    tam_okuma_ifadeleri = [
        "tum dosyayi okumaya baslamaz",
        "tum dosyayi okumaz",
    ]
    for ifade in tam_okuma_ifadeleri:
        if ifade not in agents:
            hata.append(f"AGENTS icinde tam dosya okuma yasagi eksik: {ifade}")
        if ifade not in core:
            hata.append(f"CORE icinde tam dosya okuma yasagi eksik: {ifade}")
        if ifade not in kural:
            hata.append(f"KURAL_KAYNAGI icinde tam dosya okuma yasagi eksik: {ifade}")

    al = agents.lower()
    if "exe" not in al or "bundle" not in al or "push" not in al:
        hata.append("AGENTS icinde exe/push/bundle zorunlulugu eksik")

    if "Turkce Adlandirma" not in kural and "Turkce adlandirma" not in kural:
        hata.append("KURAL_KAYNAGI icinde Turkce adlandirma bolumu eksik")
    if "TEMIZLIK_GUVENCESI" not in kural:
        hata.append("KURAL_KAYNAGI icinde temizlik guvencesi bolumu eksik")
    if "OPTIMIZE_GUVENCESI" not in kural:
        hata.append("KURAL_KAYNAGI icinde optimize guvencesi bolumu eksik")
    if "OTURUM_DEVIR_GUVENCESI" not in kural:
        hata.append("KURAL_KAYNAGI icinde oturum devir guvencesi bolumu eksik")
    if "`derle`" not in komut_sozlugu:
        hata.append("KOMUT_SOZLUGU icinde `derle` komutu eksik")
    if "`ozet`" not in komut_sozlugu:
        hata.append("KOMUT_SOZLUGU icinde `ozet` komutu eksik")
    if "2-3 satir" not in komut_sozlugu:
        hata.append("KOMUT_SOZLUGU icinde 2-3 satir cevap siniri eksik")
    if "derle.py" not in readme:
        hata.append("README icinde derle araci kaydi eksik")
    if "Derle Akisi" not in entegrasyon:
        hata.append("ENTEGRASYON_REHBERI icinde Derle Akisi bolumu eksik")
    if "2-3 satir" not in kural:
        hata.append("KURAL_KAYNAGI icinde eko/ozet cevap siniri eksik")

    danismanlik_ifadeleri = [
        "DERINLIKLI_DURUST_TAVSIYE",
        "AI yalniz komut uygulamaz",
    ]
    for ifade in danismanlik_ifadeleri:
        if ifade not in agents:
            hata.append(f"AGENTS icinde profesyonel danismanlik kural eksik: {ifade}")
        if ifade not in kural:
            hata.append(f"KURAL_KAYNAGI icinde profesyonel danismanlik kural eksik: {ifade}")

    disiplin_ifadeleri = [
        "CALISMA_DISIPLINI",
        "Tek sinir Ekonomik Token ilkesidir",
        "fren",
    ]
    for ifade in disiplin_ifadeleri:
        if ifade not in agents:
            hata.append(f"AGENTS icinde calisma disiplini eksik: {ifade}")
        if ifade not in kural:
            hata.append(f"KURAL_KAYNAGI icinde calisma disiplini eksik: {ifade}")

    state = (kok / "STATE.md").read_text(encoding="utf-8")
    for alan in state_zorunlu:
        if alan not in state:
            hata.append(f"STATE zorunlu alani eksik: {alan}")

    aktif = None
    for satir in state.splitlines():
        if satir.startswith("active_task:"):
            aktif = satir.split(":", 1)[1].strip()
            break

    if aktif is None:
        hata.append("STATE active_task alani eksik")
    elif aktif != "NONE" and not (operasyon / "plans" / f"{aktif}.md").exists():
        hata.append(f"STATE aktif gorev plani yok: Besmele/plans/{aktif}.md")

if hata:
    for h in hata:
        print("ERROR:", h)
    sys.exit(1)

print("PASS: Kok tetikleyiciler ve Besmele operasyon yapisi dogrulandi")
