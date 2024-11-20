import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class EncuestaApp:
    def __init__(self, root):
        # Conexión a la base de datos MySQL
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Usa tu nombre de usuario de MySQL
            password="campusfp",  # Usa tu contraseña de MySQL
            database="ENCUESTAS"
        )
        self.cursor = self.db_connection.cursor()

        # Configurar la ventana tkinter
        self.root = root
        self.root.title("CRUD Encuesta")
        
        # Crear los widgets para todos los campos de la tabla ENCUESTA
        self.crear_widgets()

    def crear_widgets(self):
        # Etiquetas y campos de entrada para cada columna de la tabla ENCUESTA
        self.id_encuesta_label = tk.Label(self.root, text="ID Encuesta:")
        self.id_encuesta_label.grid(row=0, column=0, padx=10, pady=5)
        self.id_encuesta_entry = tk.Entry(self.root)
        self.id_encuesta_entry.grid(row=0, column=1, padx=10, pady=5)

        self.edad_label = tk.Label(self.root, text="Edad:")
        self.edad_label.grid(row=1, column=0, padx=10, pady=5)
        self.edad_entry = tk.Entry(self.root)
        self.edad_entry.grid(row=1, column=1, padx=10, pady=5)

        self.sexo_label = tk.Label(self.root, text="Sexo:")
        self.sexo_label.grid(row=2, column=0, padx=10, pady=5)
        self.sexo_entry = tk.Entry(self.root)
        self.sexo_entry.grid(row=2, column=1, padx=10, pady=5)

        self.bebidas_semana_label = tk.Label(self.root, text="Bebidas por Semana:")
        self.bebidas_semana_label.grid(row=3, column=0, padx=10, pady=5)
        self.bebidas_semana_entry = tk.Entry(self.root)
        self.bebidas_semana_entry.grid(row=3, column=1, padx=10, pady=5)

        self.cervezas_semana_label = tk.Label(self.root, text="Cervezas por Semana:")
        self.cervezas_semana_label.grid(row=4, column=0, padx=10, pady=5)
        self.cervezas_semana_entry = tk.Entry(self.root)
        self.cervezas_semana_entry.grid(row=4, column=1, padx=10, pady=5)

        self.bebidas_fin_semana_label = tk.Label(self.root, text="Bebidas Fin de Semana:")
        self.bebidas_fin_semana_label.grid(row=5, column=0, padx=10, pady=5)
        self.bebidas_fin_semana_entry = tk.Entry(self.root)
        self.bebidas_fin_semana_entry.grid(row=5, column=1, padx=10, pady=5)

        self.bebidas_destiladas_semana_label = tk.Label(self.root, text="Bebidas Destiladas Semana:")
        self.bebidas_destiladas_semana_label.grid(row=6, column=0, padx=10, pady=5)
        self.bebidas_destiladas_semana_entry = tk.Entry(self.root)
        self.bebidas_destiladas_semana_entry.grid(row=6, column=1, padx=10, pady=5)

        self.vinos_semana_label = tk.Label(self.root, text="Vinos por Semana:")
        self.vinos_semana_label.grid(row=7, column=0, padx=10, pady=5)
        self.vinos_semana_entry = tk.Entry(self.root)
        self.vinos_semana_entry.grid(row=7, column=1, padx=10, pady=5)

        self.perdidas_control_label = tk.Label(self.root, text="Pérdidas de Control:")
        self.perdidas_control_label.grid(row=8, column=0, padx=10, pady=5)
        self.perdidas_control_entry = tk.Entry(self.root)
        self.perdidas_control_entry.grid(row=8, column=1, padx=10, pady=5)

        self.diversion_dependencia_label = tk.Label(self.root, text="Diversión / Dependencia Alcohol:")
        self.diversion_dependencia_label.grid(row=9, column=0, padx=10, pady=5)
        self.diversion_dependencia_entry = tk.Entry(self.root)
        self.diversion_dependencia_entry.grid(row=9, column=1, padx=10, pady=5)

        self.problemas_digestivos_label = tk.Label(self.root, text="Problemas Digestivos:")
        self.problemas_digestivos_label.grid(row=10, column=0, padx=10, pady=5)
        self.problemas_digestivos_entry = tk.Entry(self.root)
        self.problemas_digestivos_entry.grid(row=10, column=1, padx=10, pady=5)

        self.tension_alta_label = tk.Label(self.root, text="Tensión Alta:")
        self.tension_alta_label.grid(row=11, column=0, padx=10, pady=5)
        self.tension_alta_entry = tk.Entry(self.root)
        self.tension_alta_entry.grid(row=11, column=1, padx=10, pady=5)

        self.dolor_cabeza_label = tk.Label(self.root, text="Dolor de Cabeza:")
        self.dolor_cabeza_label.grid(row=12, column=0, padx=10, pady=5)
        self.dolor_cabeza_entry = tk.Entry(self.root)
        self.dolor_cabeza_entry.grid(row=12, column=1, padx=10, pady=5)

        # Botones para operaciones CRUD
        self.create_button = tk.Button(self.root, text="Crear", command=self.create)
        self.create_button.grid(row=13, column=0, padx=10, pady=5)

        self.read_button = tk.Button(self.root, text="Leer", command=self.read)
        self.read_button.grid(row=13, column=1, padx=10, pady=5)

        self.update_button = tk.Button(self.root, text="Actualizar", command=self.update)
        self.update_button.grid(row=14, column=0, padx=10, pady=5)

        self.delete_button = tk.Button(self.root, text="Eliminar", command=self.delete)
        self.delete_button.grid(row=14, column=1, padx=10, pady=5)

        # Treeview for displaying results
        self.tree = ttk.Treeview(self.root, columns=("ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", 
                                                     "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", 
                                                     "PerdidasControl", "DiversionDependenciaAlcohol", 
                                                     "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), 
                                  show="headings")
        self.tree.grid(row=15, column=0, columnspan=4, padx=10, pady=10)

        # Define column headers for the Treeview
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Adjustments to the buttons layout
        self.create_button.grid(row=13, column=0, padx=10, pady=5)
        self.read_button.grid(row=13, column=1, padx=10, pady=5)
        self.update_button.grid(row=14, column=0, padx=10, pady=5)
        self.delete_button.grid(row=14, column=1, padx=10, pady=5)

    def create(self):
        # Insertar un nuevo registro en la base de datos
        try:
            id_encuesta = int(self.id_encuesta_entry.get())
            edad = int(self.edad_entry.get())
            sexo = self.sexo_entry.get()
            bebidas_semana = int(self.bebidas_semana_entry.get())
            cervezas_semana = int(self.cervezas_semana_entry.get())
            bebidas_fin_semana = int(self.bebidas_fin_semana_entry.get())
            bebidas_destiladas_semana = int(self.bebidas_destiladas_semana_entry.get())
            vinos_semana = int(self.vinos_semana_entry.get())
            perdidas_control = int(self.perdidas_control_entry.get())
            diversion_dependencia = self.diversion_dependencia_entry.get()
            problemas_digestivos = self.problemas_digestivos_entry.get()
            tension_alta = self.tension_alta_entry.get()
            dolor_cabeza = self.dolor_cabeza_entry.get()

            query = """
                INSERT INTO ENCUESTA (
                    idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                    BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol,
                    ProblemasDigestivos, TensionAlta, DolorCabeza
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (
                id_encuesta, edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, 
                bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia,
                problemas_digestivos, tension_alta, dolor_cabeza
            ))
            self.db_connection.commit()

            messagebox.showinfo("Éxito", "Registro añadido exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el registro: {e}")

    def read(self):
        # Read all records from the database and display them in the Treeview
        try:
            query = "SELECT * FROM ENCUESTA"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Clear previous data in the Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new rows into the Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los registros: {e}")

    def update(self):
        # Actualizar un registro existente en la base de datos
        try:
            id_encuesta = int(self.id_encuesta_entry.get())
            edad = int(self.edad_entry.get())
            sexo = self.sexo_entry.get()
            bebidas_semana = int(self.bebidas_semana_entry.get())
            cervezas_semana = int(self.cervezas_semana_entry.get())
            bebidas_fin_semana = int(self.bebidas_fin_semana_entry.get())
            bebidas_destiladas_semana = int(self.bebidas_destiladas_semana_entry.get())
            vinos_semana = int(self.vinos_semana_entry.get())
            perdidas_control = int(self.perdidas_control_entry.get())
            diversion_dependencia = self.diversion_dependencia_entry.get()
            problemas_digestivos = self.problemas_digestivos_entry.get()
            tension_alta = self.tension_alta_entry.get()
            dolor_cabeza = self.dolor_cabeza_entry.get()

            query = """
            UPDATE ENCUESTA
            SET edad = %s, 
                Sexo = %s, 
                BebidasSemana = %s, 
                CervezasSemana = %s, 
                BebidasFinSemana = %s, 
                BebidasDestiladasSemana = %s, 
                VinosSemana = %s, 
                PerdidasControl = %s, 
                DiversionDependenciaAlcohol = %s, 
                ProblemasDigestivos = %s, 
                TensionAlta = %s, 
                DolorCabeza = %s
            WHERE idEncuesta = %s
            """
            self.cursor.execute(query, (
                edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, 
                bebidas_destiladas_semana, vinos_semana, perdidas_control, 
                diversion_dependencia, problemas_digestivos, tension_alta, 
                dolor_cabeza, id_encuesta
            ))
            self.db_connection.commit()

            messagebox.showinfo("Éxito", "Registro actualizado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el registro: {e}")

    def delete(self):
        # Eliminar un registro de la base de datos
        try:
            id_encuesta = int(self.id_encuesta_entry.get())
            query = "DELETE FROM ENCUESTA WHERE idEncuesta = %s"
            self.cursor.execute(query, (id_encuesta,))
            self.db_connection.commit()

            messagebox.showinfo("Éxito", "Registro eliminado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el registro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncuestaApp(root)
    root.mainloop()

