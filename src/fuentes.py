"""Fuentes de datos: interfaz común y sus implementaciones para CSV y JSON."""
import csv
import json
from abc import ABC, abstractmethod


class FuenteDatos(ABC):
    """Interfaz común: toda fuente devuelve una lista de diccionarios."""

    @abstractmethod
    def cargar(self, ruta):
        """Lee el archivo y devuelve una lista de diccionarios (uno por registro)."""


class FuenteCSV(FuenteDatos):
    """Lee un CSV; todos los valores quedan como texto y lo faltante es ''."""

    def cargar(self, ruta):
        with open(ruta, encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))


class FuenteJSON(FuenteDatos):
    """Lee un JSON cuyo contenido debe ser una lista de registros."""

    def cargar(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        if not isinstance(contenido, list):
            raise ValueError(
                f"El JSON debe contener una lista de registros y contiene {type(contenido).__name__}"
            )
        return contenido
