"""
Módulo de interfaz de usuario mejorada para la aplicación de facturación.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
from typing import Optional, Callable, Dict, List
import threading


class ModernStyle:
    """Clase para definir el estilo visual moderno de la aplicación."""
    
    # Paleta de colores moderna
    COLORS = {
        'primary': '#2E86AB',      # Azul principal
        'secondary': '#A23B72',     # Rosa/morado secundario
        'accent': '#F18F01',        # Naranja de acento
        'success': '#4CAF50',       # Verde éxito
        'warning': '#FF9800',       # Naranja advertencia
        'error': '#F44336',         # Rojo error
        'background': '#F8F9FA',    # Fondo claro
        'surface': '#FFFFFF',       # Superficie blanca
        'dark': '#2C3E50',          # Gris oscuro
        'text': '#34495E',          # Texto principal
        'text_light': '#7F8C8D',    # Texto secundario
        'border': '#E0E6ED',        # Bordes
        'hover': '#EBF3FD',         # Hover estado
        'gradient_start': '#667eea', # Gradiente inicio
        'gradient_end': '#764ba2'    # Gradiente fin
    }
    
    # Fuentes
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'subtitle': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'monospace': ('Consolas', 9)
    }
    
    @classmethod
    def configure_styles(cls, root):
        """Configura los estilos ttk personalizados."""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Botón principal
        style.configure(
            'Primary.TButton',
            background=cls.COLORS['primary'],
            foreground='white',
            focuscolor='none',
            font=cls.FONTS['body'],
            padding=(20, 12)
        )
        style.map(
            'Primary.TButton',
            background=[('active', '#1B5E7D'), ('pressed', '#1B5E7D')],
            relief=[('pressed', 'flat'), ('!pressed', 'raised')]
        )
        
        # Botón secundario
        style.configure(
            'Secondary.TButton',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text'],
            focuscolor='none',
            font=cls.FONTS['body'],
            padding=(15, 10),
            borderwidth=2,
            relief='solid'
        )
        style.map(
            'Secondary.TButton',
            background=[('active', cls.COLORS['hover'])],
            bordercolor=[('active', cls.COLORS['primary'])]
        )
        
        # Botón de éxito
        style.configure(
            'Success.TButton',
            background=cls.COLORS['success'],
            foreground='white',
            focuscolor='none',
            font=cls.FONTS['body'],
            padding=(20, 12)
        )
        style.map(
            'Success.TButton',
            background=[('active', '#45A049')]
        )
        
        # Frame con bordes redondeados simulados
        style.configure(
            'Card.TFrame',
            background=cls.COLORS['surface'],
            relief='flat',
            borderwidth=1
        )
        
        # LabelFrame personalizado
        style.configure(
            'Card.TLabelframe',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['subtitle'],
            relief='flat',
            borderwidth=2,
            fieldbackground=cls.COLORS['surface']
        )
        style.configure(
            'Card.TLabelframe.Label',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['primary'],
            font=cls.FONTS['subtitle']
        )
        
        # Entry personalizado
        style.configure(
            'Modern.TEntry',
            fieldbackground=cls.COLORS['surface'],
            borderwidth=2,
            relief='solid',
            bordercolor=cls.COLORS['border'],
            font=cls.FONTS['body'],
            padding=(10, 8)
        )
        style.map(
            'Modern.TEntry',
            bordercolor=[('focus', cls.COLORS['primary'])],
            lightcolor=[('focus', cls.COLORS['primary'])]
        )
        
        # Scale personalizado
        style.configure(
            'Modern.TScale',
            background=cls.COLORS['surface'],
            troughcolor=cls.COLORS['border'],
            sliderthickness=18,
            sliderlength=30,
            bordercolor=cls.COLORS['primary'],
            relief='flat'
        )
        style.map(
            'Modern.TScale',
            background=[('active', cls.COLORS['hover'])],
            bordercolor=[('active', cls.COLORS['primary'])]
        )
        
        # Notebook personalizado
        style.configure(
            'Modern.TNotebook',
            background=cls.COLORS['surface'],
            borderwidth=0
        )
        style.configure(
            'Modern.TNotebook.Tab',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['body'],
            padding=(20, 12)
        )
        style.map(
            'Modern.TNotebook.Tab',
            background=[('selected', cls.COLORS['primary']), ('active', cls.COLORS['hover'])],
            foreground=[('selected', 'white')]
        )
        
        # Treeview personalizado
        style.configure(
            'Modern.Treeview',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['body'],
            fieldbackground=cls.COLORS['surface'],
            borderwidth=0
        )
        style.configure(
            'Modern.Treeview.Heading',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['subtitle'],
            relief='flat'
        )
        style.map(
            'Modern.Treeview',
            background=[('selected', cls.COLORS['primary'])],
            foreground=[('selected', 'white')]
        )


class FileSelector:
    """Clase para manejar la selección de archivos con estilo mejorado."""
    
    @staticmethod
    def select_pdf_file(title: str = "Seleccionar archivo PDF") -> Optional[str]:
        """Abre diálogo para seleccionar archivo PDF."""
        return filedialog.askopenfilename(
            title=title,
            filetypes=[
                ("Archivos PDF", "*.pdf"),
                ("Todos los archivos", "*.*")
            ]
        )
    
    @staticmethod
    def select_excel_file(title: str = "Seleccionar archivo Excel") -> Optional[str]:
        """Abre diálogo para seleccionar archivo Excel."""
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
        """Abre diálogo para seleccionar directorio de salida."""
        return filedialog.askdirectory(title=title)


class ProgressWindow:
    """Ventana moderna para mostrar progreso de operaciones."""
    
    def __init__(self, parent, title: str = "Procesando..."):
        """Inicializa la ventana de progreso con estilo moderno."""

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("500x350")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=ModernStyle.COLORS['background'])
        # Establecer el ícono personalizado
        ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'syp.ico')
        try:
            self.window.iconbitmap(ico_path)
        except Exception as e:
            print(f"No se pudo cargar el ícono personalizado: {e}")

        # Centrar ventana
        self.center_window()

        # Configurar estilos
        ModernStyle.configure_styles(self.window)

        # Widgets
        self.setup_widgets()
        
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (350 // 2)
        self.window.geometry(f"500x350+{x}+{y}")
        
    def setup_widgets(self):
        """Configura los widgets con estilo moderno."""
        # Frame principal con padding y fondo
        main_frame = tk.Frame(
            self.window, 
            bg=ModernStyle.COLORS['surface'],
            relief='flat',
            bd=0
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header con icono (simulado con texto)
        header_frame = tk.Frame(main_frame, bg=ModernStyle.COLORS['surface'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Icono simulado
        icon_label = tk.Label(
            header_frame,
            text="⚙️",
            font=('Segoe UI', 24),
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['primary']
        )
        icon_label.pack()
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="Procesando Información",
            font=ModernStyle.FONTS['title'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text']
        )
        title_label.pack(pady=(10, 0))
        
        # Etiqueta de estado
        self.status_label = tk.Label(
            main_frame,
            text="Iniciando procesamiento...",
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text_light'],
            wraplength=450
        )
        self.status_label.pack(pady=(0, 20))
        
        # Container para la barra de progreso
        progress_container = tk.Frame(
            main_frame,
            bg=ModernStyle.COLORS['background'],
            relief='flat',
            bd=0,
            height=60
        )
        progress_container.pack(fill=tk.X, pady=(0, 20))
        progress_container.pack_propagate(False)
        
        # Barra de progreso moderna
        self.progress_bar = ttk.Progressbar(
            progress_container,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.place(relx=0.5, rely=0.5, anchor='center')
        self.progress_bar.start(8)  # Velocidad más suave
        
        # Frame para detalles
        details_frame = tk.Frame(main_frame, bg=ModernStyle.COLORS['surface'])
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details_label = tk.Label(
            details_frame,
            text="Detalles del Proceso:",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text'],
            anchor='w'
        )
        details_label.pack(fill=tk.X, pady=(0, 10))
        
        # Área de texto con estilo
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            height=8,
            font=ModernStyle.FONTS['monospace'],
            bg=ModernStyle.COLORS['background'],
            fg=ModernStyle.COLORS['text'],
            relief='flat',
            bd=0,
            padx=15,
            pady=10,
            wrap=tk.WORD
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
    def update_status(self, message: str):
        """Actualiza el mensaje de estado."""
        self.status_label.config(text=message)
        self.window.update()
        
    def add_detail(self, detail: str):
        """Añade un detalle al área de texto."""
        self.details_text.insert(tk.END, f"• {detail}\n")
        self.details_text.see(tk.END)
        self.window.update()
        
    def close(self):
        """Cierra la ventana de progreso."""
        self.progress_bar.stop()
        self.window.destroy()


class ResultsWindow:
    """Ventana moderna para mostrar resultados."""
    

    def __init__(self, parent, results: Dict):
        """Inicializa la ventana de resultados con estilo moderno."""
        self.window = tk.Toplevel(parent)
        self.window.title("Resultados del Procesamiento")
        self.window.geometry("1150x750")  # Ventana aún más grande para evitar recortes
        self.window.transient(parent)
        self.window.configure(bg=ModernStyle.COLORS['background'])
        # Establecer el ícono personalizado
        ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'syp.ico')
        try:
            self.window.iconbitmap(ico_path)
        except Exception as e:
            print(f"No se pudo cargar el ícono personalizado: {e}")

        self.results = results
        ModernStyle.configure_styles(self.window)
        self.setup_widgets()
        
    def setup_widgets(self):
        """Configura los widgets con estilo moderno."""
        # Header con título y estadísticas rápidas
        self.create_header()
        
        # Frame principal con notebook
        main_frame = tk.Frame(self.window, bg=ModernStyle.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 0))  # Sin padding bottom para el footer
        
        # Notebook moderno para pestañas
        notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas
        self.create_summary_tab(notebook)
        
        # Obtener el número de encontrados para mostrar en la pestaña
        matched_count = len(self.results.get('matched_employees', []))
        self.create_matched_tab(notebook, matched_count)
        self.create_unmatched_tab(notebook)
        
        if self.results.get('manual_suggestions'):
            self.create_suggestions_tab(notebook)
        
        # Footer con botones
        self.create_footer(main_frame)
        
    def create_header(self):
        """Crea el header con estadísticas visuales."""
        header_frame = tk.Frame(
            self.window, 
            bg=ModernStyle.COLORS['primary'], 
            height=120
        )
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Container interno
        content_frame = tk.Frame(header_frame, bg=ModernStyle.COLORS['primary'])
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        title_label = tk.Label(
            content_frame,
            text="🎯 Resultados del Procesamiento",
            font=('Segoe UI', 18, 'bold'),
            bg=ModernStyle.COLORS['primary'],
            fg='white'
        )
        title_label.pack()
        
        # Stats rápidas (solo mostrando encontrados)
        stats = self.results.get('statistics', {})
        stats_text = f"Total: {stats.get('total_matched', 0) + stats.get('total_unmatched', 0)} • "
        stats_text += f"Encontrados: {stats.get('total_matched', 0)}"
        
        stats_label = tk.Label(
            content_frame,
            text=stats_text,
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['primary'],
            fg='white'
        )
        stats_label.pack(pady=(10, 0))
        
    def create_summary_tab(self, notebook):
        """Crea la pestaña de resumen con diseño moderno."""
        frame = tk.Frame(notebook, bg=ModernStyle.COLORS['surface'])
        notebook.add(frame, text="📊 Resumen")
        
        # Container principal con scroll mejorado
        main_container = tk.Frame(frame, bg=ModernStyle.COLORS['surface'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Stats visuales con tarjetas
        self.create_stats_cards(main_container)
        
        # Información detallada
        self.create_detailed_info(main_container)
        
    def create_stats_cards(self, parent):
        """Crea tarjetas de estadísticas visuales."""
        cards_frame = tk.Frame(parent, bg=ModernStyle.COLORS['surface'])
        cards_frame.pack(fill=tk.X, pady=(0, 30))
        
        stats = self.results.get('statistics', {})
        
        # Datos para las tarjetas (solo las que queremos mostrar)
        card_data = [
            {
                'title': 'Total Procesados',
                'value': stats.get('total_matched', 0) + stats.get('total_unmatched', 0),
                'icon': '👥',
                'color': ModernStyle.COLORS['primary']
            },
            {
                'title': 'Encontrados',
                'value': stats.get('total_matched', 0),
                'icon': '✅',
                'color': ModernStyle.COLORS['success']
            }
        ]
        
        for i, card in enumerate(card_data):
            self.create_stat_card(cards_frame, card, i)
            
    def create_stat_card(self, parent, card_data, index):
        """Crea una tarjeta de estadística individual."""
        # Frame de la tarjeta
        card_frame = tk.Frame(
            parent,
            bg=card_data['color'],
            relief='flat',
            bd=0
        )
        card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Contenido interno con padding
        content_frame = tk.Frame(card_frame, bg=card_data['color'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Icono
        icon_label = tk.Label(
            content_frame,
            text=card_data['icon'],
            font=('Segoe UI', 20),
            bg=card_data['color'],
            fg='white'
        )
        icon_label.pack()
        
        # Valor
        value_label = tk.Label(
            content_frame,
            text=str(card_data['value']),
            font=('Segoe UI', 16, 'bold'),
            bg=card_data['color'],
            fg='white'
        )
        value_label.pack()
        
        # Título
        title_label = tk.Label(
            content_frame,
            text=card_data['title'],
            font=ModernStyle.FONTS['small'],
            bg=card_data['color'],
            fg='white'
        )
        title_label.pack()
        
    def create_detailed_info(self, parent):
        """Crea la información detallada del procesamiento."""
        info_frame = ttk.LabelFrame(
            parent,
            text="Información Detallada",
            style='Card.TLabelframe',
            padding="20"
        )
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """
✨ PROCESAMIENTO COMPLETADO EXITOSAMENTE

El sistema ha analizado todos los empleados del PDF de facturación y los ha comparado 

📋 DETALLES DEL PROCESO:
• Se utilizaron algoritmos de coincidencia de nombres avanzados
• Se aplicaron múltiples métodos de búsqueda para maximizar la precisión
• Los resultados se organizaron automáticamente en el PDF final
        """
        
        text_widget = tk.Text(
            info_frame,
            wrap=tk.WORD,
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text'],
            relief='flat',
            bd=0,
            padx=10,
            pady=10,
            height=10,
            state=tk.DISABLED
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Insertar texto
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, info_text.strip())
        text_widget.config(state=tk.DISABLED)
        
    def create_matched_tab(self, notebook, matched_count=None):
        """Crea la pestaña de empleados encontrados."""

        if matched_count is None:
            matched_count = len(self.results.get('matched_employees', []))
        frame = tk.Frame(notebook, bg=ModernStyle.COLORS['surface'])
        notebook.add(frame, text=f"✅ Encontrados ({matched_count})")

        # Header de la pestaña
        header_label = tk.Label(
            frame,
            text="Empleados identificados exitosamente:",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text']
        )
        header_label.pack(anchor=tk.W, padx=20, pady=(20, 10))

        # Treeview moderno
        columns = ("Nombre", "Cédula", "Centro de Costo", "Método", "Confianza")
        tree = ttk.Treeview(
            frame, 
            columns=columns, 
            show='headings', 
            height=18,
            style='Modern.Treeview'
        )

        # Configurar columnas
        tree.heading("Nombre", text="👤 Nombre")
        tree.heading("Cédula", text="🆔 Cédula")
        tree.heading("Centro de Costo", text="🏢 Centro de Costo")
        tree.heading("Método", text="🔍 Método")
        tree.heading("Confianza", text="📊 Confianza")

        # Ajustar anchos
        tree.column("Nombre", width=200)
        tree.column("Cédula", width=120)
        tree.column("Centro de Costo", width=150)
        tree.column("Método", width=120)
        tree.column("Confianza", width=100)

        # Agregar datos
        for emp in self.results.get('matched_employees', []):
            nombre_excel = emp.get('nombre_excel', '')
            tree.insert('', tk.END, values=(
                nombre_excel,
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
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=(0, 20))
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
        
    def create_unmatched_tab(self, notebook):
        """Crea la pestaña de empleados no encontrados."""
        frame = tk.Frame(notebook, bg=ModernStyle.COLORS['surface'])
        unmatched_count = len(self.results.get('unmatched_employees', []))
        notebook.add(frame, text=f"❌ No encontrados ({unmatched_count})")
        
        if not self.results.get('unmatched_employees'):
            # Mensaje de éxito cuando todos fueron encontrados
            success_frame = tk.Frame(frame, bg=ModernStyle.COLORS['surface'])
            success_frame.pack(expand=True, fill=tk.BOTH)
            
            tk.Label(
                success_frame,
                text="🎉",
                font=('Segoe UI', 48),
                bg=ModernStyle.COLORS['surface'],
                fg=ModernStyle.COLORS['success']
            ).pack(pady=(100, 20))
            
            tk.Label(
                success_frame,
                text="¡Excelente trabajo!",
                font=('Segoe UI', 18, 'bold'),
                bg=ModernStyle.COLORS['surface'],
                fg=ModernStyle.COLORS['success']
            ).pack()
            
            tk.Label(
                success_frame,
                text="Todos los empleados fueron encontrados exitosamente",
                font=ModernStyle.FONTS['body'],
                bg=ModernStyle.COLORS['surface'],
                fg=ModernStyle.COLORS['text']
            ).pack(pady=(10, 0))
            
            return
        
        # Header informativo
        header_label = tk.Label(
            frame,
            text="Empleados que requieren revisión manual:",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text']
        )
        header_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Treeview para empleados no encontrados
        columns = ("Nombre", "Cédula")
        tree = ttk.Treeview(
            frame, 
            columns=columns, 
            show='headings', 
            height=18,
            style='Modern.Treeview'
        )
        
        tree.heading("Nombre", text="👤 Nombre")
        tree.heading("Cédula", text="🆔 Cédula")
        tree.column("Nombre", width=300)
        tree.column("Cédula", width=200)
        
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
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
        
    def create_suggestions_tab(self, notebook):
        """Crea la pestaña de sugerencias con estilo mejorado."""
        frame = tk.Frame(notebook, bg=ModernStyle.COLORS['surface'])
        notebook.add(frame, text="💡 Sugerencias")
        
        # Header
        header_label = tk.Label(
            frame,
            text="Sugerencias inteligentes para coincidencias manuales:",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text']
        )
        header_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Área de texto con estilo
        text_widget = scrolledtext.ScrolledText(
            frame, 
            wrap=tk.WORD, 
            font=ModernStyle.FONTS['monospace'],
            bg=ModernStyle.COLORS['background'],
            fg=ModernStyle.COLORS['text'],
            relief='flat',
            bd=0,
            padx=20,
            pady=15
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Agregar sugerencias formateadas
        suggestions = self.results.get('manual_suggestions', {})
        for pdf_name, excel_matches in suggestions.items():
            text_widget.insert(tk.END, f"🔍 EMPLEADO PDF: {pdf_name}\n")
            text_widget.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            text_widget.insert(tk.END, "📋 Posibles coincidencias en Excel:\n\n")
            
            for i, match in enumerate(excel_matches, 1):
                text_widget.insert(tk.END, f"   {i}. 👤 {match['nombre_excel']}\n")
                text_widget.insert(tk.END, f"      🆔 Cédula: {match['cedula_excel']}\n")
                text_widget.insert(tk.END, f"      🏢 Centro: {match['centro_costo']}\n")
                text_widget.insert(tk.END, f"      📊 Similitud: {match['similitud']:.0%}\n\n")
            
            text_widget.insert(tk.END, "\n" + "═"*60 + "\n\n")
        
        text_widget.config(state=tk.DISABLED)
        
    def create_footer(self, parent):
        """Crea el footer con botones de acción."""
        # Contenedor del footer con más espacio
        footer_frame = tk.Frame(parent, bg=ModernStyle.COLORS['background'], height=80)
        footer_frame.pack(fill=tk.X, pady=(30, 20))
        footer_frame.pack_propagate(False)  # Mantener altura fija
        
        # Container para centrar los botones con padding adecuado
        buttons_container = tk.Frame(footer_frame, bg=ModernStyle.COLORS['background'])
        buttons_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Botón cerrar con estilo (primero para que quede a la izquierda)
        close_button = ttk.Button(
            buttons_container,
            text="✨ Cerrar",
            command=self.window.destroy,
            style='Primary.TButton'
        )
        close_button.pack(side=tk.LEFT, padx=(0, 15), pady=10)
        
        # Botón abrir carpeta
        open_folder_button = ttk.Button(
            buttons_container,
            text="📁 Abrir Carpeta",
            command=self.open_output_folder,
            style='Secondary.TButton'
        )
        open_folder_button.pack(side=tk.LEFT, pady=10)
        
    def open_output_folder(self):
        """Abre la carpeta de salida que el usuario escogió."""
        try:
            import subprocess
            import platform
            
            # Primero intentar obtener el directorio desde los resultados
            folder_path = self.results.get('output_directory', '')
            
            # Si no hay directorio en resultados o no existe, usar el directorio del archivo
            if not folder_path or not os.path.exists(folder_path):
                output_file = self.results.get('output_file', '')
                if output_file and os.path.exists(output_file):
                    folder_path = os.path.dirname(output_file)
                else:
                    # Último fallback
                    folder_path = os.path.expanduser("~/Documents")
            
            # Normalizar la ruta para Windows
            folder_path = os.path.normpath(folder_path)
            
            if os.path.exists(folder_path):
                # Abrir la carpeta según el sistema operativo
                if platform.system() == "Windows":
                    # Para Windows, usar la ruta normalizada sin check=True
                    # (explorer puede devolver códigos de error incluso cuando funciona)
                    try:
                        subprocess.run(['explorer', folder_path])
                    except Exception:
                        pass  # Ignorar errores, explorer frecuentemente funciona de todas formas
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(['open', folder_path])
                else:  # Linux
                    subprocess.run(['xdg-open', folder_path])
            else:
                messagebox.showwarning("Carpeta no encontrada", f"No se pudo encontrar la carpeta: {folder_path}")
        except Exception:
            # Solo mostrar error si realmente no se pudo abrir
            pass  # La mayoría de las veces explorer funciona incluso con errores


class MainApplication:
    """Aplicación principal con interfaz moderna mejorada."""
    
    def __init__(self):
        """Inicializa la aplicación con diseño moderno."""

        self.root = tk.Tk()
        self.root.title("App Facturación - Centros de Costo")
        # Establecer el ícono personalizado
        ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'syp.ico')
        try:
            self.root.iconbitmap(ico_path)
        except Exception as e:
            print(f"No se pudo cargar el ícono personalizado: {e}")

        # Configurar ventana inicial
        self.root.state('normal')  # Asegurar estado normal
        self.root.resizable(True, True)
        self.root.configure(bg=ModernStyle.COLORS['background'])

        # Configurar estilo moderno
        ModernStyle.configure_styles(self.root)
        
        # Variables
        self.pdf_path = tk.StringVar()
        self.excel_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        # Configurar directorio de salida por defecto
        self.output_dir.set(os.path.expanduser("~/Documents"))
        
        # Configurar UI y luego centrar
        self.setup_modern_ui()
        self.root.update_idletasks()  # Procesar geometría
        self.center_window()
        
    def center_window(self):
        """Centra la ventana en la pantalla con tamaño optimizado."""
        # Permitir que la ventana calcule su tamaño natural primero
        self.root.update_idletasks()
        
        # Configurar tamaño mínimo y deseado
        min_width, min_height = 900, 650
        desired_width, desired_height = 980, 720
        
        # Obtener dimensiones de pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posición centrada
        x = (screen_width // 2) - (desired_width // 2)
        y = (screen_height // 2) - (desired_height // 2)
        
        # Aplicar geometría
        self.root.geometry(f"{desired_width}x{desired_height}+{x}+{y}")
        self.root.minsize(min_width, min_height)
        
    def create_improved_scrollable_container(self):
        """Crea un container mejorado que llena la ventana y permite scroll."""
        # Frame principal que ocupe todo el espacio disponible
        main_frame = tk.Frame(self.root, bg=ModernStyle.COLORS['background'])
        main_frame.pack(fill="both", expand=True)
        
        # Canvas para el contenido scrollable
        canvas = tk.Canvas(
            main_frame, 
            bg=ModernStyle.COLORS['background'], 
            highlightthickness=0,
            bd=0
        )
        
        # Scrollbar solo cuando sea necesario
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Frame interno para el contenido
        scrollable_frame = tk.Frame(canvas, bg=ModernStyle.COLORS['background'])
        
        # Función para gestionar el scroll y el tamaño
        def on_frame_configure(event=None):
            # Actualizar región de scroll
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Obtener dimensiones
            canvas_height = canvas.winfo_height()
            frame_height = scrollable_frame.winfo_reqheight()
            
            # Mostrar/ocultar scrollbar según sea necesario
            if frame_height > canvas_height:
                scrollbar.pack(side="right", fill="y")
            else:
                scrollbar.pack_forget()
        
        def on_canvas_configure(event):
            # Asegurar que el frame interno use todo el ancho del canvas
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            on_frame_configure()
        
        # Crear ventana en canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configurar eventos
        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mousewheel binding
        def on_mousewheel(event):
            # Solo hacer scroll si la scrollbar está visible
            if scrollbar.winfo_viewable():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mousewheel a la ventana principal
        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', bind_mousewheel)
        canvas.bind('<Leave>', unbind_mousewheel)
        
        # Pack canvas (scrollbar se añade dinámicamente)
        canvas.pack(side="left", fill="both", expand=True)
        
        return scrollable_frame
        
    def setup_modern_ui(self):
        """Configura la interfaz moderna."""
        # Footer con barra de estado moderna (crear primero para que quede abajo)
        self.create_modern_footer()
        
        # Container principal con scroll mejorado
        main_container = self.create_improved_scrollable_container()
        
        # Header elegante con gradiente simulado
        self.create_modern_header(main_container)
        
        # Sección de archivos con estilo de tarjetas
        self.create_file_cards_section(main_container)
        
        # Botones de acción con estilo
        self.create_action_section(main_container)
        
        # Espaciado final para el scroll
        bottom_spacer = tk.Frame(main_container, bg=ModernStyle.COLORS['background'], height=20)
        bottom_spacer.pack(fill=tk.X)
        
    def create_scrollable_container(self):
        """Crea un container principal con scroll."""
        # Frame principal que ocupe todo el espacio disponible
        main_frame = tk.Frame(self.root, bg=ModernStyle.COLORS['background'])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Canvas y scrollbar para scroll vertical
        canvas = tk.Canvas(main_frame, bg=ModernStyle.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ModernStyle.COLORS['background'])
        
        # Función para actualizar scroll region
        def configure_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Asegurar que el frame interno tenga al menos el ancho del canvas
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:  # Evitar errores cuando el canvas no está inicializado
                canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", configure_scroll)
        
        # Crear ventana en el canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Pack canvas y scrollbar correctamente
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Guardar referencias para uso posterior
        self.canvas = canvas
        self.canvas_window = canvas_window
        
        return scrollable_frame
        
    def create_modern_header(self, parent):
        """Crea un header moderno con gradiente simulado."""
        # Frame del header con colores degradados
        header_frame = tk.Frame(
            parent, 
            bg=ModernStyle.COLORS['primary'],
            height=140
        )
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Container interno centrado
        content_frame = tk.Frame(header_frame, bg=ModernStyle.COLORS['primary'])
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Icono principal (imagen personalizada)
        try:
            from PIL import Image, ImageTk
            # Cargar y redimensionar la imagen
            image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Iconsyp.png")
            if os.path.exists(image_path):
                image = Image.open(image_path)
                # Convertir a RGBA para manejar transparencia
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                # Crear una nueva imagen con fondo del color primario
                background = Image.new('RGBA', image.size, ModernStyle.COLORS['primary'])
                # Combinar la imagen con el fondo
                combined = Image.alpha_composite(background, image)
                # Convertir de vuelta a RGB
                combined = combined.convert('RGB')
                
                # Redimensionar
                combined = combined.resize((48, 48), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(combined)
                
                icon_label = tk.Label(
                    content_frame,
                    image=photo,
                    bg=ModernStyle.COLORS['primary'],
                    bd=0,
                    highlightthickness=0
                )
                icon_label.image = photo  # Mantener referencia
                icon_label.pack(pady=(0, 5))
            else:
                # Fallback al emoji si no se encuentra la imagen
                icon_label = tk.Label(
                    content_frame,
                    text="📊",
                    font=('Segoe UI', 28),
                    bg=ModernStyle.COLORS['primary'],
                    fg='white'
                )
                icon_label.pack(pady=(0, 5))
        except ImportError:
            # Fallback si PIL no está disponible
            icon_label = tk.Label(
                content_frame,
                text="📊",
                font=('Segoe UI', 28),
                bg=ModernStyle.COLORS['primary'],
                fg='white'
            )
            icon_label.pack(pady=(0, 5))
        
        # Título principal
        title_label = tk.Label(
            content_frame,
            text="App Facturación",
            font=('Segoe UI', 20, 'bold'),
            bg=ModernStyle.COLORS['primary'],
            fg='white'
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(
            content_frame,
            text="Automatización Inteligente de Centros de Costo",
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['primary'],
            fg='white'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Descripción elegante
        desc_frame = tk.Frame(parent, bg=ModernStyle.COLORS['background'], height=80)
        desc_frame.pack(fill=tk.X)
        desc_frame.pack_propagate(False)
        
        desc_label = tk.Label(
            desc_frame,
            text="Procesa automáticamente PDFs de facturación y asigna centros de costo\nmediante búsqueda inteligente en bases de datos Excel.",
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['background'],
            fg=ModernStyle.COLORS['text_light'],
            justify=tk.CENTER
        )
        desc_label.place(relx=0.5, rely=0.5, anchor='center')
        
    def create_file_cards_section(self, parent):
        """Crea la sección de archivos con diseño de tarjetas."""
        # Container principal
        files_container = tk.Frame(parent, bg=ModernStyle.COLORS['background'])
        files_container.pack(fill=tk.X, padx=30, pady=(20, 25))
        
        # Título de sección
        section_title = tk.Label(
            files_container,
            text="📁 Selección de Archivos",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['background'],
            fg=ModernStyle.COLORS['text']
        )
        section_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Tarjeta PDF
        self.create_file_card(
            files_container,
            "📄 PDF de Facturación",
            "Seleccione el archivo PDF que contiene la información de empleados",
            self.pdf_path,
            self.select_pdf_file,
            ModernStyle.COLORS['primary']
        )
        
        # Espaciado
        tk.Frame(files_container, bg=ModernStyle.COLORS['background'], height=15).pack()
        
        # Tarjeta Excel
        self.create_file_card(
            files_container,
            "📊 Base de Datos Excel",
            "Seleccione el archivo Excel con la información de empleados y centros de costo",
            self.excel_path,
            self.select_excel_file,
            ModernStyle.COLORS['success']
        )
        
        # Espaciado
        tk.Frame(files_container, bg=ModernStyle.COLORS['background'], height=20).pack()
        
        # Tarjeta Directorio
        self.create_directory_card(files_container)
        
    def create_file_card(self, parent, title, description, path_var, command, color):
        """Crea una tarjeta individual para selección de archivos."""
        # Frame de la tarjeta con sombra simulada
        card_shadow = tk.Frame(parent, bg='#E0E0E0', height=2)
        card_shadow.pack(fill=tk.X, pady=(0, 0))
        
        card_frame = tk.Frame(
            parent,
            bg=ModernStyle.COLORS['surface'],
            relief='flat',
            bd=0
        )
        card_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Borde izquierdo colorido
        border_frame = tk.Frame(card_frame, bg=color, width=5)
        border_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Contenido de la tarjeta
        content_frame = tk.Frame(card_frame, bg=ModernStyle.COLORS['surface'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header de la tarjeta
        header_frame = tk.Frame(content_frame, bg=ModernStyle.COLORS['surface'])
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text'],
            anchor='w'
        )
        title_label.pack(side=tk.LEFT)
        
        # Botón examinar moderno
        browse_btn = ttk.Button(
            header_frame,
            text="📂 Examinar",
            command=command,
            style='Secondary.TButton'
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Descripción
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text_light'],
            anchor='w',
            wraplength=400
        )
        desc_label.pack(fill=tk.X, pady=(5, 10))
        
        # Entry para mostrar archivo seleccionado
        path_entry = ttk.Entry(
            content_frame,
            textvariable=path_var,
            state="readonly",
            style='Modern.TEntry',
            font=ModernStyle.FONTS['small']
        )
        path_entry.pack(fill=tk.X)
        
    def create_directory_card(self, parent):
        """Crea la tarjeta para seleccionar directorio de salida."""
        # Frame de la tarjeta
        card_shadow = tk.Frame(parent, bg='#E0E0E0', height=2)
        card_shadow.pack(fill=tk.X, pady=(0, 0))
        
        card_frame = tk.Frame(
            parent,
            bg=ModernStyle.COLORS['surface'],
            relief='flat',
            bd=0
        )
        card_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Borde colorido
        border_frame = tk.Frame(card_frame, bg=ModernStyle.COLORS['accent'], width=5)
        border_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Contenido
        content_frame = tk.Frame(card_frame, bg=ModernStyle.COLORS['surface'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(content_frame, bg=ModernStyle.COLORS['surface'])
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="📁 Directorio de Salida",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text'],
            anchor='w'
        )
        title_label.pack(side=tk.LEFT)
        
        browse_btn = ttk.Button(
            header_frame,
            text="📂 Cambiar",
            command=self.select_output_directory,
            style='Secondary.TButton'
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Descripción
        desc_label = tk.Label(
            content_frame,
            text="Ubicación donde se guardará el PDF procesado con los centros de costo",
            font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text_light'],
            anchor='w',
            wraplength=400
        )
        desc_label.pack(fill=tk.X, pady=(5, 10))
        
        # Entry modificable para directorio
        path_entry = ttk.Entry(
            content_frame,
            textvariable=self.output_dir,
            style='Modern.TEntry',
            font=ModernStyle.FONTS['small']
        )
        path_entry.pack(fill=tk.X)
        
    def create_advanced_settings(self, parent):
        """Crea la sección de configuración avanzada."""
        # Container de configuración
        settings_container = tk.Frame(parent, bg=ModernStyle.COLORS['background'])
        settings_container.pack(fill=tk.X, padx=30, pady=(15, 20))
        
        # Título de sección
        section_title = tk.Label(
            settings_container,
            text="⚙️ Configuración Avanzada",
            font=ModernStyle.FONTS['subtitle'],
            bg=ModernStyle.COLORS['background'],
            fg=ModernStyle.COLORS['text']
        )
        section_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Tarjeta de configuración
        card_shadow = tk.Frame(settings_container, bg='#E0E0E0', height=2)
        card_shadow.pack(fill=tk.X)
        
        settings_card = tk.Frame(
            settings_container,
            bg=ModernStyle.COLORS['surface'],
            relief='flat',
            bd=0
        )
        settings_card.pack(fill=tk.X, pady=(2, 0))
        
        # Borde colorido
        border_frame = tk.Frame(settings_card, bg=ModernStyle.COLORS['secondary'], width=5)
        border_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Contenido de configuración
        config_content = tk.Frame(settings_card, bg=ModernStyle.COLORS['surface'])
        config_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configuración de umbral
        threshold_frame = tk.Frame(config_content, bg=ModernStyle.COLORS['surface'])
        threshold_frame.pack(fill=tk.X)
        
        # Título y descripción
        threshold_title = tk.Label(
            threshold_frame,
            text="🎯 Umbral de Similitud para Nombres",
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text']
        )
        threshold_title.pack(anchor=tk.W)
        
        threshold_desc = tk.Label(
            threshold_frame,
            text="Ajuste qué tan similares deben ser los nombres para considerarse una coincidencia",
            font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text_light']
        )
        threshold_desc.pack(anchor=tk.W, pady=(2, 15))
        
        # Control deslizante moderno
        slider_frame = tk.Frame(threshold_frame, bg=ModernStyle.COLORS['surface'])
        slider_frame.pack(fill=tk.X)
        
        # Labels de valores
        labels_frame = tk.Frame(slider_frame, bg=ModernStyle.COLORS['surface'])
        labels_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            labels_frame, text="Menos estricto", font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['surface'], fg=ModernStyle.COLORS['text_light']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            labels_frame, text="Más estricto", font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['surface'], fg=ModernStyle.COLORS['text_light']
        ).pack(side=tk.RIGHT)
        
        # Slider y valor actual
        controls_frame = tk.Frame(slider_frame, bg=ModernStyle.COLORS['surface'])
        controls_frame.pack(fill=tk.X)
        
        self.similarity_var = tk.DoubleVar(value=0.7)
        similarity_scale = ttk.Scale(
            controls_frame,
            from_=0.5,
            to=1.0,
            variable=self.similarity_var,
            orient=tk.HORIZONTAL
        )
        similarity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Valor actual con estilo
        value_frame = tk.Frame(controls_frame, bg=ModernStyle.COLORS['background'])
        value_frame.pack(side=tk.RIGHT, padx=(15, 0))
        
        self.similarity_label = tk.Label(
            value_frame,
            text="0.70",
            font=('Segoe UI', 12, 'bold'),
            bg=ModernStyle.COLORS['background'],
            fg=ModernStyle.COLORS['primary'],
            padx=10,
            pady=5
        )
        self.similarity_label.pack()
        
        # Actualizar etiqueta cuando cambie el valor
        def update_similarity_label(*args):
            value = self.similarity_var.get()
            self.similarity_label.config(text=f"{value:.2f}")
            
        self.similarity_var.trace('w', update_similarity_label)
        
    def create_action_section(self, parent):
        """Crea la sección de botones de acción con estilo."""
        # Container de acciones
        action_container = tk.Frame(parent, bg=ModernStyle.COLORS['background'])
        action_container.pack(fill=tk.X, padx=30, pady=(20, 25))
        
        # Frame para los botones
        buttons_frame = tk.Frame(action_container, bg=ModernStyle.COLORS['background'])
        buttons_frame.pack(fill=tk.X)
        
        # Botón procesar principal
        self.process_button = ttk.Button(
            buttons_frame,
            text="🚀 Procesar Archivos",
            command=self.process_files,
            style='Success.TButton'
        )
        self.process_button.pack(side=tk.RIGHT, padx=(15, 0))
        
        # Botón limpiar
        clear_button = ttk.Button(
            buttons_frame,
            text="🧹 Limpiar Campos",
            command=self.clear_fields,
            style='Secondary.TButton'
        )
        clear_button.pack(side=tk.RIGHT)
        
    def create_modern_footer(self):
        """Crea un footer moderno con barra de estado."""
        # Footer frame
        footer_frame = tk.Frame(
            self.root, 
            bg=ModernStyle.COLORS['dark'],
            height=45
        )
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False)
        
        # Container interno
        footer_content = tk.Frame(footer_frame, bg=ModernStyle.COLORS['dark'])
        footer_content.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Barra de estado con icono
        status_frame = tk.Frame(footer_content, bg=ModernStyle.COLORS['dark'])
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        status_icon = tk.Label(
            status_frame,
            text="ℹ️",
            font=ModernStyle.FONTS['body'],
            bg=ModernStyle.COLORS['dark'],
            fg='white'
        )
        status_icon.pack(side=tk.LEFT, pady=12, padx=(0, 10))
        
        self.status_var = tk.StringVar(value="Listo para procesar archivos")
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['dark'],
            fg='white',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, pady=12)
        
        # Información de versión
        version_label = tk.Label(
            footer_content,
            text="v2.0 | Interfaz Moderna",
            font=ModernStyle.FONTS['small'],
            bg=ModernStyle.COLORS['dark'],
            fg=ModernStyle.COLORS['text_light']
        )
        version_label.pack(side=tk.RIGHT, pady=12)
        
    def select_pdf_file(self):
        """Selecciona archivo PDF con feedback visual."""
        file_path = FileSelector.select_pdf_file()
        if file_path:
            self.pdf_path.set(file_path)
            self.update_status(f"✅ PDF seleccionado: {os.path.basename(file_path)}", 'success')
            
    def select_excel_file(self):
        """Selecciona archivo Excel con feedback visual."""
        file_path = FileSelector.select_excel_file()
        if file_path:
            self.excel_path.set(file_path)
            self.update_status(f"✅ Excel seleccionado: {os.path.basename(file_path)}", 'success')
            
    def select_output_directory(self):
        """Selecciona directorio de salida con feedback visual."""
        dir_path = FileSelector.select_output_directory()
        if dir_path:
            self.output_dir.set(dir_path)
            self.update_status(f"📁 Directorio actualizado: {os.path.basename(dir_path)}", 'info')
            
    def clear_fields(self):
        """Limpia todos los campos con animación visual."""
        self.pdf_path.set("")
        self.excel_path.set("")
        self.output_dir.set(os.path.expanduser("~/Documents"))
        self.update_status("🧹 Campos limpiados correctamente", 'info')
        
    def update_status(self, message: str, status_type: str = 'info'):
        """Actualiza la barra de estado con colores según el tipo."""
        self.status_var.set(message)
        
        # Colores según tipo de estado
        colors = {
            'success': ModernStyle.COLORS['success'],
            'error': ModernStyle.COLORS['error'],
            'warning': ModernStyle.COLORS['warning'],
            'info': 'white'
        }
        
        self.status_label.config(fg=colors.get(status_type, 'white'))
        
    def validate_inputs(self) -> bool:
        """Valida las entradas con mensajes mejorados."""
        if not self.pdf_path.get():
            self.show_modern_error("Archivo Requerido", "Debe seleccionar un archivo PDF para procesar.")
            return False
            
        if not self.excel_path.get():
            self.show_modern_error("Base de Datos Requerida", "Debe seleccionar un archivo Excel con la base de datos.")
            return False
            
        if not self.output_dir.get():
            self.show_modern_error("Directorio Requerido", "Debe especificar un directorio de salida.")
            return False
            
        if not os.path.exists(self.pdf_path.get()):
            self.show_modern_error("Archivo No Encontrado", "El archivo PDF especificado no existe.")
            return False
            
        if not os.path.exists(self.excel_path.get()):
            self.show_modern_error("Archivo No Encontrado", "El archivo Excel especificado no existe.")
            return False
            
        if not os.path.exists(self.output_dir.get()):
            self.show_modern_error("Directorio No Encontrado", "El directorio de salida especificado no existe.")
            return False
            
        return True
        
    def show_modern_error(self, title: str, message: str):
        """Muestra errores con estilo moderno."""
        messagebox.showerror(f"❌ {title}", message)
        
    def process_files(self):
        """Procesa los archivos con UI mejorada."""
        if not self.validate_inputs():
            return
            
        # Cambiar estado del botón
        self.process_button.config(text="🔄 Procesando...", state=tk.DISABLED)
        self.update_status("🚀 Iniciando procesamiento...", 'info')
        
        # Ejecutar en hilo separado
        threading.Thread(target=self._process_files_thread, daemon=True).start()
        
    def _process_files_thread(self):
        """Hilo de procesamiento con mejor manejo de errores."""
        try:
            # Importar módulos necesarios
            from .pdf_extractor import PDFExtractor
            from .excel_processor import ExcelProcessor
            from .data_matcher import DataMatcher
            from .pdf_generator import PDFGenerator
            
            # Crear ventana de progreso moderna
            progress_window = ProgressWindow(self.root, "Procesando Facturación")
            
            try:
                # Paso 1: Extraer datos del PDF
                progress_window.update_status("🔍 Analizando PDF de facturación...")
                progress_window.add_detail("Inicializando extractor de PDF")
                
                pdf_extractor = PDFExtractor(self.pdf_path.get())
                employees_data = pdf_extractor.extract_employees_data()
                
                progress_window.add_detail(f"Encontrados {len(employees_data)} empleados en el PDF")
                
                # Paso 2: Cargar datos del Excel
                progress_window.update_status("📊 Cargando base de datos Excel...")
                progress_window.add_detail("Procesando archivo Excel")
                
                excel_processor = ExcelProcessor(self.excel_path.get())
                excel_processor.load_excel()
                column_mapping = excel_processor.detect_columns()
                
                progress_window.add_detail(f"Columnas detectadas correctamente")
                
                # Paso 3: Realizar matching
                progress_window.update_status("🤖 Realizando matching inteligente...")
                progress_window.add_detail("Aplicando algoritmos de coincidencia")
                
                matcher = DataMatcher(pdf_extractor, excel_processor)
                matching_results = matcher.perform_full_matching(0.7)  # Usar valor fijo de 0.7
                
                progress_window.add_detail(f"Matching completado:")
                progress_window.add_detail(f"  ✅ Encontrados: {matching_results['statistics']['total_matched']}")
                progress_window.add_detail(f"  ❌ No encontrados: {matching_results['statistics']['total_unmatched']}")
                progress_window.add_detail(f"  📊 Tasa de éxito: {matching_results['statistics']['match_rate']:.1%}")
                
                # Paso 4: Generar PDF
                progress_window.update_status("📄 Generando PDF final...")
                progress_window.add_detail("Creando documento consolidado")
                
                pdf_generator = PDFGenerator()
                consolidated_data = matcher.get_consolidated_data()
                
                final_pdf_path = pdf_generator.create_complete_pdf(
                    self.pdf_path.get(),
                    consolidated_data,
                    matching_results['statistics'],
                    self.output_dir.get()
                )
                
                progress_window.add_detail(f"PDF generado exitosamente")
                progress_window.update_status("✨ ¡Procesamiento completado!")
                
                # Esperar un momento para mostrar éxito
                threading.Event().wait(1)
                
                # Cerrar ventana de progreso
                progress_window.close()
                
                # Mostrar resultados
                self.show_results(matching_results, final_pdf_path)
                
            except Exception as e:
                progress_window.close()
                self.show_modern_error("Error de Procesamiento", f"Ocurrió un error durante el procesamiento:\n\n{str(e)}")
                
        except Exception as e:
            self.show_modern_error("Error Crítico", f"Error crítico en la aplicación:\n\n{str(e)}")
        finally:
            # Rehabilitar botón de procesar
            self.root.after(0, self._reset_process_button)
            
    def _reset_process_button(self):
        """Resetea el botón de procesar al estado original."""
        self.process_button.config(text="🚀 Procesar Archivos", state=tk.NORMAL)
        self.update_status("Listo para procesar archivos", 'info')
            
    def show_results(self, results: Dict, output_file: str):
        """Muestra los resultados con estilo mejorado."""
        # Actualizar barra de estado con éxito
        self.update_status(f"✅ ¡Completado! Archivo: {os.path.basename(output_file)}", 'success')
        
        # Normalizar las rutas antes de pasarlas
        normalized_output_file = os.path.normpath(output_file)
        normalized_output_dir = os.path.normpath(self.output_dir.get())
        
        # Agregar la ruta del archivo y directorio de salida a los resultados
        results['output_file'] = normalized_output_file
        results['output_directory'] = normalized_output_dir
        
        # Mostrar ventana de resultados moderna
        ResultsWindow(self.root, results)
        
        # Mensaje de éxito elegante
        stats = results['statistics']
        success_message = f"🎉 ¡Procesamiento Completado Exitosamente!\n\n"
        success_message += f"📄 Archivo generado:\n{output_file}\n\n"
        success_message += f"📊 Resumen de resultados:\n"
        success_message += f"   • Total procesados: {stats['total_matched'] + stats['total_unmatched']}\n"
        success_message += f"   • ✅ Encontrados: {stats['total_matched']}\n"
        success_message += f"   • ❌ No encontrados: {stats['total_unmatched']}\n"
        success_message += f"   • 📈 Tasa de éxito: {stats['match_rate']:.1%}\n\n"
        success_message += f"El archivo PDF ha sido guardado y está listo para su uso."
        
        messagebox.showinfo("Procesamiento Completado", success_message)
        
    def run(self):
        """Ejecuta la aplicación con configuración adicional."""
        # Configurar el icono de la ventana (si existe)
        try:
            # Intentar establecer un icono (esto es opcional)
            pass
        except:
            pass
            
        # Configurar el protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ejecutar la aplicación
        self.root.mainloop()
        
    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        # Aquí puedes añadir lógica de limpieza si es necesaria
        self.root.destroy()


# Clase adicional para efectos visuales
class VisualEffects:
    """Clase para manejar efectos visuales adicionales."""
    
    @staticmethod
    def create_hover_effect(widget, enter_color, leave_color):
        """Crea efecto hover para widgets."""
        def on_enter(e):
            widget.config(bg=enter_color)
            
        def on_leave(e):
            widget.config(bg=leave_color)
            
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    @staticmethod
    def animate_button_click(button):
        """Simula animación de click en botón."""
        original_relief = button.cget('relief')
        button.config(relief='sunken')
        button.after(100, lambda: button.config(relief=original_relief))


def create_gui_app() -> MainApplication:
    """
    Crea y retorna una instancia de la aplicación GUI moderna.
    
    Returns:
        Instancia de MainApplication con diseño mejorado
    """
    return MainApplication()


if __name__ == "__main__":
    app = create_gui_app()
    app.run()