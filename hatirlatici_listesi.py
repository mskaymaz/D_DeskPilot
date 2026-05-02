try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from hatirlatici_servisi import HatirlaticiServisi
from hatirlatici_modeli import HatirlaticiDurumu

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

        # Tablo oluşturma
        self.tablo = QtWidgets.QTableWidget()
        self.tablo.setColumnCount(4)
        self.tablo.setHorizontalHeaderLabels(["Başlık", "Zaman", "Durum", "Tekrar"])
        self.tablo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tablo.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
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
        self.btn_kapat = QtWidgets.QPushButton("Kapat")
        self.btn_kapat.clicked.connect(self.accept)
        self.btn_yenile = QtWidgets.QPushButton("Yenile")
        self.btn_yenile.clicked.connect(self.verileri_yukle)
        
        buton_layout.addStretch()
        buton_layout.addWidget(self.btn_yenile)
        buton_layout.addWidget(self.btn_kapat)
        layout.addLayout(buton_layout)

    def verileri_yukle(self):
        """Servisten verileri çekip tabloyu doldurur."""
        hatirlaticilar = self.servis.hatirlaticilari_al()
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
                HatirlaticiDurumu.TAMAMLANDI: "Tamamlandı",
                HatirlaticiDurumu.KACIRILDI: "Kaçırıldı"
            }
            durum_item = QtWidgets.QTableWidgetItem(durum_map.get(h.durum, "Bilinmiyor"))
            if h.durum == HatirlaticiDurumu.AKTIF:
                durum_item.setForeground(QtGui.QColor("#2980b9"))
            elif h.durum == HatirlaticiDurumu.TAMAMLANDI:
                durum_item.setForeground(QtGui.QColor("#27ae60"))
            
            self.tablo.setItem(i, 2, durum_item)
            
            # Tekrar
            self.tablo.setItem(i, 3, QtWidgets.QTableWidgetItem(h.tekrar_tipi.value))