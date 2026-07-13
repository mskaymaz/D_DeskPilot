from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PilDurumu:
    """Pil durumunu temsil eden veri modeli."""
    yuzde: int  # Mevcut pil yuzdesi
    sarjda: bool  # Sarj cihazi takili mi?
    durum_metni: str  # 'Normal', 'Dusuk', 'Kritik'
    zaman_damgasi: datetime  # Bilginin alindigi an
    sarj_durum_metni: str = "Bilinmiyor"
    saglik: Optional[str] = None  # Pil saglik bilgisi (destekleniyorsa)
    kalan_sure: Optional[int] = None  # Saniye cinsinden tahmini kalan sure
