"""
Módulo para procesar archivos Excel con datos de empleados y centros de costo.
"""

import pandas as pd
from typing import List, Dict, Optional, Tuple
import re


class ExcelProcessor:
    """Clase para procesar archivos Excel con datos de empleados."""
    
    def __init__(self, excel_path: str):
        """
        Inicializa el procesador con la ruta del archivo Excel.
        
        Args:
            excel_path: Ruta al archivo Excel
        """
        self.excel_path = excel_path
        self.dataframe = None
        self.column_mapping = {}
    
    def load_excel(self, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Carga el archivo Excel en un DataFrame.
        
        Args:
            sheet_name: Nombre de la hoja a cargar (None para la primera)
            
        Returns:
            DataFrame con los datos cargados
        """
        try:
            if sheet_name:
                self.dataframe = pd.read_excel(self.excel_path, sheet_name=sheet_name)
            else:
                self.dataframe = pd.read_excel(self.excel_path)
            
            # Limpiar nombres de columnas (remover espacios extra, etc.)
            self.dataframe.columns = self.dataframe.columns.str.strip()
            
            return self.dataframe
            
        except Exception as e:
            raise Exception(f"Error al cargar el archivo Excel: {str(e)}")
    
    def detect_columns(self) -> Dict[str, str]:
        """
        Detecta automáticamente las columnas relevantes en el Excel.
        
        Returns:
            Diccionario con mapeo de tipos de datos a nombres de columnas
        """
        if self.dataframe is None:
            self.load_excel()
        
        column_mapping = {
            'nombre': None,
            'cedula': None,
            'centro_costo': None
        }
        
        # Patrones para detectar columnas
        patterns = {
            'nombre': [
                r'^nombre$', r'^name$', r'nombre.*completo', r'full.*name',
                r'apellido', r'surname'
            ],
            'cedula': [
                r'cedula', r'cédula', r'cc', r'c\.c', r'identificacion', 
                r'identificación', r'documento', r'id', r'dni'
            ],
            'centro_costo': [
                r'centro.*costo', r'centro.*de.*costo', r'cost.*center',
                r'centro', r'costo', r'area', r'área', r'departamento',
                r'division', r'división', r'unidad', r'centrocostos'
            ]
        }
        
        for column in self.dataframe.columns:
            column_lower = column.lower().strip()
            
            for data_type, pattern_list in patterns.items():
                for pattern in pattern_list:
                    if re.search(pattern, column_lower):
                        # Verificación especial para nombres: evitar columnas de códigos
                        if data_type == 'nombre':
                            # Excluir columnas que contengan "codigo", "code", "id", "num"
                            if re.search(r'codigo|code|^id$|num', column_lower):
                                continue  # Saltar esta columna
                            
                            # Priorizar columnas que digan exactamente "nombre"
                            if column_lower == 'nombre' or 'nombre' in column_lower:
                                column_mapping[data_type] = column
                                print(f"✅ Detectado (prioritario): '{column}' -> {data_type}")
                                break
                        
                        if column_mapping[data_type] is None:
                            column_mapping[data_type] = column
                            print(f"✅ Detectado: '{column}' -> {data_type}")
                        break
        
        # Mostrar resultado de la detección
        print(f"📊 Detección de columnas completada: {column_mapping}")
        
        # Si no se pudieron detectar las columnas automáticamente,
        # intentar por posición (asumiendo orden: cedula, nombre, centro_costo)
        if not all(column_mapping.values()):
            missing = [k for k, v in column_mapping.items() if v is None]
            print(f"⚠️  No se detectaron algunas columnas: {missing}")
            
            columns = list(self.dataframe.columns)
            if len(columns) >= 3:
                print("🔧 Usando detección por posición:")
                print(f"   Columna 1 ('{columns[0]}') -> cédula")
                print(f"   Columna 2 ('{columns[1]}') -> nombre") 
                print(f"   Columna 3 ('{columns[2]}') -> centro_costo")
                
                column_mapping = {
                    'cedula': columns[0],
                    'nombre': columns[1],
                    'centro_costo': columns[2]
                }
        
        self.column_mapping = column_mapping
        return column_mapping
    
    def set_column_mapping(self, nombre_col: str = None, cedula_col: str = None, 
                          centro_costo_col: str = None):
        """
        Establece manualmente el mapeo de columnas.
        
        Args:
            nombre_col: Nombre de la columna de nombres
            cedula_col: Nombre de la columna de cédulas
            centro_costo_col: Nombre de la columna de centros de costo
        """
        if nombre_col:
            self.column_mapping['nombre'] = nombre_col
        if cedula_col:
            self.column_mapping['cedula'] = cedula_col
        if centro_costo_col:
            self.column_mapping['centro_costo'] = centro_costo_col
    
    def search_by_name(self, name: str) -> List[Dict[str, str]]:
        """
        Busca empleados por nombre.
        
        Args:
            name: Nombre a buscar
            
        Returns:
            Lista de empleados encontrados
        """
        if self.dataframe is None:
            self.load_excel()
        
        if not self.column_mapping:
            self.detect_columns()
        
        if not self.column_mapping['nombre']:
            raise Exception("No se pudo detectar la columna de nombres")
        
        # Busqueda flexible (parcial, sin distinción de mayúsculas)
        name_col = self.column_mapping['nombre']
        mask = self.dataframe[name_col].str.contains(name, case=False, na=False)
        
        results = []
        for _, row in self.dataframe[mask].iterrows():
            employee = {
                'nombre': str(row[name_col]) if pd.notna(row[name_col]) else '',
                'cedula': '',
                'centro_costo': ''
            }
            
            if self.column_mapping['cedula'] and pd.notna(row[self.column_mapping['cedula']]):
                employee['cedula'] = str(row[self.column_mapping['cedula']])
            
            if self.column_mapping['centro_costo'] and pd.notna(row[self.column_mapping['centro_costo']]):
                employee['centro_costo'] = str(row[self.column_mapping['centro_costo']])
            
            results.append(employee)
        
        return results
    
    def search_by_cedula(self, cedula: str) -> List[Dict[str, str]]:
        """
        Busca empleados por número de cédula.
        
        Args:
            cedula: Número de cédula a buscar
            
        Returns:
            Lista de empleados encontrados
        """
        if self.dataframe is None:
            self.load_excel()
        
        if not self.column_mapping:
            self.detect_columns()
        
        if not self.column_mapping['cedula']:
            raise Exception("No se pudo detectar la columna de cédulas")
        
        # Limpiar cédula de búsqueda (remover puntos, espacios, etc.)
        clean_cedula = re.sub(r'[^\d]', '', str(cedula))
        
        cedula_col = self.column_mapping['cedula']
        
        # Buscar coincidencias exactas o parciales
        results = []
        for _, row in self.dataframe.iterrows():
            if pd.notna(row[cedula_col]):
                row_cedula = re.sub(r'[^\d]', '', str(row[cedula_col]))
                if clean_cedula == row_cedula:
                    employee = {
                        'cedula': str(row[cedula_col]),
                        'nombre': '',
                        'centro_costo': ''
                    }
                    
                    if self.column_mapping['nombre'] and pd.notna(row[self.column_mapping['nombre']]):
                        employee['nombre'] = str(row[self.column_mapping['nombre']])
                    
                    if self.column_mapping['centro_costo'] and pd.notna(row[self.column_mapping['centro_costo']]):
                        employee['centro_costo'] = str(row[self.column_mapping['centro_costo']])
                    
                    results.append(employee)
        
        return results
    
    def search_employee(self, name: str = None, cedula: str = None) -> List[Dict[str, str]]:
        """
        Busca empleados por nombre y/o cédula.
        
        Args:
            name: Nombre a buscar (opcional)
            cedula: Cédula a buscar (opcional)
            
        Returns:
            Lista de empleados encontrados
        """
        results = []
        
        if cedula:
            results.extend(self.search_by_cedula(cedula))
        
        if name and not results:  # Solo buscar por nombre si no se encontró por cédula
            results.extend(self.search_by_name(name))
        
        # Eliminar duplicados
        unique_results = []
        seen = set()
        for emp in results:
            # Crear una clave única basada en nombre y cédula
            key = f"{emp.get('nombre', '')}-{emp.get('cedula', '')}"
            if key not in seen:
                seen.add(key)
                unique_results.append(emp)
        
        return unique_results
    
    def get_all_employees(self) -> List[Dict[str, str]]:
        """
        Obtiene todos los empleados del Excel.
        
        Returns:
            Lista con todos los empleados
        """
        if self.dataframe is None:
            self.load_excel()
        
        if not self.column_mapping:
            self.detect_columns()
        
        employees = []
        for _, row in self.dataframe.iterrows():
            employee = {
                'nombre': '',
                'cedula': '',
                'centro_costo': ''
            }
            
            if self.column_mapping['nombre'] and pd.notna(row[self.column_mapping['nombre']]):
                employee['nombre'] = str(row[self.column_mapping['nombre']])
            
            if self.column_mapping['cedula'] and pd.notna(row[self.column_mapping['cedula']]):
                employee['cedula'] = str(row[self.column_mapping['cedula']])
            
            if self.column_mapping['centro_costo'] and pd.notna(row[self.column_mapping['centro_costo']]):
                employee['centro_costo'] = str(row[self.column_mapping['centro_costo']])
            
            employees.append(employee)
        
        return employees
    
    def get_column_preview(self, max_rows: int = 5) -> Dict[str, List]:
        """
        Obtiene una vista previa de las columnas del Excel.
        
        Args:
            max_rows: Número máximo de filas a mostrar
            
        Returns:
            Diccionario con vista previa de cada columna
        """
        if self.dataframe is None:
            self.load_excel()
        
        preview = {}
        for column in self.dataframe.columns:
            preview[column] = self.dataframe[column].head(max_rows).tolist()
        
        return preview
    
    def get_sheet_names(self) -> List[str]:
        """
        Obtiene los nombres de todas las hojas del Excel.
        
        Returns:
            Lista con nombres de las hojas
        """
        try:
            excel_file = pd.ExcelFile(self.excel_path)
            return excel_file.sheet_names
        except Exception as e:
            raise Exception(f"Error al obtener nombres de hojas: {str(e)}")
    
    def validate_data(self) -> Dict[str, str]:
        """
        Valida la estructura de los datos del Excel.
        
        Returns:
            Diccionario con el estado de validación
        """
        if self.dataframe is None:
            self.load_excel()
        
        if not self.column_mapping:
            self.detect_columns()
        
        validation = {
            'status': 'ok',
            'issues': [],
            'columns_found': self.column_mapping,
            'total_rows': len(self.dataframe)
        }
        
        # Verificar columnas esenciales
        if not self.column_mapping['nombre'] and not self.column_mapping['cedula']:
            validation['status'] = 'error'
            validation['issues'].append('No se encontraron columnas de nombre ni cédula')
        
        if not self.column_mapping['centro_costo']:
            validation['status'] = 'warning'
            validation['issues'].append('No se encontró columna de centro de costo')
        
        # Verificar datos vacíos
        if self.column_mapping['nombre']:
            empty_names = self.dataframe[self.column_mapping['nombre']].isna().sum()
            if empty_names > 0:
                validation['issues'].append(f'{empty_names} filas con nombres vacíos')
        
        if self.column_mapping['cedula']:
            empty_cedulas = self.dataframe[self.column_mapping['cedula']].isna().sum()
            if empty_cedulas > 0:
                validation['issues'].append(f'{empty_cedulas} filas con cédulas vacías')
        
        return validation


def test_excel_processor():
    """Función de prueba para el procesador de Excel."""
    print("Módulo ExcelProcessor cargado correctamente.")
    print("Para usar: processor = ExcelProcessor('ruta_archivo.xlsx')")
    print("Métodos disponibles:")
    print("- load_excel(): Carga el archivo Excel")
    print("- detect_columns(): Detecta columnas automáticamente")
    print("- search_by_name(name): Busca por nombre")
    print("- search_by_cedula(cedula): Busca por cédula")
    print("- get_all_employees(): Obtiene todos los empleados")


if __name__ == "__main__":
    test_excel_processor()