import sys
try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

try:
    import ctypes
except Exception:
    ctypes = None

def ekrani_bul(isim: str) -> QtGui.QScreen:
    """Verilen isme sahip ekranı bulur, bulamazsa ana ekranı döner."""
    app = QtWidgets.QApplication.instance()
    if isim:
        for screen in app.screens():
            if screen.name() == isim:
                return screen
    return app.primaryScreen()

def pencereyi_guvenli_tas(pencere, ayarlar, ekran_adi: str = ""):
    """Pencereyi ekran sınırları içerisinde güvenli bir konuma taşır. Task 7.2: Monitör kontrolü."""
    app = QtWidgets.QApplication.instance()
    ekran = ekrani_bul(ekran_adi or getattr(ayarlar, "grup_ekran_adi", ""))
    alan = ekran.availableGeometry()

    pencere.adjustSize()
    genislik, yukseklik = pencere.width(), pencere.height()

    x, y = ayarlar.pos_x, ayarlar.pos_y

    if not alan.contains(QtCore.QPoint(x, y)):
        x = alan.left() + (alan.width() - genislik) // 2
        y = alan.top() + (alan.height() - yukseklik) // 2
        ayarlar.pos_x = x
        ayarlar.pos_y = y

    pencere.move(x, y)

def en_ustte_tut(pencere):
    """Windows üzerinde pencereyi her zaman en üstte tutmaya zorlar."""
    if sys.platform != "win32" or not ctypes:
        return
    try:
        hwnd = int(pencere.winId())
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOACTIVATE = 0x0010
        SWP_SHOWWINDOW = 0x0040
        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_TOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW,
        )
    except Exception:
        pass

def gorev_cubugu_bantlarini_al(ekran):
    """Ekrandaki görev çubuğu alanlarını hesaplar."""
    if not ekran:
        return []
    tam_alan = ekran.geometry()
    kullanilabilir_alan = ekran.availableGeometry()
    bantlar = []

    ust_h = kullanilabilir_alan.top() - tam_alan.top()
    if ust_h > 0:
        bantlar.append(QtCore.QRect(tam_alan.left(), tam_alan.top(), tam_alan.width(), ust_h))

    alt_h = tam_alan.bottom() - kullanilabilir_alan.bottom()
    if alt_h > 0:
        bantlar.append(QtCore.QRect(tam_alan.left(), kullanilabilir_alan.bottom() + 1, tam_alan.width(), alt_h))

    sol_w = kullanilabilir_alan.left() - tam_alan.left()
    if sol_w > 0:
        bantlar.append(QtCore.QRect(tam_alan.left(), tam_alan.top(), sol_w, tam_alan.height()))

    sag_w = tam_alan.right() - kullanilabilir_alan.right()
    if sag_w > 0:
        bantlar.append(QtCore.QRect(kullanilabilir_alan.right() + 1, tam_alan.top(), sag_w, tam_alan.height()))

    return bantlar

def pencere_gorev_cubugunda_mi(pencere):
    """Pencerenin herhangi bir görev çubuğu bandı üzerinde olup olmadığını kontrol eder."""
    app = QtWidgets.QApplication.instance()
    ekran = app.screenAt(pencere.frameGeometry().center()) or app.primaryScreen()
    if not ekran:
        return False
    
    pencere_geometrisi = pencere.frameGeometry()
    for bant in gorev_cubugu_bantlarini_al(ekran):
        if pencere_geometrisi.intersects(bant):
            return True
    return False