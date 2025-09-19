"""
Herramienta de Diagnóstico Final
Permite al usuario verificar exactamente qué está pasando con sus archivos reales
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def diagnostic_tool():
    """Herramienta interactiva de diagnóstico"""
    print("="*70)
    print("🔍 HERRAMIENTA DE DIAGNÓSTICO - APP FACTURACIÓN")
    print("="*70)
    print()
    print("Esta herramienta te ayudará a identificar exactamente qué está")
    print("causando que aparezcan números en lugar de nombres en tu PDF.")
    print()
    
    try:
        from src.pdf_extractor import PDFExtractor
        from src.excel_processor import ExcelProcessor
        from src.data_matcher import DataMatcher
        
        # 1. Verificar archivos
        print("1️⃣  VERIFICACIÓN DE ARCHIVOS:")
        print("-" * 40)
        
        pdf_path = input("📄 Ingresa la ruta completa de tu archivo PDF: ").strip()
        if not os.path.exists(pdf_path):
            print(f"❌ ERROR: El archivo PDF no existe: {pdf_path}")
            return
        
        excel_path = input("📊 Ingresa la ruta completa de tu archivo Excel: ").strip()
        if not os.path.exists(excel_path):
            print(f"❌ ERROR: El archivo Excel no existe: {excel_path}")
            return
        
        print("✅ Ambos archivos existen")
        print()
        
        # 2. Análisis del PDF
        print("2️⃣  ANÁLISIS DEL PDF:")
        print("-" * 40)
        
        pdf_extractor = PDFExtractor(pdf_path)
        text_preview = pdf_extractor.get_text_preview(300)
        
        print("📋 Vista previa del texto del PDF:")
        print(f"   {text_preview}")
        print()
        
        employees_data = pdf_extractor.extract_employees_data()
        print(f"👥 Empleados extraídos del PDF: {len(employees_data)}")
        
        for i, emp in enumerate(employees_data[:5], 1):  # Mostrar máximo 5
            nombre = emp.get('nombre', '')
            cedula = emp.get('cedula', '')
            print(f"   {i}. nombre: '{nombre}' | cédula: '{cedula}'")
            
            if nombre == cedula:
                print(f"      ⚠️  PROBLEMA DETECTADO: nombre igual a cédula")
            elif nombre.isdigit():
                print(f"      ⚠️  PROBLEMA DETECTADO: nombre es un número")
            elif not nombre:
                print(f"      ℹ️  Nombre vacío (normal si el PDF solo tiene cédulas)")
        
        if len(employees_data) > 5:
            print(f"   ... y {len(employees_data) - 5} empleados más")
        print()
        
        # 3. Análisis del Excel
        print("3️⃣  ANÁLISIS DEL EXCEL:")
        print("-" * 40)
        
        excel_processor = ExcelProcessor(excel_path)
        excel_processor.load_excel()
        
        column_mapping = excel_processor.detect_columns()
        print(f"📊 Columnas detectadas: {column_mapping}")
        
        all_excel_employees = excel_processor.get_all_employees()
        print(f"👥 Empleados en Excel: {len(all_excel_employees)}")
        
        for i, emp in enumerate(all_excel_employees[:5], 1):  # Mostrar máximo 5
            nombre = emp.get('nombre', '')
            cedula = emp.get('cedula', '')
            centro_costo = emp.get('centro_costo', '')
            print(f"   {i}. nombre: '{nombre}' | cédula: '{cedula}' | centro: '{centro_costo}'")
        
        if len(all_excel_employees) > 5:
            print(f"   ... y {len(all_excel_employees) - 5} empleados más")
        print()
        
        # 4. Análisis de coincidencias
        print("4️⃣  ANÁLISIS DE COINCIDENCIAS:")
        print("-" * 40)
        
        cedulas_pdf = [emp.get('cedula', '') for emp in employees_data if emp.get('cedula')]
        cedulas_excel = [emp.get('cedula', '') for emp in all_excel_employees if emp.get('cedula')]
        
        print(f"📄 Cédulas en PDF: {len(cedulas_pdf)}")
        print(f"📊 Cédulas en Excel: {len(cedulas_excel)}")
        
        # Verificar coincidencias
        coincidencias = []
        for cedula_pdf in cedulas_pdf:
            for cedula_excel in cedulas_excel:
                if str(cedula_pdf).strip() == str(cedula_excel).strip():
                    # Buscar el nombre correspondiente
                    excel_emp = next((emp for emp in all_excel_employees if str(emp.get('cedula', '')).strip() == str(cedula_excel).strip()), None)
                    if excel_emp:
                        coincidencias.append({
                            'cedula': cedula_pdf,
                            'nombre_excel': excel_emp.get('nombre', ''),
                            'centro_costo': excel_emp.get('centro_costo', '')
                        })
                    break
        
        print(f"✅ Coincidencias encontradas: {len(coincidencias)}")
        
        for i, match in enumerate(coincidencias[:5], 1):
            print(f"   {i}. Cédula: {match['cedula']} -> Nombre: '{match['nombre_excel']}' | Centro: '{match['centro_costo']}'")
        
        if len(coincidencias) > 5:
            print(f"   ... y {len(coincidencias) - 5} coincidencias más")
        print()
        
        # 5. Simulación del proceso completo
        print("5️⃣  SIMULACIÓN DEL PROCESO COMPLETO:")
        print("-" * 40)
        
        matcher = DataMatcher(pdf_extractor, excel_processor)
        matching_results = matcher.perform_full_matching(0.7)
        
        print(f"🔍 Matching completado:")
        print(f"   Encontrados: {len(matching_results.get('matched', []))}")
        print(f"   No encontrados: {len(matching_results.get('unmatched', []))}")
        print()
        
        # Datos consolidados
        consolidated_data = matcher.get_consolidated_data()
        print(f"📋 Datos consolidados: {len(consolidated_data)} empleados")
        
        problem_detected = False
        for i, emp in enumerate(consolidated_data[:5], 1):
            nombre = emp.get('nombre', '')
            cedula = emp.get('cedula', '')
            
            print(f"   {i}. NOMBRE FINAL: '{nombre}' | CÉDULA: '{cedula}'")
            
            if nombre == cedula:
                print(f"      ❌ PROBLEMA: El nombre final es igual a la cédula")
                problem_detected = True
            elif nombre.isdigit():
                print(f"      ❌ PROBLEMA: El nombre final es un número")
                problem_detected = True
            elif ' ' in nombre and len(nombre) > 5:
                print(f"      ✅ CORRECTO: Nombre formateado apropiadamente")
            else:
                print(f"      ⚠️  Nombre inusual: '{nombre}'")
        
        if len(consolidated_data) > 5:
            print(f"   ... y {len(consolidated_data) - 5} empleados más")
        print()
        
        # 6. Diagnóstico final
        print("6️⃣  DIAGNÓSTICO FINAL:")
        print("-" * 40)
        
        if not problem_detected and consolidated_data:
            print("✅ TODO ESTÁ FUNCIONANDO CORRECTAMENTE")
            print("   Los nombres finales son correctos y están formateados apropiadamente.")
            print("   Si aún ves números en tu PDF, puede ser que estés viendo un archivo generado anteriormente.")
            print("   Intenta generar un nuevo PDF con la aplicación.")
        elif not consolidated_data:
            print("❌ NO SE ENCONTRARON COINCIDENCIAS")
            print("   Las cédulas del PDF no coinciden con las del Excel.")
            print("   Verifica que las cédulas estén en el mismo formato en ambos archivos.")
        else:
            print("❌ SE DETECTARON PROBLEMAS")
            print("   Los datos consolidados aún contienen números en lugar de nombres.")
            print("   Esto podría indicar un problema en el código o en los datos.")
        
        print()
        print("💡 RECOMENDACIONES:")
        print("   1. Si todo se ve correcto aquí, regenera el PDF completo")
        print("   2. Verifica que las cédulas en ambos archivos tengan el mismo formato")
        print("   3. Asegúrate de que el Excel tenga una columna 'nombre' con nombres completos")
        print("   4. Si el problema persiste, comparte los archivos de ejemplo para revisión")
        
    except Exception as e:
        print(f"❌ ERROR durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("="*70)
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print("="*70)

if __name__ == "__main__":
    diagnostic_tool()