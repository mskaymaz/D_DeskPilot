import time
from datetime import datetime, timedelta
from PySide6 import QtCore, QtGui, QtWidgets
from core_settings import TIME_BASE_FONT_SIZE
from log_servisi import log_kaydet
from hicri_tarih_servisi import miladi_tarihten_hicriye

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
        saat, saniye, ampm = self._format_time_parts(now)
        date_text = self._format_date(now)
        hicri_text = self._format_hicri_date(now)
        self._saat_etiketlerini_guncelle(
            self.time_main_label,
            self.time_seconds_label,
            self.time_ampm_label,
            saat,
            saniye,
            ampm
        )
        self._saat_label_genisligini_sabitle()
        self.date_label.setText(date_text)
        self.hicri_date_label.setText(hicri_text)
        self._hafta_etiketlerini_guncelle(now)
        if self.free_time_window:
            self._saat_etiketlerini_guncelle(
                self.free_time_window.saat_etiketi,
                self.free_time_window.saniye_etiketi,
                self.free_time_window.ampm_etiketi,
                saat,
                saniye,
                ampm
            )
            # HTML QLabel icin adjustSize() guvenilmez; font metrikleriyle acık hesap yap
            if not self.free_time_window.surukleme_konumu:
                self._saat_pencere_boyut_guncelle()
        if self.free_date_window:
            self.free_date_window.etiket.setText(date_text)
            self.free_date_window.hicri_etiketi.setText(hicri_text)
            self._hafta_etiketlerini_guncelle(now, self.free_date_window)
            if not self.free_date_window.surukleme_konumu:
                self.free_date_window.icerik.adjustSize()
                self.free_date_window.adjustSize()
        if hasattr(self, "_rebuild_module_layout") and not getattr(self, "_group_drag", None):
            self._rebuild_module_layout(self.settings.global_scale)
            self.main_layout.activate()
            self.adjustSize()
    def _saat_label_genisligini_sabitle(self):
        genislik, _ = self._saat_olculerini_hesapla(20)
        self.time_label.setFixedWidth(genislik)

    def _saat_olculerini_hesapla(self, yatay_pay):
        scale = self.settings.global_scale * self.settings.time_scale
        base_size = int(TIME_BASE_FONT_SIZE * scale)
        sec_size = max(1, int(base_size * self.settings.time_seconds_scale))
        ampm_size = max(1, sec_size // 2)
        format_mode = getattr(self.settings, "time_format_mode", "24h" if getattr(self.settings, "time_24h", True) else "12h_ampm")
        cache_key = (
            yatay_pay,
            self.settings.time_font_family,
            base_size,
            sec_size,
            ampm_size,
            self.settings.time_bold,
            self.settings.time_seconds_visible,
            format_mode,
        )
        if getattr(self, "_saat_olcu_cache_key", None) == cache_key:
            return self._saat_olcu_cache_value
        font = QtGui.QFont(self.settings.time_font_family, base_size)
        font.setBold(self.settings.time_bold)
        sec_font = QtGui.QFont(self.settings.time_font_family, sec_size)
        ampm_font = QtGui.QFont(self.settings.time_font_family, ampm_size)
        fm = QtGui.QFontMetrics(font)
        sec_fm = QtGui.QFontMetrics(sec_font)
        ampm_fm = QtGui.QFontMetrics(ampm_font)
        genislik = fm.horizontalAdvance("88:88")
        if self.settings.time_seconds_visible:
            genislik += sec_fm.horizontalAdvance(":88" if format_mode in ("24h", "12h_plain") else ":88 ")
        if format_mode == "12h_ampm":
            genislik += ampm_fm.horizontalAdvance(" ÖÖ")
        yukseklik = fm.ascent() + fm.descent() + 6
        self._saat_olcu_cache_key = cache_key
        self._saat_olcu_cache_value = (genislik + yatay_pay, yukseklik)
        return self._saat_olcu_cache_value

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
        batt_text = f"Pil: {pil_verisi.yuzde}% ({pil_verisi.sarj_durum_metni})"
        
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
            now_ts = time.time()
            interval = max(1, int(getattr(self.settings, "battery_alert_interval", 10)))
            if now_ts - self._last_full_batt_alert_ts >= interval:
                self._play_batt_alert_sound()
                self._last_full_batt_alert_ts = now_ts
            if not self.full_charge_timer.isActive():
                self.full_charge_timer.start()
        else:
            self._last_full_batt_alert_ts = 0
            self._stop_full_charge_blink()

        if low_alert and not full_alert:
            now_ts = time.time()
            interval = max(1, int(getattr(self.settings, "battery_alert_interval", 10)))
            if now_ts - self._last_low_batt_alert_ts >= interval:
                self._play_batt_alert_sound()
                self._last_low_batt_alert_ts = now_ts
            if not self.low_batt_timer.isActive():
                self.low_batt_timer.start()
        else:
            self._last_low_batt_alert_ts = 0
            self._stop_low_batt_blink()

        # Sistem Tepsisi Özeti (Task 8.2)
        if hasattr(self, "tepsi_ikonu"):
            sonraki_h = None
            if getattr(self, "hatirlatici_servisi", None):
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
                popup = HatirlaticiBildirimPenceresi(
                    h,
                    sessiz_mod=getattr(self.settings, "sessiz_mod", False),
                )
                popup.tamamlandi_sinyali.connect(self._hatirlatici_tamamla)
                popup.ertelendi_sinyali.connect(self._hatirlatici_ertele)
                popup.destroyed.connect(lambda _=None, hid=h.id: self._aktif_popuplar.pop(hid, None))
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
            popup.destroyed.connect(lambda _=None, aid=alarm.id: self._aktif_alarm_popuplar.pop(aid, None))
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
            anahtar = f"missed_alarm:{alarm.id}"
            if getattr(self, "bildirim_servisi", None):
                if not self.bildirim_servisi.bildirim_gonderilebilir_mi(anahtar):
                    return
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

    def _format_time_parts(self, now):
        format_mode = getattr(self.settings, "time_format_mode", "24h" if getattr(self.settings, "time_24h", True) else "12h_ampm")
        if format_mode == "24h":
            hhmm = now.strftime("%H:%M")
        elif format_mode == "12h_plain":
            hhmm = now.strftime("%I:%M")
        else:
            hhmm = now.strftime("%I:%M %p")
        if format_mode == "12h_ampm":
            saat, ampm = hhmm.rsplit(" ", 1)
        else:
            saat, ampm = hhmm, ""
        saniye = f":{now.strftime('%S')}" if self.settings.time_seconds_visible else ""
        if saniye and ampm:
            saniye += " "
        return saat, saniye, ampm

    def _saat_etiketlerini_guncelle(self, saat_etiketi, saniye_etiketi, ampm_etiketi, saat, saniye, ampm):
        saat_etiketi.setText(saat)
        saniye_etiketi.setText(saniye)
        ampm_etiketi.setText(ampm)
        saniye_etiketi.setVisible(bool(saniye))
        ampm_etiketi.setVisible(bool(ampm))

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

    def _format_hicri_date(self, now):
        cache_key = now.date()
        if getattr(self, "_hicri_tarih_cache_key", None) == cache_key:
            return self._hicri_tarih_cache_value
        self._hicri_tarih_cache_key = cache_key
        self._hicri_tarih_cache_value = miladi_tarihten_hicriye(now.date()).formatla()
        return self._hicri_tarih_cache_value

    def _hafta_etiketlerini_guncelle(self, now, hedef=None):
        goster = self.settings.date_visible and getattr(self.settings, "date_show_week_number", False)
        cache_key = (now.date(), goster)
        if getattr(self, "_hafta_cache_key", None) == cache_key:
            hafta_sayi, hafta_yazi = self._hafta_cache_value
        else:
            hafta_sayi, hafta_yazi = f"{now.isocalendar().week}.", "HAFTA"
            self._hafta_cache_key = cache_key
            self._hafta_cache_value = (hafta_sayi, hafta_yazi)
        if hedef is None:
            ayrac = getattr(self, "date_week_separator_label", None)
            sayi = getattr(self, "date_week_number_label", None)
            yazi = getattr(self, "date_week_text_label", None)
        else:
            ayrac = getattr(hedef, "hafta_ayrac_etiketi", None)
            sayi = getattr(hedef, "hafta_sayi_etiketi", None)
            yazi = getattr(hedef, "hafta_yazi_etiketi", None)
        if not ayrac or not sayi or not yazi:
            return
        ayrac.setText("◆")
        sayi.setText(hafta_sayi)
        yazi.setText(hafta_yazi)
        ayrac.setVisible(goster)
        sayi.setVisible(goster)
        yazi.setVisible(goster)

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

    def _play_batt_alert_sound(self):
        if winsound is None or getattr(self.settings, "sessiz_mod", False):
            return False
        sound = str(getattr(self.settings, "battery_alert_sound_type", ""))
        try:
            if sound.endswith("2"):
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif sound.endswith("3"):
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                winsound.MessageBeep(winsound.MB_ICONHAND)
            return True
        except RuntimeError as e:
            log_kaydet(f"Pil uyari sesi calinamadi: {e}", "warning")
            return False
