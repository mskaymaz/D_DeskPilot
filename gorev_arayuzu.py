try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from gorev_servisi import GorevServisi
from gorev_modeli import GorevModeli, GorevOnceligi

class GorevArayuzuDialog(QtWidgets.QDialog):
    """
    Görevlerin (TODO) yönetildiği modern arayüz penceresi.
    Task 5.3 kapsamında oluşturulmuştur.
    """
    def __init__(self, servis: GorevServisi, parent=None):
        super().__init__(parent)
        self.servis = servis
        self.setWindowTitle("Görevlerim")
        self.setMinimumSize(450, 500)
        self._arayuz_kur()
        self.verileri_yukle()

    def _arayuz_kur(self):
        layout = QtWidgets.QVBoxLayout(self)

        # --- Üst Kısım: Yeni Görev Ekleme ---
        ekle_grubu = QtWidgets.QGroupBox("Yeni Görev Ekle")
        ekle_layout = QtWidgets.QHBoxLayout(ekle_grubu)

        self.txt_yeni_gorev = QtWidgets.QLineEdit()
        self.txt_yeni_gorev.setPlaceholderText("Yapılacak işi yazın...")
        self.txt_yeni_gorev.returnPressed.connect(self.gorev_ekle)

        self.cmb_oncelik = QtWidgets.QComboBox()
        self.cmb_oncelik.addItem("Düşük", GorevOnceligi.DUSUK)
        self.cmb_oncelik.addItem("Normal", GorevOnceligi.NORMAL)
        self.cmb_oncelik.addItem("Yüksek", GorevOnceligi.YUKSEK)
        self.cmb_oncelik.setCurrentIndex(1)

        self.btn_ekle = QtWidgets.QPushButton("Ekle")
        self.btn_ekle.clicked.connect(self.gorev_ekle)
        self.btn_ekle.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")

        ekle_layout.addWidget(self.txt_yeni_gorev, 4)
        ekle_layout.addWidget(self.cmb_oncelik, 1)
        ekle_layout.addWidget(self.btn_ekle, 1)
        layout.addWidget(ekle_grubu)

        # --- Orta Kısım: Liste ---
        self.tablo = QtWidgets.QTableWidget()
        self.tablo.setColumnCount(3)
        self.tablo.setHorizontalHeaderLabels(["Durum", "Görev", "İşlem"])
        self.tablo.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tablo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        
        # Stil
        self.tablo.setStyleSheet("""
            QTableWidget { gridline-color: #f1f2f6; border: none; }
            QHeaderView::section { background-color: #f1f2f6; padding: 4px; border: none; font-weight: bold; }
        """)
        
        layout.addWidget(self.tablo)

        # --- Alt Kısım ---
        alt_layout = QtWidgets.QHBoxLayout()
        self.btn_kapat = QtWidgets.QPushButton("Kapat")
        self.btn_kapat.clicked.connect(self.accept)
        alt_layout.addStretch()
        alt_layout.addWidget(self.btn_kapat)
        layout.addLayout(alt_layout)

    def verileri_yukle(self):
        """Görevleri servisten çekip tabloya doldurur."""
        gorevler = self.servis.gorevleri_sirali_al()
        self.tablo.setRowCount(len(gorevler))

        for i, g in enumerate(gorevler):
            # 1. Durum (Checkbox)
            cb = QtWidgets.QCheckBox()
            cb.setChecked(g.tamamlandi)
            cb.toggled.connect(lambda checked, item=g: self.durum_degistir(item, checked))
            hucre_cb = QtWidgets.QWidget()
            hucre_cb_layout = QtWidgets.QHBoxLayout(hucre_cb)
            hucre_cb_layout.addWidget(cb)
            hucre_cb_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            hucre_cb_layout.setContentsMargins(0, 0, 0, 0)
            self.tablo.setCellWidget(i, 0, hucre_cb)

            # 2. Başlık ve Öncelik İpucu
            baslik_item = QtWidgets.QTableWidgetItem(g.baslik)
            if g.tamamlandi:
                font = baslik_item.font()
                font.setStrikeOut(True)
                baslik_item.setFont(font)
                baslik_item.setForeground(QtGui.QColor("#bdc3c7"))
            
            # Öncelik rengi
            if g.oncelik == GorevOnceligi.YUKSEK:
                baslik_item.setToolTip("Yüksek Öncelik")
                baslik_item.setBackground(QtGui.QColor("#ffeaa7"))

            self.tablo.setItem(i, 1, baslik_item)

            # 3. Sil Butonu
            btn_sil = QtWidgets.QPushButton("Sil")
            btn_sil.setFixedWidth(50)
            btn_sil.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 3px;")
            btn_sil.clicked.connect(lambda _, item=g: self.gorev_sil(item))
            hucre_sil = QtWidgets.QWidget()
            hucre_sil_layout = QtWidgets.QHBoxLayout(hucre_sil)
            hucre_sil_layout.addWidget(btn_sil)
            hucre_sil_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            hucre_sil_layout.setContentsMargins(0, 0, 0, 0)
            self.tablo.setCellWidget(i, 2, hucre_sil)

    def gorev_ekle(self):
        baslik = self.txt_yeni_gorev.text().strip()
        if not baslik:
            return
        
        oncelik = self.cmb_oncelik.currentData()
        yeni_gorev = GorevModeli(baslik=baslik, oncelik=oncelik)
        self.servis.gorev_ekle(yeni_gorev)
        
        self.txt_yeni_gorev.clear()
        self.verileri_yukle()

    def durum_degistir(self, gorev, durum):
        gorev.tamamlandi = durum
        self.servis.kaydet()
        self.verileri_yukle()

    def gorev_sil(self, gorev):
        # Liste üzerinden silme işlemi
        gorevler = self.servis.gorevleri_al()
        if gorev in gorevler:
            gorevler.remove(gorev)
            self.servis.kaydet()
            self.verileri_yukle()