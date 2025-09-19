"""
Paquete principal de la aplicación de facturación.
"""

from .pdf_extractor import PDFExtractor
from .excel_processor import ExcelProcessor
from .data_matcher import DataMatcher
from .pdf_generator import PDFGenerator
from .ui import MainApplication, create_gui_app

__version__ = "1.0.0"
__author__ = "App Facturación Team"

__all__ = [
    'PDFExtractor',
    'ExcelProcessor', 
    'DataMatcher',
    'PDFGenerator',
    'MainApplication',
    'create_gui_app'
]