import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import subprocess
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import traceback  # Para obtener información detallada en caso de error

class EncuestaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Encuestas")
        self.connection = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.login_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.host_entry = ttk.Entry(self.login_frame)
        self.host_entry.grid(row=0, column=1, pady=5)
        self.host_entry.insert(0, "localhost")

        ttk.Label(self.login_frame, text="Usuario:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_entry = ttk.Entry(self.login_frame)
        self.user_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.login_frame, text="Contraseña:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.login_frame, text="Base de Datos:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.database_entry = ttk.Entry(self.login_frame)
        self.database_entry.grid(row=3, column=1, pady=5)
        self.database_entry.insert(0, "encuestas")  # Nombre de la base de datos

        self.connect_button = ttk.Button(self.login_frame, text="Conectar", command=self.connect_to_db)
        self.connect_button.grid(row=4, column=0, columnspan=2, pady=10)

    def connect_to_db(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                messagebox.showinfo("Éxito", "Conexión exitosa a la base de datos.")
                self.login_frame.destroy()
                self.create_main_frame()
        except Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos:\n{e}")
            print(f"Error al conectar: {e}")
            traceback.print_exc()  # Imprime un traceback detallado del error

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Filtros
        filter_frame = ttk.LabelFrame(self.main_frame, text="Filtros", padding="10")
        filter_frame.grid(row=0, column=0, sticky=tk.W, pady=10)

        # Edad
        ttk.Label(filter_frame, text="Edad:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.edad_entry = ttk.Entry(filter_frame, width=10)
        self.edad_entry.grid(row=0, column=1, pady=5)

        # Sexo
        ttk.Label(filter_frame, text="Sexo:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.sexo_var = tk.StringVar()
        self.sexo_combobox = ttk.Combobox(filter_frame, textvariable=self.sexo_var, values=['Hombre', 'Mujer', ''],
                                          state='readonly', width=17)
        self.sexo_combobox.grid(row=0, column=3, pady=5)
        self.sexo_combobox.current(2)  # Seleccionar vacío por defecto

        # Bebidas a la Semana
        ttk.Label(filter_frame, text="Bebidas a la Semana:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bebidas_semana_entry = ttk.Entry(filter_frame, width=10)
        self.bebidas_semana_entry.grid(row=1, column=1, pady=5)

        # Pérdidas de Control
        ttk.Label(filter_frame, text="Pérdidas de Control:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.perdidas_control_entry = ttk.Entry(filter_frame, width=10)
        self.perdidas_control_entry.grid(row=1, column=3, pady=5)

        # Botón de consulta
        self.consultar_button = ttk.Button(filter_frame, text="Consultar", command=self.consultar)
        self.consultar_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Tabla de resultados
        self.tree = ttk.Treeview(self.main_frame,
                                 columns=("ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                                          "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
                                          "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta",
                                          "DolorCabeza"),
                                 show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Botones de acción
        action_frame = ttk.Frame(self.main_frame, padding="10")
        action_frame.grid(row=2, column=0, sticky=tk.W, pady=10)

        self.grafico_barras_button = ttk.Button(action_frame, text="Gráfico de Barras", command=self.grafico_barras)
        self.grafico_barras_button.grid(row=0, column=0, padx=5)

        self.grafico_circular_button = ttk.Button(action_frame, text="Gráfico Circular", command=self.grafico_circular)
        self.grafico_circular_button.grid(row=0, column=1, padx=5)

        self.exportar_excel_button = ttk.Button(action_frame, text="Exportar a Excel", command=self.exportar_excel)
        self.exportar_excel_button.grid(row=0, column=2, padx=5)

        self.exportar_pdf_button = ttk.Button(action_frame, text="Exportar a PDF", command=self.exportar_pdf)
        self.exportar_pdf_button.grid(row=0, column=3, padx=5)

        # Button to open the other script
        self.crud_button = ttk.Button(action_frame, text="Abrir CRUD", command=self.open_crud)
        self.crud_button.grid(row=0, column=4, padx=5)

    def consultar(self):
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return

        edad = self.edad_entry.get().strip()
        sexo = self.sexo_var.get().strip()
        bebidas_semana = self.bebidas_semana_entry.get().strip()
        perdidas_control = self.perdidas_control_entry.get().strip()

        query = "SELECT * FROM ENCUESTA WHERE 1=1"
        params = []

        # Validar e incluir criterios de búsqueda solo si tienen valor
        if edad.isdigit():  # Solo agregar si es un número
            query += " AND Edad = %s"
            params.append(int(edad))
        if sexo.lower() in ['hombre', 'mujer']:  # Verifica que el valor sea "hombre" o "mujer"
            query += " AND LOWER(Sexo) = %s"
            params.append(sexo.lower())
        if bebidas_semana.isdigit():
            query += " AND BebidasSemana = %s"
            params.append(int(bebidas_semana))
        if perdidas_control.isdigit():
            query += " AND PerdidasControl = %s"
            params.append(int(perdidas_control))

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, tuple(params))
            records = cursor.fetchall()

            # Limpiar la tabla
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Insertar los datos en la tabla si hay resultados
            if records:
                for row in records:
                    self.tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron resultados para los criterios de búsqueda.")

        except Error as e:
            messagebox.showerror("Error", f"Error al ejecutar la consulta:\n{e}")
            print(f"Error al ejecutar consulta: {e}")

    def grafico_barras(self):
        # Obtener los datos visibles de la tabla
        data = []
        for row in self.tree.get_children():
            data.append(self.tree.item(row)['values'])

        if not data:
            messagebox.showwarning("Sin datos", "No hay datos en la tabla para generar el gráfico.")
            return

        try:
            # Convertir datos a un DataFrame para facilidad de manejo
            df = pd.DataFrame(data, columns=["ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                            "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana",
                                            "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                                            "TensionAlta", "DolorCabeza"])

            # Convertir la columna "Edad" a tipo entero y calcular el promedio de "BebidasSemana" por "Edad"
            df["Edad"] = df["Edad"].astype(int)
            df["BebidasSemana"] = df["BebidasSemana"].astype(float)
            promedio_bebidas = df.groupby("Edad")["BebidasSemana"].mean()

            # Crear el gráfico de barras
            plt.bar(promedio_bebidas.index, promedio_bebidas.values, color='lightgreen')
            plt.title("Promedio de Bebidas por Edad (Datos Filtrados)")
            plt.xlabel("Edad")
            plt.ylabel("Promedio de Bebidas (Semana)")
            plt.xticks(promedio_bebidas.index)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el gráfico de barras:\n{e}")

    def grafico_circular(self):
        # Obtener los datos visibles de la tabla
        data = []
        for row in self.tree.get_children():
            data.append(self.tree.item(row)['values'])

        if not data:
            messagebox.showwarning("Sin datos", "No hay datos en la tabla para generar el gráfico.")
            return

        try:
            # Convertir datos a un DataFrame para facilidad de manejo
            df = pd.DataFrame(data, columns=["ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                            "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana",
                                            "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                                            "TensionAlta", "DolorCabeza"])

            # Contar las frecuencias por edad
            df["Edad"] = df["Edad"].astype(int)
            edad_counts = df["Edad"].value_counts()

            # Crear gráfico circular
            plt.pie(edad_counts.values, labels=edad_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            plt.title("Distribución de Edades (Datos Filtrados)")
            plt.axis("equal")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico circular:\n{e}")


    def exportar_excel(self):
        # Obtener los resultados que están actualmente en la tabla
        data = []
        for row in self.tree.get_children():
            data.append(self.tree.item(row)['values'])

        if data:
            # Convertir los resultados a un DataFrame
            df = pd.DataFrame(data,
                              columns=["ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                                       "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
                                       "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta",
                                       "DolorCabeza"])

            # Exportar los datos a Excel
            output_path = os.path.join(self.base_dir, "resultados_encuesta.xlsx")
            df.to_excel(output_path, index=False)
            messagebox.showinfo("Éxito", "Datos exportados a Excel con éxito.")
        else:
            messagebox.showwarning("Sin Datos", "No hay datos para exportar.")

    def exportar_pdf(self):
        # Exportar solo los datos de la consulta en la tabla a un archivo PDF
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Resultados de la Encuesta", ln=True, align="C")

            # Recuperar los datos de la tabla
            for item in self.tree.get_children():
                row = self.tree.item(item, "values")
                row_text = "  ||  ".join(str(cell) for cell in row)
                pdf.ln(10)
                pdf.cell(200, 10, txt=row_text, ln=True)

            output_path = os.path.join(self.base_dir, "resultados_encuesta.pdf")
            pdf.output(output_path)
            messagebox.showinfo("Éxito", "Datos exportados a PDF con éxito.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a PDF:\n{e}")

    def open_crud(self):
        """Open the SGE_H2_1ºT_VesnaBorjabad_CRUD.py script."""
        try:
            script_path = os.path.join(self.base_dir, "SGE_H2_1ºT_VesnaBorjabad_CRUD.py")
            subprocess.Popen(["python", script_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el CRUD:\n{e}")
            traceback.print_exc()

if __name__ == "__main__":
    root = tk.Tk()
    app = EncuestaApp(root)
    root.mainloop()