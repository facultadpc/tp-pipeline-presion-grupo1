"""Validación, limpieza, reporte y salida a CSV."""
import csv
import re

from modelo import Paciente

PATRON_CODIGO = re.compile(r"PAC-\d{3}")

RANGOS = {
    "edad": (18, 100),
    "imc": (12, 60),
    "presion_sistolica": (70, 250),
}
GRUPOS_VALIDOS = ("A", "B")


def convertir_numero(valor):
    """Devuelve None si el dato falta; en otro caso float(valor) (puede lanzar ValueError)."""
    if valor is None:
        return None
    if isinstance(valor, str) and valor.strip() == "":
        return None
    return float(valor)


def validar_registro(registro):
    """Devuelve la lista de motivos de rechazo (vacía si el registro es válido)."""
    motivos = []

    codigo = registro.get("codigo")
    if not isinstance(codigo, str) or PATRON_CODIGO.fullmatch(codigo) is None:
        motivos.append("código con formato inválido")

    for campo, (minimo, maximo) in RANGOS.items():
        try:
            numero = convertir_numero(registro.get(campo))
        except (ValueError, TypeError):
            motivos.append(f"{campo} no numérico")
            continue
        if numero is None:
            motivos.append(f"{campo} faltante")
        elif not minimo <= numero <= maximo:
            motivos.append(f"{campo} fuera de rango")

    if registro.get("grupo") not in GRUPOS_VALIDOS:
        motivos.append("grupo inválido")

    return motivos


def limpiar(registros):
    """Devuelve (validos, rechazos). Conserva la primera aparición de cada código."""
    validos = []
    rechazos = []
    codigos_aceptados = set()

    for fila, registro in enumerate(registros, start=1):
        motivos = validar_registro(registro)
        codigo = registro.get("codigo")
        if not motivos and codigo in codigos_aceptados:
            motivos.append("código duplicado")

        if motivos:
            rechazos.append({"fila": fila, "codigo": codigo, "motivo": "; ".join(motivos)})
            continue

        codigos_aceptados.add(codigo)
        validos.append(Paciente(
            codigo,
            convertir_numero(registro["edad"]),
            convertir_numero(registro["imc"]),
            convertir_numero(registro["presion_sistolica"]),
            registro["grupo"],
        ))

    return validos, rechazos


def generar_reporte(pacientes):
    """Una fila por grupo, ordenada por grupo, sin dividir por cero."""
    reporte = []
    for grupo in GRUPOS_VALIDOS:
        del_grupo = [p for p in pacientes if p.grupo == grupo]
        cantidad = len(del_grupo)
        if cantidad:
            presion_media = round(sum(p.presion for p in del_grupo) / cantidad, 2)
            proporcion = round(sum(p.es_hipertenso() for p in del_grupo) / cantidad, 3)
        else:
            presion_media = 0.0
            proporcion = 0.0
        reporte.append({
            "grupo": grupo,
            "cantidad": cantidad,
            "presion_media": presion_media,
            "proporcion_hipertensos": proporcion,
        })
    return reporte


def guardar_csv(filas, ruta):
    """Guarda una lista de diccionarios; los encabezados son las claves del primero."""
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)
