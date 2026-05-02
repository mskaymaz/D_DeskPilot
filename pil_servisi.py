import psutil
import logging
from datetime import datetime
from typing import Optional
from pil_modeli import PilDurumu

class PilServisi:
    """Pil bilgilerini okuyan ve esik degerlerini kontrol eden servis."""
    
    def __init__(self, dusuk_esik: int = 15, kritik_esik: int = 10):
        self.dusuk_esik = dusuk_esik
        self.kritik_esik = kritik_esik
        self._onceki_sarj_durumu: Optional[bool] = None

    def mevcut_durumu_al(self) -> Optional[PilDurumu]:
        """Sistemden guncel pil verilerini okur."""
        try:
            pil = psutil.sensors_battery()
            if not pil:
                return None

            yuzde = int(pil.percent)
            sarjda = pil.power_plugged
            
            # Esik degerlerine gore durum tespiti (Task 2.2)
            durum = "Normal"
            if yuzde <= self.kritik_esik:
                durum = "Kritik"
            elif yuzde <= self.dusuk_esik:
                durum = "Dusuk"

            return PilDurumu(
                yuzde=yuzde,
                sarjda=sarjda,
                durum_metni=durum,
                zaman_damgasi=datetime.now(),
                kalan_sure=pil.secsleft if pil.secsleft != psutil.POWER_TIME_UNLIMITED else None
            )
        except Exception as e:
            logging.error(f"Pil verisi okunurken hata: {e}")
            return None

    def sarj_durumu_degisti_mi(self, yeni_sarj_durumu: bool) -> bool:
        """Sarj cihazinin takilma/cikarilma durumunu saptar (Task 2.3)."""
        if self._onceki_sarj_durumu is None:
            self._onceki_sarj_durumu = yeni_sarj_durumu
            return False

        if self._onceki_sarj_durumu != yeni_sarj_durumu:
            self._onceki_sarj_durumu = yeni_sarj_durumu
            return True
        
        return False

    def saglik_bilgisi_al(self) -> Optional[str]:
        """
        Pil saglik bilgisini dondurur (Task 2.4).
        Windows uzerinde standart psutil saglik bilgisini dogrudan vermez.
        Gelecekte WMI veya powercfg entegrasyonu buraya eklenebilir.
        Simdilik sessizce None dondurur.
        """
        return None