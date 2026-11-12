import tkinter as tk
from tkinter import messagebox
from collections import Counter
import statistics
from statistics import *

MAX_TALL = 999

def sorter_tall():
    input_text = entry.get().strip()
    if not input_text:
        messagebox.showerror("Feil", "Vennligst skriv inn tall.")
        return

    #Input
    tall_liste = []
    for t in input_text.replace(',', ' ').split():
        try:
            tall_liste.append(float(t))
        except ValueError:
            continue
        if len(tall_liste) >= MAX_TALL:
            break

    if not tall_liste:
        messagebox.showerror("Feil", "Ingen gyldige tall funnet.")
        return

    tall_liste.sort()

    #Beregninger
    gjennomsnitt = sum(tall_liste)/len(tall_liste)
    median = statistics.median(tall_liste)
    try:
        typetall = statistics.multimode(tall_liste)
    except statistics.StatisticsError:
        typetall = "Flere typetall eller ingen tydelig modus"

    frekvens = Counter(tall_liste)
    sannsynlighet = {t: f"{(f/len(tall_liste))*100:.2f}%" for t, f in frekvens.items()}
    hverdi=max(tall_liste)
    lverdi=min(tall_liste)
    vbredde=hverdi-lverdi
    standardavvik=stdev(tall_liste)
    #Q1 og Q3
    antall=len(tall_liste)
    midten=antall//2
    Nliste=tall_liste[0:midten]
    if antall%2==0:
        Øliste=tall_liste[midten:antall]
    else:
        Øliste=tall_liste[(midten+1):antall]
    Q1=statistics.median(Nliste)
    Q3=statistics.median(Øliste)
    

    # Vis resultater
    result_text = f"Sorterte tall: {tall_liste}\n"
    result_text += f"Høyeste verdi: {hverdi}\n"
    result_text += f"Laveste verdi: {lverdi}\n"
    result_text += f"Gjennomsnitt: {gjennomsnitt}\n"
    result_text += f"Median (Q2(2.Kvartil)): {median}\n"
    result_text += f"Q1 (1.Kvartil): {Q1}\n"
    result_text += f"Q3 (3.Kvartil): {Q3}\n"
    result_text += f"Typetall: {typetall}\n"
    result_text += f"Variasjonsbredde: {vbredde}\n"
    result_text += f"Standardavvik: {standardavvik}\n"
    result_text += "Sannsynlighet for hvert tall:\n"
    for t, p in sannsynlighet.items():
        result_text += f"  {t}: {p}\n"

    result_box.config(state='normal')
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, result_text)
    result_box.config(state='disabled')

# GUI-oppsett
root = tk.Tk()
root.title("Tall Sorterer")

tk.Label(root, text=f"Skriv inn opptil {MAX_TALL} tall (separert med mellomrom eller komma):").pack(pady=50)
entry = tk.Entry(root, width=100)
entry.pack(pady=10)

tk.Button(root, text="Sorter tall", command=sorter_tall).pack(pady=25)

result_box = tk.Text(root, width=120, height=30, state='disabled')
result_box.pack(pady=20)

root.mainloop()
