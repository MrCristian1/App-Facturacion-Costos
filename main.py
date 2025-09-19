"""
Script principal de la aplicación de facturación con centros de costo.

Este script puede ejecutarse de dos maneras:
1. Con interfaz gráfica (por defecto)
2. Desde línea de comandos con argumentos

Uso:
    python main.py                                  # Interfaz gráfica
    python main.py --gui                           # Interfaz gráfica explícita
    python main.py --cli pdf.pdf excel.xlsx       # Línea de comandos
    python main.py --help                         # Mostrar ayuda

Ejemplos:
    python main.py
    python main.py --cli factura.pdf empleados.xlsx --output ./resultados
    python main.py --cli factura.pdf empleados.xlsx --similarity 0.8
"""

import sys
import os
import argparse
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.pdf_extractor import PDFExtractor
    from src.excel_processor import ExcelProcessor
    from src.data_matcher import DataMatcher
    from src.pdf_generator import PDFGenerator
    from src.ui import create_gui_app
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que todas las dependencias estén instaladas:")
    print("pip install -r requirements.txt")
    sys.exit(1)


class CLIProcessor:
    """Procesador para la interfaz de línea de comandos."""
    
    def __init__(self, pdf_path: str, excel_path: str, output_dir: str = None, 
                 similarity_threshold: float = 0.7, verbose: bool = False):
        """
        Inicializa el procesador CLI.
        
        Args:
            pdf_path: Ruta al archivo PDF
            excel_path: Ruta al archivo Excel
            output_dir: Directorio de salida (opcional)
            similarity_threshold: Umbral de similitud para nombres
            verbose: Si mostrar salida detallada
        """
        self.pdf_path = pdf_path
        self.excel_path = excel_path
        self.output_dir = output_dir or os.path.dirname(pdf_path)
        self.similarity_threshold = similarity_threshold
        self.verbose = verbose
        
    def log(self, message: str):
        """Imprime mensaje si modo verbose está activado."""
        if self.verbose:
            print(f"[INFO] {message}")
            
    def validate_inputs(self) -> bool:
        """
        Valida las entradas.
        
        Returns:
            True si las entradas son válidas
        """
        if not os.path.exists(self.pdf_path):
            print(f"Error: El archivo PDF '{self.pdf_path}' no existe")
            return False
            
        if not os.path.exists(self.excel_path):
            print(f"Error: El archivo Excel '{self.excel_path}' no existe")
            return False
            
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir, exist_ok=True)
                self.log(f"Directorio de salida creado: {self.output_dir}")
            except Exception as e:
                print(f"Error: No se pudo crear el directorio de salida: {e}")
                return False
                
        return True
        
    def process(self) -> bool:
        """
        Procesa los archivos.
        
        Returns:
            True si el procesamiento fue exitoso
        """
        try:
            print("=== App Facturación - Procesamiento de Centros de Costo ===")
            print(f"PDF: {os.path.basename(self.pdf_path)}")
            print(f"Excel: {os.path.basename(self.excel_path)}")
            print(f"Salida: {self.output_dir}")
            print(f"Umbral de similitud: {self.similarity_threshold}")
            print()
            
            # Paso 1: Extraer datos del PDF
            print("1. Extrayendo datos del PDF...")
            self.log(f"Inicializando extractor para: {self.pdf_path}")
            
            pdf_extractor = PDFExtractor(self.pdf_path)
            employees_data = pdf_extractor.extract_employees_data()
            
            print(f"   ✓ Encontrados {len(employees_data)} empleados en el PDF")
            self.log(f"Empleados extraídos: {[emp.get('nombre', emp.get('cedula', 'Sin datos')) for emp in employees_data]}")
            
            # Paso 2: Cargar datos del Excel
            print("2. Cargando base de datos Excel...")
            self.log(f"Inicializando procesador para: {self.excel_path}")
            
            excel_processor = ExcelProcessor(self.excel_path)
            excel_processor.load_excel()
            column_mapping = excel_processor.detect_columns()
            
            print(f"   ✓ Excel cargado exitosamente")
            self.log(f"Columnas detectadas: {column_mapping}")
            
            # Validar que se detectaron las columnas necesarias
            if not column_mapping.get('centro_costo'):
                print("   ⚠ Advertencia: No se detectó columna de centro de costo")
            
            # Paso 3: Realizar matching
            print("3. Realizando matching de datos...")
            self.log("Iniciando proceso de matching...")
            
            matcher = DataMatcher(pdf_extractor, excel_processor)
            matching_results = matcher.perform_full_matching(self.similarity_threshold)
            
            stats = matching_results['statistics']
            print(f"   ✓ Matching completado:")
            print(f"     • Encontrados: {stats['total_matched']}")
            print(f"     • No encontrados: {stats['total_unmatched']}")
            print(f"     • Tasa de éxito: {stats['match_rate']:.1%}")
            
            # Paso 4: Generar PDF
            print("4. Generando PDF final...")
            self.log("Creando PDF con datos consolidados...")
            
            pdf_generator = PDFGenerator()
            consolidated_data = matcher.get_consolidated_data()
            
            final_pdf_path = pdf_generator.create_complete_pdf(
                self.pdf_path,
                consolidated_data,
                stats,
                self.output_dir
            )
            
            print(f"   ✓ PDF generado: {os.path.basename(final_pdf_path)}")
            print(f"   📁 Ubicación: {final_pdf_path}")
            
            # Mostrar resumen final
            print()
            print("=== RESUMEN DEL PROCESAMIENTO ===")
            print(f"Total de empleados procesados: {stats['total_matched'] + stats['total_unmatched']}")
            print(f"Empleados encontrados: {stats['total_matched']}")
            print(f"Empleados no encontrados: {stats['total_unmatched']}")
            print(f"Tasa de éxito: {stats['match_rate']:.1%}")
            print()
            print(f"✅ Archivo final: {final_pdf_path}")
            
            # Mostrar empleados no encontrados si los hay
            if matching_results['unmatched']:
                print()
                print("⚠ EMPLEADOS NO ENCONTRADOS:")
                for emp in matching_results['unmatched']:
                    nombre = emp.get('nombre', 'Sin nombre')
                    cedula = emp.get('cedula', 'Sin cédula')
                    print(f"   • {nombre} - {cedula}")
                
                # Mostrar sugerencias si están disponibles
                suggestions = matcher.suggest_manual_matches(top_n=1)
                if suggestions:
                    print()
                    print("💡 SUGERENCIAS AUTOMÁTICAS:")
                    for pdf_name, excel_matches in suggestions.items():
                        if excel_matches:
                            match = excel_matches[0]
                            print(f"   • '{pdf_name}' → '{match['nombre_excel']}' (similitud: {match['similitud']})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante el procesamiento: {str(e)}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Crea el parser de argumentos de línea de comandos.
    
    Returns:
        ArgumentParser configurado
    """
    parser = argparse.ArgumentParser(
        description='Aplicación para automatizar centros de costo en PDFs de facturación',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                                    # Interfaz gráfica
  %(prog)s --gui                             # Interfaz gráfica explícita
  %(prog)s --cli factura.pdf empleados.xlsx # Línea de comandos básico
  %(prog)s --cli factura.pdf empleados.xlsx --output ./resultados
  %(prog)s --cli factura.pdf empleados.xlsx --similarity 0.8 --verbose

Notas:
  - Si no se especifica --cli o --gui, se usará la interfaz gráfica
  - El directorio de salida por defecto es el mismo del archivo PDF
  - El umbral de similitud debe estar entre 0.5 y 1.0 (por defecto: 0.7)
        """
    )
    
    # Grupo mutuamente excluyente para modo de operación
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--gui',
        action='store_true',
        help='Ejecutar con interfaz gráfica (por defecto)'
    )
    mode_group.add_argument(
        '--cli',
        nargs=2,
        metavar=('PDF_FILE', 'EXCEL_FILE'),
        help='Ejecutar desde línea de comandos con archivos PDF y Excel'
    )
    
    # Argumentos para modo CLI
    parser.add_argument(
        '--output', '-o',
        metavar='DIR',
        help='Directorio de salida para el PDF generado'
    )
    parser.add_argument(
        '--similarity', '-s',
        type=float,
        default=0.7,
        metavar='THRESHOLD',
        help='Umbral de similitud para matching de nombres (0.5-1.0, default: 0.7)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar salida detallada'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='App Facturación v1.0.0'
    )
    
    return parser


def main():
    """Función principal de la aplicación."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Validar umbral de similitud
    if not 0.5 <= args.similarity <= 1.0:
        print("Error: El umbral de similitud debe estar entre 0.5 y 1.0")
        sys.exit(1)
    
    # Determinar modo de operación
    if args.cli:
        # Modo línea de comandos
        pdf_path, excel_path = args.cli
        
        processor = CLIProcessor(
            pdf_path=pdf_path,
            excel_path=excel_path,
            output_dir=args.output,
            similarity_threshold=args.similarity,
            verbose=args.verbose
        )
        
        if not processor.validate_inputs():
            sys.exit(1)
            
        success = processor.process()
        sys.exit(0 if success else 1)
        
    else:
        # Modo interfaz gráfica (por defecto)
        try:
            print("Iniciando interfaz gráfica...")
            app = create_gui_app()
            app.run()
        except Exception as e:
            print(f"Error al iniciar la interfaz gráfica: {e}")
            print("\nIntente usar el modo de línea de comandos:")
            print("python main.py --cli archivo.pdf empleados.xlsx")
            sys.exit(1)


if __name__ == "__main__":
    main()