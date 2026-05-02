import json
import os
from typing import List, Optional
from gorev_modeli import GorevModeli, GorevOnceligi
from utils import APP_DATA_DIR, log_kaydet

class GorevServisi:
    """
    Görevlerin (TODO) disk üzerinde kalıcı olarak saklanmasını yöneten servis.
    Task 5.2 kapsamında oluşturulmuştur.
    """
    def __init__(self):
        self.dosya_yolu = os.path.join(APP_DATA_DIR, "gorevler.json")
        self._gorevler: List[GorevModeli] = []
        self.yukle()

    def yukle(self) -> List[GorevModeli]:
        """Görevleri JSON dosyasından yükler."""
        if not os.path.exists(self.dosya_yolu):
            self._gorevler = []
            return self._gorevler

        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                ham_veri = json.load(f)
                self._gorevler = []
                for item in ham_veri:
                    model = GorevModeli.from_dict(item)
                    if model: # Geçersiz verileri ayıkla (Task 5.2 validation)
                        self._gorevler.append(model)
            log_kaydet(f"{len(self._gorevler)} görev yüklendi.")
        except Exception as e:
            log_kaydet(f"Görevler yüklenirken hata: {e}", "error")
            self._gorevler = []
        
        return self._gorevler

    def kaydet(self):
        """Görevleri atomik bir şekilde diske kaydeder (Task 1.3 prensibi)."""
        try:
            os.makedirs(APP_DATA_DIR, exist_ok=True)
            gecici_dosya = self.dosya_yolu + ".tmp"
            
            veri = [g.to_dict() for g in self._gorevler]
            
            with open(gecici_dosya, "w", encoding="utf-8") as f:
                json.dump(veri, f, ensure_ascii=False, indent=2)
            
            os.replace(gecici_dosya, self.dosya_yolu)
        except Exception as e:
            log_kaydet(f"Görevler kaydedilirken hata: {e}", "error")

    def gorev_ekle(self, gorev: GorevModeli):
        """Listeye yeni bir görev ekler ve kaydeder."""
        self._gorevler.append(gorev)
        self.kaydet()

    def gorevleri_al(self) -> List[GorevModeli]:
        return self._gorevler

    def gorevleri_sirali_al(self) -> List[GorevModeli]:
        """
        Görevleri öncelik ve tamamlanma durumuna göre sıralar:
        1. Aktifler üstte, 2. Yüksek öncelikliler önde, 3. Tamamlananlar sonda.
        """
        oncelik_sirasi = {
            GorevOnceligi.YUKSEK: 0,
            GorevOnceligi.NORMAL: 1,
            GorevOnceligi.DUSUK: 2
        }
        
        return sorted(self._gorevler, key=lambda g: (
            g.tamamlandi, # False (0) < True (1) olduğu için aktifler başa gelir
            oncelik_sirasi.get(g.oncelik, 1) # Öncelik değerine göre (0, 1, 2)
        ))