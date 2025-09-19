import pandas as pd
import os

# Crear directorio examples si no existe
os.makedirs('examples', exist_ok=True)

# Crear datos de ejemplo
data = {
    'Nombre': [
        'Juan Carlos Pérez Martínez',
        'María Fernanda García López', 
        'Carlos Eduardo Rodríguez Silva',
        'Ana Lucía Hernández Gómez',
        'Luis Miguel Torres Vargas',
        'Carmen Elena Morales Castro',
        'Diego Alejandro Ruiz Mendoza',
        'Sandra Patricia Jiménez Rojas',
        'Fernando José Castillo Herrera',
        'Claudia Isabel Ramírez Ortega'
    ],
    'Cedula': [
        '12345678',
        '23456789',
        '34567890', 
        '45678901',
        '56789012',
        '67890123',
        '78901234',
        '89012345',
        '90123456',
        '01234567'
    ],
    'Centro_de_Costo': [
        'VENTAS',
        'ADMINISTRACION',
        'PRODUCCION',
        'CONTABILIDAD', 
        'SISTEMAS',
        'MARKETING',
        'LOGISTICA',
        'CALIDAD',
        'RECURSOS_HUMANOS',
        'GERENCIA'
    ],
    'Departamento': [
        'Comercial',
        'Recursos Humanos',
        'Manufactura',
        'Finanzas',
        'Tecnología',
        'Comercial',
        'Operaciones',
        'Producción',
        'Administración',
        'Dirección'
    ]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar como Excel
excel_path = 'examples/empleados_ejemplo.xlsx'
df.to_excel(excel_path, index=False, sheet_name='Empleados')

print(f"Archivo Excel creado: {excel_path}")
print(f"Total de empleados: {len(df)}")
print("\nPrimeras 3 filas:")
print(df.head(3))