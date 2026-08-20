"""
Aplicación CLI de Lista de Tareas (Todo List)
===============================================
Solución definitiva para problemas de visualización en terminales
con desbordamiento de búfer.
"""

import csv
import os
import sys

# Variable global
todos = []

# Ruta absoluta basada en la ubicación del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "todos.csv")


def add_one_task(title):
    """Agrega una nueva tarea a la lista global 'todos'."""
    todos.append(title)


def print_list():
    """Muestra las tareas e imprime directamente forzando la salida."""
    print("\n-----------------------------------")
    print("      LISTA DE TAREAS PENDIENTES")
    print("-----------------------------------")
    
    if not todos:
        print("La lista está vacía. No hay tareas pendientes.")
    else:
        for idx, task in enumerate(todos, start=1):
            print(f"  {idx}. {task}")
        print(f"\nTotal: {len(todos)} tarea(s)")
    
    print("-----------------------------------")
    # Forzamos a la consola a volcar el texto inmediatamente
    sys.stdout.flush()


def delete_task(number_to_delete):
    """Elimina una tarea por su posición numérica (base 1)."""
    index = number_to_delete - 1

    if 0 <= index < len(todos):
        removed_task = todos.pop(index)
        print(f"✅ Tarea eliminada: '{removed_task}'")
        return True
    else:
        print(f"❌ Error: No existe una tarea en la posición {number_to_delete}.")
        return False


def save_todos():
    """Guarda las tareas en el archivo CSV."""
    try:
        with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for task in todos:
                writer.writerow([task])
        print("💾 Cambios guardados en 'todos.csv'.")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")


def load_todos():
    """Carga las tareas guardadas desde el CSV."""
    global todos
    if not os.path.exists(FILE_PATH):
        todos = []
        return

    try:
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            loaded_tasks = [row[0] for row in reader if row and len(row) > 0 and row[0].strip()]
            todos = loaded_tasks
    except Exception as e:
        print(f"❌ Error al cargar: {e}")


def main():
    """Bucle principal de la consola."""
    print("🚀 Iniciando aplicación de Lista de Tareas...")
    load_todos()

    while True:
        print("\n========================================")
        print("            MENÚ PRINCIPAL")
        print("========================================")
        print("1) Agregar tarea")
        print("2) Listar tareas")
        print("3) Eliminar tarea por número")
        print("4) Guardar en CSV")
        print("5) Cargar desde CSV")
        print("6) Salir")
        print("========================================")

        opcion = input("👉 Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            title = input("📝 Escribe el título de la tarea: ").strip()
            if title:
                add_one_task(title)
                save_todos()
                print(f"✅ Tarea '{title}' agregada exitosamente.")
            else:
                print("⚠️ No se puede agregar una tarea vacía.")

        elif opcion == "2":
            print_list()
            # Limpiamos posibles 'Enter' residuales del búfer
            sys.stdin.flush() if hasattr(sys.stdin, 'flush') else None
            input("\n[PAUSA] Presiona ENTER para regresar al menú...")

        elif opcion == "3":
            if not todos:
                print("📋 No hay tareas pendientes para eliminar.")
            else:
                print_list()
                try:
                    num_input = input("🔢 Introduce el número de la tarea a eliminar: ").strip()
                    numero = int(num_input)
                    if delete_task(numero):
                        save_todos()
                except ValueError:
                    print("❌ Error: Ingresa un número entero válido.")

        elif opcion == "4":
            save_todos()

        elif opcion == "5":
            load_todos()
            print_list()
            input("\n[PAUSA] Presiona ENTER para regresar al menú...")

        elif opcion == "6":
            print("👋 Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida. Selecciona un número del 1 al 6.")


if __name__ == "__main__":
    main()
    