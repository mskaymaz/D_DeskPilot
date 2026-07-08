import json
import os
import shutil
from datetime import datetime, timedelta
from typing import List, Optional

from alarm_modeli import AlarmModeli, AlarmDurumu
from utils import APP_DATA_DIR, log_kaydet


class AlarmServisi:
    def __init__(self):
        self.dosya_yolu = os.path.join(APP_DATA_DIR, "alarmlar.json")
        self._alarmlar: List[AlarmModeli] = []
        self.yukle()

    def yukle(self) -> List[AlarmModeli]:
        if not os.path.exists(self.dosya_yolu):
            self._alarmlar = []
            return self._alarmlar
        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                ham_veri = json.load(f)
            self._alarmlar = []
            for item in ham_veri if isinstance(ham_veri, list) else []:
                alarm = AlarmModeli.from_dict(item)
                if alarm:
                    self._alarmlar.append(alarm)
            log_kaydet(f"{len(self._alarmlar)} alarm yüklendi.")
        except Exception as e:
            log_kaydet(f"Alarmlar yüklenirken hata: {e}", "error")
            self._alarmlar = []
        return self._alarmlar

    def kaydet(self):
        try:
            os.makedirs(APP_DATA_DIR, exist_ok=True)
            gecici_dosya = self.dosya_yolu + ".tmp"
            with open(gecici_dosya, "w", encoding="utf-8") as f:
                json.dump([a.to_dict() for a in self._alarmlar], f, ensure_ascii=False, indent=2)
            if os.path.exists(self.dosya_yolu):
                shutil.copy2(self.dosya_yolu, self.dosya_yolu + ".bak")
            os.replace(gecici_dosya, self.dosya_yolu)
        except Exception as e:
            log_kaydet(f"Alarmlar kaydedilirken hata: {e}", "error")

    def alarmlari_al(self) -> List[AlarmModeli]:
        return self._alarmlar

    def alarm_ekle(self, alarm: AlarmModeli):
        self._alarmlar.append(alarm)
        self.kaydet()

    def alarm_guncelle(self, alarm: AlarmModeli) -> bool:
        for i, mevcut in enumerate(self._alarmlar):
            if mevcut.id == alarm.id:
                self._alarmlar[i] = alarm
                self.kaydet()
                return True
        return False

    def alarm_sil(self, alarm_id: str) -> bool:
        onceki = len(self._alarmlar)
        self._alarmlar = [a for a in self._alarmlar if a.id != alarm_id]
        if len(self._alarmlar) != onceki:
            self.kaydet()
            return True
        return False

    def alarm_aktiflik_degistir(self, alarm_id: str, aktif: bool) -> bool:
        for alarm in self._alarmlar:
            if alarm.id == alarm_id:
                alarm.durum = AlarmDurumu.AKTIF if aktif else AlarmDurumu.PASIF
                self.kaydet()
                return True
        return False

    def en_yakin_alarm_bul(self) -> Optional[AlarmModeli]:
        simdi = datetime.now()
        adaylar = [(a.sonraki_zamani_hesapla(simdi), a) for a in self._alarmlar]
        adaylar = [(zaman, alarm) for zaman, alarm in adaylar if zaman is not None]
        if not adaylar:
            return None
        return min(adaylar, key=lambda item: item[0])[1]

    def zamani_gelenleri_tara(self) -> List[AlarmModeli]:
        simdi = datetime.now()
        gelenler = []
        for alarm in self._alarmlar:
            if alarm.durum != AlarmDurumu.AKTIF:
                continue
            if alarm.erteleme_zamani:
                if alarm.erteleme_zamani <= simdi:
                    gelenler.append(alarm)
                continue
            if not self._bugun_calmali_mi(alarm, simdi):
                continue
            try:
                alarm_saat = datetime.strptime(alarm.saat, "%H:%M").time()
            except ValueError:
                continue
            hedef = datetime.combine(simdi.date(), alarm_saat)
            son = alarm.son_calisma_zamani
            bugun_durduruldu = son and son.date() == simdi.date() and son >= hedef
            if hedef <= simdi and not bugun_durduruldu:
                gelenler.append(alarm)
        return gelenler

    def kacirilanlari_tara(self, tolerans_saniye: int = 60) -> List[AlarmModeli]:
        simdi = datetime.now()
        kacirilanlar = []
        tolerans = timedelta(seconds=max(1, tolerans_saniye))
        for alarm in self._alarmlar:
            if alarm.durum != AlarmDurumu.AKTIF or alarm.erteleme_zamani:
                continue
            if not self._bugun_calmali_mi(alarm, simdi):
                continue
            try:
                alarm_saat = datetime.strptime(alarm.saat, "%H:%M").time()
            except ValueError:
                continue
            hedef = datetime.combine(simdi.date(), alarm_saat)
            son = alarm.son_calisma_zamani
            bugun_islem_gordu = son and son.date() == simdi.date() and son >= hedef
            if hedef + tolerans < simdi and not bugun_islem_gordu:
                alarm.durum = AlarmDurumu.KACIRILDI
                alarm.son_calisma_zamani = simdi
                alarm.erteleme_zamani = None
                kacirilanlar.append(alarm)
        if kacirilanlar:
            self.kaydet()
        return kacirilanlar

    def _bugun_calmali_mi(self, alarm: AlarmModeli, simdi: datetime) -> bool:
        if alarm.tekrar_tipi.value == "daily":
            return True
        gunler = alarm.haftanin_gunleri or []
        return simdi.weekday() in gunler

    def alarm_durdur(self, alarm_id: str) -> bool:
        for alarm in self._alarmlar:
            if alarm.id == alarm_id:
                alarm.son_calisma_zamani = datetime.now()
                alarm.erteleme_zamani = None
                self.kaydet()
                return True
        return False

    def alarm_ertele(self, alarm_id: str, dakika: int) -> bool:
        for alarm in self._alarmlar:
            if alarm.id == alarm_id:
                from datetime import timedelta
                alarm.erteleme_zamani = datetime.now() + timedelta(minutes=dakika)
                self.kaydet()
                return True
        return False

    def kacirilan_bildirildi_isaretle(self, alarm_ids: list[str]) -> bool:
        ids = set(alarm_ids)
        degisti = False
        for alarm in self._alarmlar:
            if alarm.id in ids and alarm.durum == AlarmDurumu.KACIRILDI:
                alarm.durum = AlarmDurumu.AKTIF
                alarm.son_calisma_zamani = datetime.now()
                alarm.erteleme_zamani = None
                degisti = True
        if degisti:
            self.kaydet()
        return degisti
