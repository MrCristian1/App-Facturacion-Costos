"""
Debug específico: Analizar el archivo Excel real del usuario
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_excel_real():
    """Debug del archivo Excel real"""
    print("=== DEBUG: Archivo Excel Real ===\n")
    
    try:
        from src.excel_processor import ExcelProcessor
        
        # Solicitar ruta del Excel real
        excel_path = input("📊 Ingresa la ruta completa de tu archivo Excel: ").strip()
        if not os.path.exists(excel_path):
            print(f"❌ ERROR: El archivo no existe: {excel_path}")
            return
        
        print(f"✅ Archivo encontrado: {excel_path}")
        print()
        
        # Cargar y analizar el Excel
        excel_processor = ExcelProcessor(excel_path)
        excel_processor.load_excel()
        
        # Mostrar información del DataFrame
        print("1. INFORMACIÓN GENERAL DEL EXCEL:")
        print("-" * 50)
        print(f"📋 Filas: {len(excel_processor.dataframe)}")
        print(f"📋 Columnas: {list(excel_processor.dataframe.columns)}")
        print()
        
        # Mostrar las primeras filas
        print("2. PRIMERAS 10 FILAS DEL EXCEL:")
        print("-" * 50)
        print(excel_processor.dataframe.head(10))
        print()
        
        # Detectar columnas automáticamente
        print("3. DETECCIÓN AUTOMÁTICA DE COLUMNAS:")
        print("-" * 50)
        column_mapping = excel_processor.detect_columns()
        print(f"Columnas detectadas: {column_mapping}")
        print()
        
        # Analizar cada columna detectada
        for field, column in column_mapping.items():
            if column and column in excel_processor.dataframe.columns:
                print(f"🔍 COLUMNA '{field}' -> '{column}':")
                sample_values = excel_processor.dataframe[column].head(5).tolist()
                print(f"   Valores de ejemplo: {sample_values}")
                
                # Verificar si la columna "nombre" contiene números
                if field == 'nombre':
                    if all(str(val).isdigit() for val in sample_values if pd.notna(val)):
                        print(f"   ❌ PROBLEMA: La columna '{column}' contiene NÚMEROS, no nombres!")
                    elif any(' ' in str(val) for val in sample_values if pd.notna(val)):
                        print(f"   ✅ OK: La columna '{column}' contiene nombres con espacios")
                    else:
                        print(f"   ⚠️  La columna '{column}' tiene formato inusual")
                print()
        
        # Buscar columnas que realmente contengan nombres
        print("4. BÚSQUEDA DE COLUMNAS CON NOMBRES REALES:")
        print("-" * 50)
        
        nombre_columns = []
        for col in excel_processor.dataframe.columns:
            # Tomar una muestra de valores de la columna
            sample_values = excel_processor.dataframe[col].head(10).dropna().tolist()
            
            if sample_values:
                # Verificar si parece contener nombres (strings con espacios)
                name_like = sum(
                    1 for val in sample_values 
                    if isinstance(val, str) and ' ' in val and len(val.split()) >= 2
                )
                
                if name_like >= len(sample_values) * 0.5:  # Al menos 50% parecen nombres
                    nombre_columns.append(col)
                    print(f"✅ Posible columna de nombres: '{col}'")
                    print(f"   Ejemplos: {sample_values[:3]}")
        
        if not nombre_columns:
            print("❌ No se encontraron columnas que contengan nombres de personas")
            print("💡 Verifica que tu Excel tenga una columna con nombres completos")
        
        print()
        
        # Mostrar recomendaciones
        print("5. RECOMENDACIONES:")
        print("-" * 50)
        
        if column_mapping.get('nombre') and nombre_columns:
            detected_name_col = column_mapping['nombre']
            if detected_name_col not in nombre_columns:
                print(f"❌ La columna detectada como 'nombre' ('{detected_name_col}') NO contiene nombres reales")
                print(f"✅ Columnas que SÍ contienen nombres: {nombre_columns}")
                print(f"💡 Necesitas renombrar la columna '{nombre_columns[0]}' a 'nombre' en tu Excel")
        
        print()
        print("📝 ESTRUCTURA ESPERADA DEL EXCEL:")
        print("   - Una columna llamada 'nombre' o 'Nombre' con nombres completos")
        print("   - Una columna llamada 'cedula' o 'Cedula' con números de cédula")
        print("   - Una columna llamada 'centro_costo' o similar con centros de costo")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Importar pandas aquí para el debug
    try:
        import pandas as pd
        debug_excel_real()
    except ImportError:
        print("❌ ERROR: pandas no está instalado")
        print("Ejecuta: pip install pandas")