import time
from datetime import datetime, timedelta
from PySide6 import QtCore, QtGui, QtWidgets
from log_servisi import log_kaydet

try:
    import winsound
except ImportError:
    winsound = None

class PencereGuncellemeKarishimi:
    """
    Ana pencerenin güncelleme döngülerini (Saat, Pil, Hatırlatıcı) yöneten karışım sınıfı.
    Dosya boyutu disiplini (Rule: <400 lines) için core_window'dan ayrılmıştır.
    """
    def update_time(self):
        now = datetime.now()
        time_text = self._format_time_html(now)
        date_text = self._format_date(now)
        self.time_label.setText(time_text)
        self._saat_label_genisligini_sabitle()
        self.date_label.setText(date_text)
        if self.free_time_window:
            self.free_time_window.icerik.setText(time_text)
            self.free_time_window.icerik.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            # HTML QLabel icin adjustSize() guvenilmez; font metrikleriyle acık hesap yap
            if not self.free_time_window.surukleme_konumu:
                self._saat_pencere_boyut_guncelle()
        if self.free_date_window:
            self.free_date_window.icerik.setText(date_text)
            if not self.free_date_window.surukleme_konumu:
                self.free_date_window.icerik.adjustSize()
                self.free_date_window.adjustSize()
    def _saat_label_genisligini_sabitle(self):
        genislik, _ = self._saat_olculerini_hesapla(20)
        self.time_label.setFixedWidth(genislik)
        self.time_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

    def _saat_olculerini_hesapla(self, yatay_pay):
        scale = self.settings.global_scale * self.settings.time_scale
        base_size = int(self.settings.time_font_size * scale)
        sec_size = max(1, int(base_size * self.settings.time_seconds_scale))
        ampm_size = max(1, sec_size // 2)
        font = QtGui.QFont(self.settings.time_font_family, base_size)
        font.setBold(self.settings.time_bold)
        sec_font = QtGui.QFont(self.settings.time_font_family, sec_size)
        ampm_font = QtGui.QFont(self.settings.time_font_family, ampm_size)
        fm = QtGui.QFontMetrics(font)
        sec_fm = QtGui.QFontMetrics(sec_font)
        ampm_fm = QtGui.QFontMetrics(ampm_font)
        format_mode = getattr(self.settings, "time_format_mode", "24h" if getattr(self.settings, "time_24h", True) else "12h_ampm")
        genislik = fm.horizontalAdvance("88:88")
        if self.settings.time_seconds_visible:
            genislik += sec_fm.horizontalAdvance(":88" if format_mode in ("24h", "12h_plain") else ":88 ")
        if format_mode == "12h_ampm":
            genislik += ampm_fm.horizontalAdvance(" ÖÖ")
        yukseklik = fm.ascent() + fm.descent() + 6
        return genislik + yatay_pay, yukseklik

    def _saat_pencere_boyut_guncelle(self):
        """
        Saat penceresi boyutunu font metriklerinden acıkcıa hesaplar.
        HTML icerigi nedeniyle adjustSize() cıktısı sıfır veya hatali olabilir;
        bu metot pencereyi her zaman tıklanabilir boyutta tutar.
        """
        genislik, yukseklik = self._saat_olculerini_hesapla(16)
        if self.free_time_window.width() == genislik and self.free_time_window.height() == yukseklik:
            return
        self.free_time_window.setMinimumSize(genislik, yukseklik)
        self.free_time_window.resize(genislik, yukseklik)

    def update_battery(self):
        if not getattr(self, "pil_servisi", None):
            return
        if not self.settings.battery_visible:
            self._stop_full_charge_blink()
            self._stop_low_batt_blink()
            return

        pil_verisi = self.pil_servisi.mevcut_durumu_al()
        if not pil_verisi: return

        if self.pil_servisi.sarj_durumu_degisti_mi(pil_verisi.sarjda):
            log_kaydet("Şarj durumu değişti.")

        sarj_ikonu = "⚡" if pil_verisi.sarjda else ""
        batt_text = f"Pil: {pil_verisi.yuzde}%"
        
        self.battery_label.setText(batt_text)
        self.battery_icon_label.setText(sarj_ikonu)
        self.battery_icon_label.setVisible(pil_verisi.sarjda)

        if self.free_battery_window:
            self.free_battery_window.pil_etiketi.setText(batt_text)
            self.free_battery_window.pil_ikon_etiketi.setText(sarj_ikonu)
            self.free_battery_window.pil_ikon_etiketi.setVisible(pil_verisi.sarjda)
        # Uyarı Mantığı
        full_alert = (self.settings.battery_full_alert_enabled and pil_verisi.sarjda 
                      and pil_verisi.yuzde >= self.settings.battery_full_alert_level)
        low_alert = (not pil_verisi.sarjda and pil_verisi.yuzde <= self.settings.battery_warning_level)

        if full_alert:
            if not self.full_charge_timer.isActive(): self.full_charge_timer.start()
        else:
            self._stop_full_charge_blink()

        if low_alert and not full_alert:
            if not self.low_batt_timer.isActive(): self.low_batt_timer.start()
        else:
            self._stop_low_batt_blink()

        # Sistem Tepsisi Özeti (Task 8.2)
        if hasattr(self, "tepsi_ikonu"):
            sonraki_h = self.hatirlatici_servisi.en_yakin_hatirlaticiyi_bul()
            sonraki_metin = ""
            if sonraki_h:
                zaman = sonraki_h.erteleme_zamani if sonraki_h.erteleme_zamani else sonraki_h.hatirlatma_zamani
                sonraki_metin = f"{sonraki_h.baslik} ({zaman.strftime('%H:%M')})"
            
            self.tepsi_ikonu.ozet_guncelle(pil_verisi.yuzde, pil_verisi.sarjda, sonraki_metin)

    def hatirlaticilari_kontrol_et(self):
        if not getattr(self, "hatirlatici_servisi", None):
            return
        from hatirlatici_popup import HatirlaticiBildirimPenceresi

        gelenler = self.hatirlatici_servisi.zamani_gelenleri_tara()
        for h in gelenler:
            if h.id not in self._aktif_popuplar:
                popup = HatirlaticiBildirimPenceresi(h)
                popup.tamamlandi_sinyali.connect(self._hatirlatici_tamamla)
                popup.ertelendi_sinyali.connect(self._hatirlatici_ertele)
                popup.show()
                self._aktif_popuplar[h.id] = popup

    def _hatirlatici_tamamla(self, hatirlatici_id):
        from hatirlatici_modeli import HatirlaticiDurumu

        for h in self.hatirlatici_servisi.hatirlaticilari_al():
            if h.id == hatirlatici_id:
                sonraki = h.sonraki_zamani_hesapla()
                if sonraki:
                    h.hatirlatma_zamani = sonraki
                    h.erteleme_zamani = None
                else:
                    h.durum = HatirlaticiDurumu.TAMAMLANDI
                self.hatirlatici_servisi.kaydet()
                self._aktif_popuplar.pop(hatirlatici_id, None)
                break

    def _hatirlatici_ertele(self, hatirlatici_id, dakika):
        for h in self.hatirlatici_servisi.hatirlaticilari_al():
            if h.id == hatirlatici_id:
                h.erteleme_zamani = datetime.now() + timedelta(minutes=dakika)
                self.hatirlatici_servisi.kaydet()
                self._aktif_popuplar.pop(hatirlatici_id, None)
                break

    def alarmlari_kontrol_et(self):
        if not getattr(self, "alarm_servisi", None):
            return
        from alarm_popup import AlarmBildirimPenceresi

        for alarm in self.alarm_servisi.kacirilanlari_tara():
            self._kacirilan_alarm_bildir(alarm)

        for alarm in self.alarm_servisi.zamani_gelenleri_tara():
            if alarm.id in self._aktif_alarm_popuplar:
                continue
            popup = AlarmBildirimPenceresi(
                alarm,
                sessiz_mod=getattr(self.settings, "sessiz_mod", False),
            )
            popup.durduruldu_sinyali.connect(self._alarm_durdur)
            popup.ertelendi_sinyali.connect(self._alarm_ertele)
            popup.show()
            self._aktif_alarm_popuplar[alarm.id] = popup

    def _baslangic_kacirilan_alarmlari_goster(self):
        if not getattr(self, "alarm_servisi", None):
            return
        yeni_kacirilanlar = self.alarm_servisi.kacirilanlari_tara()
        tum_kacirilanlar = [
            alarm
            for alarm in self.alarm_servisi.alarmlari_al()
            if getattr(alarm.durum, "value", alarm.durum) == "missed"
        ]
        if not tum_kacirilanlar:
            return
        satirlar = []
        yeni_ids = {alarm.id for alarm in yeni_kacirilanlar}
        for alarm in tum_kacirilanlar:
            yeni = "Yeni - " if alarm.id in yeni_ids else ""
            satirlar.append(f"{yeni}{alarm.saat} - {alarm.baslik or 'Alarm'}")
        QtWidgets.QMessageBox.warning(
            self,
            "Kaçırılan Alarmlar",
            "Kaçırılan alarmlar:\n\n" + "\n".join(satirlar),
        )
        self.alarm_servisi.kacirilan_bildirildi_isaretle([alarm.id for alarm in tum_kacirilanlar])

    def _kacirilan_alarm_bildir(self, alarm):
        baslik = alarm.baslik or "Alarm"
        mesaj = f"{baslik} ({alarm.saat}) kaçırıldı."
        log_kaydet(mesaj)
        if hasattr(self, "tepsi_ikonu"):
            self.tepsi_ikonu.showMessage(
                "Kaçırılan alarm",
                mesaj,
                QtWidgets.QSystemTrayIcon.MessageIcon.Warning,
                5000,
            )

    def _alarm_durdur(self, alarm_id):
        self.alarm_servisi.alarm_durdur(alarm_id)
        self._aktif_alarm_popuplar.pop(alarm_id, None)

    def _alarm_ertele(self, alarm_id, dakika):
        self.alarm_servisi.alarm_ertele(alarm_id, dakika)
        self._aktif_alarm_popuplar.pop(alarm_id, None)

    def _format_time_html(self, now):
        scale = self.settings.global_scale * self.settings.time_scale
        base_size = int(self.settings.time_font_size * scale)
        sec_size = max(1, int(base_size * self.settings.time_seconds_scale))
        ampm_size = max(1, sec_size // 2)
        weight = "bold" if self.settings.time_bold else "normal"
        color = self.settings.time_color
        format_mode = getattr(self.settings, "time_format_mode", "24h" if getattr(self.settings, "time_24h", True) else "12h_ampm")
        if format_mode == "24h":
            hhmm = now.strftime("%H:%M")
        elif format_mode == "12h_plain":
            hhmm = now.strftime("%I:%M")
        else:
            hhmm = now.strftime("%I:%M %p")
        if format_mode == "12h_ampm":
            saat, ampm = hhmm.rsplit(" ", 1)
            if not self.settings.time_seconds_visible:
                return (f"<span style='font-size:{base_size}px; font-weight:{weight}; color:{color};'>{saat}</span>"
                        f"<span style='font-size:{ampm_size}px; color:{color};'> {ampm}</span>")
        if not self.settings.time_seconds_visible:
            return f"<span style='font-size:{base_size}px; font-weight:{weight}; color:{color};'>{hhmm}</span>"
        if format_mode in ("24h", "12h_plain"):
            return (f"<span style='font-size:{base_size}px; font-weight:{weight}; color:{color};'>{hhmm}</span>"
                    f"<span style='font-size:{sec_size}px; color:{color};'>:{now.strftime('%S')}</span>")
        return (f"<span style='font-size:{base_size}px; font-weight:{weight}; color:{color};'>{saat}</span>"
                f"<span style='font-size:{sec_size}px; color:{color};'>:{now.strftime('%S')} </span>"
                f"<span style='font-size:{ampm_size}px; color:{color};'>{ampm}</span>")

    def _format_date(self, now):
        fmt = self.settings.date_format.strip()

        # Kullanıcı doğrudan strftime formatı girdiyse aynen kullan.
        if "%" in fmt:
            return now.strftime(fmt)

        mapping = {
            "g": "%d", "G": "%d",
            "a": "%b", "A": "%B",
            "y": "%y", "Y": "%Y",
            "h": "%a", "H": "%A",
        }
        fmt = "".join(mapping.get(ch, ch) for ch in fmt)
        return now.strftime(fmt)

    def _stop_full_charge_blink(self):
        if self.full_charge_timer.isActive(): self.full_charge_timer.stop()
        self._set_battery_color(self.settings.battery_color)

    def _toggle_full_charge_blink(self):
        self._full_charge_blink_on = not self._full_charge_blink_on
        self._set_battery_color("#00cc66" if self._full_charge_blink_on else self.settings.battery_color)

    def _stop_low_batt_blink(self):
        if self.low_batt_timer.isActive(): self.low_batt_timer.stop()
        self._set_battery_color(self.settings.battery_color)

    def _toggle_low_batt_blink(self):
        self._low_batt_blink_on = not self._low_batt_blink_on
        self._set_battery_color("#cc0000" if self._low_batt_blink_on else self.settings.battery_color)

    def _set_battery_color(self, color):
        style = f"color:{color}; opacity:{self.settings.battery_opacity};"
        self.battery_label.setStyleSheet(style)
        if self.free_battery_window:
            self.free_battery_window.pil_etiketi.setStyleSheet(style)
