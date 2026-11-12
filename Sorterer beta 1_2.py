
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from tkinter import font as tkfont
from collections import Counter
import statistics
import math
import json
import os
import ast
import operator
import csv
import random


# ============================================================
# INNSTILLINGER
# ============================================================

MAX_TALL = 999
SETTINGS_FILE = "tall_sorterer_settings.json"

DEFAULT_SETTINGS = {
    "bg": "#111318",
    "panel": "#1B1F29",
    "panel_light": "#242A36",
    "accent": "#6C8CFF",
    "text": "#F1F3F8",
    "muted": "#929BAD",
    "green": "#55D6A7",
    "red": "#FF7373",

    "font": "Consolas",
    "font_size": 10,
    "title_size": 23,
    "stats_columns": 3,

    "features": {
        "antall": True,
        "sum": True,
        "gjennomsnitt": True,
        "median": True,
        "typetall": True,
        "minimum": True,
        "maksimum": True,
        "variasjonsbredde": True,
        "quartiles": True,
        "variance": True,
        "advanced_stats": True,
        "outliers": True,
        "frequency": True,
        "histogram": True,
        "sorted_list": True,
        "calculator": True,
        "copy": True,
        "export": True
    }
}

settings = {}


def load_settings():

    global settings

    settings = json.loads(json.dumps(DEFAULT_SETTINGS))

    if os.path.exists(SETTINGS_FILE):

        try:
            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                saved = json.load(file)

            for key in DEFAULT_SETTINGS:

                if key == "features":
                    settings["features"].update(
                        saved.get("features", {})
                    )

                elif key in saved:
                    settings[key] = saved[key]

        except (OSError, json.JSONDecodeError):
            pass


def save_settings():

    try:
        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                settings,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError:

        messagebox.showerror(
            "Lagringsfeil",
            "Kunne ikke lagre innstillingene."
        )

        return False


load_settings()


# ============================================================
# FARGER OG SKRIFTTYPER
# ============================================================

def color(name):
    return settings[name]


def font(size=None, bold=False):

    size = size or settings["font_size"]

    if bold:
        return (settings["font"], size, "bold")

    return (settings["font"], size)


def title_font():

    return (
        settings["font"],
        settings["title_size"],
        "bold"
    )


# ============================================================
# HJELPEFUNKSJONER
# ============================================================

def formater(tall):

    if tall is None:
        return "–"

    if isinstance(tall, float):
        return f"{tall:g}"

    return str(tall)


# ============================================================
# STATISTIKKBEREGNING
# ============================================================

def beregn_statistikk(tall):

    tall = sorted(tall)

    antall = len(tall)

    frekvens = Counter(tall)

    data = {
        "tall": tall,
        "antall": antall,
        "sum": sum(tall),
        "gjennomsnitt": statistics.mean(tall),
        "median": statistics.median(tall),
        "typetall": statistics.multimode(tall),
        "minimum": min(tall),
        "maksimum": max(tall),
        "variasjonsbredde": max(tall) - min(tall),
        "frekvens": frekvens
    }

    # KVARTILER

    if antall >= 2:

        midten = antall // 2

        nedre = tall[:midten]

        if antall % 2 == 0:
            ovre = tall[midten:]
        else:
            ovre = tall[midten + 1:]

        q1 = statistics.median(nedre)
        q2 = statistics.median(tall)
        q3 = statistics.median(ovre)

        data["q1"] = q1
        data["q2"] = q2
        data["q3"] = q3
        data["iqr"] = q3 - q1

    else:

        data["q1"] = None
        data["q2"] = statistics.median(tall)
        data["q3"] = None
        data["iqr"] = None

    # VARIANS OG STANDARDAVVIK

    data["varians"] = statistics.pvariance(tall)
    data["standardavvik"] = statistics.pstdev(tall)

    # EKSTRA STATISTIKK
    data["median_avvik"] = statistics.median(
        abs(verdi - data["median"]) for verdi in tall
    )
    data["sum_kvadrater"] = sum(verdi ** 2 for verdi in tall)

    if antall >= 2:
        data["utvalgsvarians"] = statistics.variance(tall)
        data["utvalgsstandardavvik"] = statistics.stdev(tall)
    else:
        data["utvalgsvarians"] = None
        data["utvalgsstandardavvik"] = None

    if all(verdi > 0 for verdi in tall):
        data["geometrisk_gjennomsnitt"] = statistics.geometric_mean(tall)
        data["harmonisk_gjennomsnitt"] = statistics.harmonic_mean(tall)
    else:
        data["geometrisk_gjennomsnitt"] = None
        data["harmonisk_gjennomsnitt"] = None

    # Avvikende observasjoner etter 1,5 x IQR-regelen.
    if data["iqr"] is not None:
        nedre_grense = data["q1"] - 1.5 * data["iqr"]
        ovre_grense = data["q3"] + 1.5 * data["iqr"]
        data["outliers"] = [
            verdi for verdi in tall
            if verdi < nedre_grense or verdi > ovre_grense
        ]
        data["outlier_lower"] = nedre_grense
        data["outlier_upper"] = ovre_grense
    else:
        data["outliers"] = []
        data["outlier_lower"] = None
        data["outlier_upper"] = None

    return data


# ============================================================
# HOVEDPROGRAM
# ============================================================

siste_resultat = None


def sorter_tall(retning="stigende"):

    global siste_resultat

    input_text = entry.get().strip()

    if not input_text:

        messagebox.showwarning(
            "Mangler tall",
            "Skriv inn noen tall først."
        )

        return

    tall = []
    ugyldige = []

    for verdi in input_text.replace(
        ",", " "
    ).replace(";", " ").split():

        try:

            tallverdi = float(verdi)

            if not math.isfinite(tallverdi):
                ugyldige.append(verdi)
                continue

            tall.append(tallverdi)

        except ValueError:
            ugyldige.append(verdi)

    if not tall:

        messagebox.showerror(
            "Feil",
            "Ingen gyldige tall ble funnet."
        )

        return

    if len(tall) > MAX_TALL:

        messagebox.showwarning(
            "Maks antall",
            f"Du kan registrere maksimalt {MAX_TALL} tall."
        )

        return

    data = beregn_statistikk(tall)

    if retning == "synkende":
        data["tall"].reverse()

    siste_resultat = data

    vis_resultater()

    if ugyldige:

        status_var.set(
            f"Ferdig. {len(tall)} tall behandlet. "
            f"{len(ugyldige)} ugyldige verdier ignorert."
        )

    else:

        status_var.set(
            f"Beregning fullført. {len(tall)} tall behandlet."
        )


# ============================================================
# KNAPPER
# ============================================================

def lag_knapp(
    parent,
    tekst,
    funksjon,
    farge=None
):

    return tk.Button(
        parent,
        text=tekst,
        command=funksjon,
        bg=farge or color("accent"),
        fg="white",
        activebackground="#5475E8",
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=15,
        pady=9,
        font=font(9, True),
        cursor="hand2"
    )


# ============================================================
# STATISTIKKOVERSIKT
# ============================================================

def vis_statistikk(data):

    features = settings["features"]

    alle_verdier = [
        ("antall", "Antall tall", data["antall"]),
        ("sum", "Sum", data["sum"]),
        ("gjennomsnitt", "Gjennomsnitt", data["gjennomsnitt"]),
        ("median", "Median", data["median"]),
        ("typetall", "Typetall", ", ".join(
            formater(x) for x in data["typetall"]
        )),
        ("minimum", "Laveste verdi", data["minimum"]),
        ("maksimum", "Høyeste verdi", data["maksimum"]),
        (
            "variasjonsbredde",
            "Variasjonsbredde",
            data["variasjonsbredde"]
        )
    ]

    if features["quartiles"]:

        alle_verdier.extend([
            ("q1", "Q1", data["q1"]),
            ("q2", "Q2", data["q2"]),
            ("q3", "Q3", data["q3"]),
            ("iqr", "Kvartilbredde (IQR)", data["iqr"])
        ])

    if features["variance"]:

        alle_verdier.extend([
            ("varians", "Populasjonsvarians", data["varians"]),
            (
                "standardavvik",
                "Populasjonsstandardavvik",
                data["standardavvik"]
            )
        ])

    if features.get("advanced_stats", True):
        alle_verdier.extend([
            ("median_avvik", "Median absoluttavvik", data["median_avvik"]),
            ("sum_kvadrater", "Sum av kvadrater", data["sum_kvadrater"]),
            ("geometrisk_gjennomsnitt", "Geometrisk gjennomsnitt", data["geometrisk_gjennomsnitt"]),
            ("harmonisk_gjennomsnitt", "Harmonisk gjennomsnitt", data["harmonisk_gjennomsnitt"]),
            ("utvalgsvarians", "Utvalgsvarians", data["utvalgsvarians"]),
            ("utvalgsstandardavvik", "Utvalgsstandardavvik", data["utvalgsstandardavvik"])
        ])

    if features.get("outliers", True):
        alle_verdier.append((
            "outliers",
            "Avvikende observasjoner",
            ", ".join(formater(x) for x in data["outliers"]) if data["outliers"] else "Ingen"
        ))

    # Fjern funksjoner som er deaktivert

    verdier = [
        (navn, verdi)
        for key, navn, verdi in alle_verdier
        if features.get(key, True)
    ]

    if not verdier:
        return

    columns = settings["stats_columns"]

    for i, (navn, verdi) in enumerate(verdier):

        rad = i // columns
        kolonne = i % columns

        kort = tk.Frame(
            stats_frame,
            bg=color("panel_light"),
            padx=12,
            pady=12
        )

        kort.grid(
            row=rad,
            column=kolonne,
            sticky="nsew",
            padx=5,
            pady=5
        )

        tk.Label(
            kort,
            text=navn,
            bg=color("panel_light"),
            fg=color("muted"),
            font=font(9)
        ).pack(anchor="w")

        tk.Label(
            kort,
            text=formater(verdi),
            bg=color("panel_light"),
            fg=color("text"),
            font=font(settings["font_size"] + 2, True),
            wraplength=220
        ).pack(anchor="w", pady=(5, 0))

    for i in range(columns):
        stats_frame.columnconfigure(i, weight=1)


# ============================================================
# FREKVENSTABELL
# ============================================================

def vis_frekvens(data):

    for item in frekvens_tabell.get_children():
        frekvens_tabell.delete(item)

    for tall, antall in sorted(data["frekvens"].items()):

        prosent = antall / data["antall"] * 100

        frekvens_tabell.insert(
            "",
            "end",
            values=(
                formater(tall),
                antall,
                f"{prosent:.2f}%"
            )
        )


# ============================================================
# HISTOGRAM
# ============================================================

def tegn_histogram(data):

    histogram.delete("all")

    bredde = max(histogram.winfo_width(), 400)
    hoyde = max(histogram.winfo_height(), 220)

    tall = data["tall"]
    antall = len(tall)

    if data["minimum"] == data["maksimum"]:

        histogram.create_text(
            bredde / 2,
            hoyde / 2,
            text="Alle tallene har samme verdi",
            fill=color("text"),
            font=font(11)
        )

        return

    antall_bins = min(
        10,
        max(2, int(antall ** 0.5))
    )

    lav = data["minimum"]
    hoy = data["maksimum"]

    intervall = (hoy - lav) / antall_bins

    bins = [0] * antall_bins

    for verdi in tall:

        indeks = int((verdi - lav) / intervall)
        indeks = min(indeks, antall_bins - 1)

        bins[indeks] += 1

    maks = max(bins)

    margin = 35

    tilgjengelig_bredde = bredde - margin * 2
    tilgjengelig_hoyde = hoyde - margin * 2

    stolkebredde = tilgjengelig_bredde / antall_bins

    histogram.create_line(
        margin,
        hoyde - margin,
        bredde - margin,
        hoyde - margin,
        fill=color("muted")
    )

    for i, verdi in enumerate(bins):

        stolkehoyde = (
            verdi / maks
        ) * tilgjengelig_hoyde

        x1 = margin + i * stolkebredde + 3
        x2 = margin + (i + 1) * stolkebredde - 3

        y1 = hoyde - margin - stolkehoyde
        y2 = hoyde - margin

        histogram.create_rectangle(
            x1, y1, x2, y2,
            fill=color("accent"),
            outline=""
        )

        histogram.create_text(
            (x1 + x2) / 2,
            y1 - 10,
            text=str(verdi),
            fill=color("text"),
            font=font(9)
        )

    histogram.create_text(
        bredde / 2,
        hoyde - 10,
        text=f"Verdiområde: {formater(lav)} – {formater(hoy)}",
        fill=color("muted"),
        font=font(9)
    )


# ============================================================
# SORTERTE TALL
# ============================================================

def vis_sorterte_tall(data):

    sorted_text.configure(state="normal")
    sorted_text.delete("1.0", tk.END)

    resultat = ", ".join(
        formater(x) for x in data["tall"]
    )

    sorted_text.insert("1.0", resultat)
    sorted_text.configure(state="disabled")


# ============================================================
# RESULTATTEKST OG EKSPORT
# ============================================================

def lag_resultattekst():

    if siste_resultat is None:
        return ""

    data = siste_resultat
    features = settings["features"]

    tekst = "TALL SORTERER\n"
    tekst += "=" * 40 + "\n\n"

    if features["sorted_list"]:
        tekst += f"Sorterte tall: {data['tall']}\n\n"

    tekst += "STATISTIKK\n"

    verdier = [
        ("antall", "Antall", data["antall"]),
        ("sum", "Sum", data["sum"]),
        ("gjennomsnitt", "Gjennomsnitt", data["gjennomsnitt"]),
        ("median", "Median", data["median"]),
        ("typetall", "Typetall", data["typetall"]),
        ("minimum", "Laveste verdi", data["minimum"]),
        ("maksimum", "Høyeste verdi", data["maksimum"]),
        (
            "variasjonsbredde",
            "Variasjonsbredde",
            data["variasjonsbredde"]
        )
    ]

    if features["quartiles"]:

        verdier.extend([
            ("q1", "Q1", data["q1"]),
            ("q2", "Q2", data["q2"]),
            ("q3", "Q3", data["q3"]),
            ("iqr", "Kvartilbredde", data["iqr"])
        ])

    if features["variance"]:

        verdier.extend([
            ("varians", "Populasjonsvarians", data["varians"]),
            (
                "standardavvik",
                "Populasjonsstandardavvik",
                data["standardavvik"]
            )
        ])

    if features.get("advanced_stats", True):
        verdier.extend([
            ("median_avvik", "Median absoluttavvik", data["median_avvik"]),
            ("sum_kvadrater", "Sum av kvadrater", data["sum_kvadrater"]),
            ("geometrisk_gjennomsnitt", "Geometrisk gjennomsnitt", data["geometrisk_gjennomsnitt"]),
            ("harmonisk_gjennomsnitt", "Harmonisk gjennomsnitt", data["harmonisk_gjennomsnitt"]),
            ("utvalgsvarians", "Utvalgsvarians", data["utvalgsvarians"]),
            ("utvalgsstandardavvik", "Utvalgsstandardavvik", data["utvalgsstandardavvik"])
        ])

    if features.get("outliers", True):
        verdier.append((
            "outliers",
            "Avvikende observasjoner",
            ", ".join(formater(x) for x in data["outliers"]) if data["outliers"] else "Ingen"
        ))

    for key, navn, verdi in verdier:

        if features.get(key, True):
            tekst += f"{navn}: {verdi}\n"

    if features["frequency"]:

        tekst += "\nFREKVENSTABELL\n"

        for tall, antall in sorted(data["frekvens"].items()):

            prosent = antall / data["antall"] * 100

            tekst += (
                f"{tall}: {antall} "
                f"({prosent:.2f}%)\n"
            )

    return tekst


def kopier_resultater():

    tekst = lag_resultattekst()

    if not tekst:
        messagebox.showwarning(
            "Ingen resultater",
            "Sorter tall først."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(tekst)

    status_var.set("Resultatene er kopiert.")


def eksporter_resultater():

    tekst = lag_resultattekst()

    if not tekst:
        messagebox.showwarning(
            "Ingen resultater",
            "Sorter tall først."
        )
        return

    fil = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Tekstfiler", "*.txt"),
            ("Alle filer", "*.*")
        ],
        title="Lagre resultater"
    )

    if fil:

        try:

            with open(
                fil,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(tekst)

            status_var.set("Resultatene er eksportert.")

        except OSError as error:

            messagebox.showerror(
                "Eksportfeil",
                str(error)
            )


# ============================================================
# EKSTRA VERKTØY: CSV, TILFELDIGE TALL OG DATAINFO
# ============================================================

def importer_tall_csv():
    """Importer tall fra en CSV- eller tekstfil og legg dem til i inndatafeltet."""
    fil = filedialog.askopenfilename(
        title="Importer tall",
        filetypes=[("CSV-filer", "*.csv"), ("Tekstfiler", "*.txt"), ("Alle filer", "*.*")]
    )
    if not fil:
        return

    funnet = []
    try:
        with open(fil, "r", encoding="utf-8-sig", newline="") as f:
            innhold = f.read()
        # Godtar komma, semikolon, tabulator og mellomrom som skilletegn.
        for token in innhold.replace(";", " ").replace("\t", " ").replace(",", " ").split():
            try:
                verdi = float(token)
                if math.isfinite(verdi):
                    funnet.append(formater(verdi))
            except ValueError:
                continue
    except OSError as error:
        messagebox.showerror("Importfeil", str(error))
        return

    if not funnet:
        messagebox.showwarning("Ingen tall funnet", "Filen inneholdt ingen tall som kunne importeres.")
        return

    eksisterende = entry.get().strip()
    entry.delete(0, tk.END)
    entry.insert(0, (eksisterende + " " if eksisterende else "") + " ".join(funnet))
    status_var.set(f"Importerte {len(funnet)} tall fra fil.")


def eksporter_csv():
    """Eksporter datasettet og frekvensene til en CSV-fil."""
    if siste_resultat is None:
        messagebox.showwarning("Ingen resultater", "Sorter tall først.")
        return

    fil = filedialog.asksaveasfilename(
        title="Eksporter som CSV",
        defaultextension=".csv",
        filetypes=[("CSV-filer", "*.csv"), ("Alle filer", "*.*")]
    )
    if not fil:
        return

    try:
        with open(fil, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Tall", "Frekvens", "Andel prosent"])
            for verdi, antall in sorted(siste_resultat["frekvens"].items()):
                writer.writerow([formater(verdi), antall, f"{antall / siste_resultat['antall'] * 100:.2f}"])
        status_var.set("CSV-filen er eksportert.")
    except OSError as error:
        messagebox.showerror("Eksportfeil", str(error))


def kopier_sorterte_tall():
    if siste_resultat is None:
        messagebox.showwarning("Ingen resultater", "Sorter tall først.")
        return
    tekst = " ".join(formater(x) for x in siste_resultat["tall"])
    root.clipboard_clear()
    root.clipboard_append(tekst)
    status_var.set("Kun de sorterte tallene er kopiert.")


def fjern_duplikater():
    """Fjern gjentatte verdier fra inndatafeltet, men behold første forekomst."""
    verdier = entry.get().strip()
    if not verdier:
        messagebox.showwarning("Tomt felt", "Skriv inn tall først.")
        return

    unike = []
    ugyldige = []
    sett = set()
    for token in verdier.replace(",", " ").replace(";", " ").split():
        try:
            tall = float(token)
            if not math.isfinite(tall):
                ugyldige.append(token)
            elif tall not in sett:
                sett.add(tall)
                unike.append(formater(tall))
        except ValueError:
            ugyldige.append(token)

    entry.delete(0, tk.END)
    entry.insert(0, " ".join(unike))
    status_var.set(f"Fjernet duplikater. {len(unike)} unike tall står igjen.")


def generer_tilfeldige_tall():
    """Lag et datasett med tilfeldige heltall eller desimaltall."""
    vindu = tk.Toplevel(root)
    vindu.title("Generer tilfeldige tall")
    vindu.geometry("390x330")
    vindu.resizable(False, False)
    vindu.configure(bg=color("bg"))

    tk.Label(vindu, text="GENERER TESTDATA", bg=color("bg"), fg=color("text"), font=title_font()).pack(pady=(18, 12))
    felt = tk.Frame(vindu, bg=color("bg"), padx=22)
    felt.pack(fill="both", expand=True)

    variabler = {
        "antall": tk.StringVar(value="20"),
        "minimum": tk.StringVar(value="1"),
        "maksimum": tk.StringVar(value="100"),
        "desimaler": tk.StringVar(value="0")
    }
    etiketter = [("Antall tall (1–999)", "antall"), ("Minimum", "minimum"), ("Maksimum", "maksimum"), ("Desimaler (0–6)", "desimaler")]
    for tekst, nøkkel in etiketter:
        tk.Label(felt, text=tekst, bg=color("bg"), fg=color("text"), font=font(9)).pack(anchor="w", pady=(5, 2))
        tk.Entry(felt, textvariable=variabler[nøkkel], bg=color("panel_light"), fg=color("text"), insertbackground=color("text"), relief="flat").pack(fill="x", ipady=5)

    def lag():
        try:
            antall = int(variabler["antall"].get())
            minimum = float(variabler["minimum"].get())
            maksimum = float(variabler["maksimum"].get())
            desimaler = int(variabler["desimaler"].get())
            if not 1 <= antall <= MAX_TALL:
                raise ValueError(f"Antall må være mellom 1 og {MAX_TALL}.")
            if not math.isfinite(minimum) or not math.isfinite(maksimum) or minimum > maksimum:
                raise ValueError("Minimum og maksimum må være gyldige tall, og minimum kan ikke være større enn maksimum.")
            if not 0 <= desimaler <= 6:
                raise ValueError("Antall desimaler må være mellom 0 og 6.")
            if desimaler == 0 and math.ceil(minimum) > math.floor(maksimum):
                raise ValueError("Intervallet inneholder ingen heltall. Velg desimaler eller et større intervall.")
        except ValueError as error:
            messagebox.showerror("Ugyldige innstillinger", str(error), parent=vindu)
            return

        if desimaler == 0:
            genererte = [str(random.randint(math.ceil(minimum), math.floor(maksimum))) for _ in range(antall)]
        else:
            genererte = [str(round(random.uniform(minimum, maksimum), desimaler)) for _ in range(antall)]

        entry.delete(0, tk.END)
        entry.insert(0, " ".join(genererte))
        status_var.set(f"Genererte {antall} tilfeldige tall.")
        vindu.destroy()

    lag_knapp(felt, "Generer tall", lag).pack(fill="x", pady=16)


def vis_datasettinfo():
    if siste_resultat is None:
        messagebox.showwarning("Ingen resultater", "Sorter tall først.")
        return
    data = siste_resultat
    unike = len(data["frekvens"])
    duplikater = data["antall"] - unike
    info = (
        f"Antall observasjoner: {data['antall']}\n"
        f"Unike verdier: {unike}\n"
        f"Gjentatte observasjoner utover første forekomst: {duplikater}\n"
        f"Andel unike verdier: {unike / data['antall'] * 100:.2f}%\n"
        f"Laveste verdi: {formater(data['minimum'])}\n"
        f"Høyeste verdi: {formater(data['maksimum'])}\n"
        f"Variasjonsbredde: {formater(data['variasjonsbredde'])}"
    )
    messagebox.showinfo("Datasettinformasjon", info)


# ============================================================
# NULLSTILL
# ============================================================

def nullstill():

    global siste_resultat

    siste_resultat = None

    entry.delete(0, tk.END)

    vis_resultater()

    status_var.set("Klar til å sortere nye tall.")


# ============================================================
# KALKULATOR
# ============================================================

# Tillatte matematiske operasjoner.
# Dette gjør at kalkulatoren ikke trenger eval().

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def sikker_beregning(uttrykk):

    tre = ast.parse(uttrykk, mode="eval")

    def beregn(node):

        if isinstance(node, ast.Expression):
            return beregn(node.body)

        if isinstance(node, ast.Constant):

            if isinstance(node.value, bool):
                raise ValueError("Ugyldig verdi")

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Ugyldig verdi")

        if isinstance(node, ast.BinOp):

            operator_type = type(node.op)

            if operator_type not in OPERATORS:
                raise ValueError("Ugyldig regneoperasjon")

            venstre = beregn(node.left)
            hoyre = beregn(node.right)

            if operator_type is ast.Pow and abs(hoyre) > 100:
                raise ValueError("Eksponenten er for stor")

            if operator_type is ast.Pow and abs(venstre) > 1e100:
                raise ValueError("Tallet er for stort")

            return OPERATORS[operator_type](
                venstre,
                hoyre
            )

        if isinstance(node, ast.UnaryOp):

            operator_type = type(node.op)

            if operator_type not in OPERATORS:
                raise ValueError("Ugyldig operasjon")

            return OPERATORS[operator_type](
                beregn(node.operand)
            )

        if isinstance(node, ast.Call):

            if not isinstance(node.func, ast.Name):
                raise ValueError("Ugyldig funksjon")

            funksjoner = {
                "sqrt": math.sqrt,
                "abs": abs,
                "round": round,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log10,
                "ln": math.log,
                "pi": lambda: math.pi,
                "e": lambda: math.e
            }

            navn = node.func.id

            if navn not in funksjoner:
                raise ValueError("Ukjent funksjon")

            if node.keywords:
                raise ValueError("Ugyldig argument")

            argumenter = [
                beregn(arg) for arg in node.args
            ]

            if navn in ("pi", "e"):

                if argumenter:
                    raise ValueError("Ingen argumenter tillatt")

                return funksjoner[navn]()

            return funksjoner[navn](*argumenter)

        raise ValueError("Ugyldig uttrykk")

    resultat = beregn(tre)

    if not isinstance(resultat, (int, float)):
        raise ValueError("Ugyldig resultat")

    if not math.isfinite(resultat):
        raise ValueError("Resultatet er ikke et endelig tall")

    return resultat


def apne_kalkulator():

    if not settings["features"]["calculator"]:
        return

    window = tk.Toplevel(root)

    window.title("Kalkulator - Tall Sorterer")
    window.geometry("390x550")
    window.minsize(330, 480)
    window.configure(bg=color("bg"))

    uttrykk_var = tk.StringVar()
    resultat_var = tk.StringVar(value="Klar")

    # DISPLAY

    display = tk.Frame(
        window,
        bg=color("panel"),
        padx=15,
        pady=15
    )

    display.pack(
        fill="x",
        padx=15,
        pady=15
    )

    tk.Entry(
        display,
        textvariable=uttrykk_var,
        justify="right",
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(20)
    ).pack(fill="x", ipady=12)

    tk.Label(
        display,
        textvariable=resultat_var,
        bg=color("panel"),
        fg=color("green"),
        font=font(12)
    ).pack(anchor="e", pady=(10, 0))

    # BEREGNING

    def beregn():

        uttrykk = uttrykk_var.get().strip()

        if not uttrykk:
            return

        try:

            uttrykk = uttrykk.replace("^", "**")

            resultat = sikker_beregning(uttrykk)

            resultat_var.set(
                "= " + formater(resultat)
            )

        except ZeroDivisionError:

            resultat_var.set("Kan ikke dele på null")

        except (ValueError, TypeError, SyntaxError, OverflowError):

            resultat_var.set("Ugyldig regnestykke")

    # KNAPPFUNKSJONER

    def legg_til(verdi):

        uttrykk_var.set(
            uttrykk_var.get() + verdi
        )

    def slett():

        uttrykk_var.set("")
        resultat_var.set("Klar")

    def tilbake():

        uttrykk_var.set(
            uttrykk_var.get()[:-1]
        )

    def bruk_resultat():

        try:

            uttrykk = uttrykk_var.get().replace("^", "**")

            resultat = sikker_beregning(uttrykk)

            uttrykk_var.set(formater(resultat))
            resultat_var.set("Resultatet er satt inn")

        except Exception:

            resultat_var.set("Kan ikke bruke resultatet")

    # KNAPPEOPPSETT

    button_frame = tk.Frame(
        window,
        bg=color("bg"),
        padx=12
    )

    button_frame.pack(fill="both", expand=True)

    knapper = [
        ["C", "(", ")", "⌫"],
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "%", "+"],
        ["sqrt(", "^", "pi()", "="]
    ]

    def knappetrykk(verdi):

        if verdi == "C":
            slett()

        elif verdi == "⌫":
            tilbake()

        elif verdi == "=":
            beregn()

        elif verdi == "%":
            legg_til("/100")

        else:
            legg_til(verdi)

    for rad_index, rad in enumerate(knapper):

        button_frame.rowconfigure(
            rad_index,
            weight=1
        )

        for kol_index, verdi in enumerate(rad):

            button_frame.columnconfigure(
                kol_index,
                weight=1
            )

            knapp = tk.Button(
                button_frame,
                text=verdi,
                command=lambda v=verdi: knappetrykk(v),
                bg=(
                    color("accent")
                    if verdi == "="
                    else color("panel_light")
                ),
                fg="white",
                activebackground="#5475E8",
                relief="flat",
                font=font(12, True)
            )

            knapp.grid(
                row=rad_index,
                column=kol_index,
                sticky="nsew",
                padx=3,
                pady=3
            )

    # EKSTRA FUNKSJONER

    extra = tk.Frame(
        window,
        bg=color("bg"),
        padx=15,
        pady=10
    )

    extra.pack(fill="x")

    tk.Label(
        extra,
        text="Funksjoner: sqrt(x), abs(x), round(x), "
             "sin(x), cos(x), tan(x), log(x), ln(x), e()",
        bg=color("bg"),
        fg=color("muted"),
        font=font(8),
        wraplength=350,
        justify="left"
    ).pack(anchor="w")

    lag_knapp(
        extra,
        "Bruk resultat",
        bruk_resultat,
        color("green")
    ).pack(fill="x", pady=(8, 0))

    # ENTER FOR BEREGNING

    window.bind("<Return>", lambda event: beregn())
    window.bind("<Escape>", lambda event: slett())


# ============================================================
# VIS RESULTATER
# ============================================================

def vis_resultater():

    for widget in result_area.winfo_children():
        widget.destroy()

    if siste_resultat is None:
        return

    data = siste_resultat
    features = settings["features"]

    # STATISTIKK

    statistikk_nokler = [
        "antall",
        "sum",
        "gjennomsnitt",
        "median",
        "typetall",
        "minimum",
        "maksimum",
        "variasjonsbredde"
    ]

    har_statistikk = any(
        features.get(key, False)
        for key in statistikk_nokler
    ) or features["quartiles"] or features["variance"]

    if har_statistikk:

        tk.Label(
            result_area,
            text="STATISTIKKOVERSIKT",
            bg=color("bg"),
            fg=color("text"),
            font=font(11, True)
        ).pack(anchor="w", pady=(5, 8))

        global stats_frame

        stats_frame = tk.Frame(
            result_area,
            bg=color("bg")
        )

        stats_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        vis_statistikk(data)

    # SORTERTE TALL

    if features["sorted_list"]:

        tk.Label(
            result_area,
            text="SORTERTE TALL",
            bg=color("bg"),
            fg=color("text"),
            font=font(11, True)
        ).pack(anchor="w", pady=(5, 8))

        sorted_panel = tk.Frame(
            result_area,
            bg=color("panel"),
            padx=12,
            pady=12
        )

        sorted_panel.pack(fill="x", pady=(0, 15))

        global sorted_text

        sorted_text = tk.Text(
            sorted_panel,
            height=4,
            wrap="word",
            bg=color("panel_light"),
            fg=color("text"),
            insertbackground=color("text"),
            font=font(9),
            relief="flat",
            padx=8,
            pady=8
        )

        sorted_text.pack(fill="x")

        vis_sorterte_tall(data)

    # NEDRE OMRÅDE

    lower = tk.Frame(
        result_area,
        bg=color("bg")
    )

    lower.pack(
        fill="both",
        expand=True
    )

    # FREKVENSTABELL

    if features["frequency"]:

        left = tk.Frame(
            lower,
            bg=color("panel"),
            padx=12,
            pady=12
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        tk.Label(
            left,
            text="FREKVENSTABELL",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True)
        ).pack(anchor="w", pady=(0, 10))

        table_frame = tk.Frame(
            left,
            bg=color("panel")
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        global frekvens_tabell

        frekvens_tabell = ttk.Treeview(
            table_frame,
            columns=("tall", "antall", "prosent"),
            show="headings",
            height=10
        )

        table_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=frekvens_tabell.yview
        )

        frekvens_tabell.configure(
            yscrollcommand=table_scroll.set
        )

        table_scroll.pack(side="right", fill="y")

        frekvens_tabell.pack(
            side="left",
            fill="both",
            expand=True
        )

        for column, title in [
            ("tall", "Tall"),
            ("antall", "Antall"),
            ("prosent", "Prosent")
        ]:

            frekvens_tabell.heading(
                column,
                text=title
            )

            frekvens_tabell.column(
                column,
                width=90,
                anchor="center"
            )

        vis_frekvens(data)

    # HISTOGRAM

    if features["histogram"]:

        right = tk.Frame(
            lower,
            bg=color("panel"),
            padx=12,
            pady=12
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        tk.Label(
            right,
            text="HISTOGRAM",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True)
        ).pack(anchor="w", pady=(0, 10))

        global histogram

        histogram = tk.Canvas(
            right,
            bg=color("panel"),
            highlightthickness=0,
            height=220
        )

        histogram.pack(
            fill="both",
            expand=True
        )

        histogram.bind(
            "<Configure>",
            lambda event: tegn_histogram(siste_resultat)
            if siste_resultat else None
        )

        tegn_histogram(data)


# ============================================================
# INNSTILLINGSMENY
# ============================================================

def apne_innstillinger():

    if hasattr(apne_innstillinger, "window"):

        try:

            if apne_innstillinger.window.winfo_exists():
                apne_innstillinger.window.lift()
                return

        except tk.TclError:
            pass

    window = tk.Toplevel(root)
    apne_innstillinger.window = window

    window.title("Innstillinger")
    window.geometry("650x780")
    window.minsize(500, 550)
    window.configure(bg=color("bg"))

    # SCROLLBAR

    outer = tk.Frame(
        window,
        bg=color("bg")
    )

    outer.pack(
        fill="both",
        expand=True
    )

    settings_canvas = tk.Canvas(
        outer,
        bg=color("bg"),
        highlightthickness=0
    )

    settings_scroll = ttk.Scrollbar(
        outer,
        orient="vertical",
        command=settings_canvas.yview
    )

    settings_canvas.configure(
        yscrollcommand=settings_scroll.set
    )

    settings_scroll.pack(
        side="right",
        fill="y"
    )

    settings_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    content = tk.Frame(
        settings_canvas,
        bg=color("bg"),
        padx=20,
        pady=20
    )

    content_id = settings_canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    content.bind(
        "<Configure>",
        lambda event: settings_canvas.configure(
            scrollregion=settings_canvas.bbox("all")
        )
    )

    settings_canvas.bind(
        "<Configure>",
        lambda event: settings_canvas.itemconfigure(
            content_id,
            width=event.width
        )
    )

    def seksjon(tittel):

        tk.Label(
            content,
            text=tittel,
            bg=color("bg"),
            fg=color("text"),
            font=font(12, True)
        ).pack(anchor="w", pady=(18, 8))

    # FARGER

    def fargerad(navn, key):

        rad = tk.Frame(
            content,
            bg=color("bg")
        )

        rad.pack(fill="x", pady=4)

        tk.Label(
            rad,
            text=navn,
            bg=color("bg"),
            fg=color("text"),
            font=font(9)
        ).pack(side="left")

        def velg():

            valgt = colorchooser.askcolor(
                color=settings[key],
                title=f"Velg {navn}"
            )

            if valgt and valgt[1]:

                settings[key] = valgt[1]
                knapp.configure(bg=valgt[1])

        knapp = tk.Button(
            rad,
            bg=settings[key],
            width=8,
            relief="flat",
            command=velg
        )

        knapp.pack(side="right")

    seksjon("UTSEENDE OG FARGER")

    fargerad("Bakgrunnsfarge", "bg")
    fargerad("Panelfarge", "panel")
    fargerad("Kortfarge", "panel_light")
    fargerad("Tekstfarge", "text")
    fargerad("Sekundær tekst", "muted")
    fargerad("Aksentfarge", "accent")
    fargerad("Statusfarge", "green")
    fargerad("Feilfarge", "red")

    # SKRIFT

    seksjon("SKRIFT OG TYPOGRAFI")

    tk.Label(
        content,
        text="Skrifttype",
        bg=color("bg"),
        fg=color("text"),
        font=font(9)
    ).pack(anchor="w")

    font_var = tk.StringVar(
        value=settings["font"]
    )

    font_combo = ttk.Combobox(
        content,
        textvariable=font_var,
        values=sorted(set(tkfont.families(root))),
        state="readonly"
    )

    font_combo.pack(
        fill="x",
        pady=(5, 10)
    )

    tk.Label(
        content,
        text="Skriftstørrelse",
        bg=color("bg"),
        fg=color("text"),
        font=font(9)
    ).pack(anchor="w")

    font_size_var = tk.IntVar(
        value=settings["font_size"]
    )

    tk.Spinbox(
        content,
        from_=8,
        to=20,
        textvariable=font_size_var,
        bg=color("panel_light"),
        fg=color("text"),
        relief="flat"
    ).pack(fill="x", pady=(5, 10))

    tk.Label(
        content,
        text="Overskriftsstørrelse",
        bg=color("bg"),
        fg=color("text"),
        font=font(9)
    ).pack(anchor="w")

    title_size_var = tk.IntVar(
        value=settings["title_size"]
    )

    tk.Spinbox(
        content,
        from_=16,
        to=40,
        textvariable=title_size_var,
        bg=color("panel_light"),
        fg=color("text"),
        relief="flat"
    ).pack(fill="x", pady=(5, 10))

    # LAYOUT

    seksjon("LAYOUT")

    tk.Label(
        content,
        text="Kolonner i statistikkoversikten",
        bg=color("bg"),
        fg=color("text"),
        font=font(9)
    ).pack(anchor="w")

    columns_var = tk.IntVar(
        value=settings["stats_columns"]
    )

    ttk.Combobox(
        content,
        textvariable=columns_var,
        values=[1, 2, 3, 4, 5],
        state="readonly"
    ).pack(fill="x", pady=(5, 10))

    # FUNKSJONSVALG

    seksjon("VELG FUNKSJONER")

    tk.Label(
        content,
        text="Bestem hvilke beregninger og verktøy som skal være aktive.",
        bg=color("bg"),
        fg=color("muted"),
        font=font(9),
        wraplength=500
    ).pack(anchor="w", pady=(0, 10))

    feature_names = {
        "antall": "Antall tall",
        "sum": "Sum",
        "gjennomsnitt": "Gjennomsnitt",
        "median": "Median",
        "typetall": "Typetall",
        "minimum": "Laveste verdi",
        "maksimum": "Høyeste verdi",
        "variasjonsbredde": "Variasjonsbredde",
        "quartiles": "Kvartiler (Q1, Q2, Q3 og IQR)",
        "variance": "Varians og standardavvik",
        "advanced_stats": "Utvidet statistikk (MAD, geometrisk/harmonisk gjennomsnitt m.m.)",
        "outliers": "Finn avvikende observasjoner (1,5 × IQR)",
        "frequency": "Frekvenstabell",
        "histogram": "Histogram",
        "sorted_list": "Vis sorterte tall",
        "calculator": "Kalkulator",
        "copy": "Kopier resultater",
        "export": "Eksporter TXT"
    }

    feature_vars = {}

    # GRUPPER FUNKSJONENE

    groups = {
        "Statistiske beregninger": [
            "antall",
            "sum",
            "gjennomsnitt",
            "median",
            "typetall",
            "minimum",
            "maksimum",
            "variasjonsbredde"
        ],
        "Avanserte beregninger": [
            "quartiles",
            "variance",
            "advanced_stats",
            "outliers"
        ],
        "Visningsfunksjoner": [
            "frequency",
            "histogram",
            "sorted_list"
        ],
        "Verktøy": [
            "calculator",
            "copy",
            "export"
        ]
    }

    for group_name, keys in groups.items():

        group_frame = tk.Frame(
            content,
            bg=color("panel"),
            padx=12,
            pady=10
        )

        group_frame.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            group_frame,
            text=group_name,
            bg=color("panel"),
            fg=color("accent"),
            font=font(9, True)
        ).pack(anchor="w", pady=(0, 5))

        for key in keys:

            var = tk.BooleanVar(
                value=settings["features"][key]
            )

            feature_vars[key] = var

            tk.Checkbutton(
                group_frame,
                text=feature_names[key],
                variable=var,
                bg=color("panel"),
                fg=color("text"),
                activebackground=color("panel"),
                activeforeground=color("text"),
                selectcolor=color("panel_light"),
                font=font(9)
            ).pack(anchor="w", pady=2)

    # HJELPEFUNKSJONER FOR VALG

    def velg_alle():

        for var in feature_vars.values():
            var.set(True)

    def fjern_alle():

        for var in feature_vars.values():
            var.set(False)

    selection_buttons = tk.Frame(
        content,
        bg=color("bg")
    )

    selection_buttons.pack(
        fill="x",
        pady=10
    )

    lag_knapp(
        selection_buttons,
        "Velg alle",
        velg_alle,
        color("panel_light")
    ).pack(side="left", padx=(0, 5))

    lag_knapp(
        selection_buttons,
        "Fjern alle",
        fjern_alle,
        color("panel_light")
    ).pack(side="left")

    # LAGRE INNSTILLINGER

    seksjon("LAGRE INNSTILLINGER")

    def bruk_innstillinger():

        try:

            settings["font"] = font_var.get()

            settings["font_size"] = max(
                8,
                min(20, int(font_size_var.get()))
            )

            settings["title_size"] = max(
                16,
                min(40, int(title_size_var.get()))
            )

            settings["stats_columns"] = max(
                1,
                min(5, int(columns_var.get()))
            )

        except (ValueError, tk.TclError):

            messagebox.showerror(
                "Ugyldige verdier",
                "Kontroller skriftstørrelse og kolonner."
            )

            return False

        for key, var in feature_vars.items():
            settings["features"][key] = var.get()

        rebuild_interface()

        status_var.set("Innstillingene er brukt.")

        return True

    def lagre_og_lukk():

        if bruk_innstillinger():

            if save_settings():

                status_var.set(
                    "Innstillingene er lagret."
                )

                window.destroy()

    def standardinnstillinger():

        global settings

        settings = json.loads(
            json.dumps(DEFAULT_SETTINGS)
        )

        save_settings()

        window.destroy()

        rebuild_interface()

        status_var.set(
            "Standardinnstillinger gjenopprettet."
        )

    buttons = tk.Frame(
        content,
        bg=color("bg")
    )

    buttons.pack(
        fill="x",
        pady=(10, 25)
    )

    lag_knapp(
        buttons,
        "Bruk",
        bruk_innstillinger
    ).pack(side="left", padx=(0, 5))

    lag_knapp(
        buttons,
        "Lagre og lukk",
        lagre_og_lukk,
        color("green")
    ).pack(side="left", padx=5)

    lag_knapp(
        buttons,
        "Standard",
        standardinnstillinger,
        color("panel_light")
    ).pack(side="right")


# ============================================================
# HJELPESYSTEM OG EASTER EGGS
# ============================================================

def vis_hjelpevindu(tittel, innhold):
    vindu = tk.Toplevel(root)
    vindu.title(tittel)
    vindu.geometry("680x540")
    vindu.minsize(480, 360)
    vindu.configure(bg=color("bg"))

    tk.Label(
        vindu,
        text=tittel,
        bg=color("bg"),
        fg=color("text"),
        font=title_font()
    ).pack(anchor="w", padx=20, pady=(18, 12))

    ramme = tk.Frame(vindu, bg=color("bg"))
    ramme.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    tekst = tk.Text(
        ramme,
        wrap="word",
        bg=color("panel"),
        fg=color("text"),
        insertbackground=color("text"),
        font=font(10),
        relief="flat",
        padx=14,
        pady=14
    )
    scrollbar_hjelp = ttk.Scrollbar(ramme, orient="vertical", command=tekst.yview)
    tekst.configure(yscrollcommand=scrollbar_hjelp.set)
    scrollbar_hjelp.pack(side="right", fill="y")
    tekst.pack(side="left", fill="both", expand=True)
    tekst.insert("1.0", innhold)
    tekst.configure(state="disabled")


def vis_kom_i_gang():
    vis_hjelpevindu("Kom i gang med Tall Sorterer", """
VELKOMMEN TIL TALL SORTERER!

1. Skriv tallene i feltet øverst.
2. Skill tallene med mellomrom, komma eller semikolon.
3. Velg «Sorter stigende» eller «Sorter synkende».
4. Resultatene vises under inndatafeltet.

EKSEMPEL
12, 8, 15, 4, 12, 20, 8

Du kan bruke Innstillinger til å velge hvilke statistiske beregninger,
tabeller og diagrammer som skal vises. Du kan også endre farger,
skrifttype og antall kolonner.

Kopier eller eksporter resultatene med knappene nederst.
Kalkulatoren åpnes fra knappen ved siden av sorteringsknappene.

FLERE VERKTØY
Åpne Verktøy-menyen for å generere tilfeldige testdata, importere tall
fra CSV/TXT, fjerne duplikater, kopiere bare tallene eller eksportere
frekvenstabellen som CSV.
""")


def vis_statistikkhjelp():
    vis_hjelpevindu("Forklaring av statistikk", """
GRUNNLEGGENDE BEGREPER

Antall: Hvor mange tall datasettet inneholder.
Sum: Summen av alle tallene.
Gjennomsnitt: Sum delt på antall.
Median: Den midterste verdien i sortert rekkefølge.
Typetall: Verdien eller verdiene som forekommer oftest.
Minimum/maksimum: Laveste og høyeste verdi.
Variasjonsbredde: Maksimum minus minimum.

KVARTILER
Q1 er nedre kvartil, Q2 er medianen og Q3 er øvre kvartil.
IQR (interkvartilbredde) er Q3 minus Q1.

VARIASJON
Populasjonsvarians og populasjonsstandardavvik beskriver spredningen
i hele datasettet. Utvalgsvarians og utvalgsstandardavvik bruker
utvalgsformelen med n-1.

UTVIDET STATISTIKK
Median absoluttavvik (MAD): Medianen av avstandene fra medianen.
Geometrisk gjennomsnitt: Nyttig blant annet ved vekstrater; krever positive tall.
Harmonisk gjennomsnitt: Nyttig for visse forholdstall; krever positive tall.
Sum av kvadrater: Summen av hvert tall ganget med seg selv.

AVVIKENDE OBSERVASJONER
Programmet bruker 1,5 × IQR-regelen. Verdier utenfor grensene
Q1 - 1,5 × IQR og Q3 + 1,5 × IQR blir markert som mulige avvik.
Dette er en indikasjon, ikke automatisk en feil i datasettet.
""")


def vis_kalkulatorhjelp():
    vis_hjelpevindu("Kalkulatorhjelp", """
KALKULATOREN

Støttede operatorer: +, -, *, /, //, %, ** og parenteser.
Du kan bruke ^ som potens i kalkulatorens tastatur.

Funksjoner:
sqrt(x) – kvadratrot
abs(x) – absoluttverdi
round(x) – avrunding
sin(x), cos(x), tan(x) – trigonometriske funksjoner
log(x) – 10-logaritme
ln(x) – naturlig logaritme
pi() – pi
e() – Eulers tall

Trigonometriske funksjoner bruker radianer.
Eksempel: sin(pi()/2)
""")


def vis_hurtigtaster():
    vis_hjelpevindu("Hurtigtaster", """
CTRL + ENTER       Sorter stigende
CTRL + SHIFT + ENTER  Sorter synkende
CTRL + L           Nullstill inndata og resultater
CTRL + ,           Åpne innstillinger
CTRL + SHIFT + C   Kopier resultater
CTRL + E           Eksporter resultater
F1                 Åpne hjelp / kom i gang
F2                 Generer tilfeldige testdata
F3                 Importer tall fra CSV/TXT

Flere funksjoner finnes i Verktøy-menyen. De kan åpnes med musen.

I kalkulatoren:
ENTER              Beregn uttrykket
ESC                Tøm kalkulatorfeltet
""")


def vis_om_programmet():
    vis_hjelpevindu("Om Tall Sorterer", """
TALL SORTERER – versjon 3.1

Et Python-basert program for sortering, statistikk og enkel analyse.

Funksjoner:
• Sortering stigende og synkende
• Grunnleggende og utvidet statistikk
• Kvartiler og avviksanalyse
• Frekvenstabell og histogram
• Innebygd kalkulator
• Tilpassbare farger, skrifttyper og visningsvalg
• Kopiering og eksport av resultater i TXT og CSV
• Import av tall fra CSV/TXT og generering av tilfeldige testdata
• Verktøy for duplikater og datasettinformasjon
• Hjelpemeny med forklaringer og hurtigtaster
• Flere skjulte easter eggs

Laget med Python og Tkinter.
""")


def opprett_hjelpemeny():
    menubar = tk.Menu(root)
    filmeny = tk.Menu(menubar, tearoff=0)
    filmeny.add_command(label="Nullstill", command=nullstill, accelerator="Ctrl+L")
    filmeny.add_separator()
    filmeny.add_command(label="Avslutt", command=root.destroy)
    menubar.add_cascade(label="Program", menu=filmeny)

    innstillingsmeny = tk.Menu(menubar, tearoff=0)
    innstillingsmeny.add_command(label="Innstillinger", command=apne_innstillinger, accelerator="Ctrl+,")
    innstillingsmeny.add_command(label="Gjenopprett standardinnstillinger", command=standardinnstillinger_global)
    menubar.add_cascade(label="Innstillinger", menu=innstillingsmeny)

    verktoy = tk.Menu(menubar, tearoff=0)
    verktoy.add_command(label="Generer tilfeldige tall", command=generer_tilfeldige_tall)
    verktoy.add_command(label="Importer tall fra CSV/TXT", command=importer_tall_csv)
    verktoy.add_command(label="Fjern duplikater fra inndata", command=fjern_duplikater)
    verktoy.add_separator()
    verktoy.add_command(label="Kopier kun sorterte tall", command=kopier_sorterte_tall)
    verktoy.add_command(label="Eksporter frekvenstabell som CSV", command=eksporter_csv)
    verktoy.add_command(label="Vis datasettinformasjon", command=vis_datasettinfo)
    menubar.add_cascade(label="Verktøy", menu=verktoy)

    hjelp = tk.Menu(menubar, tearoff=0)
    hjelp.add_command(label="Kom i gang", command=vis_kom_i_gang)
    hjelp.add_command(label="Statistiske begreper", command=vis_statistikkhjelp)
    hjelp.add_command(label="Kalkulatorhjelp", command=vis_kalkulatorhjelp)
    hjelp.add_separator()
    hjelp.add_command(label="Hurtigtaster", command=vis_hurtigtaster)
    hjelp.add_command(label="Om Tall Sorterer", command=vis_om_programmet)
    menubar.add_cascade(label="Hjelp", menu=hjelp)
    root.config(menu=menubar)


def standardinnstillinger_global():
    global settings
    settings = json.loads(json.dumps(DEFAULT_SETTINGS))
    save_settings()
    rebuild_interface()
    oppdater_ttk()
    status_var.set("Standardinnstillinger gjenopprettet.")


# Easter eggs: rolige fargeoverganger, ikke blinkende strobelys.
_easter_egg_vindu = None
_easter_egg_job = None
_easter_egg_farger = ["#26334a", "#334b50", "#49364b", "#3d4935", "#343b59"]
_easter_egg_aktiv = None


def sjekk_easter_egg(event=None):
    global _easter_egg_aktiv
    tekst = entry.get().strip().upper()
    hemmeligheter = {
        "TIRIL KAN IKKE LESE": (
            "TIRIL KAN IKKE LESE",
            "Du fant Tiril-hemmeligheten i Tall Sorterer!"
        ),
        "JOHAN-OLAI ER SMART": (
            "JOHAN-OLAI ER SMART",
            "Easter egg funnet. Statistikken stemmer visst!"
        ),
        "PETER ER DUM": (
            "PETER ER DUM",
            "Et gammelt rykte har nådd Tall Sorterer ..."
        )
    }
    if tekst in hemmeligheter and _easter_egg_aktiv is None:
        _easter_egg_aktiv = tekst
        entry.delete(0, tk.END)
        vis_easter_egg(*hemmeligheter[tekst])


def vis_easter_egg(overskrift, undertekst):
    global _easter_egg_vindu
    global _easter_egg_job

    if _easter_egg_vindu is not None:
        return

    vindu = tk.Toplevel(root)
    _easter_egg_vindu = vindu
    vindu.title("Hemmelig easter egg!")
    vindu.geometry("650x330")
    vindu.resizable(False, False)
    vindu.configure(bg=_easter_egg_farger[0])

    hovedtekst = tk.Label(
        vindu, text=overskrift,
        font=(settings["font"], 25, "bold"),
        bg=_easter_egg_farger[0], fg="white"
    )
    hovedtekst.pack(expand=True, padx=20, pady=(35, 5))

    undertekst_label = tk.Label(
        vindu, text=undertekst,
        font=font(11), bg=_easter_egg_farger[0], fg="white"
    )
    undertekst_label.pack(pady=10)

    def lukk():
        global _easter_egg_vindu, _easter_egg_job, _easter_egg_aktiv
        if _easter_egg_job is not None:
            try:
                vindu.after_cancel(_easter_egg_job)
            except tk.TclError:
                pass
        _easter_egg_vindu = None
        _easter_egg_job = None
        _easter_egg_aktiv = None
        vindu.destroy()

    tk.Button(
        vindu, text="Lukk", command=lukk,
        bg="#202636", fg="white", relief="flat",
        padx=25, pady=8
    ).pack(pady=(10, 25))

    def animer(indeks=0):
        global _easter_egg_job
        if _easter_egg_vindu is None or not vindu.winfo_exists():
            return
        farge = _easter_egg_farger[indeks % len(_easter_egg_farger)]
        vindu.configure(bg=farge)
        hovedtekst.configure(bg=farge)
        undertekst_label.configure(bg=farge)
        _easter_egg_job = vindu.after(850, lambda: animer(indeks + 1))

    animer()


# ============================================================
# BYGG HOVEDVINDU
# ============================================================

def rebuild_interface():

    global main
    global stats_frame
    global result_area
    global entry
    global status_var
    global export_frame

    for widget in main.winfo_children():
        widget.destroy()

    # OVERSKRIFT

    header = tk.Frame(
        main,
        bg=color("bg")
    )

    header.pack(fill="x")

    title_frame = tk.Frame(
        header,
        bg=color("bg")
    )

    title_frame.pack(side="left")

    tk.Label(
        title_frame,
        text="TALL SORTERER",
        bg=color("bg"),
        fg=color("text"),
        font=title_font()
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Statistikk, analyse og tallbehandling",
        bg=color("bg"),
        fg=color("muted"),
        font=font(9)
    ).pack(anchor="w", pady=(2, 15))

    # INNSTILLINGSKNAPP

    lag_knapp(
        header,
        "⚙ Innstillinger",
        apne_innstillinger,
        color("panel_light")
    ).pack(side="right", pady=5)

    # INPUTPANEL

    input_frame = tk.Frame(
        main,
        bg=color("panel"),
        padx=18,
        pady=15
    )

    input_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        input_frame,
        text=f"LEGG INN TALL (MAKS {MAX_TALL})",
        bg=color("panel"),
        fg=color("text"),
        font=font(10, True)
    ).pack(anchor="w")

    tk.Label(
        input_frame,
        text="Skill tallene med mellomrom, komma eller semikolon.",
        bg=color("panel"),
        fg=color("muted"),
        font=font(9)
    ).pack(anchor="w", pady=(3, 10))

    global entry

    entry = tk.Entry(
        input_frame,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(12),
        borderwidth=0
    )

    entry.pack(
        fill="x",
        ipady=12
    )
    entry.bind("<KeyRelease>", sjekk_easter_egg)

    # KNAPPER

    button_frame = tk.Frame(
        input_frame,
        bg=color("panel")
    )

    button_frame.pack(
        fill="x",
        pady=(12, 0)
    )

    lag_knapp(
        button_frame,
        "Sorter stigende",
        lambda: sorter_tall("stigende")
    ).pack(side="left", padx=(0, 7))

    lag_knapp(
        button_frame,
        "Sorter synkende",
        lambda: sorter_tall("synkende"),
        color("panel_light")
    ).pack(side="left", padx=7)

    lag_knapp(
        button_frame,
        "Nullstill",
        nullstill,
        color("panel_light")
    ).pack(side="right")

    # KALKULATOR

    if settings["features"]["calculator"]:

        lag_knapp(
            button_frame,
            "Kalkulator",
            apne_kalkulator,
            color("panel_light")
        ).pack(side="right", padx=7)

    # RESULTATOMRÅDE

    global result_area

    result_area = tk.Frame(
        main,
        bg=color("bg")
    )

    result_area.pack(
        fill="both",
        expand=True
    )

    # EKSPORTKNAPPER

    if (
        settings["features"]["copy"]
        or settings["features"]["export"]
    ):

        export_frame = tk.Frame(
            main,
            bg=color("bg")
        )

        export_frame.pack(
            fill="x",
            pady=(15, 5)
        )

        if settings["features"]["copy"]:

            lag_knapp(
                export_frame,
                "Kopier resultater",
                kopier_resultater,
                color("panel_light")
            ).pack(side="left", padx=(0, 8))

        if settings["features"]["export"]:

            lag_knapp(
                export_frame,
                "Eksporter TXT",
                eksporter_resultater,
                color("panel_light")
            ).pack(side="left")

    # STATUS

    global status_var

    tk.Label(
        main,
        textvariable=status_var,
        bg=color("bg"),
        fg=color("green"),
        font=font(9)
    ).pack(
        anchor="w",
        pady=(8, 0)
    )

    # VIS TIDLIGERE RESULTATER

    if siste_resultat is not None:
        vis_resultater()

    root.update_idletasks()

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


# ============================================================
# TTK-TEMA
# ============================================================

def oppdater_ttk():

    style.configure(
        "Treeview",
        background=color("panel_light"),
        foreground=color("text"),
        fieldbackground=color("panel_light"),
        rowheight=30,
        font=font(10),
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background=color("panel"),
        foreground=color("text"),
        font=font(10, True),
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[
            ("selected", color("accent"))
        ],
        foreground=[
            ("selected", "white")
        ]
    )


# ============================================================
# HOVEDVINDU OG SCROLLBAR
# ============================================================

root = tk.Tk()

root.title("Tall Sorterer")
root.geometry("1100x850")
root.minsize(750, 600)
root.configure(bg=color("bg"))

style = ttk.Style()
style.theme_use("clam")

status_var = tk.StringVar(
    value="Klar til å sortere nye tall."
)

scroll_container = tk.Frame(
    root,
    bg=color("bg")
)

scroll_container.pack(
    fill="both",
    expand=True
)

canvas = tk.Canvas(
    scroll_container,
    bg=color("bg"),
    highlightthickness=0
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar = ttk.Scrollbar(
    scroll_container,
    orient="vertical",
    command=canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

main = tk.Frame(
    canvas,
    bg=color("bg"),
    padx=25,
    pady=20
)

main_window = canvas.create_window(
    (0, 0),
    window=main,
    anchor="nw"
)


# ============================================================
# SCROLLFUNKSJONER
# ============================================================

def oppdater_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def tilpass_bredde(event):

    canvas.itemconfigure(
        main_window,
        width=event.width
    )


main.bind(
    "<Configure>",
    oppdater_scroll
)

canvas.bind(
    "<Configure>",
    tilpass_bredde
)


def musehjul(event):

    if event.delta:

        canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )


canvas.bind_all(
    "<MouseWheel>",
    musehjul
)


# ============================================================
# TASTATURSNARVEIER
# ============================================================

root.bind(
    "<Control-Return>",
    lambda event: sorter_tall("stigende")
)

root.bind(
    "<Control-l>",
    lambda event: nullstill()
)

root.bind(
    "<Control-comma>",
    lambda event: apne_innstillinger()
)

root.bind(
    "<Control-Shift-Return>",
    lambda event: sorter_tall("synkende")
)
root.bind("<Control-Shift-C>", lambda event: kopier_resultater())
root.bind("<Control-e>", lambda event: eksporter_resultater())
root.bind("<F1>", lambda event: vis_kom_i_gang())
root.bind("<F2>", lambda event: generer_tilfeldige_tall())
root.bind("<F3>", lambda event: importer_tall_csv())


# ============================================================
# START PROGRAMMET
# ============================================================

oppdater_ttk()

rebuild_interface()
opprett_hjelpemeny()

root.mainloop()

