import time
from typing import Dict

class BildirimServisi:
    """Bildirimlerin merkezi yonetimi ve soguma surelerini (Task 3.2) kontrol eden servis."""
    
    def __init__(self):
        # Bildirim anahtarlarini ve son gosterilme zamanlarini tutar
        self._bildirim_gecmisi: Dict[str, float] = {}

    def bildirim_gonderilebilir_mi(self, anahtar: str, soguma_suresi: int) -> bool:
        """
        Belirlenen anahtar icin bildirimin tekrar gosterilip gosterilemeyecegini kontrol eder.
        Task 3.2: Spam korumasi saglar.
        """
        simdi = time.time()
        son_zaman = self._bildirim_gecmisi.get(anahtar, 0)
        
        if simdi - son_zaman >= soguma_suresi:
            self._bildirim_gecmisi[anahtar] = simdi
            return True
            
        return False