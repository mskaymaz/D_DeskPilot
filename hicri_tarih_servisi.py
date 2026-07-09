from __future__ import annotations

from dataclasses import dataclass
from datetime import date


HICRI_AY_ADLARI = (
    "Muharrem",
    "Safer",
    "Rebiulevvel",
    "Rebiulahir",
    "Cemaziyelevvel",
    "Cemaziyelahir",
    "Recep",
    "Saban",
    "Ramazan",
    "Sevval",
    "Zilkade",
    "Zilhicce",
)

_HICRI_EPOCH_JDN = 1948439


@dataclass(frozen=True)
class HicriTarih:
    yil: int
    ay: int
    gun: int

    @property
    def ay_adi(self) -> str:
        return HICRI_AY_ADLARI[self.ay - 1]

    def formatla(self) -> str:
        return f"{self.gun} {self.ay_adi} {self.yil}"


def miladi_tarihten_hicriye(miladi: date) -> HicriTarih:
    jdn = _miladi_jdn(miladi)
    yil = (30 * (jdn - _HICRI_EPOCH_JDN) + 10646) // 10631

    ay = 1
    while ay < 12 and jdn >= _hicri_jdn(yil, ay + 1, 1):
        ay += 1

    gun = jdn - _hicri_jdn(yil, ay, 1) + 1
    return HicriTarih(yil=yil, ay=ay, gun=gun)


def bugunun_hicri_tarihi() -> HicriTarih:
    return miladi_tarihten_hicriye(date.today())


def _miladi_jdn(miladi: date) -> int:
    a = (14 - miladi.month) // 12
    y = miladi.year + 4800 - a
    m = miladi.month + 12 * a - 3
    return miladi.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def _hicri_jdn(yil: int, ay: int, gun: int) -> int:
    return (
        gun
        + (59 * (ay - 1) + 1) // 2
        + (yil - 1) * 354
        + (3 + 11 * yil) // 30
        + _HICRI_EPOCH_JDN
        - 1
    )
