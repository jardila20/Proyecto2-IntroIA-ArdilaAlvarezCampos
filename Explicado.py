"""
Proyecto II Intro a la IA Sudoku 
- Realizado por Juan L. Ardila, Juan S. Álvarez y Samuel E. Campos
- Profesor Julio O. Palacio - PUJ

Funcionalidades principales:
- Imprime los 9 cuadros 3x3 de un Sudoku correctamente formateados.
- Permite cargar el tablero desde un archivo .txt (9 líneas, 9 números por línea,
  separados por espacios o comas; 0 = celda vacía).
- Implementa tres estrategias de resolución:
    1) Fuerza Bruta (FB)
    2) Backtracking (BT)
    3) Backtracking + Forward Checking (BT+FC)
"""

import time      # Para medir tiempos de ejecución de cada estrategia
import copy      # Para clonar el tablero y no mezclar estrategias
import os        # Para manejar rutas y verificar existencia del archivo


# ----------------------------------------------------------------------
# LECTURA DESDE ARCHIVO
# ----------------------------------------------------------------------

def leer_tablero_desde_txt(ruta):
    """
    Lee un archivo .txt que contiene un tablero Sudoku 9x9.
    - Cada línea debe tener 9 números (0 = vacío).
    - Los números pueden estar separados por espacios o comas.
    Retorna una lista de listas (matriz 9x9 de enteros).
    """
    tablero = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()          # Quitar espacios al inicio/fin
            if not linea:                  # Saltar líneas vacías
                continue
            linea = linea.replace(',', ' ')  # Reemplazar comas por espacios
            nums = [int(x) for x in linea.split() if x]
            if len(nums) != 9:
                raise ValueError("Cada línea debe tener exactamente 9 números.")
            tablero.append(nums)
    if len(tablero) != 9:
        raise ValueError("El archivo debe tener exactamente 9 líneas.")
    return tablero


# ----------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ----------------------------------------------------------------------

def encontrar_espacio_vacio(tablero):
    """
    Busca la primera celda vacía (con valor 0) en el tablero.
    Retorna (fila, columna) si encuentra una vacía, de lo contrario (None, None).
    """
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None


def movimiento_valido(tablero, fila, col, num):
    """
    Verifica si es válido colocar 'num' en la celda (fila, col).
    Restricciones:
    - El número no puede repetirse en la misma fila.
    - El número no puede repetirse en la misma columna.
    - El número no puede repetirse en la subcuadrícula 3x3 correspondiente.
    """
    # Fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False
    # Columna
    for x in range(9):
        if tablero[x][col] == num:
            return False
    # Subcuadro 3x3
    fila_ini, col_ini = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[fila_ini + i][col_ini + j] == num:
                return False
    return True


def impresion(tablero): 
    """
    Imprime el tablero en formato de Sudoku:
    - Cada subcuadro 3x3 delimitado con barras verticales y horizontales.
    - Los ceros se muestran como puntos (.) para indicar celdas vacías.
    """
    sep = "+-------+-------+-------+"
    print(sep)
    for i in range(9):
        fila_tokens = []
        for j in range(9):
            if j % 3 == 0:
                fila_tokens.append("|")
            val = tablero[i][j]
            ch = str(val) if val != 0 else "."
            fila_tokens.append(ch)
        fila_tokens.append("|")
        print(" ".join(fila_tokens))
        if (i + 1) % 3 == 0:
            print(sep)


# ----------------------------------------------------------------------
# SOLUCIÓN 1 – FUERZA BRUTA (FB)
# ----------------------------------------------------------------------

def solucion1_FB(tablero):
    """
    Estrategia de fuerza bruta:
    - Busca la primera celda vacía.
    - Intenta colocar números del 1 al 9 secuencialmente.
    - Valida con movimiento_valido.
    - Si ninguna opción funciona, devuelve "No hay solución".
    """
    fila, col = encontrar_espacio_vacio(tablero)
    if fila is None:  # Caso base: no hay vacíos
        return tablero
    for num in range(1, 10):
        if movimiento_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            res = solucion1_FB(tablero)
            if isinstance(res, list):
                return res
            tablero[fila][col] = 0  # retroceder
    return "No hay solución"


# ----------------------------------------------------------------------
# SOLUCIÓN 2 – BACKTRACKING (BT)
# ----------------------------------------------------------------------

def solucion2_BT(tablero):
    """
    Estrategia de backtracking clásico:
    - Igual que fuerza bruta, pero con ligera mejora:
      genera una lista de candidatos válidos para la celda actual.
    - Llama recursivamente a sí misma.
    """
    fila, col = encontrar_espacio_vacio(tablero)
    if fila is None:
        return tablero
    candidatos = [num for num in range(1,10) if movimiento_valido(tablero, fila, col, num)]
    for num in candidatos:
        tablero[fila][col] = num
        res = solucion2_BT(tablero)
        if isinstance(res, list):
            return res
        tablero[fila][col] = 0
    return "No hay solución"


# ----------------------------------------------------------------------
# SOLUCIÓN 3 – BACKTRACKING + FORWARD CHECKING (BT+FC)
# ----------------------------------------------------------------------

def construir_dominios(tablero):
    """
    Construye un diccionario con dominios posibles para cada celda vacía.
    Ejemplo: {(0,0): {1,2,3}, (0,1): {5,6}, ...}
    """
    dominios = {}
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                posibles = set()
                for num in range(1, 10):
                    if movimiento_valido(tablero, i, j, num):
                        posibles.add(num)
                dominios[(i, j)] = posibles
    return dominios


def vecinos(i, j):
    """
    Devuelve las coordenadas de todas las celdas vecinas de (i,j):
    - Misma fila
    - Misma columna
    - Misma subcuadrícula 3x3
    """
    v = set()
    for c in range(9):
        if c != j: v.add((i, c))
    for r in range(9):
        if r != i: v.add((r, j))
    fi, cj = 3 * (i // 3), 3 * (j // 3)
    for r in range(fi, fi + 3):
        for c in range(cj, cj + 3):
            if (r, c) != (i, j):
                v.add((r, c))
    return v


def fc_asignar_y_podar(tablero, dominios, i, j, valor):
    """
    Poda hacia adelante:
    - Asigna 'valor' a la celda (i,j).
    - Elimina 'valor' del dominio de sus vecinos.
    - Si algún vecino queda sin opciones, retorna None (inconsistencia).
    """
    nuevos_dom = {pos: set(vals) for pos, vals in dominios.items()}
    if (i, j) in nuevos_dom:
        del nuevos_dom[(i, j)]
    for (r, c) in vecinos(i, j):
        if (r, c) in nuevos_dom and valor in nuevos_dom[(r, c)]:
            nuevos_dom[(r, c)].remove(valor)
            if len(nuevos_dom[(r, c)]) == 0:
                return None
    return nuevos_dom


def solucion3_BT_FC(tablero):
    """
    Estrategia Backtracking + Forward Checking:
    - Similar al backtracking.
    - Usa dominios y poda temprana para evitar caminos imposibles.
    """
    i, j = encontrar_espacio_vacio(tablero)
    if i is None:
        return tablero
    dominios = construir_dominios(tablero)
    if (i, j) not in dominios or len(dominios[(i, j)]) == 0:
        return "No hay solución"
    for valor in sorted(dominios[(i, j)]):
        tablero[i][j] = valor
        nuevos_dom = fc_asignar_y_podar(tablero, dominios, i, j, valor)
        if nuevos_dom is not None:
            res = solucion3_BT_FC(tablero)
            if isinstance(res, list):
                return res
        tablero[i][j] = 0
    return "No hay solución"


# ----------------------------------------------------------------------
# VALIDACIÓN DE TABLERO
# ----------------------------------------------------------------------

def tablero_valido(tablero):
    """
    Verifica que el tablero inicial no tenga conflictos:
    - Ninguna fila tiene números repetidos.
    - Ninguna columna tiene números repetidos.
    - Ningún subcuadro 3x3 tiene números repetidos.
    Los ceros se ignoran.
    """
    # Filas
    for i in range(9):
        fila = [x for x in tablero[i] if x != 0]
        if len(fila) != len(set(fila)):
            return False
    # Columnas
    for j in range(9):
        col = [tablero[i][j] for i in range(9) if tablero[i][j] != 0]
        if len(col) != len(set(col)):
            return False
    # Subcuadros
    for sr in range(0, 9, 3):
        for sc in range(0, 9, 3):
            vals = []
            for i in range(sr, sr + 3):
                for j in range(sc, sc + 3):
                    if tablero[i][j] != 0:
                        vals.append(tablero[i][j])
            if len(vals) != len(set(vals)):
                return False
    return True


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # 1) Cargar tablero desde tablero.txt
    ruta_txt = os.path.join(os.path.dirname(__file__), "tablero.txt")
    if not os.path.exists(ruta_txt):
        print("ERROR: No se encontró 'tablero.txt'.")
        raise SystemExit(1)

    try:
        tablero = leer_tablero_desde_txt(ruta_txt)
    except Exception as e:
        print(f"ERROR al leer 'tablero.txt': {e}")
        raise SystemExit(1)

    print("TABLERO INICIAL:")
    impresion(tablero)

    # 2) Validar tablero antes de resolver
    if not tablero_valido(tablero):
        print("\nERROR: El tablero inicial es inválido (hay conflictos).")
        raise SystemExit(1)

    # 3) Resolver con las tres estrategias
    t1, t2, t3 = copy.deepcopy(tablero), copy.deepcopy(tablero), copy.deepcopy(tablero)

    t0 = time.perf_counter(); r1 = solucion1_FB(t1); t1_time = time.perf_counter() - t0
    t0 = time.perf_counter(); r2 = solucion2_BT(t2); t2_time = time.perf_counter() - t0
    t0 = time.perf_counter(); r3 = solucion3_BT_FC(t3); t3_time = time.perf_counter() - t0

    # 4) Mostrar resultados
    print("\n=== RESULTADOS ===")

    print("\nSolución 1 – Fuerza Bruta")
    impresion(r1 if isinstance(r1, list) else [[r1]])
    print(f"Tiempo: {t1_time:.6f} s")

    print("\nSolución 2 – Backtracking")
    impresion(r2 if isinstance(r2, list) else [[r2]])
    print(f"Tiempo: {t2_time:.6f} s")

    print("\nSolución 3 – Backtracking + Forward Checking")
    impresion(r3 if isinstance(r3, list) else [[r3]])
    print(f"Tiempo: {t3_time:.6f} s")
