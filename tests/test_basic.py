"""
Tests básicos para la aplicación de facturación.
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.pdf_extractor import PDFExtractor
from src.excel_processor import ExcelProcessor
from src.data_matcher import DataMatcher


class TestPDFExtractor(unittest.TestCase):
    """Tests para el extractor de PDF."""
    
    def test_normalize_text_functionality(self):
        """Test de funcionalidad básica sin archivos."""
        # Test de normalización de texto (método interno)
        from src.data_matcher import DataMatcher
        
        matcher = DataMatcher(None, None)
        
        # Test normalización básica
        result = matcher.normalize_text("José María Pérez")
        expected = "jose maria perez"
        self.assertEqual(result, expected)
        
        # Test con espacios extra
        result = matcher.normalize_text("  Juan   Carlos  ")
        expected = "juan carlos"
        self.assertEqual(result, expected)


class TestExcelProcessor(unittest.TestCase):
    """Tests para el procesador de Excel."""
    
    def test_column_detection(self):
        """Test de detección de columnas sin archivo real."""
        # Crear datos de prueba en memoria
        import pandas as pd
        
        # Simular datos de empleados
        test_data = {
            'Nombre Completo': ['Juan Pérez', 'María García'],
            'CC': ['12345678', '87654321'],
            'Centro de Costo': ['Ventas', 'Administración']
        }
        
        df = pd.DataFrame(test_data)
        
        # Crear instancia y asignar dataframe manualmente para testing
        processor = ExcelProcessor("")  # Path vacío para testing
        processor.dataframe = df
        
        # Test detección de columnas
        mapping = processor.detect_columns()
        
        self.assertIn('nombre', mapping)
        self.assertIn('cedula', mapping)
        self.assertIn('centro_costo', mapping)


class TestDataMatcher(unittest.TestCase):
    """Tests para el matcher de datos."""
    
    def test_name_similarity(self):
        """Test de cálculo de similitud de nombres."""
        from src.data_matcher import DataMatcher
        
        matcher = DataMatcher(None, None)
        
        # Test coincidencia exacta
        similarity = matcher.calculate_name_similarity("Juan Pérez", "Juan Pérez")
        self.assertEqual(similarity, 1.0)
        
        # Test similitud alta
        similarity = matcher.calculate_name_similarity("Juan Pérez", "Juan Perez")
        self.assertGreater(similarity, 0.8)
        
        # Test similitud baja
        similarity = matcher.calculate_name_similarity("Juan Pérez", "María García")
        self.assertLess(similarity, 0.5)
        
        # Test con nombres vacíos
        similarity = matcher.calculate_name_similarity("", "Juan Pérez")
        self.assertEqual(similarity, 0.0)


if __name__ == '__main__':
    print("Ejecutando tests básicos...")
    unittest.main(verbosity=2)