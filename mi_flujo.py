"""Flujo de exportaciones por producto: extrae, valida y guarda con fecha. (una linea que diga que hace).
Integrantes: Esteban Vizuete
Fuente: datos/exportaciones.csv (datos SINTETICOS de clase)
SI FALLA: si el CSV no llega o cambia el numero de filas o el total, el flujo se detiene con ERROR en flujo.log y codigo de salida 1; avisar al analista de datos del BCE o al responsable de la fuente (que pasa si la fuente no llega o cambia, y A QUIEN habria que avisar)"""
import logging, sys
from datetime import date
import pandas as pd

# ---------- 1 · PARAMETROS (todo lo que puede cambiar, junto y arriba) ----------
RUTA_ENTRADA    = "datos/exportaciones.csv"
SALIDA          = f"salida/mi_flujo_{date.today().isoformat()}.csv"
FILAS_ESPERADAS = 6
TOTAL_ESPERADO  = 8679.13
# agregue aqui otro parametro de comprobacion, por ejemplo un total esperado

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("flujo.log"), logging.StreamHandler()])
log = logging.getLogger("mi_flujo")

# ---------- 2 · LAS TRES FUNCIONES (cada una con su docstring) ----------
def extraer():
    """Lee el CSV de entrada y devuelve la tabla."""
    tabla = pd.read_csv(RUTA_ENTRADA)
    log.info("extraidas %d filas", len(tabla))
    return tabla

def transformar(tabla):
    """Valida numero de filas y total, y agrega la participacion porcentual."""
    if len(tabla) != FILAS_ESPERADAS:
        raise ValueError(f"esperaba {FILAS_ESPERADAS} filas y llegaron {len(tabla)}")
    total = round(tabla["monto_mm_usd"].sum(), 2)
    if abs(total - TOTAL_ESPERADO) > 0.01:
        raise ValueError(f"el total cambio: esperaba {TOTAL_ESPERADO} y salio {total}")
    tabla["participacion_pct"] = (tabla["monto_mm_usd"] / total * 100).round(2)
    return tabla

def cargar(tabla):
    """Guarda la tabla en salida/ con la fecha del corte en el nombre."""
    import os; os.makedirs("salida", exist_ok=True)
    tabla.to_csv(SALIDA, index=False)
    log.info("guardado %s (%d filas)", SALIDA, len(tabla))

# ---------- 3 · LA LOGICA, EN ORDEN ----------
if __name__ == "__main__":
    try:
        cargar(transformar(extraer())); log.info("FIN OK")
    except Exception as error:
        log.error("EL FLUJO FALLO: %s", error); sys.exit(1)
