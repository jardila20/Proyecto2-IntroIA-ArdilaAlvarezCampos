"""
Sudoku - Proyecto 2 Intro a IA por Ardila, Álvarez y Campos
- Imprime 9 cuadros 3x3 correctamente
- Permite cargar el tablero desde un .txt (9 líneas, 9 números por línea, separados por espacios o comas; 0 = vacío)
- Tres estrategias: Fuerza Bruta (FB), Backtracking (BT), Backtracking + Forward Checking (BT+FC)
"""

import time
import copy
import os

# ------------------------- Lectura desde archivo -------------------------

def leer_tablero_desde_txt(ruta):
    """
    Lee un tablero 9x9 desde un .txt.
    Formatos válidos por línea (ejemplos):
      0 0 3 0 2 0 6 0 0
      0,0,3,0,2,0,6,0,0
    Devuelve una lista de listas (9x9) de enteros.
    """
    tablero = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            # permitir comas o espacios
            linea = linea.replace(',', ' ')
            nums = [int(x) for x in linea.split() if x]
            if len(nums) != 9:
                raise ValueError("Cada línea debe tener 9 números. Revisa tu archivo.")
            tablero.append(nums)
    if len(tablero) != 9:
        raise ValueError("El archivo debe tener exactamente 9 líneas con 9 números cada una.")
    return tablero

# ------------------------- Auxiliares -------------------------

def encontrar_espacio_vacio(tablero):
    """Devuelve (fila, col) de la primera celda vacía (con 0). Si no hay, retorna (None, None)."""
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None

def movimiento_valido(tablero, fila, col, num):
    """Verifica si 'num' se puede poner en (fila, col) sin romper fila/col/subcuadrícula."""
    # Verificar fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False
    # Verificar columna
    for x in range(9):
        if tablero[x][col] == num:
            return False
    # Verificar subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[i + fila_inicial][j + col_inicial] == num:
                return False
    return True

def impresion(tablero):
    """Imprime el tablero con los 9 cuadros 3x3 bien formados."""
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
        # Agrupar con espacios entre números
        # Convertir a formato: | a b c | d e f | g h i |
        # Ya pusimos barras en fila_tokens; ahora unimos con espacios
        print(" ".join(fila_tokens))
        if (i + 1) % 3 == 0:
            print(sep)

# --------------------------- 1) Fuerza Bruta (FB) ---------------------------

def solucion1_FB(tablero):
    fila, col = encontrar_espacio_vacio(tablero)
    if fila is None:
        return tablero
    for num in range(1, 10):
        if movimiento_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            res = solucion1_FB(tablero)
            if isinstance(res, list):
                return res
            tablero[fila][col] = 0
    return "No hay solución"

# --------------------------- 2) Backtracking (BT) ---------------------------

def solucion2_BT(tablero):
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

# -------- 3) Backtracking + Comprobación hacia Adelante (BT+FC) --------

def construir_dominios(tablero):
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

# ---------------------------------- MAIN ----------------------------------
if __name__ == "__main__":
    # Si existe 'tablero.txt' en la misma carpeta, se usa; si no, se usa el del enunciado.
    ruta_txt = os.path.join(os.path.dirname(__file__), "tablero.txt")
    if os.path.exists(ruta_txt):
        tablero = leer_tablero_desde_txt(ruta_txt)
    else:
        tablero = [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0]
        ]

    print("TABLERO INICIAL:")
    impresion(tablero)

    # Copias para no mezclar resultados entre estrategias
    t1 = copy.deepcopy(tablero)
    t2 = copy.deepcopy(tablero)
    t3 = copy.deepcopy(tablero)

    # 1) FB
    t0 = time.perf_counter()
    r1 = solucion1_FB(t1)
    t1_time = time.perf_counter() - t0

    # 2) BT
    t0 = time.perf_counter()
    r2 = solucion2_BT(t2)
    t2_time = time.perf_counter() - t0

    # 3) BT + FC
    t0 = time.perf_counter()
    r3 = solucion3_BT_FC(t3)
    t3_time = time.perf_counter() - t0

    print("\n=== RESULTADOS ===")

    print("\nSolución 1 – Fuerza Bruta")
    if isinstance(r1, list):
        impresion(r1)
    else:
        print(r1)
    print(f"Tiempo aprox.: {t1_time:.6f} s")

    print("\nSolución 2 – Backtracking")
    if isinstance(r2, list):
        impresion(r2)
    else:
        print(r2)
    print(f"Tiempo aprox.: {t2_time:.6f} s")

    print("\nSolución 3 – BT + Comprobación hacia Adelante")
    if isinstance(r3, list):
        impresion(r3)
    else:
        print(r3)
    print(f"Tiempo aprox.: {t3_time:.6f} s")
