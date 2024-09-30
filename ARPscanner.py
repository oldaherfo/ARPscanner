from tkinter import *
import threading
import scapy.all as scapy
import requests


raiz = Tk()
valores = []

def buscarvendor(mac_address):
    url = f'https://www.macvendorlookup.com/api/v2/{mac_address}'
    try:
        vendor = requests.get(url).json()
        return vendor[0]['company']
    except (requests.RequestException, KeyError, IndexError):
        return "Vendor Desconocido"

def scanner(ip_address):
    capa2 = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    capa3 = scapy.ARP(pdst=ip_address)
    paquete_final = capa2 / capa3
    resultado = scapy.srp(paquete_final, verbose=False, timeout=2)[0]

    resultados = []
    for n in resultado:
        vendor = buscarvendor(n[1].hwsrc)
        nuevo_valor = f"[+] HOST: {n[1].psrc}      MAC: {n[1].hwsrc}        Vendor: {vendor}"
        resultados.append(nuevo_valor)
    return resultados

def scanner_thread():
    ip_address = txt1.get()
    threading.Thread(target=run_scanner, args=(ip_address,), daemon=True).start()

def run_scanner(ip_address):
    global valores
    valores = scanner(ip_address)
    boton1.config(text="Escaneando...")
    actualizar_resultados()

def actualizar_resultados():
    lbl2.config(text='\n'.join(valores))
    lbl2.after(100, actualizar_resultados)  # Para asegurarse de que la GUI se mantenga actualizada


raiz.title("ARPscanner_by_Oldaherfo")
raiz.resizable(1, 1)
raiz.geometry("550x400")
raiz.config(background="white")

# Elementos
lbl0 = Label(raiz, 
text="""
        ___        ____      ____ 
      /     |      / __  |   / __  |
    / / |  |    / /_/ /  / /_/ /
  / ___   |  / _, _/  / ____/ 
/_/     |_|/_/ |_|  /_/         SCANNER
                         

""", bg="white", justify="left")
lbl1 = Label(raiz, text="Por favor introduzca el rango IP a escanear IP/subred: ", bg="white", justify="left")
txt1 = Entry(raiz, background="gray")
boton1 = Button(raiz, text="Comenzar Escaneo", command=scanner_thread)
lbl2 = Label(raiz, text="", bg="white", justify="left", anchor="nw")
lbl3  = Label(raiz, text="Creado por Oldaherfo - 2024", bg="white")

# Posiciones
lbl0.pack(pady=10)
lbl1.pack()
txt1.pack(pady=6)
boton1.pack(pady=6)
lbl2.pack(pady=6, fill='both', expand=True)
lbl3.pack(pady=10)

raiz.mainloop()