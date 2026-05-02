from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid
from typing import Optional

class TekrarTipi(Enum):
    """Hatırlatıcının tekrar etme sıklığını belirleyen enum."""
    YOK = "none"
    GUNLUK = "daily"
    HAFTALIK = "weekly"

class HatirlaticiDurumu(Enum):
    """Hatırlatıcının güncel yaşam döngüsü durumu."""
    AKTIF = "active"
    TAMAMLANDI = "completed"
    KACIRILDI = "missed"

@dataclass
class HatirlaticiModeli:
    """
    Hatırlatıcı verilerini tutan temel veri modeli.
    Task 4.1 kapsamında oluşturulmuştur.
    """
    baslik: str # Hatırlatıcı başlığı
    hatirlatma_zamani: datetime # Hatırlatıcının çalacağı zaman
    aciklama: str = "" # İsteğe bağlı açıklama
    id: str = field(default_factory=lambda: str(uuid.uuid4())) # Benzersiz kimlik
    tekrar_tipi: TekrarTipi = TekrarTipi.YOK # Tekrar tipi
    durum: HatirlaticiDurumu = HatirlaticiDurumu.AKTIF # Mevcut durum
    erteleme_zamani: Optional[datetime] = None # Eğer ertelendiyse yeni zaman
    olusturulma_zamani: datetime = field(default_factory=datetime.now) # Oluşturulma tarihi

    def to_dict(self):
        """Modeli JSON formatına uygun sözlüğe dönüştürür."""
        data = asdict(self)
        data["hatirlatma_zamani"] = self.hatirlatma_zamani.isoformat()
        data["tekrar_tipi"] = self.tekrar_tipi.value
        data["durum"] = self.durum.value
        if self.erteleme_zamani:
            data["erteleme_zamani"] = self.erteleme_zamani.isoformat()
        data["olusturulma_zamani"] = self.olusturulma_zamani.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Sözlük verisinden HatirlaticiModeli nesnesi oluşturur."""
        try:
            # Tarih formatlarını datetime nesnesine geri çevir
            data["hatirlatma_zamani"] = datetime.fromisoformat(data["hatirlatma_zamani"])
            data["olusturulma_zamani"] = datetime.fromisoformat(data["olusturulma_zamani"])
            if data.get("erteleme_zamani"):
                data["erteleme_zamani"] = datetime.fromisoformat(data["erteleme_zamani"])
            
            # Enum değerlerini geri yükle
            data["tekrar_tipi"] = TekrarTipi(data["tekrar_tipi"])
            data["durum"] = HatirlaticiDurumu(data["durum"])
            
            return cls(**data)
        except (ValueError, KeyError) as e:
            # Veri bozuksa veya format uymuyorsa hata dönebilir (Task 4.2 doğrulaması)
            return None

    def sonraki_zamani_hesapla(self) -> Optional[datetime]:
        """Tekrar tipine göre bir sonraki hatırlatma zamanını hesaplar."""
        # Task 4.5 kapsamında eklenmiştir.
        if self.tekrar_tipi == TekrarTipi.GUNLUK:
            return self.hatirlatma_zamani + timedelta(days=1)
        elif self.tekrar_tipi == TekrarTipi.HAFTALIK:
            return self.hatirlatma_zamani + timedelta(weeks=1)
        return None