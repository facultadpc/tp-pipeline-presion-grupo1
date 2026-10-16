# Pipeline de control de presión arterial

**Integrantes:** Fernandez Santiago Manuel, Martinez Teo, Playa Tomas

## Problema y usuario
Un equipo de salud recibe mediciones de presión arterial en CSV y JSON con errores de carga.
El programa descarta los registros inválidos, informa el motivo de cada rechazo y resume
la presión sistólica por grupo del estudio.

## Datos
Ver `data/README.md`. Cada fila corresponde a un paciente con una medición.

## Estructura
- `src/fuentes.py`: `FuenteDatos` (abstracta), `FuenteCSV` y `FuenteJSON`.
- `src/modelo.py`: clase `Paciente`.
- `src/pipeline.py`: validación, limpieza, reporte y guardado en CSV.
- `src/main.py`: punto de entrada.
- `tests/test_pipeline.py`: pruebas automáticas.

## Ejecución
No requiere bibliotecas externas (Python 3.10 o superior).
```bash
python src/main.py data/mediciones.csv
```
Genera `outputs/reporte.csv` y `outputs/rechazos.csv`.

## Pruebas
```bash
python tests/test_pipeline.py
```

## Reglas de limpieza
- Código con formato `PAC-` y tres dígitos (expresión regular `PAC-\d{3}`, validada con `fullmatch`).
- Edad entre 18 y 100, IMC entre 12 y 60, presión sistólica entre 70 y 250 (extremos incluidos).
- Grupos admitidos: `A` y `B`.
- Faltantes (cadena vacía en CSV, `null` en JSON) y valores no numéricos se rechazan con su motivo.
- Duplicados: se conserva la primera aparición de cada código y las siguientes se rechazan.
- Cada rechazo registra fila (contando desde 1), código y motivo(s).

## Resultado de ejemplo
```
Leídos: 58 | válidos: 50 | rechazados: 8
{'grupo': 'A', 'cantidad': 27, 'presion_media': 127.26, 'proporcion_hipertensos': 0.185}
{'grupo': 'B', 'cantidad': 23, 'presion_media': 118.61, 'proporcion_hipertensos': 0.13}
```

## Limitaciones
- Datos simulados con fines didácticos (50 pacientes válidos).
- El umbral de hipertensión (140 mmHg) es un criterio simplificado, no un diagnóstico clínico.
- `main.py` lee solo CSV; la fuente JSON está implementada y probada pero no se elige desde la línea de comandos.
- La expresión regular valida el formato del código, no que el paciente exista.
