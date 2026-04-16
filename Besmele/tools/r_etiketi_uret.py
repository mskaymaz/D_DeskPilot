from datetime import datetime


def r_etiketi_uret():
    """r_etiketi: teslim ve build icin kanonik R.yymmdd_hhmm etiketi uretir."""
    return datetime.now().astimezone().strftime("R.%y%m%d_%H%M")
