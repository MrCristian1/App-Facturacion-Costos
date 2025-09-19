"""
Script de debug para verificar el flujo de datos entre PDF → Excel → Tabla final
"""

import sys
import os
import pandas as pd

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher

def debug_data_flow():
    """Debug del flujo de datos completo."""
    print("=== DEBUG: Flujo de Datos PDF → Excel → Tabla ===\n")
    
    # 1. Cargar y mostrar datos del Excel
    print("1. DATOS DEL EXCEL:")
    print("=" * 40)
    
    try:
        # Crear DataFrame directamente para testing
        excel_data = {
            'Nombre': [
                'TRUJILLOPEREZMARIACLARA',
                'GARCIALOPEZMARIAFERNANDA', 
                'RODRIGUEZSILVACARLOSYEDUARDO'
            ],
            'Cedula': ['12345678', '23456789', '34567890'],
            'Centro_de_Costo': ['VENTAS', 'ADMINISTRACION', 'PRODUCCION']
        }
        
        df = pd.DataFrame(excel_data)
        print(df)
        
        # 2. Simular procesamiento
        print("\n2. SIMULACIÓN DE MATCHING:")
        print("=" * 40)
        
        # Simular empleado encontrado por cédula
        empleado_matcheado = {
            'nombre_pdf': '',  # No hay nombre en PDF, solo cédula
            'nombre_excel': 'TRUJILLOPEREZMARIACLARA',  # Nombre del Excel
            'cedula': '12345678',
            'centro_costo': 'VENTAS',
            'match_method': 'cedula',
            'confidence': 1.0
        }
        
        print(f"Empleado matcheado (simulado):")
        for key, value in empleado_matcheado.items():
            print(f"  {key}: {value}")
        
        # 3. Probar formateo de nombre
        print("\n3. FORMATEO DE NOMBRE:")
        print("=" * 40)
        
        matcher = DataMatcher(None, None)
        nombre_original = empleado_matcheado['nombre_excel']
        nombre_formateado = matcher.format_name(nombre_original)
        
        print(f"Nombre original: {nombre_original}")
        print(f"Nombre formateado: {nombre_formateado}")
        
        # 4. Probar get_consolidated_data
        print("\n4. DATOS CONSOLIDADOS FINALES:")
        print("=" * 40)
        
        # Simular el resultado que debería dar get_consolidated_data
        matcher.matched_employees = [empleado_matcheado]
        matcher.unmatched_employees = []
        
        consolidated = matcher.get_consolidated_data()
        
        if consolidated:
            emp = consolidated[0]
            print(f"Datos finales para la tabla:")
            for key, value in emp.items():
                print(f"  {key}: {value}")
        else:
            print("ERROR: No se generaron datos consolidados")
            
        print(f"\n✓ El nombre en la tabla debería ser: '{nombre_formateado}'")
        print(f"✓ La cédula en la tabla debería ser: '12345678'")
        
    except Exception as e:
        print(f"ERROR en debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_data_flow()