"""
Script de validación simple para verificar que todos los módulos se cargan correctamente.
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Prueba que todos los módulos se puedan importar correctamente."""
    print("=== Validación de Módulos de la App Facturación ===\n")
    
    try:
        print("1. Probando importación de pdf_extractor...")
        from src.pdf_extractor import PDFExtractor
        print("   ✓ PDFExtractor importado correctamente")
        
        print("2. Probando importación de excel_processor...")
        from src.excel_processor import ExcelProcessor
        print("   ✓ ExcelProcessor importado correctamente")
        
        print("3. Probando importación de data_matcher...")
        from src.data_matcher import DataMatcher
        print("   ✓ DataMatcher importado correctamente")
        
        print("4. Probando importación de pdf_generator...")
        from src.pdf_generator import PDFGenerator
        print("   ✓ PDFGenerator importado correctamente")
        
        print("5. Probando importación de ui...")
        from src.ui import MainApplication, create_gui_app
        print("   ✓ UI modules importados correctamente")
        
        print("\n=== Pruebas Básicas de Funcionalidad ===\n")
        
        # Test básico de DataMatcher
        print("6. Probando funcionalidad de DataMatcher...")
        matcher = DataMatcher(None, None)
        
        # Test normalización de texto
        result = matcher.normalize_text("José María Pérez")
        expected = "jose maria perez"
        assert result == expected, f"Esperado '{expected}', obtenido '{result}'"
        print("   ✓ Normalización de texto funciona correctamente")
        
        # Test similitud de nombres
        similarity = matcher.calculate_name_similarity("Juan Pérez", "Juan Pérez")
        assert similarity == 1.0, f"Esperado 1.0, obtenido {similarity}"
        print("   ✓ Cálculo de similitud funciona correctamente")
        
        print("7. Probando funcionalidad de PDFGenerator...")
        generator = PDFGenerator()
        print("   ✓ PDFGenerator se inicializa correctamente")
        
        print("\n=== Verificación de Dependencias ===\n")
        
        print("8. Verificando dependencias instaladas...")
        
        import pdfplumber
        print("   ✓ pdfplumber disponible")
        
        import pandas as pd
        print("   ✓ pandas disponible")
        
        import reportlab
        print("   ✓ reportlab disponible")
        
        import PyPDF2
        print("   ✓ PyPDF2 disponible")
        
        import openpyxl
        print("   ✓ openpyxl disponible")
        
        print("\n=== ¡TODAS LAS VALIDACIONES EXITOSAS! ===")
        print("\nLa aplicación está lista para usar.")
        print("\nPara ejecutar la aplicación:")
        print("  - Interfaz gráfica: python main.py")
        print("  - Línea de comandos: python main.py --cli archivo.pdf empleados.xlsx")
        print("  - Ayuda: python main.py --help")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\nAsegúrese de instalar todas las dependencias:")
        print("pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return False

def test_file_structure():
    """Verifica que la estructura de archivos sea correcta."""
    print("\n=== Verificación de Estructura de Archivos ===\n")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'src/__init__.py',
        'src/pdf_extractor.py',
        'src/excel_processor.py',
        'src/data_matcher.py',
        'src/pdf_generator.py',
        'src/ui.py',
        'examples/empleados_ejemplo.csv',
        'examples/README.md'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✓ {file_path}")
        else:
            print(f"   ❌ {file_path} (FALTANTE)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠ Archivos faltantes: {len(missing_files)}")
        return False
    else:
        print("\n✓ Todos los archivos requeridos están presentes")
        return True

if __name__ == "__main__":
    print("Iniciando validación de la App Facturación...\n")
    
    # Verificar estructura de archivos
    structure_ok = test_file_structure()
    
    # Verificar imports y funcionalidad
    if structure_ok:
        imports_ok = test_imports()
        
        if imports_ok:
            print(f"\n{'='*50}")
            print("🎉 ¡VALIDACIÓN COMPLETA EXITOSA!")
            print("La aplicación está lista para usar.")
            print(f"{'='*50}")
        else:
            print(f"\n{'='*50}")
            print("❌ VALIDACIÓN FALLÓ")
            print("Revise los errores arriba y corrija antes de usar la aplicación.")
            print(f"{'='*50}")
            sys.exit(1)
    else:
        print("\n❌ Estructura de archivos incompleta")
        sys.exit(1)