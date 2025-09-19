"""
Módulo para extraer texto y datos de empleados desde PDFs de facturación.
"""

import pdfplumber
import re
from typing import List, Dict, Optional


class PDFExtractor:
    """Clase para extraer datos de empleados desde PDFs de facturación."""
    
    def __init__(self, pdf_path: str):
        """
        Inicializa el extractor con la ruta del PDF.
        
        Args:
            pdf_path: Ruta al archivo PDF
        """
        self.pdf_path = pdf_path
        self.text_content = ""
        self.employees_data = []
    
    def extract_text(self) -> str:
        """
        Extrae todo el texto del PDF.
        
        Returns:
            Texto completo extraído del PDF
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                self.text_content = text
                return text
                
        except Exception as e:
            raise Exception(f"Error al extraer texto del PDF: {str(e)}")
    
    def extract_employee_names(self) -> List[str]:
        """
        Extrae nombres de empleados del texto del PDF.
        Busca patrones comunes de nombres (2-3 palabras capitalizadas).
        
        Returns:
            Lista de nombres de empleados encontrados
        """
        if not self.text_content:
            self.extract_text()
        
        # Patrón para nombres: 2-3 palabras que empiecen con mayúscula
        name_pattern = r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2}\b'
        
        names = re.findall(name_pattern, self.text_content)
        
        # Filtrar nombres muy comunes que probablemente no sean empleados
        excluded_words = {'Factura', 'Empresa', 'Cliente', 'Total', 'Fecha', 'Número', 
                         'Descripción', 'Cantidad', 'Precio', 'Valor', 'Descuento',
                         'Impuesto', 'Base', 'Tarifa', 'Código', 'Producto', 'Servicio'}
        
        filtered_names = []
        for name in names:
            # Verificar que no sea una palabra excluida
            if not any(word in name for word in excluded_words):
                # Verificar que tenga al menos 2 palabras
                if len(name.split()) >= 2:
                    filtered_names.append(name.strip())
        
        # Eliminar duplicados manteniendo el orden
        unique_names = list(dict.fromkeys(filtered_names))
        
        return unique_names
    
    def extract_cedulas(self) -> List[str]:
        """
        Extrae números de cédula del texto del PDF.
        Busca patrones de números de identificación colombianos.
        
        Returns:
            Lista de números de cédula encontrados
        """
        if not self.text_content:
            self.extract_text()
        
        # Patrones comunes para cédulas colombianas
        cedula_patterns = [
            r'\b\d{7,10}\b',  # Números de 7 a 10 dígitos
            r'\b\d{1,3}\.?\d{3}\.?\d{3}\b',  # Formato con puntos (ej: 12.345.678)
            r'\bC\.?C\.?\s*:?\s*(\d{7,10})\b',  # Con prefijo C.C.
            r'\bCédula\s*:?\s*(\d{7,10})\b',  # Con palabra "Cédula"
            r'\bIdentificación\s*:?\s*(\d{7,10})\b'  # Con palabra "Identificación"
        ]
        
        cedulas = []
        
        for pattern in cedula_patterns:
            matches = re.findall(pattern, self.text_content, re.IGNORECASE)
            if isinstance(matches[0] if matches else None, tuple):
                # Si el patrón tiene grupos de captura
                cedulas.extend([match[0] if isinstance(match, tuple) else match for match in matches])
            else:
                cedulas.extend(matches)
        
        # Limpiar y validar cédulas
        cleaned_cedulas = []
        for cedula in cedulas:
            # Remover puntos y espacios
            clean_cedula = re.sub(r'[^\d]', '', str(cedula))
            # Validar longitud (7-10 dígitos para cédulas colombianas)
            if 7 <= len(clean_cedula) <= 10:
                cleaned_cedulas.append(clean_cedula)
        
        # Eliminar duplicados
        unique_cedulas = list(dict.fromkeys(cleaned_cedulas))
        
        return unique_cedulas
    
    def extract_employees_data(self) -> List[Dict[str, str]]:
        """
        Extrae SOLO cédulas del PDF - Los nombres vendrán del Excel.
        
        Returns:
            Lista de diccionarios con cédulas (sin nombres del PDF)
        """
        # SOLO extraer cédulas - ignorar nombres del PDF
        cedulas = self.extract_cedulas()
        
        employees = []
        
        # Crear un empleado por cada cédula encontrada
        for cedula in cedulas:
            employees.append({
                'nombre': '',  # Siempre vacío - vendrá del Excel
                'cedula': cedula,
                'centro_costo': ''  # Se llenará desde el Excel
            })
        
        self.employees_data = employees
        return employees
    
    def get_text_preview(self, max_chars: int = 500) -> str:
        """
        Obtiene una vista previa del texto extraído.
        
        Args:
            max_chars: Número máximo de caracteres a mostrar
            
        Returns:
            Vista previa del texto
        """
        if not self.text_content:
            self.extract_text()
        
        if len(self.text_content) <= max_chars:
            return self.text_content
        else:
            return self.text_content[:max_chars] + "..."
    
    def search_text(self, pattern: str, case_sensitive: bool = False) -> List[str]:
        """
        Busca un patrón específico en el texto del PDF.
        
        Args:
            pattern: Patrón a buscar (puede ser regex)
            case_sensitive: Si la búsqueda es sensible a mayúsculas
            
        Returns:
            Lista de coincidencias encontradas
        """
        if not self.text_content:
            self.extract_text()
        
        flags = 0 if case_sensitive else re.IGNORECASE
        matches = re.findall(pattern, self.text_content, flags)
        
        return matches


def test_pdf_extractor():
    """Función de prueba para el extractor de PDF."""
    # Esta función se puede usar para probar el módulo
    print("Módulo PDFExtractor cargado correctamente.")
    print("Para usar: extractor = PDFExtractor('ruta_archivo.pdf')")
    print("Métodos disponibles:")
    print("- extract_text(): Extrae todo el texto")
    print("- extract_employee_names(): Extrae nombres de empleados")
    print("- extract_cedulas(): Extrae números de cédula")
    print("- extract_employees_data(): Extrae datos completos")


if __name__ == "__main__":
    test_pdf_extractor()