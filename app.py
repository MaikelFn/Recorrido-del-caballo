from flask import Flask, render_template, request, session
from logica import generar_ruta_caballo 

"""
app.py - Servidor Flask para la visualización del Knight's Tour (Recorrido del Caballo).

Descripción:
  recoge parámetros del usuario (tamaño del tablero y posición inicial),
  invoca la lógica del Knight's Tour (modulo logica.py) y renderiza plantillas Jinja2 para:
    - entrada de parámetros (Entradas.html)
    - vista previa del tablero (Tablero.html)
    - animación / resultado (Ruta.html)

"""

app = Flask(__name__)
app.secret_key = 'claveultramegahipersecretaquenadieadivinara'

@app.route('/')
def main():

    """
    Ruta principal (GET).
    
    Entradas:
      - ninguna (GET)
    Salidas:
      - renderiza la plantilla 'Entradas.html' que contiene el formulario inicial.
    Restricciones:
      - ninguna
    """

    return render_template('Entradas.html')

@app.route('/tablero', methods=['POST'])
def tablero():

    """
    Ruta que recibe los parámetros del formulario inicial y muestra la vista previa del tablero.
    
    Entradas:
      - request.form['tamaño']  : tamaño del tablero (esperado como entero en string)
      - request.form['fila']    : fila inicial del caballo (esperado como entero en string)
      - request.form['columna'] : columna inicial del caballo (esperado como entero en string)
    
    Salidas:
      - renderiza 'Tablero.html' pasando las variables (tamaño, fila, columna).
    
    Restricciones / efectos:
      - Convierte los valores recibidos a int directamente con int(...). Si el formulario no
        envía valores válidos, se lanzará ValueError y la petición fallará.
      - Guarda los valores en session para que estén disponibles en pasos posteriores.
    """

    tamaño = int(request.form.get('tamaño'))
    fila = int(request.form.get('fila'))
    columna = int(request.form.get('columna'))

    session['tamaño'] = tamaño
    session['fila'] = fila
    session['columna'] = columna

    return render_template('Tablero.html', tamaño=tamaño, fila=fila, columna=columna)

@app.route('/generar', methods=['POST'])
def generar():

    """
    Ruta que inicia la generación del recorrido y renderiza la vista de la ruta.

    Flujo:
      1. Recupera desde session los parámetros (tamaño, fila, columna) establecidos previamente.
      2. Lee request.form['Recorrido'] para determinar el tipo ('abierto' o 'cerrado').
      3. Invoca generar_ruta_caballo(tamaño, fila, columna, tipo) que debe devolver:
        (Ruta, tiempo_total) donde Ruta es la lista de pasos/eventos y tiempo_total es el tiempo
        de cómputo en segundos.
      4. Renderiza 'Ruta.html' pasando Ruta, Tamaño, Tipo y Tiempo.

    Entradas:
      - session['tamaño'], session['fila'], session['columna'] (esperados)
      - request.form['Recorrido'] (esperado: 'abierto' o 'cerrado')

    Salidas:
      - render_template('Ruta.html', Ruta=Ruta, Tamaño=tamaño, Tipo=tipo, Tiempo=tiempo_total)
      """

    tamaño = session.get('tamaño')
    fila = session.get('fila')
    columna = session.get('columna')
    Recorrido = request.form.get('Recorrido')

    session['Recorrido'] = Recorrido

    tipo = Recorrido
    if tipo == 'cerrado' and tamaño % 2 != 0:
        return render_template('Error.html', mensaje="No existe recorrido cerrado para tableros de tamaño impar.", tamaño=tamaño)

    Ruta, tiempo_total = generar_ruta_caballo(tamaño, fila, columna, tipo)
    if not Ruta:
        return render_template('Error.html', mensaje=f"No existe un recorrido {tipo} para esta configuración.", tamaño=tamaño)

    return render_template('Ruta.html', Ruta=Ruta, Tamaño=tamaño, Tipo=tipo, Tiempo=tiempo_total)


@app.route('/reiniciar')
def reiniciar():

    """
    Ruta para regenerar el mismo recorrido usando los parámetros almacenados en session.

    Entradas:
      - session['tamaño'], session['fila'], session['columna'], session['Recorrido']

    Salidas:
      - render_template('Ruta.html', Ruta=Ruta, Tamaño=tamaño, Tipo=tipo, Tiempo=tiempo_total)
    """

    tamaño = session.get('tamaño')
    fila = session.get('fila')
    columna = session.get('columna')
    Recorrido = session.get('Recorrido')
    
    tipo = Recorrido
    
    Ruta, tiempo_total = generar_ruta_caballo(tamaño, fila, columna, tipo)
    return render_template('Ruta.html', Ruta=Ruta, Tamaño=tamaño, Tipo=tipo, Tiempo=tiempo_total)


@app.route('/inicio')
def inicio():

    """
    Ruta que limpia la sesión y vuelve al formulario de entrada.

    Entradas:
      - ninguna
    Salidas:
      - render_template('Entradas.html')
    Efectos:
      - session.clear() elimina todas las claves almacenadas en session.
    """

    session.clear()
    return render_template('Entradas.html')

if __name__ == '__main__':
    app.run(debug=True)