```python
from cemir_error.ccerror import error_tracking

def bolum_hesapla(a, b):
    return a / b


try:
    sonuc = bolum_hesapla(5, 0)
except Exception as e:
    import sys
    error_tracking(e, sys, "de")


```

![Örnek Çıktı](https://raw.githubusercontent.com/muslu/cemir_error/main/output.png)

[](https://)
