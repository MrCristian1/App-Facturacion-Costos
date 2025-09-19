"""
Debug específico: Simular el problema real donde el PDF contiene números 
en lugar de nombres en la extracción
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher

def test_problematic_pdf_data():
    """Simula el problema real: PDF con números como nombres"""
    print("=== DEBUG: Problema con números en lugar de nombres ===\n")
    
    try:
        # 1. Simular datos problemáticos del PDF
        print("1. SIMULANDO DATOS PROBLEMÁTICOS DEL PDF:")
        print("=" * 60)
        
        # Estos datos simulan lo que extract_employees_data() devolvería
        # si el PDF tiene números donde deberían estar los nombres
        pdf_employees_problematicos = [
            {'nombre': '12345678', 'cedula': '12345678'},  # ¡Nombre = Cédula!
            {'nombre': '23456789', 'cedula': '23456789'},  # ¡Nombre = Cédula!
        ]
        
        print("Datos problemáticos extraídos del PDF:")
        for i, emp in enumerate(pdf_employees_problematicos):
            print(f"  Empleado {i+1}: nombre='{emp['nombre']}', cedula='{emp['cedula']}'")
            if emp['nombre'] == emp['cedula']:
                print(f"    ❌ PROBLEMA: El nombre es igual a la cédula!")
        
        # 2. Cargar Excel
        print("\\n2. CARGANDO EXCEL:")
        print("=" * 60)
        
        excel_processor = ExcelProcessor('examples/empleados_ejemplo.xlsx')
        excel_processor.load_excel()
        
        # 3. Simular matching manual con datos problemáticos
        print("\\n3. SIMULANDO MATCHING CON DATOS PROBLEMÁTICOS:")
        print("=" * 60)
        
        matcher = DataMatcher(None, excel_processor)
        matched_employees = []
        
        for pdf_emp in pdf_employees_problematicos:
            cedula = pdf_emp['cedula']
            excel_results = excel_processor.search_by_cedula(cedula)
            
            if excel_results:
                excel_emp = excel_results[0]
                
                # Esto es lo que hace match_by_cedula en la realidad
                matched_emp = {
                    'nombre_pdf': pdf_emp.get('nombre', ''),     # NÚMERO problemático
                    'nombre_excel': excel_emp.get('nombre', ''), # NOMBRE correcto
                    'cedula': cedula,
                    'centro_costo': excel_emp.get('centro_costo', ''),
                    'match_method': 'cedula',
                    'confidence': 1.0
                }
                matched_employees.append(matched_emp)
                
                print(f"Match para cédula {cedula}:")
                print(f"  nombre_pdf (del PDF): '{matched_emp['nombre_pdf']}'")
                print(f"  nombre_excel (del Excel): '{matched_emp['nombre_excel']}'")
                print(f"  ¿Nombre PDF es número?: {matched_emp['nombre_pdf'].isdigit()}")
        
        # Asignar al matcher
        matcher.matched_employees = matched_employees
        matcher.unmatched_employees = []
        
        # 4. Probar get_consolidated_data con datos problemáticos
        print("\\n4. DATOS CONSOLIDADOS (con datos problemáticos):")
        print("=" * 60)
        
        consolidated_data = matcher.get_consolidated_data()
        
        print(f"Total de empleados consolidados: {len(consolidated_data)}")
        
        for i, emp in enumerate(consolidated_data):
            print(f"\\nEmpleado consolidado {i+1}:")
            print(f"  nombre: '{emp.get('nombre', '')}'")
            print(f"  cedula: '{emp.get('cedula', '')}'")
            print(f"  centro_costo: '{emp.get('centro_costo', '')}'")
            
            # Verificar si el problema persiste
            nombre = emp.get('nombre', '')
            cedula = emp.get('cedula', '')
            
            if nombre == cedula:
                print(f"  ❌ ERROR: El nombre final sigue siendo igual a la cédula!")
                print(f"  CAUSA: get_consolidated_data() no está priorizando el nombre del Excel")
            elif nombre.isdigit():
                print(f"  ❌ ERROR: El nombre final es un número!")
            elif nombre and ' ' in nombre:
                print(f"  ✅ OK: El nombre es correcto y formateado")
            else:
                print(f"  ⚠️  El nombre tiene un formato inusual: '{nombre}'")
        
        # 5. Verificar la lógica interna de get_consolidated_data
        print("\\n5. VERIFICACIÓN DE LA LÓGICA INTERNA:")
        print("=" * 60)
        
        for i, emp in enumerate(matched_employees):
            print(f"\\nEmpleado {i+1} - Análisis de get_consolidated_data():")
            
            nombre_excel = emp.get('nombre_excel')
            nombre_pdf = emp.get('nombre_pdf')
            
            print(f"  nombre_excel disponible: '{nombre_excel}' ({'SÍ' if nombre_excel else 'NO'})")
            print(f"  nombre_pdf disponible: '{nombre_pdf}' ({'SÍ' if nombre_pdf else 'NO'})")
            
            # Simular la lógica de get_consolidated_data
            nombre_a_usar = ""
            if emp.get('nombre_excel'):
                nombre_a_usar = emp.get('nombre_excel')
                print(f"  → Usando nombre_excel: '{nombre_a_usar}'")
            elif emp.get('nombre_pdf'):
                nombre_a_usar = emp.get('nombre_pdf')
                print(f"  → Usando nombre_pdf: '{nombre_a_usar}' (¡PROBLEMA!)")
            
            nombre_formateado = matcher.format_name(nombre_a_usar) if nombre_a_usar else ''
            print(f"  → Nombre final formateado: '{nombre_formateado}'")
        
    except Exception as e:
        print(f"ERROR en debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_problematic_pdf_data()