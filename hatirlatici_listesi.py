try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from hatirlatici_servisi import HatirlaticiServisi
from datetime import datetime
from hatirlatici_modeli import HatirlaticiModeli, HatirlaticiDurumu


class HatirlaticiOlusturDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, hatirlatici=None):
        super().__init__(parent)
        self.setWindowTitle(
            "Hatırlatıcı Düzenle" if hatirlatici else "Yeni Hatırlatıcı"
        )
        self.setMinimumWidth(360)
        self.hatirlatici = hatirlatici

        form = QtWidgets.QFormLayout(self)
        self.txt_baslik = QtWidgets.QLineEdit()
        self.txt_baslik.setPlaceholderText("Hatırlatıcı başlığı")

        self.txt_aciklama = QtWidgets.QPlainTextEdit()
        self.txt_aciklama.setPlaceholderText("Açıklama (isteğe bağlı)")
        self.txt_aciklama.setFixedHeight(80)

        self.dt_zaman = QtWidgets.QDateTimeEdit(
            QtCore.QDateTime.currentDateTime().addSecs(3600)
        )
        self.dt_zaman.setCalendarPopup(True)
        self.dt_zaman.setDisplayFormat("dd.MM.yyyy HH:mm")

        if hatirlatici:
            self.txt_baslik.setText(hatirlatici.baslik)
            self.txt_aciklama.setPlainText(hatirlatici.aciklama)
            self.dt_zaman.setDateTime(
                QtCore.QDateTime.fromSecsSinceEpoch(
                    int(hatirlatici.hatirlatma_zamani.timestamp())
                )
            )

        form.addRow("Başlık", self.txt_baslik)
        form.addRow("Açıklama", self.txt_aciklama)
        form.addRow("Tarih ve saat", self.dt_zaman)

        butonlar = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        butonlar.accepted.connect(self._olustur)
        butonlar.rejected.connect(self.reject)
        form.addRow(butonlar)

    def _olustur(self):
        baslik = self.txt_baslik.text().strip()
        if not baslik:
            QtWidgets.QMessageBox.warning(
                self,
                "Yeni Hatırlatıcı",
                "Lütfen bir başlık girin.",
            )
            self.txt_baslik.setFocus()
            return

        zaman = datetime.fromtimestamp(self.dt_zaman.dateTime().toSecsSinceEpoch())
        if self.hatirlatici is None:
            self.hatirlatici = HatirlaticiModeli(
                baslik=baslik,
                aciklama=self.txt_aciklama.toPlainText().strip(),
                hatirlatma_zamani=zaman,
            )
        else:
            self.hatirlatici.baslik = baslik
            self.hatirlatici.aciklama = self.txt_aciklama.toPlainText().strip()
            self.hatirlatici.hatirlatma_zamani = zaman
            self.hatirlatici.erteleme_zamani = None
        self.accept()

class HatirlaticiListesiDialog(QtWidgets.QDialog):
    """
    Tüm hatırlatıcıların listelendiği modern arayüz penceresi.
    Task 4.6 kapsamında oluşturulmuştur.
    """
    def __init__(self, servis: HatirlaticiServisi, parent=None):
        super().__init__(parent)
        self.servis = servis
        self.setWindowTitle("Hatırlatıcı Listesi")
        self.setMinimumSize(500, 400)
        self._arayuz_kur()
        self.verileri_yukle()

    def _arayuz_kur(self):
        layout = QtWidgets.QVBoxLayout(self)

        gorunum_layout = QtWidgets.QHBoxLayout()
        gorunum_layout.addWidget(QtWidgets.QLabel("Görünüm:"))
        self.cmb_gorunum = QtWidgets.QComboBox()
        self.cmb_gorunum.addItem("Yaklaşan", "yaklasan")
        self.cmb_gorunum.addItem("Günlük Özet", "gunluk")
        self.cmb_gorunum.addItem("Kaçırılanlar", "kacirilan")
        self.cmb_gorunum.addItem("Tümü", "tum")
        self.cmb_gorunum.currentIndexChanged.connect(self.verileri_yukle)
        gorunum_layout.addWidget(self.cmb_gorunum)
        gorunum_layout.addStretch()
        layout.addLayout(gorunum_layout)

        # Tablo oluşturma
        self.tablo = QtWidgets.QTableWidget()
        self.tablo.setColumnCount(4)
        self.tablo.setHorizontalHeaderLabels(["Başlık", "Zaman", "Durum", "Tekrar"])
        self.tablo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tablo.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablo.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.tablo.setAlternatingRowColors(True)
        
        # Stil
        self.tablo.setStyleSheet("""
            QTableWidget {
                gridline-color: #dcdde1;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f5f6fa;
                padding: 4px;
                font-weight: bold;
                border: 1px solid #dcdde1;
            }
        """)

        layout.addWidget(self.tablo)

        # Alt butonlar
        buton_layout = QtWidgets.QHBoxLayout()
        self.btn_yeni = QtWidgets.QPushButton("Yeni Hatırlatıcı")
        self.btn_yeni.clicked.connect(self.yeni_hatirlatici)
        self.btn_duzenle = QtWidgets.QPushButton("Seçileni Düzenle")
        self.btn_duzenle.clicked.connect(self.duzenle_hatirlatici)
        self.btn_toplu_ertele = QtWidgets.QPushButton("Seçilenleri Ertele")
        self.btn_toplu_ertele.clicked.connect(self.toplu_ertele)
        self.btn_toplu_etkinlestir = QtWidgets.QPushButton("Seçilenleri Etkinleştir")
        self.btn_toplu_etkinlestir.clicked.connect(
            lambda: self.toplu_etkinlestir(True)
        )
        self.btn_toplu_devre_disi = QtWidgets.QPushButton(
            "Seçilenleri Devre Dışı Bırak"
        )
        self.btn_toplu_devre_disi.clicked.connect(
            lambda: self.toplu_etkinlestir(False)
        )
        self.btn_kapat = QtWidgets.QPushButton("Kapat")
        self.btn_kapat.clicked.connect(self.accept)
        self.btn_yenile = QtWidgets.QPushButton("Yenile")
        self.btn_yenile.clicked.connect(self.verileri_yukle)
        
        buton_layout.addStretch()
        buton_layout.addWidget(self.btn_yeni)
        buton_layout.addWidget(self.btn_duzenle)
        buton_layout.addWidget(self.btn_toplu_ertele)
        buton_layout.addWidget(self.btn_toplu_etkinlestir)
        buton_layout.addWidget(self.btn_toplu_devre_disi)
        buton_layout.addWidget(self.btn_yenile)
        buton_layout.addWidget(self.btn_kapat)
        layout.addLayout(buton_layout)

    def verileri_yukle(self):
        """Servisten verileri çekip tabloyu doldurur."""
        if self.cmb_gorunum.currentData() == "yaklasan":
            hatirlaticilar = self.servis.yaklasan_hatirlaticilari_al()
            self.setWindowTitle("Yaklaşan Hatırlatıcılar")
        elif self.cmb_gorunum.currentData() == "gunluk":
            hatirlaticilar = self.servis.gunluk_hatirlaticilari_al()
            self.setWindowTitle("Günlük Hatırlatıcı Özeti")
        elif self.cmb_gorunum.currentData() == "kacirilan":
            hatirlaticilar = self.servis.kacirilan_hatirlaticilari_al()
            self.setWindowTitle("Kaçırılan Hatırlatıcılar")
        else:
            hatirlaticilar = self.servis.hatirlaticilari_al()
            self.setWindowTitle("Hatırlatıcı Listesi")
        self._gorunum_hatirlaticilari = hatirlaticilar
        self.tablo.setRowCount(len(hatirlaticilar))

        for i, h in enumerate(hatirlaticilar):
            # Başlık
            self.tablo.setItem(i, 0, QtWidgets.QTableWidgetItem(h.baslik))
            
            # Zaman (Erteleme varsa onu göster)
            zaman = h.erteleme_zamani if h.erteleme_zamani else h.hatirlatma_zamani
            zaman_str = zaman.strftime("%d.%m.%Y %H:%M")
            self.tablo.setItem(i, 1, QtWidgets.QTableWidgetItem(zaman_str))
            
            # Durum
            durum_map = {
                HatirlaticiDurumu.AKTIF: "Aktif",
                HatirlaticiDurumu.DEVRE_DISI: "Devre Dışı",
                HatirlaticiDurumu.TAMAMLANDI: "Tamamlandı",
                HatirlaticiDurumu.KACIRILDI: "Kaçırıldı"
            }
            durum_item = QtWidgets.QTableWidgetItem(durum_map.get(h.durum, "Bilinmiyor"))
            if h.durum == HatirlaticiDurumu.AKTIF:
                durum_item.setForeground(QtGui.QColor("#2980b9"))
            elif h.durum == HatirlaticiDurumu.DEVRE_DISI:
                durum_item.setForeground(QtGui.QColor("#7f8c8d"))
            elif h.durum == HatirlaticiDurumu.TAMAMLANDI:
                durum_item.setForeground(QtGui.QColor("#27ae60"))
            
            self.tablo.setItem(i, 2, durum_item)
            
            # Tekrar
            self.tablo.setItem(i, 3, QtWidgets.QTableWidgetItem(h.tekrar_tipi.value))

    def yeni_hatirlatici(self):
        dialog = HatirlaticiOlusturDialog(self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        self.servis.hatirlatici_ekle(dialog.hatirlatici)
        self.verileri_yukle()

    def duzenle_hatirlatici(self):
        secili_satirlar = self.tablo.selectionModel().selectedRows()
        if len(secili_satirlar) != 1:
            QtWidgets.QMessageBox.information(
                self,
                "Hatırlatıcı Düzenle",
                "Lütfen düzenlemek için tek bir hatırlatıcı seçin.",
            )
            return

        satir = secili_satirlar[0].row()
        mevcut = self._gorunum_hatirlaticilari[satir]
        dialog = HatirlaticiOlusturDialog(self, mevcut)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        self.servis.hatirlaticiyi_guncelle(dialog.hatirlatici)
        self.verileri_yukle()

    def toplu_ertele(self):
        """Seçilen aktif hatırlatıcıları aynı süreyle erteler."""
        secili_satirlar = sorted(
            {index.row() for index in self.tablo.selectionModel().selectedRows()}
        )
        if not secili_satirlar:
            QtWidgets.QMessageBox.information(
                self,
                "Toplu Erteleme",
                "Lütfen en az bir hatırlatıcı seçin.",
            )
            return

        dakika, tamam = QtWidgets.QInputDialog.getInt(
            self,
            "Toplu Erteleme",
            "Kaç dakika ertelensin?",
            10,
            1,
            10080,
        )
        if not tamam:
            return

        secilenler = [
            self._gorunum_hatirlaticilari[satir]
            for satir in secili_satirlar
        ]
        ertelenen_sayi = self.servis.hatirlaticilari_ertele(secilenler, dakika)
        self.verileri_yukle()
        QtWidgets.QMessageBox.information(
            self,
            "Toplu Erteleme",
            f"{ertelenen_sayi} hatırlatıcı {dakika} dakika ertelendi.",
        )

    def toplu_etkinlestir(self, etkin):
        """Seçilen aktif veya devre dışı hatırlatıcıların durumunu değiştirir."""
        secili_satirlar = sorted(
            {index.row() for index in self.tablo.selectionModel().selectedRows()}
        )
        if not secili_satirlar:
            QtWidgets.QMessageBox.information(
                self,
                "Hatırlatıcı Durumu",
                "Lütfen en az bir hatırlatıcı seçin.",
            )
            return

        secilenler = [
            self._gorunum_hatirlaticilari[satir]
            for satir in secili_satirlar
        ]
        degisen_sayi = self.servis.hatirlaticilari_etkinlestir(
            secilenler,
            etkin,
        )
        self.verileri_yukle()
        eylem = "etkinleştirildi" if etkin else "devre dışı bırakıldı"
        QtWidgets.QMessageBox.information(
            self,
            "Hatırlatıcı Durumu",
            f"{degisen_sayi} hatırlatıcı {eylem}.",
        )
