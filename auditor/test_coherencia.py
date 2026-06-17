"""Pruebas del verificador, incluido el CONTROL NEGATIVO.

El control negativo es esencial: introduce a proposito una incoherencia y
comprueba que el verificador la detecta. Si no saltara, no sabriamos si el
guardarrail sigue vivo.

Se puede ejecutar con pytest o como script:  python auditor/test_coherencia.py
"""
from decimal import Decimal

from coherencia import cargar_libro, cargar_resumen, verificar


def test_datos_limpios_dan_sano():
    resultado = verificar(cargar_libro(), cargar_resumen())
    assert resultado["veredicto"] == "SANO"
    assert all(r["ok"] for r in resultado["invariantes"])


def test_control_negativo_resumen_manipulado():
    # El libro queda intacto: cada asiento cuadra y el total global cuadra.
    # Solo manipulamos el RESUMEN derivado (una "capa" distinta del sistema).
    libro = cargar_libro()
    resumen = cargar_resumen()
    primera_cuenta = next(iter(resumen))
    resumen[primera_cuenta] = resumen[primera_cuenta] + Decimal("100.00")  # incoherencia plantada

    resultado = verificar(libro, resumen)
    inv = {r["id"]: r for r in resultado["invariantes"]}

    # INV-1 e INV-2 siguen en verde: el libro no se ha tocado.
    assert inv["INV-1"]["ok"] is True
    assert inv["INV-2"]["ok"] is True
    # ...pero INV-3 detecta que el resumen ya no corresponde con el libro.
    assert inv["INV-3"]["ok"] is False
    assert resultado["veredicto"] == "ENFERMO"


if __name__ == "__main__":
    test_datos_limpios_dan_sano()
    test_control_negativo_resumen_manipulado()
    print("OK - las 2 pruebas pasan (datos limpios = SANO; control negativo detectado).")
