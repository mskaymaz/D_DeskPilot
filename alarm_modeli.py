from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, time
from enum import Enum
from typing import Optional
import uuid


class AlarmTekrarTipi(Enum):
    GUNLUK = "daily"
    HAFTALIK = "weekly"


class AlarmDurumu(Enum):
    AKTIF = "active"
    PASIF = "inactive"
    KACIRILDI = "missed"


@dataclass
class AlarmModeli:
    baslik: str
    saat: str
    aciklama: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tekrar_tipi: AlarmTekrarTipi = AlarmTekrarTipi.GUNLUK
    haftanin_gunleri: list[int] = field(default_factory=list)
    durum: AlarmDurumu = AlarmDurumu.AKTIF
    snooze_dakika: int = 5
    ses_tipi: str = "Varsayılan"
    ses_seviyesi: int = 70
    tts_aktif: bool = False
    erteleme_zamani: Optional[datetime] = None
    son_calisma_zamani: Optional[datetime] = None
    olusturulma_zamani: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        data = asdict(self)
        data["tekrar_tipi"] = self.tekrar_tipi.value
        data["durum"] = self.durum.value
        data["erteleme_zamani"] = self.erteleme_zamani.isoformat() if self.erteleme_zamani else None
        data["son_calisma_zamani"] = self.son_calisma_zamani.isoformat() if self.son_calisma_zamani else None
        data["olusturulma_zamani"] = self.olusturulma_zamani.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict):
        try:
            data = dict(data)
            data["tekrar_tipi"] = AlarmTekrarTipi(data.get("tekrar_tipi", AlarmTekrarTipi.GUNLUK.value))
            data["durum"] = AlarmDurumu(data.get("durum", AlarmDurumu.AKTIF.value))
            data["olusturulma_zamani"] = datetime.fromisoformat(data["olusturulma_zamani"])
            if data.get("erteleme_zamani"):
                data["erteleme_zamani"] = datetime.fromisoformat(data["erteleme_zamani"])
            if data.get("son_calisma_zamani"):
                data["son_calisma_zamani"] = datetime.fromisoformat(data["son_calisma_zamani"])
            cls._saat_dogrula(data["saat"])
            data["haftanin_gunleri"] = [int(g) for g in data.get("haftanin_gunleri", []) if 0 <= int(g) <= 6]
            return cls(**data)
        except (TypeError, ValueError, KeyError):
            return None

    @staticmethod
    def _saat_dogrula(saat: str) -> time:
        return datetime.strptime(saat, "%H:%M").time()

    def sonraki_zamani_hesapla(self, simdi: Optional[datetime] = None) -> Optional[datetime]:
        if self.durum != AlarmDurumu.AKTIF:
            return None
        simdi = simdi or datetime.now()
        if self.erteleme_zamani and self.erteleme_zamani > simdi:
            return self.erteleme_zamani

        alarm_saati = self._saat_dogrula(self.saat)
        aday = datetime.combine(simdi.date(), alarm_saati)
        if aday <= simdi:
            aday += timedelta(days=1)

        if self.tekrar_tipi == AlarmTekrarTipi.GUNLUK:
            return aday

        gunler = self.haftanin_gunleri or [simdi.weekday()]
        for offset in range(8):
            haftalik_aday = datetime.combine((simdi + timedelta(days=offset)).date(), alarm_saati)
            if haftalik_aday > simdi and haftalik_aday.weekday() in gunler:
                return haftalik_aday
        return None
