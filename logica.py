import copy
import time

def CrearTablero(Tamaño, FilaInicial, ColumnaInicial):
    """
    Funcion encargada de crear la matriz que representa el tablero de ajedrez.
    
    Args:
        Tamaño (int): Tamaño del tablero (n x n).
        FilaInicial (int): Fila inicial del caballo.
        ColumnaInicial (int): Columna inicial del caballo.
        
    Returns:
        list: Matriz que representa el tablero de ajedrez.
    Notes:
        La matriz se inicializa con -1 (no visitada) en todas las posiciones, 
        excepto en la posición inicial del caballo, que se establece en 0 (caballo).
    """
    tablero = []
    for fila in range(Tamaño):
        subLista = []
        for columna in range(Tamaño):
            subLista.append(-1)
        tablero.append(subLista)
    tablero[FilaInicial][ColumnaInicial] = 0
    return tablero

def Movimiento_Valido(tablero, filaActual, colActual, Tamaño):
    """
    Evalúa si un movimiento esta dentro de los límites del tablero y si la posición no ha sido visitada.
    
    Args:
        tablero (list): Matriz que representa el tablero de ajedrez.
        filaActual (int): Fila actual del caballo.
        colActual (int): Columna actual del caballo.
        Tamaño (int): Tamaño del tablero (n x n).
        
    Returns:
        bool: True si el movimiento es válido, False en caso contrario.
    
    Notes:
        Esta función se utiliza para verificar si el caballo puede moverse a una posición en el tablero.
        Acepta posiciones no visitadas (-1) como válidas.
    """
    if 0 <= filaActual < Tamaño and 0 <= colActual < Tamaño:
        if tablero[filaActual][colActual] == -1:
            return True
    return False


def Encontrar_Camino_Abierto(filaActual, colActual, tablero, Tamaño, contador, Ruta):
    """
    Funcion recursiva para encontrar un camino abierto del caballo en el tablero,
    evaluando todas las posibles posiciones a partir de la posición actual.
    
    Args:
        filaActual (int): Fila actual del caballo.
        colActual (int): Columna actual del caballo.
        tablero (list): Matriz que representa el tablero de ajedrez.
        Tamaño (int): Tamaño del tablero (n x n).
        contador (int): Contador de movimientos realizados por el caballo.
        Ruta (list): Lista que almacena los estados del tablero durante el recorrido.
    
    Returns:
        bool: True si se encuentra un camino abierto, False en caso contrario.
    
    Notes:
        Un camino abierto es aquel en el que el caballo visita todas las casillas del tablero
        pero no necesariamente regresa a la posición inicial.
    """
    if contador == Tamaño * Tamaño:
        tablero[filaActual][colActual] = 'C'  # Marcar la última posición con 'C'
        Ruta.append(copy.deepcopy(tablero))
        tablero[filaActual][colActual] = contador - 1  # Restaurar el número
        return True
    
    if Movimiento_Valido(tablero, filaActual+2, colActual-1, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual+2, colActual-1, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual+2, colActual+1, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual+2, colActual+1, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-2, colActual-1, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual-2, colActual-1, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-2, colActual+1, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual-2, colActual+1, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual+1, colActual-2, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual+1, colActual-2, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-1, colActual-2, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual-1, colActual-2, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual+1, colActual+2, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual+1, colActual+2, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-1, colActual+2, Tamaño):
        if realizar_movimiento_Abierto(tablero, filaActual-1, colActual+2, Tamaño, contador, filaActual, colActual, Ruta):
            return True
        
    return False

def realizar_movimiento_Abierto(tablero, filaActual, colActual, Tamaño, contador, filaAnterior, colAnterior, Ruta):
    """
    Realiza el movimiento del caballo en el tablero y guarda el número de movimiento.
    
    Args:
        Ruta: Lista que almacena tuplas (fila, columna, tipo) donde tipo es 'A' (avance) o 'R' (retroceso)
    """
    tablero[filaActual][colActual] = contador
    Ruta.append((filaActual, colActual, 'A'))
    
    if Encontrar_Camino_Abierto(filaActual, colActual, tablero, Tamaño, contador + 1, Ruta):
        return True

    tablero[filaActual][colActual] = -1
    Ruta.append((filaAnterior, colAnterior, 'R'))

    return False

def Encontrar_Camino_Cerrado(filaActual, colActual, tablero, Tamaño, contador, soluciones, Ruta):
    """
    Encuentra un camino cerrado del caballo en el tablero, asegurando que el último movimiento
    pueda volver a la posición inicial.
    
    Args:
        filaActual (int): Fila actual del caballo.
        colActual (int): Columna actual del caballo.
        tablero (list): Matriz que representa el tablero de ajedrez.
        Tamaño (int): Tamaño del tablero (n x n).
        contador (int): Contador de movimientos realizados por el caballo.
        soluciones (list): Lista de tuplas con las posiciones adyacentes a la posición inicial.
    
    Returns:
        bool: True si se encuentra un camino cerrado, False en caso contrario.
    
    Notes:
        Un camino cerrado es aquel en el que el caballo visita todas las casillas del tablero
        y termina en una posición adyacente a la inicial, desde la cual puede regresar con un movimiento válido.
    """
    
    if contador == Tamaño * Tamaño:
        if (filaActual, colActual) in soluciones:
            tablero[filaActual][colActual] = 'C'
            Ruta.append(copy.deepcopy(tablero))
            return True
        return False
    
    if Movimiento_Valido(tablero, filaActual+2, colActual-1, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual+2, colActual-1, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual+2, colActual+1, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual+2, colActual+1, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-2, colActual-1, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual-2, colActual-1, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-2, colActual+1, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual-2, colActual+1, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual+1, colActual-2, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual+1, colActual-2, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-1, colActual-2, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual-1, colActual-2, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual+1, colActual+2, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual+1, colActual+2, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
        
    if Movimiento_Valido(tablero, filaActual-1, colActual+2, Tamaño):
        if Realizar_Movimiento_Cerrado(tablero, filaActual-1, colActual+2, Tamaño, contador, soluciones, filaActual, colActual, Ruta):
            return True
    return False

def Realizar_Movimiento_Cerrado(tablero, filaActual, colActual, Tamaño, contador, soluciones, filaAnterior, colAnterior, Ruta):
    """
    Realiza el movimiento del caballo en el tablero y guarda el número de movimiento.
    
    Args:
        tablero (list): Matriz que representa el tablero de ajedrez.
        filaActual (int): Fila a la que se mueve el caballo.
        colActual (int): Columna a la que se mueve el caballo.
        Tamaño (int): Tamaño del tablero (n x n).
        contador (int): Contador de movimientos realizados por el caballo.
        soluciones (list): Lista de tuplas con las posiciones adyacentes a la posición inicial.
        filaAnterior (int): Fila de la posición anterior del caballo.
        colAnterior (int): Columna de la posición anterior del caballo.
    
    Returns:
        bool: True si se encuentra un camino cerrado, False en caso contrario.
    
    Notes:
        Esta función guarda el número de movimiento en cada posición visitada del tablero.
    """
    tablero[filaActual][colActual] = contador  # guardar el número del movimiento actual
    Ruta.append((filaActual, colActual, 'A'))
    
    if Encontrar_Camino_Cerrado(filaActual, colActual, tablero, Tamaño, contador + 1, soluciones, Ruta):
        return True
    tablero[filaActual][colActual] = -1  # restaurar como no visitada
    Ruta.append((filaAnterior, colAnterior, 'R'))
    
    return False


def Encontrar_Soluciones(tablero, fila, columna, tamaño):
    """
    Encuentra todas las posiciones válidas adyacentes a la posición inicial del caballo.
    
    Args:
        tablero (list): Matriz que representa el tablero de ajedrez.
        fila (int): Fila inicial del caballo.
        columna (int): Columna inicial del caballo.
        tamaño (int): Tamaño del tablero (n x n).
        
    Returns:
        list: Lista de tuplas con las posiciones adyacentes válidas a la posición inicial.
    
    Notes:
        Esta función evalúa los 8 movimientos posibles del caballo desde la posición inicial
        y retorna aquellas posiciones que son válidas.
    """
    adyacentes = []
    if Movimiento_Valido(tablero, fila + 2, columna - 1, tamaño):
        adyacentes.append((fila + 2, columna - 1))
    if Movimiento_Valido(tablero, fila + 2, columna + 1, tamaño):
        adyacentes.append((fila + 2, columna + 1))
    if Movimiento_Valido(tablero, fila - 2, columna - 1, tamaño):
        adyacentes.append((fila - 2, columna - 1))
    if Movimiento_Valido(tablero, fila - 2, columna + 1, tamaño):
        adyacentes.append((fila - 2, columna + 1))
    if Movimiento_Valido(tablero, fila + 1, columna - 2, tamaño):
        adyacentes.append((fila + 1, columna - 2))
    if Movimiento_Valido(tablero, fila + 1, columna + 2, tamaño):
        adyacentes.append((fila + 1, columna + 2))
    if Movimiento_Valido(tablero, fila - 1, columna - 2, tamaño):
        adyacentes.append((fila - 1, columna - 2))
    if Movimiento_Valido(tablero, fila - 1, columna + 2, tamaño):
        adyacentes.append((fila - 1, columna + 2))
    return adyacentes

def generar_ruta_caballo(tamaño, fila, columna, tipo):
    """
    Genera la ruta del recorrido del caballo en el tablero de ajedrez.

    Args:
        tamaño (int): Tamaño del tablero (n x n).
        fila (int): Fila inicial del caballo.
        columna (int): Columna inicial del caballo.
        tipo (str): Tipo de recorrido ('abierto' o 'cerrado').

    Returns:
        tuple: (Ruta, tiempo_total)
            Ruta (list): Lista de movimientos realizados por el caballo.
            tiempo_total (float): Tiempo que tardó en encontrar la solución (en segundos).

    Notes:
        Si no se encuentra solución, Ruta será una lista vacía.
    """
    inicio = time.perf_counter()
    tablero2 = CrearTablero(tamaño, fila, columna)

    Ruta = [(fila, columna, 'A')]

    if tipo == 'cerrado':
        soluciones = Encontrar_Soluciones(tablero2, fila, columna, tamaño)
        if Encontrar_Camino_Cerrado(fila, columna, tablero2, tamaño, 1, soluciones, Ruta):
            fin = time.perf_counter()
            tiempo_total = fin - inicio
            return Ruta, tiempo_total
    else:
        if Encontrar_Camino_Abierto(fila, columna, tablero2, tamaño, 1, Ruta):
            fin = time.perf_counter()
            tiempo_total = fin - inicio
            return Ruta, tiempo_total

    fin = time.perf_counter()
    tiempo_total = fin - inicio
    return [], tiempo_total

