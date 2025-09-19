# Manual de Instalación y Uso - App Facturación

## Instalación

### Paso 1: Configurar Python
Asegúrese de tener Python 3.8 o superior instalado.

### Paso 2: Crear entorno virtual (recomendado)
```bash
python -m venv .venv
```

### Paso 3: Activar entorno virtual
**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Paso 4: Instalar dependencias
```bash
pip install -r requirements.txt
```

Si hay problemas con la instalación, instale manualmente:
```bash
pip install pdfplumber==0.10.0
pip install pandas==2.0.3
pip install reportlab==4.0.4
pip install PyPDF2==3.0.1
pip install openpyxl==3.1.2
```

## Uso de la Aplicación

### Interfaz Gráfica (Recomendado)
```bash
python main.py
```

### Línea de Comandos
```bash
python main.py --cli archivo_factura.pdf empleados.xlsx
```

### Opciones adicionales
```bash
python main.py --cli factura.pdf empleados.xlsx --output ./resultados --similarity 0.8 --verbose
```

## Estructura de Archivos

La aplicación espera:

1. **PDF de Facturación**: Archivo PDF que contenga nombres o cédulas de empleados
2. **Excel de Empleados**: Archivo Excel con las siguientes columnas (detectadas automáticamente):
   - Nombres de empleados
   - Números de cédula
   - Centros de costo

## Ejemplo de Archivo Excel

| Nombre | Cedula | Centro_de_Costo |
|--------|--------|-----------------|
| Juan Pérez | 12345678 | VENTAS |
| María García | 23456789 | ADMINISTRACION |

## Proceso Automático

1. **Extracción**: La aplicación extrae nombres y cédulas del PDF
2. **Matching**: Busca coincidencias en el Excel por cédula (exacta) o nombre (similitud)
3. **Consolidación**: Crea una tabla con los centros de costo encontrados
4. **Generación**: Produce un PDF final con el original + la tabla de centros de costo

## Resultados

La aplicación genera:
- PDF final con datos consolidados
- Reporte de empleados encontrados/no encontrados
- Estadísticas del procesamiento
- Sugerencias para matches manuales

## Solución de Problemas

### Error "No module named X"
```bash
pip install -r requirements.txt
```

### Problemas con PDF
- Verifique que el PDF contenga texto extraíble (no solo imágenes)
- Asegúrese de que los nombres estén claramente formateados

### Problemas con Excel
- Use formato .xlsx (Excel moderno)
- Asegúrese de que las columnas tengan encabezados claros
- Los nombres de empleados deben estar en una sola columna

### Baja tasa de matching
- Ajuste el umbral de similitud (--similarity)
- Verifique la calidad de los datos en ambos archivos
- Use las sugerencias automáticas para matches manuales

## Soporte

Para problemas o mejoras, revise:
1. Los archivos de log generados
2. Las sugerencias automáticas de matching
3. La documentación técnica en el código