"""
Módulo para generar nuevas páginas PDF con tablas de datos consolidados y fusionar con el PDF original.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
from typing import List, Dict, Optional
import os
from datetime import datetime


class PDFGenerator:
    """Clase para generar PDFs con tablas de datos consolidados."""
    
    def __init__(self):
        """Inicializa el generador de PDF."""
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
    
    def _create_custom_styles(self) -> Dict:
        """
        Crea estilos personalizados para el documento.
        
        Returns:
            Diccionario con estilos personalizados
        """
        custom_styles = {}
        
        # Estilo para título principal
        custom_styles['title'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.darkblue
        )
        
        # Estilo para subtítulos
        custom_styles['subtitle'] = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=20,
            textColor=colors.darkblue
        )
        
        # Estilo para texto normal
        custom_styles['normal'] = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12
        )
        
        return custom_styles
    
    def create_data_table(self, data: List[Dict[str, str]], 
                         include_confidence: bool = False) -> Table:
        """
        Crea una tabla con los datos consolidados.
        
        Args:
            data: Lista de diccionarios con datos de empleados
            include_confidence: Si incluir columna de confianza
            
        Returns:
            Objeto Table de reportlab
        """
        if not data:
            # Tabla vacía si no hay datos
            table_data = [["No se encontraron datos de empleados"]]
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            return table
        
        # Encabezados de la tabla
        if include_confidence:
            headers = ["Nombre Empleado", "Cédula", "Centro de Costo", "Estado", "Confianza"]
        else:
            headers = ["Nombre Empleado", "Cédula", "Centro de Costo", "Estado"]
        
        # Crear datos de la tabla
        table_data = [headers]
        
        for emp in data:
            row = [
                emp.get('nombre', ''),
                emp.get('cedula', ''),
                emp.get('centro_costo', ''),
                emp.get('estado_match', '')
            ]
            
            if include_confidence:
                row.append(emp.get('confianza', ''))
            
            table_data.append(row)
        
        # Crear tabla
        table = Table(table_data, repeatRows=1)
        
        # Estilo de la tabla
        style = [
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternar colores de filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey])
        ]
        
        # Colorear filas según el estado del match
        for i, emp in enumerate(data, 1):
            estado = emp.get('estado_match', '').lower()
            if 'no encontrado' in estado:
                style.append(('BACKGROUND', (0, i), (-1, i), colors.lightcoral))
            elif 'encontrado' in estado:
                style.append(('BACKGROUND', (0, i), (-1, i), colors.lightgreen))
        
        table.setStyle(TableStyle(style))
        
        return table
    
    def create_statistics_table(self, statistics: Dict) -> Table:
        """
        Crea una tabla con estadísticas del matching.
        
        Args:
            statistics: Diccionario con estadísticas
            
        Returns:
            Objeto Table con estadísticas
        """
        stats_data = [
            ["Estadística", "Valor"],
            ["Total de empleados en PDF", str(statistics.get('total_matched', 0) + statistics.get('total_unmatched', 0))],
            ["Empleados encontrados", str(statistics.get('total_matched', 0))],
            ["Empleados no encontrados", str(statistics.get('total_unmatched', 0))],
            ["Tasa de éxito", f"{statistics.get('match_rate', 0):.1%}"]
        ]
        
        table = Table(stats_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def generate_consolidation_pdf(self, consolidated_data: List[Dict[str, str]], 
                                 statistics: Dict, 
                                 output_path: str,
                                 title: str = "Centros de Costo - Facturación") -> str:
        """
        Genera un PDF nuevo con los datos consolidados.
        
        Args:
            consolidated_data: Datos consolidados de empleados
            statistics: Estadísticas del matching
            output_path: Ruta donde guardar el PDF
            title: Título del documento
            
        Returns:
            Ruta del archivo generado
        """
        # Crear documento
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Elementos del documento
        story = []
        
        # Título principal
        title_para = Paragraph(title, self.custom_styles['title'])
        story.append(title_para)
        story.append(Spacer(1, 20))
        
        # Información del documento
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        info_text = f"<b>Fecha de generación:</b> {date_str}<br/>"
        info_text += f"<b>Total de empleados procesados:</b> {len(consolidated_data)}"
        info_para = Paragraph(info_text, self.custom_styles['normal'])
        story.append(info_para)
        story.append(Spacer(1, 20))
        
        # Estadísticas

        # --- Sección de estadísticas comentada para no mostrar en el PDF ---
        # if statistics:
        #     stats_title = Paragraph("Estadísticas del Procesamiento", self.custom_styles['subtitle'])
        #     story.append(stats_title)
        #     story.append(Spacer(1, 10))
        #     
        #     stats_table = self.create_statistics_table(statistics)
        #     story.append(stats_table)
        #     story.append(Spacer(1, 30))
        
        # Tabla principal de datos (solo empleados encontrados)
        if consolidated_data:
            data_title = Paragraph("Empleados Encontrados - Centros de Costo Asignados", self.custom_styles['subtitle'])
            story.append(data_title)
            story.append(Spacer(1, 15))
            
            # Crear y agregar tabla de datos
            data_table = self.create_data_table(consolidated_data, include_confidence=True)
            story.append(data_table)
            
            # Información adicional si hay empleados no encontrados
            # --- Sección de nota de empleados no encontrados comentada ---
            # if statistics and statistics.get('total_unmatched', 0) > 0:
            #     story.append(Spacer(1, 20))
            #     unmatched_note = Paragraph(
            #         f"<b>Nota:</b> {statistics['total_unmatched']} empleados no fueron encontrados en la base de datos. "
            #         "Consulte el reporte detallado para ver sugerencias de matching manual.",
            #         self.custom_styles['normal']
            #     )
            #     story.append(unmatched_note)
        else:
            # Si no hay empleados encontrados
            data_title = Paragraph("Resultados del Procesamiento", self.custom_styles['subtitle'])
            story.append(data_title)
            story.append(Spacer(1, 15))
            
            no_data_text = """
            <b>No se encontraron coincidencias automáticas.</b><br/>
            Ningún empleado del PDF pudo ser identificado automáticamente en la base de datos Excel.<br/>
            Revise los datos de entrada y considere ajustar el umbral de similitud.
            """
            no_data_para = Paragraph(no_data_text.strip(), self.custom_styles['normal'])
            story.append(no_data_para)
        
        # Notas adicionales
    # --- Sección de notas comentada ---
    # story.append(Spacer(1, 30))
    # notes_title = Paragraph("Notas", self.custom_styles['subtitle'])
    # story.append(notes_title)
    # 
    # notes_text = """
    # • <b>Estado 'Encontrado (cedula)':</b> Empleado encontrado por coincidencia exacta de cédula<br/>
    # • <b>Estado 'Encontrado (nombre)':</b> Empleado encontrado por similitud de nombre<br/>
    # • <b>Estado 'No encontrado':</b> Empleado no pudo ser identificado en la base de datos<br/>
    # • <b>Confianza:</b> Nivel de certeza del matching (1.00 = coincidencia exacta, 0.70+ = muy probable)
    # """
    # notes_para = Paragraph(notes_text, self.custom_styles['normal'])
    # story.append(notes_para)
        
        # Construir documento
        doc.build(story)
        
        return output_path
    
    def merge_pdfs(self, original_pdf_path: str, new_pdf_path: str, 
                  output_path: str) -> str:
        """
        Fusiona el PDF original con el PDF de datos consolidados.
        
        Args:
            original_pdf_path: Ruta del PDF original
            new_pdf_path: Ruta del PDF con datos consolidados
            output_path: Ruta del PDF final fusionado
            
        Returns:
            Ruta del archivo fusionado
        """
        try:
            # Leer PDFs
            original_reader = PdfReader(original_pdf_path)
            new_reader = PdfReader(new_pdf_path)
            
            # Crear writer
            writer = PdfWriter()
            
            # Agregar todas las páginas del PDF original
            for page in original_reader.pages:
                writer.add_page(page)
            
            # Agregar todas las páginas del PDF nuevo
            for page in new_reader.pages:
                writer.add_page(page)
            
            # Escribir archivo fusionado
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error al fusionar PDFs: {str(e)}")
    
    def create_complete_pdf(self, original_pdf_path: str, 
                          consolidated_data: List[Dict[str, str]], 
                          statistics: Dict,
                          output_directory: str,
                          filename_prefix: str = "facturacion_completa") -> str:
        """
        Crea el PDF completo fusionando el original con los datos consolidados.
        
        Args:
            original_pdf_path: Ruta del PDF original
            consolidated_data: Datos consolidados
            statistics: Estadísticas del matching
            output_directory: Directorio donde guardar el resultado
            filename_prefix: Prefijo para el nombre del archivo
            
        Returns:
            Ruta del PDF final generado
        """
        # Crear nombres de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_pdf_name = f"temp_consolidation_{timestamp}.pdf"
        final_pdf_name = f"{filename_prefix}_{timestamp}.pdf"
        
        temp_pdf_path = os.path.join(output_directory, temp_pdf_name)
        final_pdf_path = os.path.join(output_directory, final_pdf_name)
        
        try:
            # Generar PDF con datos consolidados
            self.generate_consolidation_pdf(
                consolidated_data, 
                statistics, 
                temp_pdf_path,
                "Centros de Costo - Facturación Electrónica"
            )
            
            # Fusionar con PDF original
            merged_path = self.merge_pdfs(original_pdf_path, temp_pdf_path, final_pdf_path)
            
            # Limpiar archivo temporal
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            
            return merged_path
            
        except Exception as e:
            # Limpiar archivos temporales en caso de error
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            raise Exception(f"Error al crear PDF completo: {str(e)}")
    
    def create_standalone_report(self, consolidated_data: List[Dict[str, str]], 
                               statistics: Dict,
                               output_path: str) -> str:
        """
        Crea un reporte standalone sin fusionar con el PDF original.
        
        Args:
            consolidated_data: Datos consolidados
            statistics: Estadísticas del matching
            output_path: Ruta donde guardar el reporte
            
        Returns:
            Ruta del archivo generado
        """
        return self.generate_consolidation_pdf(
            consolidated_data,
            statistics,
            output_path,
            "Reporte de Centros de Costo"
        )


def test_pdf_generator():
    """Función de prueba para el generador de PDF."""
    print("Módulo PDFGenerator cargado correctamente.")
    print("Para usar:")
    print("1. generator = PDFGenerator()")
    print("2. generator.create_complete_pdf(original_pdf, data, stats, output_dir)")
    print("Métodos disponibles:")
    print("- create_complete_pdf(): Crea PDF completo fusionado")
    print("- create_standalone_report(): Crea reporte independiente")
    print("- merge_pdfs(): Fusiona dos PDFs")


if __name__ == "__main__":
    test_pdf_generator()