"""
Test rápido después de simplificar el código
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher

def test_simplified_flow():
    """Test del flujo simplificado"""
    print("=== TEST: Flujo Simplificado (Solo Excel) ===\n")
    
    try:
        # 1. Simular datos del PDF (SOLO cédulas)
        print("1. DATOS DEL PDF (SOLO CÉDULAS):")
        print("-" * 40)
        
        pdf_employees_simplified = [
            {'nombre': '', 'cedula': '12345678'},  # Nombre SIEMPRE vacío
            {'nombre': '', 'cedula': '23456789'},  # Nombre SIEMPRE vacío
        ]
        
        for i, emp in enumerate(pdf_employees_simplified, 1):
            print(f"  Empleado {i}: cédula='{emp['cedula']}', nombre='{emp['nombre']}'")
        
        # 2. Cargar Excel
        print("\n2. CARGANDO EXCEL:")
        print("-" * 40)
        
        excel_processor = ExcelProcessor('examples/empleados_ejemplo.xlsx')
        excel_processor.load_excel()
        
        # 3. Matching simplificado
        print("\n3. MATCHING SIMPLIFICADO:")
        print("-" * 40)
        
        matcher = DataMatcher(None, excel_processor)
        matched_employees = []
        
        for pdf_emp in pdf_employees_simplified:
            cedula = pdf_emp['cedula']
            excel_results = excel_processor.search_by_cedula(cedula)
            
            if excel_results:
                excel_emp = excel_results[0]
                matched_emp = {
                    'nombre_excel': excel_emp.get('nombre', ''),  # SOLO del Excel
                    'cedula': cedula,
                    'centro_costo': excel_emp.get('centro_costo', ''),
                    'match_method': 'cedula',
                    'confidence': 1.0
                }
                matched_employees.append(matched_emp)
                print(f"  ✅ Cédula {cedula} -> '{excel_emp.get('nombre', '')}'")
        
        matcher.matched_employees = matched_employees
        
        # 4. Datos consolidados simplificados
        print("\n4. DATOS CONSOLIDADOS:")
        print("-" * 40)
        
        consolidated_data = matcher.get_consolidated_data()
        
        for i, emp in enumerate(consolidated_data, 1):
            nombre = emp.get('nombre', '')
            cedula = emp.get('cedula', '')
            print(f"  Empleado {i}:")
            print(f"    nombre: '{nombre}'")
            print(f"    cedula: '{cedula}'")
            
            if nombre.isdigit():
                print(f"    ❌ ERROR: Nombre es número")
            elif ' ' in nombre:
                print(f"    ✅ OK: Nombre correcto")
            else:
                print(f"    ⚠️  Nombre inusual: '{nombre}'")
        
        # 5. Verificación final
        print("\n5. VERIFICACIÓN FINAL:")
        print("-" * 40)
        
        if all(' ' in emp.get('nombre', '') for emp in consolidated_data):
            print("✅ PERFECTO: Todos los nombres son correctos")
            print("✅ El código simplificado funciona correctamente")
            print("✅ Solo se usan nombres del Excel")
        else:
            print("❌ Todavía hay problemas con algunos nombres")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simplified_flow()