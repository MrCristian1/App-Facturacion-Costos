# App Facturación - Automatización de Centros de Costo

## Descripción

Aplicación en Python para automatizar el proceso de añadir centros de costo a PDFs de facturación electrónica mediante búsqueda en base de datos Excel.

## Características

- Extracción automática de datos de empleados desde PDFs
- Búsqueda de centros de costo en bases de datos Excel
- Generación de tabla consolidada
- Inserción automática en el PDF original

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python main.py
```

## Uso

1. Ejecutar el script principal
2. Seleccionar el PDF de facturación
3. Seleccionar el archivo Excel con la base de empleados
4. El sistema generará automáticamente un PDF con los centros de costo añadidos

## Estructura del proyecto

```
App Facturacion/
├── src/
│   ├── pdf_extractor.py      # Extracción de datos del PDF
│   ├── excel_processor.py    # Procesamiento de datos Excel
│   ├── data_matcher.py       # Lógica de matching
│   ├── pdf_generator.py      # Generación de PDF
│   └── ui.py                 # Interfaz de usuario
├── tests/                    # Pruebas unitarias
├── examples/                 # Archivos de ejemplo
├── requirements.txt          # Dependencias
└── main.py                   # Script principal
```

## Tecnologías utilizadas

- **pdfplumber**: Extracción de texto de PDFs
- **pandas**: Procesamiento de datos Excel
- **reportlab**: Generación de PDFs
- **PyPDF2**: Manipulación de PDFs
- **tkinter**: Interfaz gráfica de usuario