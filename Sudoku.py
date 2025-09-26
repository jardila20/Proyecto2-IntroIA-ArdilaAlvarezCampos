"""
Proyecto II Intro a la IA Sudoku 
- Realizado por Juan L. Ardila, Juan S. Álvarez y Samuel E. Campos
- Profesor Julio O. Palacio - PUJ
- Imprime 9 cuadros 3x3 correctamente
- Permite cargar el tablero desde un .txt (9 líneas, 9 números por línea, separados por espacios o comas; 0 = vacío)
- Tres estrategias: Fuerza Bruta (FB), Backtracking (BT), Backtracking + Forward Checking (BT+FC)
"""

import time
import copy
import os

# Lectura desde archivo

def leer_tablero_desde_txt(ruta):
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
                raise ValueError("Cada línea debe tener 9 números. Revise su archivo.")
            tablero.append(nums)
    if len(tablero) != 9:
        raise ValueError("El archivo debe tener exactamente 9 líneas con 9 números cada una.")
    return tablero

# Auxiliares 

def encontrar_espacio_vacio(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None

def movimiento_valido(tablero, fila, col, num):
    # Verifica fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False
    # Verifica columna
    for x in range(9):
        if tablero[x][col] == num:
            return False
    # Verifica cuadritos 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[i + fila_inicial][j + col_inicial] == num:
                return False
    return True

def impresion(tablero): 
    # Imprime un tablero 9x9 bien formateado.
    if not isinstance(tablero, list) or len(tablero) != 9 or any(len(fila) != 9 for fila in tablero):
        print("Error: el objeto pasado a impresion no es un tablero 9x9 válido")
        return

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


# Solución 1 - Fuerza Bruta (FB)

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

# Solución 2 - Backtracking (BT)

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

# Solución 3 - Backtracking + Comprobación hacia Adelante (BT+FC)

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

def tablero_valido(tablero):
    """Verifica que no haya repeticiones (1..9) en filas, columnas y subcuadros 3x3.
    Los ceros (vacíos) se ignoran en la validación."""
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
    # Subcuadros 3x3
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

# MAIN 
if __name__ == "__main__":
   # 1) Cargar tablero EXCLUSIVAMENTE desde tablero.txt (mismo directorio)
    ruta_txt = os.path.join(os.path.dirname(__file__), "tablero.txt")
    if not os.path.exists(ruta_txt):
        print("ERROR: No se encontró 'tablero.txt' en la misma carpeta del script.")
        print("Crea el archivo con 9 líneas y 9 números por línea (0 = vacío).")
        raise SystemExit(1)

    try:
        tablero = leer_tablero_desde_txt(ruta_txt)  # debe existir tu función de lectura
    except Exception as e:
        print(f"ERROR al leer 'tablero.txt': {e}")
        raise SystemExit(1)

    print("TABLERO INICIAL:")
    impresion(tablero)

    # 2) Validación inicial estricta
    if not tablero_valido(tablero):
        print("\nERROR: El tablero inicial es inválido (rompe reglas de Sudoku).")
        print("Revisa filas/columnas/subcuadros: no deben tener números repetidos.")
        raise SystemExit(1)

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
