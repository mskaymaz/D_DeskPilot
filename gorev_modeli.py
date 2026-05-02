from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import uuid
from typing import Optional

class GorevOnceligi(Enum):
    """Görevin önem derecesini belirleyen enum."""
    DUSUK = "low"
    NORMAL = "normal"
    YUKSEK = "high"

@dataclass
class GorevModeli:
    """
    Yapılacak görev (TODO) verilerini tutan veri modeli.
    Task 5.1 kapsamında oluşturulmuştur.
    """
    baslik: str # Görev başlığı
    oncelik: GorevOnceligi = GorevOnceligi.NORMAL # Öncelik seviyesi
    tamamlandi: bool = False # Tamamlanma durumu
    id: str = field(default_factory=lambda: str(uuid.uuid4())) # Benzersiz kimlik
    bitis_tarihi: Optional[datetime] = None # İsteğe bağlı son tarih
    olusturulma_zamani: datetime = field(default_factory=datetime.now) # Oluşturulma tarihi

    def to_dict(self):
        """Modeli JSON formatına uygun sözlüğe dönüştürür."""
        data = asdict(self)
        data["oncelik"] = self.oncelik.value
        if self.bitis_tarihi:
            data["bitis_tarihi"] = self.bitis_tarihi.isoformat()
        data["olusturulma_zamani"] = self.olusturulma_zamani.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Sözlük verisinden GorevModeli nesnesi oluşturur."""
        try:
            # Enum geri yükleme
            if "oncelik" in data:
                data["oncelik"] = GorevOnceligi(data["oncelik"])
            
            # Tarihleri geri yükleme
            if data.get("bitis_tarihi"):
                data["bitis_tarihi"] = datetime.fromisoformat(data["bitis_tarihi"])
            
            if "olusturulma_zamani" in data:
                data["olusturulma_zamani"] = datetime.fromisoformat(data["olusturulma_zamani"])
            
            return cls(**data)
        except (ValueError, KeyError):
            return None

    def __post_init__(self):
        """Başlık kontrolü."""
        self.baslik = self.baslik.strip()