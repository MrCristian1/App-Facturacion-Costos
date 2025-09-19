"""
Script para probar el formateo de nombres.
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_matcher import DataMatcher

def test_name_formatting():
    """Prueba la funcionalidad de formateo de nombres."""
    print("=== Prueba de Formateo de Nombres ===\n")
    
    matcher = DataMatcher(None, None)
    
    # Casos de prueba
    test_cases = [
        "TRUJILLOPEREZMARIACLARA",
        "GARCIALOPEZMARIAFERNANDA", 
        "RODRIGUEZSILVACARLOSYEDUARDO",
        "HERNANDEZGOMEZANALUCIA",
        "TORRESVARGASLUISMIGUEL",
        "MORALESCASTROCARMENELENA",
        "RUIZMENDOZADIEGOALEJANDRO",
        "JIMENEZROJASSANDRAPATRICIA",
        "CASTILLOHERRERAFERNANDOJOSE",
        "RAMIREZORTEGACLAUDIAISABEL"
    ]
    
    print("Nombres originales → Nombres formateados:")
    print("=" * 60)
    
    for nombre_original in test_cases:
        nombre_formateado = matcher.format_name(nombre_original)
        print(f"{nombre_original:<30} → {nombre_formateado}")
    
    print("\n✓ Prueba de formateo completada")

if __name__ == "__main__":
    test_name_formatting()