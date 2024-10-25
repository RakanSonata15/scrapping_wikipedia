import tkinter as tk
import requests

# URL server FastAPI (ubah jika diperlukan)
API_URL = "http://127.0.0.1:8000/calculate"

# Membuat jendela utama
root = tk.Tk()
root.title("Kalkulator")

# Input untuk kalkulator
entry = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief='solid')
entry.grid(row=0, column=0, columnspan=4)

# Fungsi untuk menangani klik tombol
def button_click(symbol):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + symbol)

def calculate():
    expression = entry.get()
    print(f"Mengirim ekspresi: {expression} ke FastAPI")  # Debugging untuk melihat ekspresi yang dikirim
    response = requests.post(API_URL, json={"expression": expression})
    print(response.status_code, response.json())  # Debugging untuk melihat respons dari FastAPI
    if response.status_code == 200:
        result = response.json().get("result", "Error")
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    else:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")



def clear():
    entry.delete(0, tk.END)

# Menambahkan tombol-tombol ke kalkulator
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

for (text, row, col) in buttons:
    if text == '=':
        button = tk.Button(root, text=text, width=5, height=2, command=calculate)
    else:
        button = tk.Button(root, text=text, width=5, height=2, command=lambda t=text: button_click(t))
    button.grid(row=row, column=col)

# Tombol untuk menghapus (clear)
clear_button = tk.Button(root, text='C', width=5, height=2, command=clear)
clear_button.grid(row=5, column=0)

# Menjalankan loop utama GUI
root.mainloop()
