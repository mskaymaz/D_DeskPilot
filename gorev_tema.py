from dataclasses import dataclass


@dataclass(frozen=True)
class GorevTema:
    """Todo paneli için sade, yerel ve değiştirilebilir tema modeli."""

    panel_rengi: str = "#f6f8fb"
    kart_rengi: str = "#ffffff"
    metin_rengi: str = "#1f2933"
    ikincil_metin_rengi: str = "#64748b"
    vurgu_rengi: str = "#3b82f6"
    kenarlik_rengi: str = "#d8e0ea"
    tamamlandi_rengi: str = "#94a3b8"
    yuksek_oncelik_rengi: str = "#f97316"
    normal_oncelik_rengi: str = "#3b82f6"
    dusuk_oncelik_rengi: str = "#22c55e"

    def panel_stili(self) -> str:
        return f"""
            QWidget {{
                background-color: {self.panel_rengi};
                color: {self.metin_rengi};
            }}
        """

    def kart_stili(self) -> str:
        return f"""
            QFrame {{
                background-color: {self.kart_rengi};
                border: 1px solid {self.kenarlik_rengi};
                border-radius: 14px;
            }}
        """

    def buton_stili(self) -> str:
        return f"""
            QPushButton {{
                background-color: {self.vurgu_rengi};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 7px 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.92;
            }}
        """

    def sil_buton_stili(self) -> str:
        return """
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                font-weight: bold;
            }
        """


VARSAYILAN_GOREV_TEMASI = GorevTema()
