import tkinter as tk
import random
import string
import re
import time

# =========================
# RESPONSIVE
# =========================
def on_resize(event):
    size = max(10, int(event.width / 25))
    entry.config(font=("Courier", size))
    titulo.config(font=("Courier", size+4, "bold"))

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
        barra.create_rectangle(0, 0, score*80, 25, fill=colores[score-1])
    else:
        barra.create_rectangle(0, 0, 20, 25, fill="grey")


def tiempo_crack(password):
    charset = 0

    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'\d', password): charset += 10
    if re.search(r'[@$!%*?&]', password): charset += 8

    if charset == 0:
        return "No definido"

    combinaciones = charset ** len(password)
    velocidad = 1_000_000_000  # intentos por segundo

    segundos = combinaciones / velocidad

    if segundos < 60:
        return f"{int(segundos)} segundos"
    elif segundos < 3600:
        return f"{int(segundos/60)} minutos"
    elif segundos < 86400:
        return f"{int(segundos/3600)} horas"
    elif segundos < 31536000:
        return f"{int(segundos/86400)} días"
    else:
        return f"{int(segundos/31536000)} años"


def verificar():
    pwd = entry.get()
    score = evaluar(pwd)
    actualizar_barra(score)

    tiempo = tiempo_crack(pwd)
    resultado.config(text=f"Tiempo de crack: {tiempo}", fg="#00ff00")


def generar():
    inicio = time.time()

    chars = ""
    if var_mayus.get(): chars += string.ascii_uppercase
    if var_minus.get(): chars += string.ascii_lowercase
    if var_nums.get(): chars += string.digits
    if var_simbols.get(): chars += "@$!%*?&"

    if chars == "":
        resultado.config(text="Selecciona opciones", fg="red")
        return

    longitud = int(scale.get())
    pwd = ''.join(random.choice(chars) for _ in range(longitud))

    entry.delete(0, tk.END)
    entry.insert(0, pwd)

    score = evaluar(pwd)
    actualizar_barra(score)

    fin = time.time()
    tiempo_gen = round(fin - inicio, 5)

    crack = tiempo_crack(pwd)
    resultado.config(text=f"Generada en {tiempo_gen}s | Crack: {crack}", fg="#00ff00")


def toggle_password():
    if entry.cget("show") == "*":
        entry.config(show="")
    else:
        entry.config(show="*")


def salir():
    root.destroy()

# =========================
# VENTANA
# =========================

root = tk.Tk()
root.title("Verificador Chernobyl")
root.geometry("700x500")
root.configure(bg="#0d0d0d")

root.bind("<Configure>", on_resize)

# Título
titulo = tk.Label(root, text="VERIFICADOR CHERNOBYL", fg="#00ff00", bg="#0d0d0d", font=("Courier", 18, "bold"))
titulo.pack(pady=10)

# Entrada
entry = tk.Entry(root, width=40, show="*", bg="black", fg="#00ff00", insertbackground="#00ff00")
entry.pack(pady=10)

# Mostrar
tk.Button(root, text="Mostrar/Ocultar", command=toggle_password, bg="black", fg="#00ff00").pack()

# Barra
barra = tk.Canvas(root, width=400, height=25, bg="black", highlightthickness=0)
barra.pack(pady=10)

# Opciones
frame = tk.Frame(root, bg="#0d0d0d")
frame.pack()

var_mayus = tk.BooleanVar(value=True)
var_minus = tk.BooleanVar(value=True)
var_nums = tk.BooleanVar(value=True)
var_simbols = tk.BooleanVar(value=True)

tk.Checkbutton(frame, text="A-Z", variable=var_mayus, bg="#0d0d0d", fg="#00ff00").grid(row=0, column=0)
tk.Checkbutton(frame, text="a-z", variable=var_minus, bg="#0d0d0d", fg="#00ff00").grid(row=0, column=1)
tk.Checkbutton(frame, text="0-9", variable=var_nums, bg="#0d0d0d", fg="#00ff00").grid(row=0, column=2)
tk.Checkbutton(frame, text="@#$", variable=var_simbols, bg="#0d0d0d", fg="#00ff00").grid(row=0, column=3)

# Longitud
scale = tk.Scale(root, from_=4, to=32, orient="horizontal", bg="#0d0d0d", fg="#00ff00", label="Longitud")
scale.set(12)
scale.pack()

# Botones
tk.Button(root, text="Verificar", command=verificar, bg="black", fg="#00ff00").pack(pady=5)
tk.Button(root, text="Generar", command=generar, bg="black", fg="#00ff00").pack(pady=5)
tk.Button(root, text="Exit", command=salir, bg="black", fg="red").pack(pady=10)

# Resultado
resultado = tk.Label(root, text="", bg="#0d0d0d", fg="#00ff00")
resultado.pack()

root.mainloop()