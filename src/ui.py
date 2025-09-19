"""
Módulo de interfaz de usuario para la aplicación de facturación.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
from typing import Optional, Callable, Dict, List
import threading


class FileSelector:
    """Clase para manejar la selección de archivos."""
    
    @staticmethod
    def select_pdf_file(title: str = "Seleccionar archivo PDF") -> Optional[str]:
        """
        Abre diálogo para seleccionar archivo PDF.
        
        Args:
            title: Título del diálogo
            
        Returns:
            Ruta del archivo seleccionado o None
        """
        return filedialog.askopenfilename(
            title=title,
            filetypes=[
                ("Archivos PDF", "*.pdf"),
                ("Todos los archivos", "*.*")
            ]
        )
    
    @staticmethod
    def select_excel_file(title: str = "Seleccionar archivo Excel") -> Optional[str]:
        """
        Abre diálogo para seleccionar archivo Excel.
        
        Args:
            title: Título del diálogo
            
        Returns:
            Ruta del archivo seleccionado o None
        """
        return filedialog.askopenfilename(
            title=title,
            filetypes=[
                ("Archivos Excel", "*.xlsx;*.xls"),
                ("Excel nuevo", "*.xlsx"),
                ("Excel antiguo", "*.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
    
    @staticmethod
    def select_output_directory(title: str = "Seleccionar directorio de salida") -> Optional[str]:
        """
        Abre diálogo para seleccionar directorio de salida.
        
        Args:
            title: Título del diálogo
            
        Returns:
            Ruta del directorio seleccionado o None
        """
        return filedialog.askdirectory(title=title)


class ProgressWindow:
    """Ventana para mostrar progreso de operaciones largas."""
    
    def __init__(self, parent, title: str = "Procesando..."):
        """
        Inicializa la ventana de progreso.
        
        Args:
            parent: Ventana padre
            title: Título de la ventana
        """
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"400x200+{x}+{y}")
        
        # Widgets
        self.setup_widgets()
        
    def setup_widgets(self):
        """Configura los widgets de la ventana."""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Etiqueta de estado
        self.status_label = ttk.Label(
            main_frame, 
            text="Iniciando procesamiento...",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=(0, 20))
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            main_frame,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 20))
        self.progress_bar.start()
        
        # Área de texto para detalles
        self.details_text = scrolledtext.ScrolledText(
            main_frame,
            height=6,
            width=50,
            font=("Courier", 9)
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
    def update_status(self, message: str):
        """
        Actualiza el mensaje de estado.
        
        Args:
            message: Nuevo mensaje de estado
        """
        self.status_label.config(text=message)
        self.window.update()
        
    def add_detail(self, detail: str):
        """
        Añade un detalle al área de texto.
        
        Args:
            detail: Detalle a añadir
        """
        self.details_text.insert(tk.END, detail + "\n")
        self.details_text.see(tk.END)
        self.window.update()
        
    def close(self):
        """Cierra la ventana de progreso."""
        self.progress_bar.stop()
        self.window.destroy()


class ResultsWindow:
    """Ventana para mostrar resultados del procesamiento."""
    
    def __init__(self, parent, results: Dict):
        """
        Inicializa la ventana de resultados.
        
        Args:
            parent: Ventana padre
            results: Diccionario con resultados del procesamiento
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Resultados del Procesamiento")
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        self.results = results
        self.setup_widgets()
        
    def setup_widgets(self):
        """Configura los widgets de la ventana."""
        # Frame principal con scrollbar
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de resumen
        self.create_summary_tab(notebook)
        
        # Pestaña de empleados encontrados
        self.create_matched_tab(notebook)
        
        # Pestaña de empleados no encontrados
        self.create_unmatched_tab(notebook)
        
        # Pestaña de sugerencias
        if self.results.get('manual_suggestions'):
            self.create_suggestions_tab(notebook)
        
        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Cerrar",
            command=self.window.destroy
        ).pack(side=tk.RIGHT)
        
    def create_summary_tab(self, notebook):
        """Crea la pestaña de resumen."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Resumen")
        
        # Estadísticas
        stats = self.results.get('statistics', {})
        
        info_text = f"""
RESUMEN DEL PROCESAMIENTO

Total de empleados procesados: {stats.get('total_matched', 0) + stats.get('total_unmatched', 0)}
Empleados encontrados: {stats.get('total_matched', 0)}
Empleados no encontrados: {stats.get('total_unmatched', 0)}
Tasa de éxito: {stats.get('match_rate', 0):.1%}

El procesamiento se ha completado exitosamente.
Se ha generado un PDF con los empleados encontrados y sus centros de costo.

NOTA: En la tabla "Empleados Encontrados" del PDF solo aparecen los empleados 
que fueron identificados exitosamente en la base de datos Excel.
Los empleados no encontrados se muestran en secciones separadas del reporte.
        """
        
        text_widget = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=20,
            pady=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, info_text.strip())
        text_widget.config(state=tk.DISABLED)
        
    def create_matched_tab(self, notebook):
        """Crea la pestaña de empleados encontrados."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"Encontrados ({len(self.results.get('matched_employees', []))})")
        
        # Treeview para mostrar datos - SOLO DATOS DEL EXCEL
        columns = ("Nombre", "Cédula", "Centro de Costo", "Método", "Confianza")
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Agregar datos - SOLO DEL EXCEL
        for emp in self.results.get('matched_employees', []):
            # SOLO usar el nombre del Excel
            nombre_excel = emp.get('nombre_excel', '')
            
            tree.insert('', tk.END, values=(
                nombre_excel,  # SOLO nombre del Excel
                emp.get('cedula', ''),
                emp.get('centro_costo', ''),
                emp.get('match_method', ''),
                f"{emp.get('confidence', 0):.2f}"
            ))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
        
    def create_unmatched_tab(self, notebook):
        """Crea la pestaña de empleados no encontrados."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"No encontrados ({len(self.results.get('unmatched_employees', []))})")
        
        if not self.results.get('unmatched_employees'):
            label = ttk.Label(frame, text="¡Excelente! Todos los empleados fueron encontrados.", 
                            font=("Arial", 12))
            label.pack(expand=True)
            return
        
        # Treeview para mostrar datos
        columns = ("Nombre", "Cédula")
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        # Agregar datos
        for emp in self.results.get('unmatched_employees', []):
            tree.insert('', tk.END, values=(
                emp.get('nombre', ''),
                emp.get('cedula', '')
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
    def create_suggestions_tab(self, notebook):
        """Crea la pestaña de sugerencias manuales."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Sugerencias")
        
        # Texto explicativo
        label = ttk.Label(
            frame, 
            text="Sugerencias para empleados no encontrados automáticamente:",
            font=("Arial", 10, "bold")
        )
        label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Área de texto para sugerencias
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Agregar sugerencias
        suggestions = self.results.get('manual_suggestions', {})
        for pdf_name, excel_matches in suggestions.items():
            text_widget.insert(tk.END, f"\\nEmpleado PDF: {pdf_name}\\n")
            text_widget.insert(tk.END, "Posibles coincidencias en Excel:\\n")
            
            for i, match in enumerate(excel_matches, 1):
                text_widget.insert(tk.END, f"  {i}. {match['nombre_excel']} ")
                text_widget.insert(tk.END, f"(Cédula: {match['cedula_excel']}) ")
                text_widget.insert(tk.END, f"- Centro: {match['centro_costo']} ")
                text_widget.insert(tk.END, f"- Similitud: {match['similitud']}\\n")
            
            text_widget.insert(tk.END, "\\n" + "-"*50 + "\\n")
        
        text_widget.config(state=tk.DISABLED)


class MainApplication:
    """Aplicación principal con interfaz gráfica."""
    
    def __init__(self):
        """Inicializa la aplicación principal."""
        self.root = tk.Tk()
        self.root.title("App Facturación - Centros de Costo")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.pdf_path = tk.StringVar()
        self.excel_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        # Configurar directorio de salida por defecto
        self.output_dir.set(os.path.expanduser("~/Documents"))
        
        self.setup_ui()
        self.center_window()
        
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="App Facturación - Automatización de Centros de Costo",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Descripción
        desc_text = """
Esta aplicación automatiza el proceso de añadir centros de costo a PDFs de facturación
mediante búsqueda en bases de datos Excel de empleados.
        """
        desc_label = ttk.Label(main_frame, text=desc_text.strip(), justify=tk.CENTER)
        desc_label.pack(pady=(0, 30))
        
        # Sección de archivos
        self.create_file_selection_section(main_frame)
        
        # Configuración adicional
        self.create_settings_section(main_frame)
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para procesar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(20, 0))
        
    def create_file_selection_section(self, parent):
        """Crea la sección de selección de archivos."""
        # Frame para selección de archivos
        files_frame = ttk.LabelFrame(parent, text="Selección de Archivos", padding="10")
        files_frame.pack(fill=tk.X, pady=(0, 20))
        
        # PDF de facturación
        pdf_frame = ttk.Frame(files_frame)
        pdf_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(pdf_frame, text="PDF de Facturación:").pack(anchor=tk.W)
        pdf_entry_frame = ttk.Frame(pdf_frame)
        pdf_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        pdf_entry = ttk.Entry(pdf_entry_frame, textvariable=self.pdf_path, state="readonly")
        pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            pdf_entry_frame,
            text="Examinar...",
            command=self.select_pdf_file,
            width=12
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Excel de empleados
        excel_frame = ttk.Frame(files_frame)
        excel_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(excel_frame, text="Excel de Empleados:").pack(anchor=tk.W)
        excel_entry_frame = ttk.Frame(excel_frame)
        excel_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        excel_entry = ttk.Entry(excel_entry_frame, textvariable=self.excel_path, state="readonly")
        excel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            excel_entry_frame,
            text="Examinar...",
            command=self.select_excel_file,
            width=12
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Directorio de salida
        output_frame = ttk.Frame(files_frame)
        output_frame.pack(fill=tk.X)
        
        ttk.Label(output_frame, text="Directorio de Salida:").pack(anchor=tk.W)
        output_entry_frame = ttk.Frame(output_frame)
        output_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        output_entry = ttk.Entry(output_entry_frame, textvariable=self.output_dir)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            output_entry_frame,
            text="Examinar...",
            command=self.select_output_directory,
            width=12
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_settings_section(self, parent):
        """Crea la sección de configuración."""
        settings_frame = ttk.LabelFrame(parent, text="Configuración", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Umbral de similitud para nombres
        similarity_frame = ttk.Frame(settings_frame)
        similarity_frame.pack(fill=tk.X)
        
        ttk.Label(similarity_frame, text="Umbral de similitud para nombres:").pack(side=tk.LEFT)
        
        self.similarity_var = tk.DoubleVar(value=0.7)
        similarity_scale = ttk.Scale(
            similarity_frame,
            from_=0.5,
            to=1.0,
            variable=self.similarity_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        similarity_scale.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.similarity_label = ttk.Label(similarity_frame, text="0.70")
        self.similarity_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Actualizar etiqueta cuando cambie el valor
        def update_similarity_label(*args):
            self.similarity_label.config(text=f"{self.similarity_var.get():.2f}")
        
        self.similarity_var.trace('w', update_similarity_label)
        
    def create_action_buttons(self, parent):
        """Crea los botones de acción."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón procesar
        self.process_button = ttk.Button(
            button_frame,
            text="Procesar Archivos",
            command=self.process_files,
            style="Accent.TButton"
        )
        self.process_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botón limpiar
        ttk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_fields
        ).pack(side=tk.RIGHT)
        
    def select_pdf_file(self):
        """Selecciona archivo PDF."""
        file_path = FileSelector.select_pdf_file()
        if file_path:
            self.pdf_path.set(file_path)
            self.status_var.set(f"PDF seleccionado: {os.path.basename(file_path)}")
            
    def select_excel_file(self):
        """Selecciona archivo Excel."""
        file_path = FileSelector.select_excel_file()
        if file_path:
            self.excel_path.set(file_path)
            self.status_var.set(f"Excel seleccionado: {os.path.basename(file_path)}")
            
    def select_output_directory(self):
        """Selecciona directorio de salida."""
        dir_path = FileSelector.select_output_directory()
        if dir_path:
            self.output_dir.set(dir_path)
            self.status_var.set(f"Directorio de salida: {dir_path}")
            
    def clear_fields(self):
        """Limpia todos los campos."""
        self.pdf_path.set("")
        self.excel_path.set("")
        self.output_dir.set(os.path.expanduser("~/Documents"))
        self.status_var.set("Campos limpiados")
        
    def validate_inputs(self) -> bool:
        """
        Valida las entradas del usuario.
        
        Returns:
            True si las entradas son válidas
        """
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Debe seleccionar un archivo PDF")
            return False
            
        if not self.excel_path.get():
            messagebox.showerror("Error", "Debe seleccionar un archivo Excel")
            return False
            
        if not self.output_dir.get():
            messagebox.showerror("Error", "Debe seleccionar un directorio de salida")
            return False
            
        if not os.path.exists(self.pdf_path.get()):
            messagebox.showerror("Error", "El archivo PDF no existe")
            return False
            
        if not os.path.exists(self.excel_path.get()):
            messagebox.showerror("Error", "El archivo Excel no existe")
            return False
            
        if not os.path.exists(self.output_dir.get()):
            messagebox.showerror("Error", "El directorio de salida no existe")
            return False
            
        return True
        
    def process_files(self):
        """Procesa los archivos seleccionados."""
        if not self.validate_inputs():
            return
            
        # Deshabilitar botón de procesar
        self.process_button.config(state=tk.DISABLED)
        
        # Ejecutar procesamiento en hilo separado
        threading.Thread(target=self._process_files_thread, daemon=True).start()
        
    def _process_files_thread(self):
        """Hilo de procesamiento de archivos."""
        try:
            # Importar módulos necesarios (importación tardía para evitar problemas de UI)
            from .pdf_extractor import PDFExtractor
            from .excel_processor import ExcelProcessor
            from .data_matcher import DataMatcher
            from .pdf_generator import PDFGenerator
            
            # Crear ventana de progreso
            progress_window = ProgressWindow(self.root, "Procesando Facturación")
            
            try:
                # Paso 1: Extraer datos del PDF
                progress_window.update_status("Extrayendo datos del PDF...")
                progress_window.add_detail("Inicializando extractor de PDF...")
                
                pdf_extractor = PDFExtractor(self.pdf_path.get())
                employees_data = pdf_extractor.extract_employees_data()
                
                progress_window.add_detail(f"Encontrados {len(employees_data)} empleados en el PDF")
                
                # Paso 2: Cargar datos del Excel
                progress_window.update_status("Cargando base de datos Excel...")
                progress_window.add_detail("Inicializando procesador de Excel...")
                
                excel_processor = ExcelProcessor(self.excel_path.get())
                excel_processor.load_excel()
                column_mapping = excel_processor.detect_columns()
                
                progress_window.add_detail(f"Columnas detectadas: {column_mapping}")
                
                # Paso 3: Realizar matching
                progress_window.update_status("Realizando matching de datos...")
                progress_window.add_detail("Iniciando proceso de matching...")
                
                matcher = DataMatcher(pdf_extractor, excel_processor)
                matching_results = matcher.perform_full_matching(self.similarity_var.get())
                
                progress_window.add_detail(f"Matching completado:")
                progress_window.add_detail(f"  - Encontrados: {matching_results['statistics']['total_matched']}")
                progress_window.add_detail(f"  - No encontrados: {matching_results['statistics']['total_unmatched']}")
                progress_window.add_detail(f"  - Tasa de éxito: {matching_results['statistics']['match_rate']:.1%}")
                
                # Paso 4: Generar PDF
                progress_window.update_status("Generando PDF final...")
                progress_window.add_detail("Creando PDF con datos consolidados...")
                
                pdf_generator = PDFGenerator()
                consolidated_data = matcher.get_consolidated_data()
                
                final_pdf_path = pdf_generator.create_complete_pdf(
                    self.pdf_path.get(),
                    consolidated_data,
                    matching_results['statistics'],
                    self.output_dir.get()
                )
                
                progress_window.add_detail(f"PDF generado: {os.path.basename(final_pdf_path)}")
                progress_window.update_status("¡Procesamiento completado!")
                
                # Cerrar ventana de progreso
                progress_window.close()
                
                # Mostrar resultados
                self.show_results(matching_results, final_pdf_path)
                
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", f"Error durante el procesamiento:\\n{str(e)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error crítico:\\n{str(e)}")
        finally:
            # Rehabilitar botón de procesar
            self.root.after(0, lambda: self.process_button.config(state=tk.NORMAL))
            
    def show_results(self, results: Dict, output_file: str):
        """
        Muestra los resultados del procesamiento.
        
        Args:
            results: Resultados del matching
            output_file: Ruta del archivo generado
        """
        # Actualizar barra de estado
        self.status_var.set(f"¡Completado! Archivo generado: {os.path.basename(output_file)}")
        
        # Mostrar ventana de resultados
        ResultsWindow(self.root, results)
        
        # Mostrar mensaje de éxito
        message = f"Procesamiento completado exitosamente.\\n\\n"
        message += f"Archivo generado: {output_file}\\n\\n"
        message += f"Empleados procesados: {results['statistics']['total_matched'] + results['statistics']['total_unmatched']}\\n"
        message += f"Encontrados: {results['statistics']['total_matched']}\\n"
        message += f"No encontrados: {results['statistics']['total_unmatched']}\\n"
        message += f"Tasa de éxito: {results['statistics']['match_rate']:.1%}"
        
        messagebox.showinfo("Procesamiento Completado", message)
        
    def run(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()


def create_gui_app() -> MainApplication:
    """
    Crea y retorna una instancia de la aplicación GUI.
    
    Returns:
        Instancia de MainApplication
    """
    return MainApplication()


if __name__ == "__main__":
    app = create_gui_app()
    app.run()