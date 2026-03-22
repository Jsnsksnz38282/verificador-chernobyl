import tkinter as tk
import random
import string
import re

# =========================
# LEER LOGO
# =========================
def cargar_logo():
    try:
        with open("logo.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "VERIFICADOR CHERNOBYL"

# =========================
# VARIABLES
# =========================
mostrar = False

# =========================
# FUNCIONES
# =========================

def evaluar(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'\d', password): score += 1
    if re.search(r'[@$!%*?&]', password): score += 1
    return score


def actualizar_barra(score):
    colores = ["red", "orange", "yellow", "lightgreen", "lime"]
    barra.delete("all")
    if score > 0:
        barra.create_rectangle(0, 0, score*60, 20, fill=colores[score-1])
    else:
        barra.create_rectangle(0, 0, 10, 20, fill="grey")


def verificar():
    pwd = entry.get()
    score = evaluar(pwd)
    actualizar_barra(score)


def generar():
    global mostrar
    caracteres = string.ascii_letters + string.digits + "@$!%*?&"
    pwd = ''.join(random.choice(caracteres) for _ in range(12))
    entry.delete(0, tk.END)
    entry.insert(0, pwd)
    entry.config(show="")  # mostrar la generada
    btn_mostrar.config(text="Ocultar")
    mostrar = True
    score = evaluar(pwd)
    actualizar_barra(score)


def toggle_password():
    global mostrar
    if mostrar:
        entry.config(show="*")
        btn_mostrar.config(text="Mostrar")
        mostrar = False
    else:
        entry.config(show="")
        btn_mostrar.config(text="Ocultar")
        mostrar = True


def salir():
    root.destroy()

# =========================
# VENTANA
# =========================

root = tk.Tk()
root.title("Verificador Chernobyl")
root.geometry("500x420")
root.configure(bg="#0d0d0d")

# LOGO
logo_text = cargar_logo()
logo_label = tk.Label(root, text=logo_text, fg="#00ff00", bg="#0d0d0d", font=("Courier", 8), justify="left")
logo_label.pack(pady=5)

# Entrada
entry = tk.Entry(root, width=35, show="*", bg="black", fg="#00ff00", insertbackground="#00ff00")
entry.pack(pady=10)

# Botón mostrar
btn_mostrar = tk.Button(root, text="Mostrar", command=toggle_password, bg="black", fg="#00ff00")
btn_mostrar.pack(pady=5)

# Barra de seguridad
barra = tk.Canvas(root, width=300, height=20, bg="black", highlightthickness=0)
barra.pack(pady=5)

# Botones
btn_verificar = tk.Button(root, text="Verificar contraseña", command=verificar, bg="black", fg="#00ff00")
btn_verificar.pack(pady=5)

btn_generar = tk.Button(root, text="Crear contraseña", command=generar, bg="black", fg="#00ff00")
btn_generar.pack(pady=5)

btn_salir = tk.Button(root, text="Exit", command=salir, bg="black", fg="red")
btn_salir.pack(pady=15)

# Ejecutar
root.mainloop()