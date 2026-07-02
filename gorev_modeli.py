from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Union
import uuid


class GorevOnceligi(Enum):
    DUSUK = "low"
    NORMAL = "normal"
    YUKSEK = "high"


@dataclass
class GorevModeli:
    baslik: str
    aciklama: str = ""
    oncelik: Union[GorevOnceligi, str] = GorevOnceligi.NORMAL
    tamamlandi: bool = False
    iptal_edildi: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bitis_tarihi: Optional[datetime] = None
    tamamlanma_zamani: Optional[datetime] = None
    iptal_zamani: Optional[datetime] = None
    olusturulma_zamani: datetime = field(default_factory=datetime.now)

    def suresi_gecti_mi(self) -> bool:
        return bool(
            self.bitis_tarihi
            and not self.tamamlandi
            and not self.iptal_edildi
            and datetime.now() > self.bitis_tarihi
        )

    def to_dict(self):
        data = asdict(self)
        data["oncelik"] = self.oncelik.value if isinstance(self.oncelik, GorevOnceligi) else str(self.oncelik or GorevOnceligi.NORMAL.value)
        for alan in ("bitis_tarihi", "tamamlanma_zamani", "iptal_zamani", "olusturulma_zamani"):
            data[alan] = data[alan].isoformat() if data.get(alan) else None
        return data

    @classmethod
    def from_dict(cls, data: dict):
        try:
            data = dict(data)
            data.setdefault("aciklama", "")
            data.setdefault("iptal_edildi", False)
            data.setdefault("tamamlanma_zamani", None)
            data.setdefault("iptal_zamani", None)

            if "oncelik" in data:
                try:
                    data["oncelik"] = GorevOnceligi(data["oncelik"])
                except ValueError:
                    data["oncelik"] = str(data["oncelik"] or GorevOnceligi.NORMAL.value)

            for alan in ("bitis_tarihi", "tamamlanma_zamani", "iptal_zamani", "olusturulma_zamani"):
                if data.get(alan):
                    data[alan] = datetime.fromisoformat(data[alan])

            return cls(**data)
        except (ValueError, KeyError, TypeError):
            return None

    def __post_init__(self):
        self.baslik = (self.baslik or "").strip()
        self.aciklama = (self.aciklama or "").strip()
        if isinstance(self.oncelik, str):
            self.oncelik = self.oncelik.strip() or GorevOnceligi.NORMAL.value
