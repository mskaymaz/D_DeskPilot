import json
import os
import shutil
from typing import List
from datetime import datetime, timedelta
from gorev_modeli import GorevModeli, GorevOnceligi
from utils import APP_DATA_DIR, log_kaydet
from oncelik_yonetimi import priority_key


class GorevServisi:
    def __init__(self):
        self.dosya_yolu = os.path.join(APP_DATA_DIR, "gorevler.json")
        self._gorevler: List[GorevModeli] = []
        self.yukle()

    def yukle(self) -> List[GorevModeli]:
        if not os.path.exists(self.dosya_yolu):
            self._gorevler = []
            return self._gorevler

        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                ham_veri = json.load(f)

            self._gorevler = []
            for item in ham_veri:
                model = GorevModeli.from_dict(item)
                if model:
                    self._gorevler.append(model)

            log_kaydet(f"{len(self._gorevler)} görev yüklendi.")
        except Exception as e:
            log_kaydet(f"Görevler yüklenirken hata: {e}", "error")
            self._gorevler = []

        return self._gorevler

    def kaydet(self):
        try:
            os.makedirs(APP_DATA_DIR, exist_ok=True)
            gecici_dosya = self.dosya_yolu + ".tmp"

            with open(gecici_dosya, "w", encoding="utf-8") as f:
                json.dump([g.to_dict() for g in self._gorevler], f, ensure_ascii=False, indent=2)

            if os.path.exists(self.dosya_yolu):
                shutil.copy2(self.dosya_yolu, self.dosya_yolu + ".bak")
            os.replace(gecici_dosya, self.dosya_yolu)
        except Exception as e:
            log_kaydet(f"Görevler kaydedilirken hata: {e}", "error")

    def gorev_ekle(self, gorev: GorevModeli):
        self._gorevler.append(gorev)
        self.kaydet()

    def gorevleri_al(self) -> List[GorevModeli]:
        return self._gorevler

    def cope_tasi(self, gorev: GorevModeli):
        gorev.cope_atildi = True
        gorev.cope_atilma_zamani = datetime.now()
        self.kaydet()

    def copten_geri_yukle(self, gorev: GorevModeli):
        gorev.cope_atildi = False
        gorev.cope_atilma_zamani = None
        self.kaydet()

    def kalici_sil(self, gorev: GorevModeli):
        self._gorevler = [g for g in self._gorevler if g is not gorev]
        self.kaydet()

    def cop_suresi_dolanlari_sil(self, gun_sayisi: int) -> int:
        try:
            gun_sayisi = max(0, int(gun_sayisi))
        except (TypeError, ValueError):
            gun_sayisi = 30
        sinir = datetime.now() - timedelta(days=gun_sayisi)
        onceki_sayi = len(self._gorevler)
        self._gorevler = [
            gorev for gorev in self._gorevler
            if not gorev.cope_atildi or not gorev.cope_atilma_zamani or gorev.cope_atilma_zamani > sinir
        ]
        silinen_sayi = onceki_sayi - len(self._gorevler)
        if silinen_sayi:
            self.kaydet()
        return silinen_sayi

    def gorevleri_sirali_al(self) -> List[GorevModeli]:
        oncelik_sirasi = {
            "high": 0,
            "normal": 1,
            "low": 2,
        }

        def siralama(g: GorevModeli):
            if g.cope_atildi:
                return (5, g.cope_atilma_zamani or g.olusturulma_zamani)
            if g.iptal_edildi:
                return (4, g.iptal_zamani or g.olusturulma_zamani)
            if g.tamamlandi:
                return (3, g.tamamlanma_zamani or g.olusturulma_zamani)

            return (
                oncelik_sirasi.get(priority_key(g.oncelik), 1),
                0 if g.bitis_tarihi else 1,
                g.bitis_tarihi or g.olusturulma_zamani,
                g.sira,
            )

        return sorted(self._gorevler, key=siralama)
