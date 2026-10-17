"""Clase del dominio: un paciente ya validado."""


class Paciente:
    """Registro validado: atributos numericos float y grupo 'A' o 'B'."""

    UMBRAL_HIPERTENSION = 140  # mmHg; criterio didáctico simplificado, no es diagnóstico

    def __init__(self, codigo, edad, imc, presion, grupo):
        self.codigo = codigo
        self.edad = edad
        self.imc = imc
        self.presion = presion
        self.grupo = grupo

    def franja_etaria(self):
        if self.edad < 40:
            return "18-39"
        if self.edad < 60:
            return "40-59"
        return "60+"

    def es_hipertenso(self):
        return self.presion >= self.UMBRAL_HIPERTENSION

    def __str__(self):
        return (f"{self.codigo} | grupo {self.grupo} | {self.edad:g} años | "
                f"PAS {self.presion:g} mmHg")
