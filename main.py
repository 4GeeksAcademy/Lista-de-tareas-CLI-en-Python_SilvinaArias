"""
Aplicación CLI de Lista de Tareas (Todo List)
===============================================
Una aplicación de consola interactiva que permite gestionar tareas pendientes
con persistencia en archivo CSV. Desarrollada únicamente con la librería estándar de Python.

Funcionalidades:
  - Agregar tareas a la lista en memoria
  - Listar todas las tareas con numeración visible
  - Eliminar tareas por su número de posición
  - Guardar las tareas en un archivo CSV
  - Cargar las tareas desde un archivo CSV
  - Menú interactivo con bucle principal
"""

import csv
import os

# =============================================================================
# VARIABLE GLOBAL
# =============================================================================
# Lista global que almacena los títulos de las tareas pendientes en memoria.
# Se inicializa vacía y se va poblando durante la ejecución del programa.
todos = []


# =============================================================================
# FUNCIÓN: add_one_task(title)
# =============================================================================
def add_one_task(title):
    """
    Agrega una nueva tarea a la lista global 'todos'.

    Recibe un título (string) como parámetro y lo añade al final de la lista.
    No realiza ninguna validación adicional; simplemente inserta el título
    tal como fue proporcionado por el usuario.

    Parámetros:
        title (str): El título o descripción de la tarea a agregar.

    Retorna:
        None. La modificación se realiza directamente sobre la lista global.
    """
    todos.append(title)


# =============================================================================
# FUNCIÓN: print_list()
# =============================================================================
def print_list():
    """
    Muestra todas las tareas almacenadas en la lista global 'todos'.

    Cada tarea se muestra precedida por su número de posición empezando desde 1
    (formato legible para el usuario). Si la lista está vacía, se muestra un
    mensaje informativo indicando que no hay tareas pendientes.

    Parámetros:
        Ninguno.

    Retorna:
        None. La salida se imprime directamente en la consola.
    """
    if not todos:
        # La lista está vacía: mostramos un mensaje claro al usuario
        print("\n📋 No hay tareas pendientes. ¡Agrega una nueva tarea!")
        return

    # La lista tiene elementos: los recorremos e imprimimos con numeración
    print("\n📋 === LISTA DE TAREAS ===")
    for idx, task in enumerate(todos, start=1):
        print(f"  {idx}. {task}")
    print("=========================\n")


# =============================================================================
# FUNCIÓN: delete_task(number_to_delete)
# =============================================================================
def delete_task(number_to_delete):
    """
    Elimina una tarea de la lista global 'todos' según su posición numérica.

    El usuario proporciona un número empezando desde 1 (base 1). Internamente
    se convierte al índice correspondiente de la lista de Python (base 0)
    restando 1. Si el número está fuera del rango válido, se muestra un mensaje
    de error y no se modifica la lista.

    Parámetros:
        number_to_delete (int): Número de posición de la tarea a eliminar
                                (en base 1, tal como lo ve el usuario).

    Retorna:
        None. La eliminación se realiza directamente sobre la lista global.
    """
    # Convertimos de base 1 (usuario) a base 0 (Python)
    index = number_to_delete - 1

    # Verificamos si el índice está dentro del rango válido de la lista
    if 0 <= index < len(todos):
        # Extraemos la tarea eliminada para mostrar confirmación al usuario
        removed_task = todos.pop(index)
        print(f"✅ Tarea eliminada: \"{removed_task}\"")
    else:
        # El número proporcionado no corresponde a ninguna tarea existente
        print(f"❌ Error: No existe una tarea en la posición {number_to_delete}. "
              f"Actualmente hay {len(todos)} tarea(s) en la lista.")


# =============================================================================
# FUNCIÓN: save_todos()
# =============================================================================
def save_todos():
    """
    Persiste la lista actual de tareas en el archivo local 'todos.csv'.

    Abre (o crea) el archivo 'todos.csv' en modo escritura y guarda cada tarea
    como una fila individual. Utiliza el módulo 'csv' de la librería estándar
    para garantizar un formato correcto.

    Formato del CSV:
        Una sola columna sin cabecera, donde cada fila contiene el título
        de una tarea.

    Parámetros:
        Ninguno.

    Retorna:
        None. El archivo se escribe directamente en el disco.
    """
    # Abrimos el archivo en modo escritura ('w'), con newline='' para evitar
    # líneas en blanco adicionales en sistemas Windows.
    with open("todos.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Recorremos cada tarea en la lista y la escribimos como una fila
        # El writer espera una lista/iterable de columnas; entregamos [tarea].
        for task in todos:
            writer.writerow([task])

    print(f"💾 {len(todos)} tarea(s) guardada(s) correctamente en 'todos.csv'.")


# =============================================================================
# FUNCIÓN: load_todos()
# =============================================================================
def load_todos():
    """
    Lee el archivo 'todos.csv' (si existe) y reconstruye la lista global 'todos'
    en memoria.

    Si el archivo no existe, se muestra un aviso y la lista permanece vacía.
    Si existe, se lee cada fila y se agrega el título a la lista.

    Esta función se invoca automáticamente al iniciar el script para recuperar
    las tareas guardadas en la sesión anterior, y también puede llamarse desde
    el menú interactivo cuando el usuario lo solicite.

    Parámetros:
        Ninguno.

    Retorna:
        None. La lista global 'todos' se actualiza directamente.
    """
    global todos  # Necesario para reasignar la lista global

    # Verificamos si el archivo existe antes de intentar abrirlo
    if not os.path.exists("todos.csv"):
        print("ℹ️  No se encontró el archivo 'todos.csv'. Se inicia con la lista vacía.")
        todos = []  # Reiniciamos la lista por si acaso
        return

    # El archivo existe: lo abrimos y leemos su contenido
    with open("todos.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        # Reconstruimos la lista leyendo cada fila del CSV
        # Cada fila es una lista con un solo elemento (el título de la tarea)
        todos = [row[0] for row in reader if row]  # Filtramos filas vacías

    print(f"📂 {len(todos)} tarea(s) cargada(s) desde 'todos.csv'.")


# =============================================================================
# FUNCIÓN PRINCIPAL: main()
# =============================================================================
def main():
    """
    Función principal que orquesta el flujo de la aplicación CLI.

    Al iniciar:
      1. Carga automáticamente las tareas desde 'todos.csv' (si existe).
      2. Entra en un bucle while infinito que muestra un menú interactivo.
      3. El usuario puede elegir entre 6 opciones numéricas.
      4. El bucle se rompe cuando el usuario selecciona la opción "Salir" (6).

    No recibe parámetros ni retorna valores. La interacción se realiza
    íntegramente a través de la consola.
    """
    # --- CARGA INICIAL AUTOMÁTICA ---
    # Al arrancar el programa, recuperamos las tareas de la sesión anterior
    # si existe el archivo 'todos.csv'.
    print("🚀 Iniciando aplicación de Lista de Tareas...")
    load_todos()

    # --- BUCLE PRINCIPAL DEL MENÚ ---
    while True:
        # Mostramos el menú de opciones al usuario
        print("\n" + "=" * 40)
        print("          MENÚ PRINCIPAL")
        print("=" * 40)
        print("  1) Agregar tarea")
        print("  2) Listar tareas")
        print("  3) Eliminar tarea por número")
        print("  4) Guardar en CSV")
        print("  5) Cargar desde CSV")
        print("  6) Salir")
        print("=" * 40)

        # Solicitamos la opción al usuario
        opcion = input("👉 Selecciona una opción (1-6): ").strip()

        # --- PROCESAMOS LA OPCIÓN SELECCIONADA ---
        if opcion == "1":
            # Opción 1: Agregar tarea
            title = input("📝 Escribe el título de la tarea: ").strip()
            if title:
                add_one_task(title)
                print(f"✅ Tarea \"{title}\" agregada correctamente.")
            else:
                print("⚠️  No se puede agregar una tarea vacía. Intenta de nuevo.")

        elif opcion == "2":
            # Opción 2: Listar tareas
            print_list()

        elif opcion == "3":
            # Opción 3: Eliminar tarea por número
            try:
                numero = int(input("🔢 Introduce el número de la tarea a eliminar: ").strip())
                delete_task(numero)
            except ValueError:
                print("❌ Error: Debes ingresar un número válido.")

        elif opcion == "4":
            # Opción 4: Guardar en CSV
            save_todos()

        elif opcion == "5":
            # Opción 5: Cargar desde CSV
            load_todos()

        elif opcion == "6":
            # Opción 6: Salir del programa
            print("👋 ¡Gracias por usar la aplicación! Hasta luego.")
            break  # Rompe el bucle while y finaliza el programa

        else:
            # Opción no válida
            print("❌ Opción no válida. Por favor, selecciona un número entre 1 y 6.")


# =============================================================================
# PUNTO DE ENTRADA DEL SCRIPT
# =============================================================================
# Esta condición garantiza que el código solo se ejecute cuando este archivo
# se ejecuta directamente (no cuando se importa como módulo desde otro script).
if __name__ == "__main__":
    main()