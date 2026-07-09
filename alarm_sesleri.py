try:
    import winsound
except ImportError:
    winsound = None


def alarm_sesini_cal(ses_tipi: str) -> bool:
    if winsound is None:
        return False

    if ses_tipi == "Kısa zil":
        winsound.Beep(1100, 120)
        winsound.Beep(1400, 120)
        return True

    if ses_tipi == "Yumuşak zil":
        winsound.Beep(660, 220)
        winsound.Beep(880, 260)
        return True

    winsound.MessageBeep(winsound.MB_OK)
    return True
