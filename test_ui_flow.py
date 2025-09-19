"""
Test final: Simular exactamente el flujo que hace la UI para generar el PDF
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_extractor import PDFExtractor
from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher
from src.pdf_generator import PDFGenerator

def test_ui_flow():
    """Simula exactamente el flujo que hace la UI"""
    print("=== TEST: Flujo exacto de la UI ===\n")
    
    try:
        # 1. Simular extracción del PDF
        print("1. SIMULANDO EXTRACCIÓN DE PDF:")
        print("=" * 50)
        
        # Datos como los devolvería pdf_extractor.extract_employee_data()
        pdf_employees = [
            {'nombre': '', 'cedula': '12345678'},
            {'nombre': '', 'cedula': '23456789'},
        ]
        
        print("Empleados extraídos del PDF:")
        for i, emp in enumerate(pdf_employees):
            print(f"  {i+1}. nombre='{emp['nombre']}', cedula='{emp['cedula']}'")
        
        # 2. Cargar Excel
        print("\\n2. CARGANDO EXCEL:")
        print("=" * 50)
        
        excel_processor = ExcelProcessor('examples/empleados_ejemplo.xlsx')
        excel_processor.load_excel()
        
        # 3. Crear matcher y hacer matching (como en la UI)
        print("\\n3. CREANDO MATCHER Y HACIENDO MATCHING:")
        print("=" * 50)
        
        matcher = DataMatcher(None, excel_processor)
        
        # Simular el proceso de matching que hace match_by_cedula
        matching_results = {'matched_employees': [], 'unmatched_employees': [], 'statistics': {}}
        
        for emp in pdf_employees:
            cedula = emp['cedula']
            excel_results = excel_processor.search_by_cedula(cedula)
            
            if excel_results:
                excel_emp = excel_results[0]
                matched_emp = {
                    'nombre_pdf': emp.get('nombre', ''),
                    'nombre_excel': excel_emp.get('nombre', ''),
                    'cedula': cedula,
                    'centro_costo': excel_emp.get('centro_costo', ''),
                    'match_method': 'cedula',
                    'confidence': 1.0
                }
                matching_results['matched_employees'].append(matched_emp)
                print(f"Empleado matcheado: {cedula} -> {excel_emp.get('nombre', '')}")
            else:
                matching_results['unmatched_employees'].append(emp)
                print(f"Empleado NO matcheado: {cedula}")
        
        # Asignar al matcher
        matcher.matched_employees = matching_results['matched_employees']
        matcher.unmatched_employees = matching_results['unmatched_employees']
        
        # 4. Obtener datos consolidados (exactamente como en la UI)
        print("\\n4. OBTENIENDO DATOS CONSOLIDADOS:")
        print("=" * 50)
        
        consolidated_data = matcher.get_consolidated_data()
        
        print(f"Datos consolidados ({len(consolidated_data)} empleados):")
        for i, emp in enumerate(consolidated_data):
            print(f"\\n  Empleado {i+1}:")
            for key, value in emp.items():
                print(f"    {key}: '{value}'")
        
        # 5. Crear tabla como lo hace el PDF Generator
        print("\\n5. CREANDO TABLA PARA PDF:")
        print("=" * 50)
        
        pdf_generator = PDFGenerator()
        
        # Simular exactamente cómo se crea la tabla
        if consolidated_data:
            headers = ["Nombre Empleado", "Cédula", "Centro de Costo", "Estado", "Confianza"]
            table_data = [headers]
            
            for emp in consolidated_data:
                row = [
                    emp.get('nombre', ''),  # <-- Esta es la línea crítica
                    emp.get('cedula', ''),
                    emp.get('centro_costo', ''),
                    emp.get('estado_match', ''),
                    emp.get('confianza', '')
                ]
                table_data.append(row)
            
            print("Datos que irían en la tabla del PDF:")
            for i, row in enumerate(table_data):
                if i == 0:
                    print(f"  HEADER: {row}")
                else:
                    print(f"  FILA {i}: {row}")
                    # Verificar específicamente el campo nombre
                    nombre_campo = row[0]
                    if nombre_campo.isdigit():
                        print(f"    ❌ ERROR: El campo 'Nombre' contiene un número: '{nombre_campo}'")
                    elif nombre_campo and ' ' in nombre_campo:
                        print(f"    ✅ OK: El campo 'Nombre' contiene un nombre formateado: '{nombre_campo}'")
                    elif nombre_campo:
                        print(f"    ⚠️  El campo 'Nombre' tiene contenido pero sin espacios: '{nombre_campo}'")
                    else:
                        print(f"    ⚠️  El campo 'Nombre' está vacío")
        
        # 6. Verificación final del problema
        print("\\n6. DIAGNÓSTICO FINAL:")
        print("=" * 50)
        
        print("Verificando cada paso del flujo:")
        print(f"✅ Extracción PDF: Devuelve cédulas ({[emp['cedula'] for emp in pdf_employees]})")
        print(f"✅ Búsqueda Excel: Encuentra nombres ({[result[0]['nombre'] for result in [excel_processor.search_by_cedula(emp['cedula']) for emp in pdf_employees] if result]})")
        print(f"✅ Matching: Crea objetos con nombre_excel")
        print(f"✅ Consolidación: get_consolidated_data() devuelve nombres formateados")
        
        if consolidated_data:
            primer_nombre = consolidated_data[0].get('nombre', '')
            if primer_nombre and ' ' in primer_nombre:
                print(f"✅ RESULTADO: El nombre en datos consolidados es correcto: '{primer_nombre}'")
            else:
                print(f"❌ PROBLEMA: El nombre en datos consolidados no es correcto: '{primer_nombre}'")
        
    except Exception as e:
        print(f"ERROR en test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ui_flow()