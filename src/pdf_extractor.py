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
        Busca nombres después de "Nombre del afiliado" y alrededor de "Cédula".
        
        Returns:
            Lista de nombres de empleados encontrados
        """
        if not self.text_content:
            self.extract_text()
        
        names = []
        
        # Patrón 1: Buscar después de "Nombre del afiliado"
        pattern1 = r'Nombre\s+del\s+afiliado[:\s]*([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\s]+?)(?=\n|Cédula|C\.C|Documento|$)'
        matches1 = re.findall(pattern1, self.text_content, re.IGNORECASE)
        
        for match in matches1:
            clean_name = match.strip()
            if len(clean_name) > 3:  # Nombre mínimo
                names.append(clean_name)
        
        # Patrón 2: Buscar a la izquierda de "Cédula"
        # Formato: "NOMBRE APELLIDO    Cédula    1234567"
        pattern2 = r'([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\s]+?)\s+Cédula\s+(\d+)'
        matches2 = re.findall(pattern2, self.text_content, re.IGNORECASE)
        
        for match in matches2:
            clean_name = match[0].strip()
            if len(clean_name) > 3:  # Nombre mínimo
                names.append(clean_name)
        
        # Patrón 3: Buscar nombres con formato más general cerca de cédulas
        lines = self.text_content.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'cédula|cedula|c\.c|documento', line, re.IGNORECASE):
                # Buscar en la línea anterior
                if i > 0:
                    prev_line = lines[i-1].strip()
                    name_match = re.search(r'^([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\s]+?)$', prev_line)
                    if name_match and len(name_match.group(1)) > 3:
                        names.append(name_match.group(1).strip())
                
                # Buscar en la misma línea (antes de cédula)
                name_in_line = re.search(r'^([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\s]+?)\s+(?:cédula|cedula|c\.c)', line, re.IGNORECASE)
                if name_in_line and len(name_in_line.group(1)) > 3:
                    names.append(name_in_line.group(1).strip())
        
        # Limpiar y filtrar nombres
        filtered_names = []
        excluded_words = {'Factura', 'Empresa', 'Cliente', 'Total', 'Fecha', 'Número', 
                         'Descripción', 'Cantidad', 'Precio', 'Valor', 'Descuento',
                         'Impuesto', 'Base', 'Tarifa', 'Código', 'Producto', 'Servicio',
                         'Nombre', 'Afiliado', 'Del', 'Cédula', 'Documento'}
        
        for name in names:
            # Verificar que no sea una palabra excluida
            if not any(word.upper() in name.upper() for word in excluded_words):
                # Verificar que tenga al menos 2 palabras o sea un nombre compuesto
                if len(name.split()) >= 2 or len(name) > 10:
                    filtered_names.append(name.strip())
        
        # Eliminar duplicados manteniendo el orden
        unique_names = list(dict.fromkeys(filtered_names))
        
        return unique_names
        
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
        Extrae nombres y cédulas del PDF, asociándolos correctamente.
        
        Returns:
            Lista de diccionarios con datos de empleados
        """
        # Extraer nombres y cédulas por separado
        names = self.extract_employee_names()
        cedulas = self.extract_cedulas()
        
        print(f"📄 PDF - Nombres extraídos: {len(names)}")
        for i, name in enumerate(names[:5], 1):  # Mostrar primeros 5
            print(f"   {i}. '{name}'")
        
        print(f"📄 PDF - Cédulas extraídas: {len(cedulas)}")
        for i, cedula in enumerate(cedulas[:5], 1):  # Mostrar primeras 5
            print(f"   {i}. '{cedula}'")
        
        employees = []
        
        # Intentar asociar nombres y cédulas
        if len(names) == len(cedulas):
            # Si hay igual cantidad, asociar por posición
            print("✅ Asociando nombres y cédulas por posición (cantidades iguales)")
            for i, name in enumerate(names):
                employees.append({
                    'nombre': name,
                    'cedula': cedulas[i],
                    'centro_costo': ''  # Se llenará desde el Excel
                })
        else:
            # Si no coinciden las cantidades, intentar asociación por proximidad en el texto
            print("🔍 Asociando nombres y cédulas por proximidad en el texto")
            
            # Buscar asociaciones directas en el texto
            text_lines = self.text_content.split('\n')
            used_names = set()
            used_cedulas = set()
            
            for line in text_lines:
                # Buscar líneas que contengan tanto un nombre como una cédula
                for name in names:
                    for cedula in cedulas:
                        if name in line and cedula in line and name not in used_names and cedula not in used_cedulas:
                            employees.append({
                                'nombre': name,
                                'cedula': cedula,
                                'centro_costo': ''
                            })
                            used_names.add(name)
                            used_cedulas.add(cedula)
                            print(f"   ✅ Asociado: '{name}' -> {cedula}")
                            break
            
            # Agregar cédulas restantes sin nombre
            for cedula in cedulas:
                if cedula not in used_cedulas:
                    employees.append({
                        'nombre': '',  # Sin nombre, se obtendrá del Excel si es posible
                        'cedula': cedula,
                        'centro_costo': ''
                    })
                    print(f"   ⚠️  Cédula sin nombre asociado: {cedula}")
        
        self.employees_data = employees
        print(f"📋 Total empleados procesados: {len(employees)}")
        
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