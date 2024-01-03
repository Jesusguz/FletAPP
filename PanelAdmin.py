import flet as ft
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import re  # Importa el módulo de expresiones regulares

cred = credentials.Certificate("observaciones-eaa5f-firebase-adminsdk-vhtlq-c2ab67c954.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Hacer que 'table' sea una variable global
table = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Alumno")),
        ft.DataColumn(ft.Text("Aviso")),
        ft.DataColumn(ft.Text("Fecha")),
    ],
    rows=[]
)

def main(page: ft.Page):
    def dropdown_changed(e):
        # Limpiar la tabla
        table.rows.clear()

        # Buscar datos en Firestore
        avisos_ref = db.collection('avisos')
        docs = avisos_ref.stream()

        # Añadir datos a la tabla
        registros_hoy = 0  # Contador de registros de hoy
        for doc in docs:
            data = doc.to_dict()
            fecha = data.get('fecha')
            alumnos = re.split(r'(?<=\))', data['alumnos'])  # Separar los alumnos por ')'
            for alumno in alumnos:
                if alumno:  # Ignorar cadenas vacías
                    alumno = alumno.strip()
                    if "primaria" in alumno.lower() and dropdown.value == "Primaria":  # Filtrar por nivel primaria
                        if fecha is not None and fecha.date() == datetime.now().date():
                            registros_hoy += 1
                            row = ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(alumno)),
                                    ft.DataCell(ft.Text(data['aviso'])),
                                    ft.DataCell(ft.Text(str(fecha.date()))),
                                ],
                            )
                            table.rows.append(row)
                    elif "(secundaria)" in alumno.lower() and dropdown.value == "SECUNDARIA":  # Filtrar por nivel secundaria
                        if fecha is not None and fecha.date() == datetime.now().date():
                            registros_hoy += 1
                            row = ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(alumno)),
                                    ft.DataCell(ft.Text(data['aviso'])),
                                    ft.DataCell(ft.Text(str(fecha.date()))),
                                ],
                            )
                            table.rows.append(row)

        # Si no hay registros de hoy, imprimir un mensaje y añadir una fila a la tabla
        if registros_hoy == 0:
            print("No hay registros de hoy")
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text('No Hay registros hoy')),
                    ft.DataCell(ft.Text('')),
                    ft.DataCell(ft.Text('')),
                ],
            )
            table.rows.append(row)

        # Actualizar la página
        page.update()

    # Añade un título
    page.title="Panel Administrativo"

    # Añade un selector
    dropdown = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("Primaria"),
            ft.dropdown.Option("SECUNDARIA"),
            ft.dropdown.Option("BACHILLERATO"),
        ],
        autofocus=True,
    )
    print(dropdown.value)
    page.add(dropdown)

    # Añade la tabla
    page.add(table)

ft.app(target=main)
