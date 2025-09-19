"""
Script de debug completo para detectar exactamente dónde está el problema
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_extractor import PDFExtractor
from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher
from src.pdf_generator import PDFGenerator

def debug_complete_flow():
    """Debug del flujo completo usando archivos reales"""
    print("=== DEBUG COMPLETO: Flujo Real de la Aplicación ===\n")
    
    try:
        # 1. Crear datos de prueba simulados
        print("1. CREANDO DATOS DE PRUEBA:")
        print("=" * 50)
        
        # Simular datos del PDF (como si hubieran sido extraídos)
        pdf_data_simulado = [
            {'nombre': '', 'cedula': '12345678'},  # Solo cédula, sin nombre
            {'nombre': '', 'cedula': '23456789'},  # Solo cédula, sin nombre
        ]
        
        print("Datos simulados del PDF:")
        for i, emp in enumerate(pdf_data_simulado):
            print(f"  Empleado {i+1}: nombre='{emp['nombre']}', cedula='{emp['cedula']}'")
        
        # 2. Configurar procesador de Excel
        print("\n2. CONFIGURANDO EXCEL PROCESSOR:")
        print("=" * 50)
        
        excel_processor = ExcelProcessor('examples/empleados_ejemplo.xlsx')
        excel_processor.load_excel()
        column_mapping = excel_processor.detect_columns()
        
        print(f"Columnas detectadas: {column_mapping}")
        
        # 3. Buscar empleados por cédula
        print("\n3. BÚSQUEDA POR CÉDULA:")
        print("=" * 50)
        
        for emp in pdf_data_simulado:
            cedula = emp['cedula']
            excel_results = excel_processor.search_by_cedula(cedula)
            print(f"\\nBúsqueda para cédula {cedula}:")
            if excel_results:
                for result in excel_results:
                    print(f"  Encontrado: {result}")
            else:
                print(f"  No encontrado")
        
        # 4. Simular matching completo
        print("\\n4. SIMULACIÓN DE MATCHING:")
        print("=" * 50)
        
        matcher = DataMatcher(None, excel_processor)
        
        # Simular empleados matcheados como los produciría match_by_cedula
        matched_employees = []
        
        for emp in pdf_data_simulado:
            cedula = emp['cedula']
            excel_results = excel_processor.search_by_cedula(cedula)
            
            if excel_results:
                excel_emp = excel_results[0]
                matched_emp = {
                    'nombre_pdf': emp.get('nombre', ''),  # Vacío desde PDF
                    'nombre_excel': excel_emp.get('nombre', ''),  # Del Excel
                    'cedula': cedula,
                    'centro_costo': excel_emp.get('centro_costo', ''),
                    'match_method': 'cedula',
                    'confidence': 1.0
                }
                matched_employees.append(matched_emp)
                print(f"Empleado matcheado para cédula {cedula}:")
                for key, value in matched_emp.items():
                    print(f"  {key}: '{value}'")
        
        # Asignar a matcher
        matcher.matched_employees = matched_employees
        matcher.unmatched_employees = []
        
        # 5. Probar get_consolidated_data
        print("\\n5. DATOS CONSOLIDADOS (get_consolidated_data):")
        print("=" * 50)
        
        consolidated_data = matcher.get_consolidated_data()
        
        print(f"Total de empleados consolidados: {len(consolidated_data)}")
        
        for i, emp in enumerate(consolidated_data):
            print(f"\\nEmpleado consolidado {i+1}:")
            for key, value in emp.items():
                print(f"  {key}: '{value}'")
                
        # 6. Verificar qué se está pasando al PDF
        print("\\n6. VERIFICACIÓN FINAL:")
        print("=" * 50)
        
        print("Datos que se pasarían al generador de PDF:")
        for emp in consolidated_data:
            nombre = emp.get('nombre', 'NO_DEFINIDO')
            cedula = emp.get('cedula', 'NO_DEFINIDO')
            print(f"  Nombre: '{nombre}' | Cédula: '{cedula}'")
            
            if nombre == cedula:
                print(f"  ❌ ERROR: El nombre es igual a la cédula!")
            elif nombre and nombre != 'NO_DEFINIDO':
                print(f"  ✅ OK: Nombre es diferente de cédula")
            else:
                print(f"  ⚠️  ADVERTENCIA: Nombre vacío o indefinido")
        
    except Exception as e:
        print(f"ERROR en debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_complete_flow()