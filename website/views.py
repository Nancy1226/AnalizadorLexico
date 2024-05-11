import re
from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

def analizar_codigo(codigo):
    reservadas = ["for", "do", "while", "if", "else"]
    parentesis_abre = ["("]
    parentesis_cierra = [")"]

    tokens_totales = []
    contador_reservadas = 0
    contador_parentesis_abre = 0
    contador_parentesis_cierra = 0

    lineas = codigo.split("\n")
    for i, linea in enumerate(lineas):
        tokens_linea = []

        # Buscar palabras reservadas
        for token in reservadas:
            matches = re.findall(r"\b{}\b".format(token), linea)
            for match in matches:
                tokens_linea.append(f"<Reservada {token}> {token}")
                linea = linea.replace(match, " ", 1)
                contador_reservadas += 1

        # Buscar paréntesis de apertura
        matches = re.findall(r"(?<!\()(\()(?!\()", linea)
        for match in matches:
            tokens_linea.append(f"<Parentesis_apertura {match}>")
            linea = linea.replace(match, " ", 1)
            contador_parentesis_abre += 1

        # Buscar paréntesis de cierre
        matches = re.findall(r"(?<!\))(\))(?!\))", linea)
        for match in matches:
            tokens_linea.append(f"<Parentesis en cierre {match}>")
            linea = linea.replace(match, " ", 1)
            contador_parentesis_cierra += 1

        # Agregar cualquier símbolo no definido
        linea = linea.strip()
        if len(linea) > 0:
            tokens_linea.append("<Simbolo no definido> {}".format(linea))

        tokens_totales.extend([(i+1, token) for token in tokens_linea])

    return tokens_totales, contador_reservadas, contador_parentesis_abre, contador_parentesis_cierra

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si se envió el formulario de carga de archivos
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return render_template('home.html', error="No se seleccionó ningún archivo")
            # Leer el contenido del archivo
            codigo = file.read().decode("utf-8")
        else:
            # Si no se envió el formulario de carga de archivos, asumimos que se envió el formulario de textarea
            codigo = request.form['codigo']

        # Realizar el análisis del código
        tokens_totales, contador_reservadas, contador_parentesis_abre, contador_parentesis_cierra = analizar_codigo(codigo)

        # Renderizar el template con los resultados
        return render_template('home.html', tokens=tokens_totales, contador_reservadas=contador_reservadas, contador_parentesis_abre=contador_parentesis_abre, contador_parentesis_cierra=contador_parentesis_cierra)

    return render_template('home.html', error=None)