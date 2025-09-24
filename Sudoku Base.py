def encontrar_espacio_vacio(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None


def movimiento_valido(tablero, fila, col, num):
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
    for fila in tablero:
        print(fila)
        
def solucion1_FB(tablero):
    
      #return True or False
      
def solucion2_BT(tablero):
    
      #return True or False 
      
def solucion3_BT_FC(tablero):
    
      #return True or False 
      
if __name__ == "__main__":
    
    tablero = [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]]
    
    print("\nSolución:")
    resultado = solucion1_FB(tablero)
    if isinstance(resultado, str):
        print(resultado)
    else:
        for fila in resultado:
            print(fila) 
