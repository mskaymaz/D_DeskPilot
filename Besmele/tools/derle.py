from argparse import ArgumentParser
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import tomllib

arac_dizini = Path(__file__).resolve().parent
if str(arac_dizini) not in sys.path:
    sys.path.insert(0, str(arac_dizini))
from r_etiketi_uret import r_etiketi_uret


class DerlemeHatasi(RuntimeError):
    """derleme_hatasi: kullaniciya net sebep vermek icin kontrollu hata sinifi."""


def komut_calistir(argumanlar, repo_kok):
    """komut_calistir: dis araci calistirir, ciktiyi yazdirir ve hata durumunda durdurur."""
    sonuc = subprocess.run(
        argumanlar,
        cwd=repo_kok,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if sonuc.stdout:
        print(sonuc.stdout, end="")
    if sonuc.stderr:
        print(sonuc.stderr, end="", file=sys.stderr)
    if sonuc.returncode != 0:
        komut_metni = " ".join(str(parca) for parca in argumanlar)
        raise DerlemeHatasi(f"Komut basarisiz: {komut_metni}")
    return sonuc


def varsayilan_cikti_koku(repo_kok):
    """cikti_koku: repo disinda ama repoya yakin dagitim klasoru secimi."""
    return repo_kok.parent / "ciktilar" / repo_kok.name


def etiketli_ad_uret(uygulama_adi, etiket):
    """etiketli_ad: kullanici adina tek bir R etiketini zorunlu olarak ekler."""
    return f"{uygulama_adi}_{etiket}"


def repo_teknolojisi_bul(repo_kok, ham_giris):
    """repo_teknolojisi: baskin build ekosistemini kok izlerinden cikarir."""
    giris_yolu = goreli_yol(repo_kok, ham_giris)
    if giris_yolu:
        uzanti = giris_yolu.suffix.lower()
        if uzanti == ".py":
            return "python"
        if uzanti in {".csproj", ".sln"}:
            return "dotnet"

    if (repo_kok / "pubspec.yaml").exists():
        return "flutter"
    if list(repo_kok.glob("*.sln")) or list(repo_kok.rglob("*.csproj")):
        return "dotnet"
    if (repo_kok / "package.json").exists():
        return "node"
    if (repo_kok / "go.mod").exists():
        return "go"
    if (repo_kok / "Cargo.toml").exists():
        return "rust"

    python_izleri = [
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "main.py",
        "app.py",
    ]
    if any((repo_kok / iz).exists() for iz in python_izleri):
        return "python"

    py_dosyalari = [
        aday
        for aday in repo_kok.rglob("*.py")
        if "Besmele" not in aday.parts and ".venv" not in aday.parts and "venv" not in aday.parts
    ]
    if py_dosyalari:
        return "python"

    raise DerlemeHatasi("Desteklenen build izi bulunamadi. `--giris` veya proje dosyasi gerekir.")


def hedef_bul(repo_kok, teknoloji, hedef):
    """hedef_tipi: kullanici secmediyse teknoloji ve klasor yapisina gore dogal hedefi bulur."""
    if hedef != "auto":
        return hedef

    isletim = platform.system()
    if teknoloji == "flutter":
        if isletim == "Windows" and (repo_kok / "windows").exists():
            return "windows"
        if isletim == "Linux" and (repo_kok / "linux").exists():
            return "linux"
        if isletim == "Darwin" and (repo_kok / "macos").exists():
            return "macos"
        if (repo_kok / "web").exists():
            return "web"
        if (repo_kok / "android").exists():
            return "android-apk"
        if (repo_kok / "ios").exists():
            return "ios"
        raise DerlemeHatasi("Flutter hedefi otomatik secilemedi. `--hedef` verin.")

    if teknoloji == "node":
        return "web"

    if isletim == "Windows":
        return "windows"
    if isletim == "Linux":
        return "linux"
    if isletim == "Darwin":
        return "macos"
    raise DerlemeHatasi("Isletim sistemi desteklenmiyor.")


def goreli_yol(repo_kok, ham_yol):
    """goreli_yol: kullanici girdisini repo kokune gore mutlak yola cevirir."""
    if not ham_yol:
        return None
    yol = Path(ham_yol)
    return yol if yol.is_absolute() else (repo_kok / yol).resolve()


def python_giris_bul(repo_kok, ham_giris):
    """python_giris: PyInstaller icin ana .py girisini secmeye yardim eder."""
    dogrudan = goreli_yol(repo_kok, ham_giris)
    if dogrudan:
        if not dogrudan.exists():
            raise DerlemeHatasi(f"Python giris dosyasi bulunamadi: {dogrudan}")
        return dogrudan

    adaylar = ["main.py", "app.py", "src/main.py", "src/app.py"]
    for aday in adaylar:
        yol = repo_kok / aday
        if yol.exists():
            return yol

    py_dosyalari = [
        aday
        for aday in repo_kok.rglob("*.py")
        if "Besmele" not in aday.parts and ".venv" not in aday.parts and "venv" not in aday.parts
    ]
    if len(py_dosyalari) == 1:
        return py_dosyalari[0]
    raise DerlemeHatasi("Python icin tekil giris dosyasi secilemedi. `--giris` verin.")


def dotnet_proje_bul(repo_kok, ham_giris):
    """dotnet_projesi: publish icin tekil .sln veya .csproj hedefini secmeye yardim eder."""
    dogrudan = goreli_yol(repo_kok, ham_giris)
    if dogrudan:
        if not dogrudan.exists():
            raise DerlemeHatasi(f"Dotnet proje dosyasi bulunamadi: {dogrudan}")
        return dogrudan

    cozumler = list(repo_kok.glob("*.sln"))
    if len(cozumler) == 1:
        return cozumler[0]
    projeler = list(repo_kok.rglob("*.csproj"))
    if len(projeler) == 1:
        return projeler[0]
    raise DerlemeHatasi("Dotnet icin tekil proje secilemedi. `--giris` ile .sln veya .csproj verin.")


def paket_yoneticisi_bul(repo_kok):
    """paket_yoneticisi: Node projesinde mevcut lock dosyasina gore build komutunu secer."""
    if (repo_kok / "pnpm-lock.yaml").exists():
        return ["pnpm", "build"]
    if (repo_kok / "yarn.lock").exists():
        return ["yarn", "build"]
    return ["npm", "run", "build"]


def web_cikti_klasoru_bul(repo_kok):
    """web_cikti_klasoru: yaygin web build ciktilari arasindan en uygun klasoru bulur."""
    adaylar = ["out", "dist", "build", ".next"]
    for aday in adaylar:
        yol = repo_kok / aday
        if yol.exists():
            return yol
    raise DerlemeHatasi("Web build ciktisi bulunamadi. Beklenen klasorler: out, dist, build, .next")


def flutter_cikti_yolu_bul(repo_kok, hedef):
    """flutter_ciktisi: secilen flutter hedefinin bilinen sonuc yolunu verir."""
    if hedef == "windows":
        return repo_kok / "build" / "windows" / "x64" / "runner" / "Release"
    if hedef == "linux":
        return repo_kok / "build" / "linux" / "x64" / "release" / "bundle"
    if hedef == "macos":
        return repo_kok / "build" / "macos" / "Build" / "Products" / "Release"
    if hedef == "web":
        return repo_kok / "build" / "web"
    if hedef == "android-apk":
        return repo_kok / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"
    if hedef == "android-aab":
        return repo_kok / "build" / "app" / "outputs" / "bundle" / "release" / "app-release.aab"
    if hedef == "ios":
        return repo_kok / "build" / "ios" / "iphoneos"
    raise DerlemeHatasi(f"Desteklenmeyen flutter hedefi: {hedef}")


def kopyala_ve_etiketle(kaynak, cikti_koku, etiketli_ad, hedef):
    """etiketli_cikti: dosya veya klasoru repo disi dagitim alanina tasir."""
    cikti_koku.mkdir(parents=True, exist_ok=True)

    if kaynak.is_file():
        uzanti = kaynak.suffix.lstrip(".")
        cikti_adi = f"{etiketli_ad}.{uzanti or 'paket'}"
        son_yol = cikti_koku / cikti_adi
        shutil.copy2(kaynak, son_yol)
        return son_yol

    son_yol = cikti_koku / etiketli_ad
    if son_yol.exists():
        shutil.rmtree(son_yol)
    shutil.copytree(kaynak, son_yol)

    if hedef in {"windows", "linux", "macos"}:
        exe_adaylari = []
        if hedef == "windows":
            exe_adaylari = list(son_yol.glob("*.exe"))
        else:
            exe_adaylari = [aday for aday in son_yol.iterdir() if aday.is_file() and os_calistirilabilir_mi(aday)]

        if len(exe_adaylari) == 1:
            eski = exe_adaylari[0]
            yeni = son_yol / f"{etiketli_ad}{eski.suffix}"
            eski.rename(yeni)

    return son_yol


def os_calistirilabilir_mi(yol):
    """calistirilabilirlik: klasor icindeki ana ikiliyi ayirt etmek icin izin bakisi."""
    return yol.stat().st_mode & 0o111 != 0


def python_derle(repo_kok, cikti_koku, etiketli_ad, giris):
    """python_derlemesi: PyInstaller ile tek dosya dagitimi uretir."""
    giris_yolu = python_giris_bul(repo_kok, giris)
    with tempfile.TemporaryDirectory(prefix="besmele_py_", dir=cikti_koku) as gecici:
        gecici_yol = Path(gecici)
        komut = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconfirm",
            "--clean",
            "--name",
            etiketli_ad,
            "--distpath",
            str(cikti_koku),
            "--workpath",
            str(gecici_yol / "build"),
            "--specpath",
            str(gecici_yol / "spec"),
            str(giris_yolu),
        ]
        komut_calistir(komut, repo_kok)
    return cikti_koku / f"{etiketli_ad}.exe"


def dotnet_runtime_bul(hedef):
    """runtime_tipi: dotnet publish icin hedef runtime kimligini secmeye yardim eder."""
    mimari = "arm64" if platform.machine().lower() in {"arm64", "aarch64"} else "x64"
    esleme = {
        "windows": f"win-{mimari}",
        "linux": f"linux-{mimari}",
        "macos": f"osx-{mimari}",
    }
    if hedef not in esleme:
        raise DerlemeHatasi(f"Dotnet icin hedef desteklenmiyor: {hedef}")
    return esleme[hedef]


def dotnet_derle(repo_kok, cikti_koku, etiketli_ad, hedef, giris):
    """dotnet_derlemesi: self-contained ve tek dosya publish deneyimi uretir."""
    proje_yolu = dotnet_proje_bul(repo_kok, giris)
    with tempfile.TemporaryDirectory(prefix="besmele_dotnet_", dir=cikti_koku) as gecici:
        gecici_yol = Path(gecici)
        komut = [
            "dotnet",
            "publish",
            str(proje_yolu),
            "-c",
            "Release",
            "-r",
            dotnet_runtime_bul(hedef),
            "--self-contained",
            "true",
            "-p:PublishSingleFile=true",
            "-p:IncludeNativeLibrariesForSelfExtract=true",
            "-o",
            str(gecici_yol),
        ]
        komut_calistir(komut, repo_kok)

        adaylar = list(gecici_yol.glob("*.exe")) if hedef == "windows" else [aday for aday in gecici_yol.iterdir() if aday.is_file()]
        ana_dosyalar = [
            aday
            for aday in adaylar
            if aday.suffix not in {".pdb", ".json", ".dll", ".deps.json", ".runtimeconfig.json"}
        ]
        if not ana_dosyalar:
            raise DerlemeHatasi("Dotnet publish sonrasi ana cikti bulunamadi.")
        kaynak = ana_dosyalar[0]
        hedef_uzanti = kaynak.suffix.lstrip(".") or "bin"
        son_yol = cikti_koku / f"{etiketli_ad}.{hedef_uzanti}"
        shutil.copy2(kaynak, son_yol)
        return son_yol


def flutter_derle(repo_kok, cikti_koku, etiketli_ad, hedef):
    """flutter_derlemesi: ekosistemin dogal hedefini derler ve ciktiyi repo disina alir."""
    komut_esleme = {
        "windows": ["flutter", "build", "windows", "--release"],
        "linux": ["flutter", "build", "linux", "--release"],
        "macos": ["flutter", "build", "macos", "--release"],
        "web": ["flutter", "build", "web", "--release"],
        "android-apk": ["flutter", "build", "apk", "--release"],
        "android-aab": ["flutter", "build", "appbundle", "--release"],
        "ios": ["flutter", "build", "ios", "--release", "--no-codesign"],
    }
    if hedef not in komut_esleme:
        raise DerlemeHatasi(f"Flutter hedefi desteklenmiyor: {hedef}")
    komut_calistir(komut_esleme[hedef], repo_kok)

    kaynak = flutter_cikti_yolu_bul(repo_kok, hedef)
    if not kaynak.exists():
        raise DerlemeHatasi(f"Flutter cikti yolu bulunamadi: {kaynak}")
    return kopyala_ve_etiketle(kaynak, cikti_koku, etiketli_ad, hedef)


def node_derle(repo_kok, cikti_koku, etiketli_ad):
    """node_derlemesi: package manager build scriptini calistirir ve web ciktisini tasir."""
    komut_calistir(paket_yoneticisi_bul(repo_kok), repo_kok)
    kaynak = web_cikti_klasoru_bul(repo_kok)
    return kopyala_ve_etiketle(kaynak, cikti_koku, etiketli_ad, "web")


def go_derle(repo_kok, cikti_koku, etiketli_ad, hedef, giris):
    """go_derlemesi: tek dosya ikiliyi dogrudan hedef klasore yazar."""
    uzanti = ".exe" if hedef == "windows" else ""
    son_yol = cikti_koku / f"{etiketli_ad}{uzanti}"
    komut = ["go", "build", "-o", str(son_yol)]
    if giris:
        komut.append(giris)
    komut_calistir(komut, repo_kok)
    return son_yol


def rust_paket_adi_bul(repo_kok):
    """rust_paket_adi: Cargo.toml icinden varsayilan ikili adini okumaya calisir."""
    kargo_yolu = repo_kok / "Cargo.toml"
    veri = tomllib.loads(kargo_yolu.read_text(encoding="utf-8"))
    ikililer = veri.get("bin")
    if isinstance(ikililer, list) and len(ikililer) == 1 and "name" in ikililer[0]:
        return str(ikililer[0]["name"])
    paket = veri.get("package", {})
    ad = str(paket.get("name", "")).strip()
    if not ad:
        raise DerlemeHatasi("Cargo.toml icinde paket adi bulunamadi.")
    return ad


def rust_derle(repo_kok, cikti_koku, etiketli_ad, hedef):
    """rust_derlemesi: cargo release ikilisini alir ve etiketli ciktiya kopyalar."""
    komut_calistir(["cargo", "build", "--release"], repo_kok)
    paket_adi = rust_paket_adi_bul(repo_kok)
    uzanti = ".exe" if hedef == "windows" else ""
    kaynak = repo_kok / "target" / "release" / f"{paket_adi}{uzanti}"
    if not kaynak.exists():
        raise DerlemeHatasi(f"Rust ikilisi bulunamadi: {kaynak}")
    son_yol = cikti_koku / f"{etiketli_ad}{uzanti}"
    shutil.copy2(kaynak, son_yol)
    return son_yol


def kuru_kosum_yaz(teknoloji, hedef, repo_kok, cikti_koku, etiketli_ad):
    """kuru_kosum: gercek derleme yapmadan secilen stratejiyi kullaniciya yazar."""
    print(f"TEKNOLOJI: {teknoloji}")
    print(f"HEDEF: {hedef}")
    print(f"REPO: {repo_kok}")
    print(f"CIKTI_KOKU: {cikti_koku}")
    print(f"CIKTI_ADI: {etiketli_ad}")


def ana():
    arguman = ArgumentParser(description="Platforma uygun derleme yapar ve ciktiya R etiketli ad verir.")
    arguman.add_argument("--ad", required=True, help="Ciktiya yazilacak uygulama adi.")
    arguman.add_argument("--repo", default=".", help="Derlenecek repo kok yolu.")
    arguman.add_argument(
        "--hedef",
        default="auto",
        choices=["auto", "windows", "linux", "macos", "web", "android-apk", "android-aab", "ios"],
        help="Otomatik secim yerine dogrudan hedef ver.",
    )
    arguman.add_argument(
        "--giris",
        default="",
        help="Gerekirse Python ana dosyasi, dotnet proje dosyasi veya build girisi.",
    )
    arguman.add_argument(
        "--cikti-koku",
        default="",
        help="Repo disi dagitim kok dizini. Varsayilan: ../ciktilar/<repo>",
    )
    arguman.add_argument(
        "--kuru-kosum",
        action="store_true",
        help="Derleme yapmadan secilen teknoloji/hedef/cikti bilgisini yaz.",
    )
    secim = arguman.parse_args()

    repo_kok = Path(secim.repo).resolve()
    teknoloji = repo_teknolojisi_bul(repo_kok, secim.giris)
    hedef = hedef_bul(repo_kok, teknoloji, secim.hedef)
    etiket = r_etiketi_uret()
    etiketli_ad = etiketli_ad_uret(secim.ad.strip(), etiket)
    cikti_koku = goreli_yol(repo_kok, secim.cikti_koku) if secim.cikti_koku else varsayilan_cikti_koku(repo_kok)
    cikti_koku.mkdir(parents=True, exist_ok=True)

    if secim.kuru_kosum:
        kuru_kosum_yaz(teknoloji, hedef, repo_kok, cikti_koku, etiketli_ad)
        return

    if teknoloji == "python":
        son_yol = python_derle(repo_kok, cikti_koku, etiketli_ad, secim.giris)
    elif teknoloji == "dotnet":
        son_yol = dotnet_derle(repo_kok, cikti_koku, etiketli_ad, hedef, secim.giris)
    elif teknoloji == "flutter":
        son_yol = flutter_derle(repo_kok, cikti_koku, etiketli_ad, hedef)
    elif teknoloji == "node":
        son_yol = node_derle(repo_kok, cikti_koku, etiketli_ad)
    elif teknoloji == "go":
        son_yol = go_derle(repo_kok, cikti_koku, etiketli_ad, hedef, secim.giris)
    elif teknoloji == "rust":
        son_yol = rust_derle(repo_kok, cikti_koku, etiketli_ad, hedef)
    else:
        raise DerlemeHatasi(f"Desteklenmeyen teknoloji: {teknoloji}")

    print(f"TEKNOLOJI: {teknoloji}")
    print(f"HEDEF: {hedef}")
    print(f"R: {etiket}")
    print(f"CIKTI: {son_yol}")


if __name__ == "__main__":
    try:
        ana()
    except DerlemeHatasi as hata:
        print(f"HATA: {hata}", file=sys.stderr)
        raise SystemExit(1)
