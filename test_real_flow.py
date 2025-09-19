"""
Test final: Ejecutar el flujo completo con archivos reales
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_extractor import PDFExtractor
from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher
from src.pdf_generator import PDFGenerator

def test_real_application_flow():
    """Ejecuta el flujo real de la aplicación paso a paso"""
    print("=== TEST: Flujo Real de la Aplicación ===\n")
    
    try:
        # Crear un PDF de prueba con contenido problemático
        print("1. CREANDO PDF DE PRUEBA CON CONTENIDO PROBLEMÁTICO:")
        print("=" * 60)
        
        # Vamos a crear un PDF simple que contenga números como si fueran nombres
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        pdf_test_path = "test_problematic.pdf"
        c = canvas.Canvas(pdf_test_path, pagesize=letter)
        
        # Escribir contenido que causaría el problema
        c.drawString(100, 750, "LISTADO DE EMPLEADOS")
        c.drawString(100, 720, "12345678")  # Número que se interpretaría como nombre
        c.drawString(100, 700, "CC: 12345678")
        c.drawString(100, 680, "23456789")  # Otro número
        c.drawString(100, 660, "CC: 23456789")
        
        c.save()
        print(f"PDF de prueba creado: {pdf_test_path}")
        
        # 2. Ejecutar extracción real del PDF
        print("\\n2. EXTRACCIÓN REAL DEL PDF:")
        print("=" * 60)
        
        pdf_extractor = PDFExtractor(pdf_test_path)
        employees_data = pdf_extractor.extract_employees_data()
        
        print(f"Datos extraídos del PDF ({len(employees_data)} empleados):")
        for i, emp in enumerate(employees_data):
            print(f"  {i+1}. nombre='{emp.get('nombre', '')}', cedula='{emp.get('cedula', '')}'")
            if emp.get('nombre') == emp.get('cedula'):
                print(f"      ❌ DETECTADO: nombre igual a cédula")
        
        # 3. Cargar Excel real
        print("\\n3. CARGANDO EXCEL REAL:")
        print("=" * 60)
        
        excel_processor = ExcelProcessor('examples/empleados_ejemplo.xlsx')
        excel_processor.load_excel()
        
        # 4. Ejecutar matching real
        print("\\n4. MATCHING REAL:")
        print("=" * 60)
        
        matcher = DataMatcher(pdf_extractor, excel_processor)
        matching_results = matcher.perform_full_matching(0.7)
        
        print(f"Resultados del matching:")
        print(f"  Encontrados: {len(matching_results.get('matched', []))}")
        print(f"  No encontrados: {len(matching_results.get('unmatched', []))}")
        
        # Mostrar detalles de empleados matcheados
        for i, emp in enumerate(matching_results.get('matched', [])):
            print(f"\\n  Empleado matcheado {i+1}:")
            print(f"    nombre_pdf: '{emp.get('nombre_pdf', '')}'")
            print(f"    nombre_excel: '{emp.get('nombre_excel', '')}'")
            print(f"    cedula: '{emp.get('cedula', '')}'")
            print(f"    metodo: {emp.get('match_method', '')}")
        
        # 5. Obtener datos consolidados reales
        print("\\n5. DATOS CONSOLIDADOS REALES:")
        print("=" * 60)
        
        consolidated_data = matcher.get_consolidated_data()
        
        print(f"Datos consolidados ({len(consolidated_data)} empleados):")
        for i, emp in enumerate(consolidated_data):
            print(f"\\n  Empleado {i+1}:")
            print(f"    nombre: '{emp.get('nombre', '')}'")
            print(f"    cedula: '{emp.get('cedula', '')}'")
            print(f"    centro_costo: '{emp.get('centro_costo', '')}'")
            
            # Verificar el problema
            nombre = emp.get('nombre', '')
            cedula = emp.get('cedula', '')
            
            if nombre == cedula:
                print(f"    ❌ PROBLEMA: nombre = cédula")
            elif nombre.isdigit():
                print(f"    ❌ PROBLEMA: nombre es número")
            elif ' ' in nombre:
                print(f"    ✅ OK: nombre formateado correctamente")
            else:
                print(f"    ⚠️  nombre inusual: '{nombre}'")
        
        # 6. Simular generación de PDF
        print("\\n6. SIMULANDO GENERACIÓN DE PDF:")
        print("=" * 60)
        
        pdf_generator = PDFGenerator()
        
        # Simular creación de tabla como lo hace el PDF generator
        if consolidated_data:
            headers = ["Nombre Empleado", "Cédula", "Centro de Costo", "Estado", "Confianza"]
            table_data = [headers]
            
            for emp in consolidated_data:
                row = [
                    emp.get('nombre', ''),  # Este es el campo crítico
                    emp.get('cedula', ''),
                    emp.get('centro_costo', ''),
                    emp.get('estado_match', ''),
                    emp.get('confianza', '')
                ]
                table_data.append(row)
            
            print("Datos que aparecerían en el PDF final:")
            for i, row in enumerate(table_data):
                if i == 0:
                    print(f"  ENCABEZADOS: {row}")
                else:
                    print(f"  FILA {i}: {row}")
                    if i == 1:  # Verificar primera fila de datos
                        nombre_final = row[0]
                        if nombre_final.isdigit():
                            print(f"    ❌ EL PROBLEMA ESTÁ AQUÍ: '{nombre_final}' es un número")
                        else:
                            print(f"    ✅ Nombre correcto: '{nombre_final}'")
        
        # Limpiar archivo de prueba
        if os.path.exists(pdf_test_path):
            os.remove(pdf_test_path)
            print(f"\\nArchivo de prueba eliminado: {pdf_test_path}")
        
    except Exception as e:
        print(f"ERROR en test: {e}")
        import traceback
        traceback.print_exc()
        
        # Limpiar en caso de error
        if os.path.exists("test_problematic.pdf"):
            os.remove("test_problematic.pdf")

if __name__ == "__main__":
    test_real_application_flow()