import json
import os
from datetime import datetime
from typing import List, Optional
from hatirlatici_modeli import HatirlaticiModeli, HatirlaticiDurumu
from utils import APP_DATA_DIR, log_kaydet

class HatirlaticiServisi:
    """
    Hatırlatıcıların disk üzerinde kalıcı olarak saklanmasını yöneten servis.
    Task 4.2 kapsamında oluşturulmuştur.
    """
    def __init__(self):
        self.dosya_yolu = os.path.join(APP_DATA_DIR, "hatirlaticilar.json")
        self._hatirlaticilar: List[HatirlaticiModeli] = []
        self.yukle()

    def yukle(self) -> List[HatirlaticiModeli]:
        """Hatırlatıcıları JSON dosyasından yükler."""
        if not os.path.exists(self.dosya_yolu):
            self._hatirlaticilar = []
            return self._hatirlaticilar

        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                ham_veri = json.load(f)
                self._hatirlaticilar = []
                for item in ham_veri:
                    model = HatirlaticiModeli.from_dict(item)
                    if model: # Sadece geçerli olanları ekle (Task 4.2 doğrulaması)
                        self._hatirlaticilar.append(model)
            log_kaydet(f"{len(self._hatirlaticilar)} hatırlatıcı yüklendi.")
        except Exception as e:
            log_kaydet(f"Hatırlatıcılar yüklenirken hata: {e}", "error")
            self._hatirlaticilar = []
        
        return self._hatirlaticilar

    def kaydet(self):
        """Hatırlatıcıları atomik bir şekilde disket kaydeder."""
        try:
            os.makedirs(APP_DATA_DIR, exist_ok=True)
            gecici_dosya = self.dosya_yolu + ".tmp"
            
            veri = [h.to_dict() for h in self._hatirlaticilar]
            
            with open(gecici_dosya, "w", encoding="utf-8") as f:
                json.dump(veri, f, ensure_ascii=False, indent=2)
            
            os.replace(gecici_dosya, self.dosya_yolu)
        except Exception as e:
            log_kaydet(f"Hatırlatıcılar kaydedilirken hata: {e}", "error")

    def hatirlatici_ekle(self, hatirlatici: HatirlaticiModeli):
        """Listeye yeni bir hatırlatıcı ekler ve kaydeder."""
        self._hatirlaticilar.append(hatirlatici)
        self.kaydet()

    def hatirlaticilari_al(self) -> List[HatirlaticiModeli]:
        return self._hatirlaticilar

    def en_yakin_hatirlaticiyi_bul(self) -> Optional[HatirlaticiModeli]:
        """Gelecekteki en yakın aktif hatırlatıcıyı bulur. Task 8.2 için eklenmiştir."""
        simdi = datetime.now()
        gelecektekiler = []
        for h in self._hatirlaticilar:
            if h.durum == HatirlaticiDurumu.AKTIF:
                zaman = h.erteleme_zamani if h.erteleme_zamani else h.hatirlatma_zamani
                if zaman > simdi:
                    gelecektekiler.append((zaman, h))
        
        if not gelecektekiler:
            return None
            
        return min(gelecektekiler, key=lambda x: x[0])[1]

    def zamani_gelenleri_tara(self) -> List[HatirlaticiModeli]:
        """Zamanı gelmiş veya geçmiş aktif hatırlatıcıları bulur."""
        simdi = datetime.now()
        gelenler = []
        
        for h in self._hatirlaticilar:
            if h.durum == HatirlaticiDurumu.AKTIF:
                # Erteleme varsa erteleme zamanına, yoksa normal zamana bak
                hedef_zaman = h.erteleme_zamani if h.erteleme_zamani else h.hatirlatma_zamani
                if hedef_zaman <= simdi:
                    gelenler.append(h)
        
        return gelenler