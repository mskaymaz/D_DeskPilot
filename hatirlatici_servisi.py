import json
import os
import shutil
from datetime import datetime, timedelta
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
            
            if os.path.exists(self.dosya_yolu):
                shutil.copy2(self.dosya_yolu, self.dosya_yolu + ".bak")
            os.replace(gecici_dosya, self.dosya_yolu)
        except Exception as e:
            log_kaydet(f"Hatırlatıcılar kaydedilirken hata: {e}", "error")

    def hatirlatici_ekle(self, hatirlatici: HatirlaticiModeli):
        """Listeye yeni bir hatırlatıcı ekler ve kaydeder."""
        self._hatirlaticilar.append(hatirlatici)
        self.kaydet()

    def hatirlaticiyi_guncelle(self, hatirlatici: HatirlaticiModeli) -> bool:
        """Var olan hatırlatıcıyı kimliği üzerinden günceller ve kaydeder."""
        for index, mevcut in enumerate(self._hatirlaticilar):
            if mevcut.id == hatirlatici.id:
                self._hatirlaticilar[index] = hatirlatici
                self.kaydet()
                return True
        return False

    def hatirlaticilari_al(self) -> List[HatirlaticiModeli]:
        return self._hatirlaticilar

    def yaklasan_hatirlaticilari_al(self) -> List[HatirlaticiModeli]:
        """Aktif ve gelecekteki hatırlatıcıları zaman sırasıyla döndürür."""
        simdi = datetime.now()
        gelecektekiler = []
        for hatirlatici in self._hatirlaticilar:
            if hatirlatici.durum != HatirlaticiDurumu.AKTIF:
                continue
            zaman = (
                hatirlatici.erteleme_zamani
                if hatirlatici.erteleme_zamani
                else hatirlatici.hatirlatma_zamani
            )
            if zaman > simdi:
                gelecektekiler.append((zaman, hatirlatici))

        gelecektekiler.sort(key=lambda item: item[0])
        return [hatirlatici for _, hatirlatici in gelecektekiler]

    def gunluk_hatirlaticilari_al(self, tarih=None) -> List[HatirlaticiModeli]:
        """Belirtilen güne ait hatırlatıcıları saat sırasıyla döndürür."""
        hedef_tarih = tarih or datetime.now().date()
        gunluk = []
        for hatirlatici in self._hatirlaticilar:
            zaman = (
                hatirlatici.erteleme_zamani
                if hatirlatici.erteleme_zamani
                else hatirlatici.hatirlatma_zamani
            )
            if zaman.date() == hedef_tarih:
                gunluk.append((zaman, hatirlatici))

        gunluk.sort(key=lambda item: item[0])
        return [hatirlatici for _, hatirlatici in gunluk]

    def kacirilan_hatirlaticilari_al(self) -> List[HatirlaticiModeli]:
        """Kaçırıldı durumundaki hatırlatıcıları zaman sırasıyla döndürür."""
        kacirilanlar = [
            hatirlatici
            for hatirlatici in self._hatirlaticilar
            if hatirlatici.durum == HatirlaticiDurumu.KACIRILDI
        ]
        return sorted(
            kacirilanlar,
            key=lambda hatirlatici: hatirlatici.hatirlatma_zamani,
        )

    def hatirlaticilari_ertele(self, hatirlaticilar, dakika: int) -> int:
        """Aktif hatırlatıcıları belirtilen dakika kadar erteler."""
        yeni_zaman = datetime.now() + timedelta(minutes=max(1, int(dakika)))
        ertelenen_sayi = 0
        for hatirlatici in hatirlaticilar:
            if hatirlatici.durum != HatirlaticiDurumu.AKTIF:
                continue
            hatirlatici.erteleme_zamani = yeni_zaman
            ertelenen_sayi += 1

        if ertelenen_sayi:
            self.kaydet()
        return ertelenen_sayi

    def hatirlaticilari_etkinlestir(self, hatirlaticilar, etkin: bool) -> int:
        """Seçilen aktif/devre dışı hatırlatıcıların durumunu değiştirir."""
        kaynak_durum = (
            HatirlaticiDurumu.DEVRE_DISI
            if etkin
            else HatirlaticiDurumu.AKTIF
        )
        hedef_durum = (
            HatirlaticiDurumu.AKTIF
            if etkin
            else HatirlaticiDurumu.DEVRE_DISI
        )
        degisen_sayi = 0
        for hatirlatici in hatirlaticilar:
            if hatirlatici.durum != kaynak_durum:
                continue
            hatirlatici.durum = hedef_durum
            degisen_sayi += 1

        if degisen_sayi:
            self.kaydet()
        return degisen_sayi

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

    def kacirilanlari_tara(self, tolerans_saniye: int = 60) -> List[HatirlaticiModeli]:
        """Tolerans süresini aşan aktif hatırlatıcıları kaçırıldı olarak işaretler."""
        simdi = datetime.now()
        tolerans = timedelta(seconds=max(1, tolerans_saniye))
        kacirilanlar = []

        for hatirlatici in self._hatirlaticilar:
            if hatirlatici.durum != HatirlaticiDurumu.AKTIF:
                continue
            hedef_zaman = (
                hatirlatici.erteleme_zamani
                if hatirlatici.erteleme_zamani
                else hatirlatici.hatirlatma_zamani
            )
            if hedef_zaman + tolerans < simdi:
                hatirlatici.durum = HatirlaticiDurumu.KACIRILDI
                hatirlatici.erteleme_zamani = None
                kacirilanlar.append(hatirlatici)

        if kacirilanlar:
            self.kaydet()
        return kacirilanlar
