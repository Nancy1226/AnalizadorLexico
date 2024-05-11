import re
import tkinter as tk

reservadas = ["for", "do", "while", "if", "else"]
parentesis_abre = ["("]
parentesis_cierra = [")"]

def analizar_linea(linea):
    tokens = []
    for token in reservadas:
        matches = re.findall(r"\b{}\b".format(token), linea)
        for match in matches:
            tokens.append(f"<Reservada {token}> {token}")
            linea = linea.replace(match, " ", 1)
    matches = re.findall(r"(?<!\()(\()(?!\()", linea)
    for match in matches:
        tokens.append(f"<Parentesis_apertura {match}>")
        linea = linea.replace(match, " ", 1)
    matches = re.findall(r"(?<!\))(\))(?!\))", linea)
    for match in matches:
        tokens.append(f"<Parentesis en cierre {match}>")
        linea = linea.replace(match, " ", 1)
    linea = linea.strip()
    if len(linea) > 0:
        tokens.append("<Simbolo no definido> {}".format(linea))
    return tokens

def analizar_codigo():
    codigo = entrada_texto.get("1.0", tk.END)
    lineas = codigo.split("\n")
    tokens_totales = []
    for i, linea in enumerate(lineas):
        tokens_linea = analizar_linea(linea)
        for token in tokens_linea:
            tokens_totales.append((i+1, token))

    resultado_texto.delete("1.0", tk.END)
    for numero_linea, token in tokens_totales:
        resultado_texto.insert(tk.END, f"Linea {numero_linea} {token}\n")

    contador_reservadas = len([token for numero_linea, token in tokens_totales if token.startswith("<Reservada")])
    contador_Parentesis_apertura = len([token for numero_linea, token in tokens_totales if token.startswith("<Parentesis_apertura")])
    contador_Parentesis_cierre = len([token for numero_linea, token in tokens_totales if token.startswith("<Parentesis en cierre")])

    resultado_texto.insert(tk.END, f"\nPalabras reservadas encontradas: {contador_reservadas}\n")
    resultado_texto.insert(tk.END, f"Parentesis de apertura encontrados: {contador_Parentesis_apertura}\n")
    resultado_texto.insert(tk.END, f"Parentesis de cierre encontrados: {contador_Parentesis_cierre}\n")

# Crear ventana
ventana = tk.Tk()
ventana.title("Analizador léxico")

# Crear entrada de texto para código
entrada_texto = tk.Text(ventana, height=20, width=50)
entrada_texto.pack(side=tk.LEFT, padx=10, pady=10)

# Crear botón para analizar código
boton_analizar = tk.Button(ventana, text="Analizar", command=analizar_codigo)
boton_analizar.pack(side=tk.LEFT, padx=10, pady=10)

# Crear cuadro de texto para mostrar resultados
resultado_texto = tk.Text(ventana, height=20, width=50)
resultado_texto.pack(side=tk.LEFT, padx=10, pady=10)

ventana.mainloop()