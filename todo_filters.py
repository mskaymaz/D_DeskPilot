from datetime import datetime, timedelta


def todo_ayar_degeri(settings, alan, varsayilan):
    try:
        return max(0, int(getattr(settings, alan, varsayilan)))
    except (TypeError, ValueError):
        return varsayilan


def _durum_suresi_icinde_mi(zaman, settings, alan, varsayilan):
    if not zaman:
        return True
    return datetime.now() - zaman <= timedelta(days=todo_ayar_degeri(settings, alan, varsayilan))


def _varsayilan_listede_gorunur_mu(gorev, settings):
    if gorev.tamamlandi:
        zaman = gorev.tamamlanma_zamani or gorev.olusturulma_zamani
        return _durum_suresi_icinde_mi(zaman, settings, "todo_completed_visible_days", 7)
    if gorev.iptal_edildi:
        zaman = gorev.iptal_zamani or gorev.olusturulma_zamani
        return _durum_suresi_icinde_mi(zaman, settings, "todo_cancelled_visible_days", 7)
    return True


def filtrelenmis_gorevleri_al(gorevler, filtre, settings):
    gorevler = list(gorevler)
    bugun = datetime.now().date()
    yarin = bugun + timedelta(days=1)
    hafta_sonu = bugun + timedelta(days=7)

    if filtre == "date":
        gorevler = [g for g in gorevler if not g.cope_atildi]
        return sorted(
            gorevler,
            key=lambda g: (
                0 if g.bitis_tarihi else 1,
                g.bitis_tarihi or g.olusturulma_zamani,
                g.sira,
            ),
        )
    if filtre == "today":
        return [
            g for g in gorevler
            if g.bitis_tarihi and g.bitis_tarihi.date() == bugun
            and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi
        ]
    if filtre == "tomorrow":
        return [
            g for g in gorevler
            if g.bitis_tarihi and g.bitis_tarihi.date() == yarin
            and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi
        ]
    if filtre == "week":
        return [
            g for g in gorevler
            if g.bitis_tarihi and bugun <= g.bitis_tarihi.date() <= hafta_sonu
            and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi
        ]
    if filtre == "no_date":
        return [
            g for g in gorevler
            if not g.bitis_tarihi and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi
        ]
    if filtre == "overdue":
        return [g for g in gorevler if g.suresi_gecti_mi() and not g.cope_atildi]
    if filtre == "completed":
        return [g for g in gorevler if g.tamamlandi and not g.cope_atildi]
    if filtre == "cancelled":
        return [g for g in gorevler if g.iptal_edildi and not g.cope_atildi]
    if filtre == "trash":
        return [g for g in gorevler if g.cope_atildi]
    return [
        g for g in gorevler
        if not g.cope_atildi and _varsayilan_listede_gorunur_mu(g, settings)
    ]
