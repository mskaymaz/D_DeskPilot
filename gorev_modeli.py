from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
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
    cope_atildi: bool = False
    sira: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bitis_tarihi: Optional[datetime] = None
    tamamlanma_zamani: Optional[datetime] = None
    iptal_zamani: Optional[datetime] = None
    cope_atilma_zamani: Optional[datetime] = None
    olusturulma_zamani: datetime = field(default_factory=datetime.now)
    yapilacaklar: List[str] = field(default_factory=list)

    def suresi_gecti_mi(self) -> bool:
        return bool(
            self.bitis_tarihi
            and not self.tamamlandi
            and not self.iptal_edildi
            and not self.cope_atildi
            and datetime.now() > self.bitis_tarihi
        )

    def to_dict(self):
        data = asdict(self)
        data["oncelik"] = self.oncelik.value if isinstance(self.oncelik, GorevOnceligi) else str(self.oncelik or GorevOnceligi.NORMAL.value)
        for alan in ("bitis_tarihi", "tamamlanma_zamani", "iptal_zamani", "cope_atilma_zamani", "olusturulma_zamani"):
            data[alan] = data[alan].isoformat() if data.get(alan) else None
        return data

    @classmethod
    def from_dict(cls, data: dict):
        try:
            data = dict(data)
            durum = data.get("durum", data.get("status"))
            allowed_fields = {field.name for field in cls.__dataclass_fields__.values()}
            data = {key: value for key, value in data.items() if key in allowed_fields}
            data.setdefault("aciklama", "")
            data.setdefault("yapilacaklar", [])
            data.setdefault("iptal_edildi", durum == "cancelled")
            data.setdefault("cope_atildi", durum == "trashed")
            data.setdefault("tamamlandi", durum == "completed")
            data.setdefault("sira", 0)
            data.setdefault("tamamlanma_zamani", None)
            data.setdefault("iptal_zamani", None)
            data.setdefault("cope_atilma_zamani", None)

            if "oncelik" in data:
                try:
                    data["oncelik"] = GorevOnceligi(data["oncelik"])
                except ValueError:
                    data["oncelik"] = str(data["oncelik"] or GorevOnceligi.NORMAL.value)

            for alan in ("bitis_tarihi", "tamamlanma_zamani", "iptal_zamani", "cope_atilma_zamani", "olusturulma_zamani"):
                if data.get(alan):
                    data[alan] = datetime.fromisoformat(data[alan])

            return cls(**data)
        except (ValueError, KeyError, TypeError):
            return None

    def __post_init__(self):
        self.baslik = (self.baslik or "").strip()
        self.aciklama = (self.aciklama or "").strip()
        if isinstance(self.yapilacaklar, str):
            self.yapilacaklar = self.yapilacaklar.splitlines()
        self.yapilacaklar = [str(item).strip() for item in (self.yapilacaklar or []) if str(item).strip()]
        if isinstance(self.oncelik, str):
            self.oncelik = self.oncelik.strip() or GorevOnceligi.NORMAL.value
        try:
            self.sira = int(self.sira or 0)
        except (TypeError, ValueError):
            self.sira = 0

    @property
    def durum(self) -> str:
        if self.cope_atildi:
            return "trashed"
        if self.iptal_edildi:
            return "cancelled"
        if self.tamamlandi:
            return "completed"
        return "active"
