import pandas as pd

# Crear datos de ejemplo
data = {
    'nombre': ['Maria Clara Trujillo Perez', 'Juan Carlos Ramirez Lopez'],
    'cedula': ['12345678', '23456789'],
    'centro_costo': ['VENTAS', 'CONTABILIDAD']
}

df = pd.DataFrame(data)

# Guardar como Excel
df.to_excel('examples/empleados_ejemplo.xlsx', index=False)
print("Archivo Excel creado: examples/empleados_ejemplo.xlsx")
print(df)