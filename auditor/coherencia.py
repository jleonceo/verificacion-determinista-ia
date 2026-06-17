"""Verificador de coherencia determinista — versión genérica de demostración.

Recomprueba la coherencia de un libro contable de doble partida SIN usar IA:
solo aritmética. Por eso da siempre la misma respuesta, sea cual sea el modelo
de IA que haya generado o manipulado los datos, y es inmune al "cambio de modelo".

No depende de ninguna base de datos ni de datos reales: lee dos CSV de ejemplo.
"""
from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIBRO = RAIZ / "datos_ejemplo" / "libro_sintetico.csv"
RESUMEN = RAIZ / "datos_ejemplo" / "resumen_por_cuenta.csv"


def cargar_libro(ruta: Path = LIBRO) -> list[dict]:
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for fila in filas:
        fila["debe"] = Decimal(fila["debe"])
        fila["haber"] = Decimal(fila["haber"])
    return filas


def cargar_resumen(ruta: Path = RESUMEN) -> dict[str, Decimal]:
    with open(ruta, encoding="utf-8") as f:
        return {fila["cuenta"]: Decimal(fila["saldo"]) for fila in csv.DictReader(f)}


def verificar(libro: list[dict], resumen: dict[str, Decimal]) -> dict:
    """Devuelve {'invariantes': [...], 'veredicto': 'SANO' | 'ENFERMO'}."""
    resultados = []

    # INV-1 - Cuadre global: el total del debe es igual al total del haber.
    debe = sum((f["debe"] for f in libro), Decimal("0"))
    haber = sum((f["haber"] for f in libro), Decimal("0"))
    resultados.append({
        "id": "INV-1",
        "nombre": "Cuadre global (total del debe = total del haber)",
        "ok": debe == haber,
        "detalle": f"debe={debe}  haber={haber}  diferencia={debe - haber}",
    })

    # INV-2 - Cuadre por asiento: cada asiento cuadra por si mismo.
    descuadrados = []
    for a in sorted({f["asiento"] for f in libro}):
        d = sum((f["debe"] for f in libro if f["asiento"] == a), Decimal("0"))
        h = sum((f["haber"] for f in libro if f["asiento"] == a), Decimal("0"))
        if d != h:
            descuadrados.append(f"asiento {a} (debe={d}, haber={h})")
    resultados.append({
        "id": "INV-2",
        "nombre": "Cuadre por asiento (cada asiento cuadra solo)",
        "ok": not descuadrados,
        "detalle": "todos los asientos cuadran" if not descuadrados else "; ".join(descuadrados),
    })

    # INV-3 - Coherencia entre capas: el resumen por cuenta coincide con
    # recalcular el saldo desde el libro. Esta es la clave: un libro puede
    # cuadrar consigo mismo (INV-1 e INV-2 en verde) y AUN ASI el resumen
    # derivado no corresponder con sus datos de origen.
    saldos_reales: dict[str, Decimal] = {}
    for f in libro:
        saldos_reales[f["cuenta"]] = saldos_reales.get(f["cuenta"], Decimal("0")) + f["debe"] - f["haber"]
    incoherencias = []
    for c in sorted(set(saldos_reales) | set(resumen)):
        real = saldos_reales.get(c, Decimal("0"))
        declarado = resumen.get(c, Decimal("0"))
        if real != declarado:
            incoherencias.append(f"cuenta {c} (resumen={declarado}, real={real})")
    resultados.append({
        "id": "INV-3",
        "nombre": "Coherencia entre capas (resumen = recalculo desde el libro)",
        "ok": not incoherencias,
        "detalle": "el resumen corresponde con el libro" if not incoherencias else "; ".join(incoherencias),
    })

    veredicto = "SANO" if all(r["ok"] for r in resultados) else "ENFERMO"
    return {"invariantes": resultados, "veredicto": veredicto}


def informe(resultado: dict) -> str:
    lineas = ["Verificador de coherencia determinista (sin IA)", "=" * 50]
    for r in resultado["invariantes"]:
        marca = "OK   " if r["ok"] else "FALLA"
        lineas.append(f"[{marca}] {r['id']} - {r['nombre']}")
        lineas.append(f"         {r['detalle']}")
    lineas.append("-" * 50)
    lineas.append(f"VEREDICTO: {resultado['veredicto']}")
    return "\n".join(lineas)


def main() -> int:
    resultado = verificar(cargar_libro(), cargar_resumen())
    print(informe(resultado))
    return 0 if resultado["veredicto"] == "SANO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
