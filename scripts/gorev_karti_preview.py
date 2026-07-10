from datetime import datetime, timedelta

try:
    from PySide6 import QtWidgets
except ImportError:
    from PyQt6 import QtWidgets

from kart import GorevKarti
from gorev_modeli import GorevModeli, GorevOnceligi


def main():
    app = QtWidgets.QApplication([])
    pencere = QtWidgets.QWidget()
    pencere.setWindowTitle("Görev Kartı Önizleme")
    pencere.resize(620, 260)

    layout = QtWidgets.QVBoxLayout(pencere)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(1)

    ornekler = [
        GorevModeli("Bugünkü Todo kart tasarımını test et", GorevOnceligi.YUKSEK, bitis_tarihi=datetime.now() + timedelta(hours=3)),
        GorevModeli("Tema altyapısını gözden geçir", GorevOnceligi.NORMAL, bitis_tarihi=datetime.now() + timedelta(days=1)),
        GorevModeli("Reminder için ortak kart kararlarını not al", GorevOnceligi.DUSUK),
    ]

    for gorev in ornekler:
        kart = GorevKarti(gorev)
        kart.durum_degisti.connect(lambda g, d: print(f"Durum: {g.baslik} -> {d}"))
        kart.sil_istendi.connect(lambda g: print(f"Sil: {g.baslik}"))
        layout.addWidget(kart)

    layout.addStretch()
    pencere.show()
    app.exec()


if __name__ == "__main__":
    main()
