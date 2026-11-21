"""Convierte la lectura de la hoja «Registro de Observaciones» (texto con columnas
separadas por tabulaciones, tal como la devuelve el conector de Microsoft 365)
en datos.json para la página.

Uso: python3 actualizar.py lectura.txt datos.json
"""
import json
import sys
from datetime import datetime, timezone

HOJA = "## Sheet: Registro de Observaciones"


def main(entrada, salida):
    texto = open(entrada, encoding="utf-8").read()
    if HOJA not in texto:
        sys.exit("No se encontró la hoja «Registro de Observaciones»; no se cambia datos.json")
    parte = texto[texto.index(HOJA):]
    for corte in ("\nFormulas:", "\n## Sheet:"):
        i = parte.find(corte, 1)
        if i > 0:
            parte = parte[:i]
    filas = []
    for linea in parte.split("\n"):
        c = [x.strip() for x in linea.split("\t")]
        if not c[0].startswith("OBS-") or len(c) < 12 or not c[5]:
            continue
        c += [""] * (13 - len(c))
        filas.append({
            "id": c[0], "frente": c[1], "sector": c[2], "cuadrante": c[3], "area": c[4],
            "observacion": c[5], "descripcion": c[6], "fecha_registro": c[7][:10],
            "fecha_subsanacion": c[8][:10], "responsable": c[11],
        })
    if not filas:
        sys.exit("La hoja no tiene observaciones; no se cambia datos.json")
    nuevo = {"actualizado": datetime.now(timezone.utc).isoformat(timespec="seconds"), "filas": filas}
    try:
        viejo = json.load(open(salida, encoding="utf-8"))
        if viejo.get("filas") == filas:
            print("SIN_CAMBIOS", len(filas))
            # Igual se refresca la hora para que la página muestre que se revisó.
    except Exception:
        pass
    json.dump(nuevo, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK", len(filas), "observaciones")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
