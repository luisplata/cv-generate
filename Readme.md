## Requisitos
- Python 3.10+
- pdflatex (LaTeX) disponible en la ruta

## Instalacion rapida
1. Crear entorno: `python -m venv venv`
2. Activar entorno: `source venv/Scripts/activate` (Windows PowerShell/CMD) o `source venv/bin/activate` (Linux/macOS)
3. Instalar dependencias: `pip install -r requirements.txt`

## Estructura de datos
- Datos base: `data/master/master.yaml`
- Ofertas/variantes: archivos `.yaml` en `data/offers/` (uno por oferta)
- Plantilla LaTeX: `templates/ats.tex`

## Uso
1. Asegurate de tener los YAML completos en `data/master/` y `data/offers/`.
2. Ejecuta el generador: `python generate.py`
3. Los PDFs se guardan en `build/<nombre_oferta>/<nombre_oferta>.pdf`.

## Crear una nueva oferta
1. Copia un YAML existente en `data/offers/` y renombralo (ejemplo: `MiOferta.yaml`).
2. Ajusta `profile` y `focus` dentro del YAML para reflejar el rol.
3. Vuelve a correr `python generate.py` para generar el PDF.