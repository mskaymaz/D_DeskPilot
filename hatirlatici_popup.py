from datetime import datetime, timedelta
try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from hatirlatici_modeli import HatirlaticiModeli, HatirlaticiDurumu
from utils import resource_path, ICON_FILE

class HatirlaticiBildirimPenceresi(QtWidgets.QWidget):
    """
    Zamanı gelen hatırlatıcılar için modern, çerçevesiz açılır pencere.
    Task 4.4 kapsamında oluşturulmuştur.
    """
    tamamlandi_sinyali = QtCore.Signal(str) # Hatırlatıcı ID
    ertelendi_sinyali = QtCore.Signal(str, int) # Hatırlatıcı ID, Dakika

    def __init__(self, hatirlatici: HatirlaticiModeli, parent=None):
        super().__init__(parent, QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.Tool)
        self.hatirlatici = hatirlatici
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self._arayuz_kur()
        self._konumlandir()

    def _arayuz_kur(self):
        # Ana gövde stili
        self.govde = QtWidgets.QFrame(self)
        self.govde.setObjectName("Govde")
        self.govde.setStyleSheet("""
            #Govde {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 12px;
            }
            QLabel { color: white; font-family: 'Segoe UI'; }
            QPushButton {
                background-color: #34495e;
                color: white;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1abc9c; }
            #Baslik { font-size: 16px; font-weight: bold; color: #1abc9c; }
            #Aciklama { font-size: 13px; color: #bdc3c7; }
        """)

        layout = QtWidgets.QVBoxLayout(self.govde)
        
        # Başlık ve Açıklama
        self.lbl_baslik = QtWidgets.QLabel(self.hatirlatici.baslik)
        self.lbl_baslik.setObjectName("Baslik")
        self.lbl_baslik.setWordWrap(True)
        
        self.lbl_aciklama = QtWidgets.QLabel(self.hatirlatici.aciklama if self.hatirlatici.aciklama else "Hatırlatıcı zamanı geldi!")
        self.lbl_aciklama.setObjectName("Aciklama")
        self.lbl_aciklama.setWordWrap(True)

        layout.addWidget(self.lbl_baslik)
        layout.addWidget(self.lbl_aciklama)
        layout.addSpacing(10)

        # Butonlar
        buton_layout = QtWidgets.QGridLayout()
        
        self.btn_tamamla = QtWidgets.QPushButton("Tamamla")
        self.btn_tamamla.clicked.connect(self._tamamla_tiklandi)
        
        self.btn_ertele_5 = QtWidgets.QPushButton("5 Dk Ertele")
        self.btn_ertele_5.clicked.connect(lambda: self._ertele_tiklandi(5))
        
        self.btn_ertele_10 = QtWidgets.QPushButton("10 Dk Ertele")
        self.btn_ertele_10.clicked.connect(lambda: self._ertele_tiklandi(10))
        
        self.btn_ertele_60 = QtWidgets.QPushButton("1 Saat Ertele")
        self.btn_ertele_60.clicked.connect(lambda: self._ertele_tiklandi(60))

        buton_layout.addWidget(self.btn_tamamla, 0, 0, 1, 2)
        buton_layout.addWidget(self.btn_ertele_5, 1, 0)
        buton_layout.addWidget(self.btn_ertele_10, 1, 1)
        buton_layout.addWidget(self.btn_ertele_60, 2, 0, 1, 2)

        layout.addLayout(buton_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.govde)
        self.setFixedSize(300, 220)

    def _konumlandir(self):
        # Ekranın sağ alt köşesine konumlandır
        ekran = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        x = ekran.right() - self.width() - 20
        y = ekran.bottom() - self.height() - 20
        self.move(x, y)

    def _tamamla_tiklandi(self):
        self.tamamlandi_sinyali.emit(self.hatirlatici.id)
        self.close()

    def _ertele_tiklandi(self, dakika):
        self.ertelendi_sinyali.emit(self.hatirlatici.id, dakika)
        self.close()