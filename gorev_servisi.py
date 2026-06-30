import json
import os
from typing import List
from gorev_modeli import GorevModeli, GorevOnceligi
from utils import APP_DATA_DIR, log_kaydet


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

            os.replace(gecici_dosya, self.dosya_yolu)
        except Exception as e:
            log_kaydet(f"Görevler kaydedilirken hata: {e}", "error")

    def gorev_ekle(self, gorev: GorevModeli):
        self._gorevler.append(gorev)
        self.kaydet()

    def gorevleri_al(self) -> List[GorevModeli]:
        return self._gorevler

    def gorevleri_sirali_al(self) -> List[GorevModeli]:
        oncelik_sirasi = {
            GorevOnceligi.YUKSEK: 0,
            GorevOnceligi.NORMAL: 1,
            GorevOnceligi.DUSUK: 2,
        }

        def siralama(g: GorevModeli):
            if g.iptal_edildi:
                return (4, g.iptal_zamani or g.olusturulma_zamani)
            if g.tamamlandi:
                return (3, g.tamamlanma_zamani or g.olusturulma_zamani)

            return (
                oncelik_sirasi.get(g.oncelik, 1),
                0 if g.suresi_gecti_mi() else 1,
                g.bitis_tarihi or g.olusturulma_zamani,
            )

        return sorted(self._gorevler, key=siralama)
