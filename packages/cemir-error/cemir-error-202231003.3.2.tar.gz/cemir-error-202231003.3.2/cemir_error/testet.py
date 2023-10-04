from ccerror import error_tracking


def bolum_hesapla(a, b):
    return a / b


try:
    sonuc = bolum_hesapla(5, 0)
except Exception as e:
    import sys
    error_tracking(type(e).__name__, sys.exc_info()[2], "de")
