"""
Debug rápido: Verificar detección de columnas
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def quick_column_test():
    """Test rápido de detección de columnas"""
    print("=== TEST: Detección de Columnas ===\n")
    
    try:
        from src.excel_processor import ExcelProcessor
        import pandas as pd
        
        # Crear datos de prueba que simulen tu Excel
        test_data = {
            'Nombre': ['JUAN CARLOS PEREZ', 'MARIA ELENA GOMEZ'],
            'Documento': ['06010', '52701035'],
            'Centro Costo': ['CC028-ROCKETFELLERPHILANTHROPYADVISORS', 'CC033-HSI']
        }
        
        df = pd.DataFrame(test_data)
        print("DATOS DE PRUEBA (simulando tu Excel):")
        print(df)
        print()
        
        # Guardar como Excel temporal
        test_file = 'test_columns.xlsx'
        df.to_excel(test_file, index=False)
        
        # Probar detección
        excel_processor = ExcelProcessor(test_file)
        excel_processor.load_excel()
        
        print("COLUMNAS EN EL ARCHIVO:")
        print(f"  {list(excel_processor.dataframe.columns)}")
        print()
        
        # Detectar columnas
        column_mapping = excel_processor.detect_columns()
        
        print("COLUMNAS DETECTADAS:")
        for field, column in column_mapping.items():
            print(f"  {field}: '{column}'")
        print()
        
        # Probar búsqueda por cédula
        if column_mapping['cedula']:
            print("PRUEBA DE BÚSQUEDA POR CÉDULA:")
            
            # Buscar cédulas de prueba
            test_cedulas = ['06010', '52701035', '1037606010']
            
            for cedula in test_cedulas:
                results = excel_processor.search_by_cedula(cedula)
                print(f"  Búsqueda '{cedula}':")
                if results:
                    for result in results:
                        print(f"    Encontrado: {result}")
                else:
                    print(f"    No encontrado")
        
        # Limpiar archivo temporal
        if os.path.exists(test_file):
            os.remove(test_file)
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_column_test()