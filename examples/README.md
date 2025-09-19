# Archivos de Ejemplo

## empleados_ejemplo.csv
Archivo CSV con datos de empleados de ejemplo que se puede convertir a Excel.

Contiene las siguientes columnas:
- Nombre: Nombre completo del empleado
- Cedula: Número de identificación
- Centro_de_Costo: Centro de costo asignado
- Departamento: Departamento al que pertenece

## Cómo usar los archivos de ejemplo

1. **Convertir CSV a Excel:**
   ```python
   import pandas as pd
   df = pd.read_csv('empleados_ejemplo.csv')
   df.to_excel('empleados_ejemplo.xlsx', index=False)
   ```

2. **Crear un PDF de prueba:**
   Para probar la aplicación, necesitará crear un PDF que contenga algunos de los nombres o cédulas de los empleados listados en el archivo Excel.

## Empleados de ejemplo incluidos:

1. Juan Carlos Pérez Martínez - 12345678 - VENTAS
2. María Fernanda García López - 23456789 - ADMINISTRACION  
3. Carlos Eduardo Rodríguez Silva - 34567890 - PRODUCCION
4. Ana Lucía Hernández Gómez - 45678901 - CONTABILIDAD
5. Luis Miguel Torres Vargas - 56789012 - SISTEMAS
6. Carmen Elena Morales Castro - 67890123 - MARKETING
7. Diego Alejandro Ruiz Mendoza - 78901234 - LOGISTICA
8. Sandra Patricia Jiménez Rojas - 89012345 - CALIDAD
9. Fernando José Castillo Herrera - 90123456 - RECURSOS_HUMANOS
10. Claudia Isabel Ramírez Ortega - 01234567 - GERENCIA

## Uso de la aplicación

Para probar la aplicación con estos datos:

1. Cree un PDF que contenga algunos de estos nombres o cédulas
2. Use el archivo CSV (o conviértalo a Excel)
3. Ejecute la aplicación:
   ```bash
   python main.py
   ```
   o desde línea de comandos:
   ```bash
   python main.py --cli archivo.pdf empleados_ejemplo.xlsx
   ```