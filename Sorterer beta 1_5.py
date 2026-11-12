import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from tkinter import font as tkfont
from collections import Counter
from datetime import datetime
import statistics
import math
import json
import os
import ast
import operator
import random
import csv
import re
import colorsys


# ============================================================
# INNSTILLINGER
# ============================================================

VERSJON = "2.0"
MAX_TALL = 999
HISTORIKK_MAKS = 30
SETTINGS_FILE = "tall_sorterer_settings.json"
HISTORY_FILE = "tall_sorterer_historikk.json"

FARGENOKLER = [
    "bg", "panel", "panel_light", "accent",
    "text", "muted", "green", "red"
]

THEMES = {
    "Midnatt": {
        "bg": "#111318", "panel": "#1B1F29", "panel_light": "#242A36",
        "accent": "#6C8CFF", "text": "#F1F3F8", "muted": "#929BAD",
        "green": "#55D6A7", "red": "#FF7373"
    },
    "Lys": {
        "bg": "#F4F6FB", "panel": "#FFFFFF", "panel_light": "#E6EAF3",
        "accent": "#3D5AFE", "text": "#1B1F29", "muted": "#6B7385",
        "green": "#1E9E6A", "red": "#D93636"
    },
    "Hacker": {
        "bg": "#050805", "panel": "#0B140B", "panel_light": "#122012",
        "accent": "#1FA83A", "text": "#B6FFB6", "muted": "#5C9A5C",
        "green": "#39FF14", "red": "#FF4040"
    },
    "Solnedgang": {
        "bg": "#1E1220", "panel": "#2B1A2E", "panel_light": "#3A2440",
        "accent": "#FF7A59", "text": "#FFEFE6", "muted": "#C79AA8",
        "green": "#FFC857", "red": "#FF4D6D"
    },
    "Hav": {
        "bg": "#0B1B26", "panel": "#12293A", "panel_light": "#183649",
        "accent": "#2EC4B6", "text": "#E8F6F8", "muted": "#7FA3B0",
        "green": "#7BE0AD", "red": "#FF6B6B"
    }
}

DEFAULT_SETTINGS = {
    "theme": "Midnatt",
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
    "decimals": 4,

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
        "extra": True,
        "percentiles": True,
        "outliers": True,
        "frequency": True,
        "histogram": True,
        "boxplot": True,
        "sorted_list": True,
        "calculator": True,
        "converter": True,
        "random": True,
        "import": True,
        "history": True,
        "copy": True,
        "export": True,
        "csv": True,
        "fun": True
    }
}

settings = {}
historikk = []


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

        except (OSError, json.JSONDecodeError, AttributeError):
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


def last_historikk():

    global historikk

    historikk = []

    if os.path.exists(HISTORY_FILE):

        try:
            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):
                historikk = [
                    h for h in data
                    if isinstance(h, dict)
                    and "tekst" in h
                    and "tid" in h
                ][-HISTORIKK_MAKS:]

        except (OSError, json.JSONDecodeError):
            historikk = []


def lagre_historikk():

    try:
        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                historikk[-HISTORIKK_MAKS:],
                file,
                indent=2,
                ensure_ascii=False
            )

    except OSError:
        pass


load_settings()
last_historikk()


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

    if isinstance(tall, (list, tuple)):

        if not tall:
            return "Ingen"

        return ", ".join(formater(x) for x in tall)

    if isinstance(tall, str):
        return tall

    if isinstance(tall, int):
        return str(tall)

    if isinstance(tall, float):

        if not math.isfinite(tall):
            return str(tall)

        if tall.is_integer() and abs(tall) < 1e15:
            return str(int(tall))

        desimaler = settings["decimals"]

        tekst = f"{tall:.{desimaler}f}"

        if "." in tekst:
            tekst = tekst.rstrip("0").rstrip(".")

        if tekst in ("-0", ""):
            tekst = "0"

        if tekst == "0" and tall != 0:
            return f"{tall:.3g}"

        return tekst

    return str(tall)


def kalk_format(tall):

    if isinstance(tall, int):
        return str(tall)

    if isinstance(tall, float):

        if tall.is_integer() and abs(tall) < 1e15:
            return str(int(tall))

        return f"{tall:.12g}"

    return str(tall)


def nytt_vindu(tittel, geometri, minstorrelse=None):

    vindu = tk.Toplevel(root)
    vindu.title(tittel)
    vindu.geometry(geometri)
    vindu.configure(bg=color("bg"))

    if minstorrelse:
        vindu.minsize(*minstorrelse)

    return vindu


def lag_sjekk(parent, tekst, var, bg):

    return tk.Checkbutton(
        parent,
        text=tekst,
        variable=var,
        bg=bg,
        fg=color("text"),
        activebackground=bg,
        activeforeground=color("text"),
        selectcolor=color("panel_light"),
        font=font(9),
        highlightthickness=0,
        bd=0
    )


# ============================================================
# STATISTIKKBEREGNING
# ============================================================

def persentil(sortert, p):

    if len(sortert) == 1:
        return sortert[0]

    k = (len(sortert) - 1) * p / 100

    nedre = math.floor(k)
    ovre = math.ceil(k)

    if nedre == ovre:
        return sortert[int(k)]

    return sortert[nedre] + (
        sortert[ovre] - sortert[nedre]
    ) * (k - nedre)


def beregn_statistikk(tall):

    tall = sorted(tall)

    antall = len(tall)

    frekvens = Counter(tall)

    snitt = statistics.mean(tall)

    data = {
        "tall": tall,
        "antall": antall,
        "sum": sum(tall),
        "gjennomsnitt": snitt,
        "median": statistics.median(tall),
        "typetall": statistics.multimode(tall),
        "minimum": min(tall),
        "maksimum": max(tall),
        "variasjonsbredde": max(tall) - min(tall),
        "frekvens": frekvens,
        "retning": "stigende"
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

        data["ut_lav"] = q1 - 1.5 * (q3 - q1)
        data["ut_hoy"] = q3 + 1.5 * (q3 - q1)

        data["uteliggere"] = [
            x for x in tall
            if x < data["ut_lav"] or x > data["ut_hoy"]
        ]

    else:

        data["q1"] = None
        data["q2"] = statistics.median(tall)
        data["q3"] = None
        data["iqr"] = None
        data["ut_lav"] = None
        data["ut_hoy"] = None
        data["uteliggere"] = []

    # VARIANS OG STANDARDAVVIK

    data["varians"] = statistics.pvariance(tall)
    data["standardavvik"] = statistics.pstdev(tall)

    # UTVIDET STATISTIKK

    sd = data["standardavvik"]

    data["utvalgs_std"] = (
        statistics.stdev(tall) if antall >= 2 else None
    )

    data["standardfeil"] = (
        data["utvalgs_std"] / math.sqrt(antall)
        if data["utvalgs_std"] is not None else None
    )

    data["geometrisk"] = (
        math.exp(sum(math.log(x) for x in tall) / antall)
        if all(x > 0 for x in tall) else None
    )

    data["harmonisk"] = (
        antall / sum(1 / x for x in tall)
        if all(x > 0 for x in tall) else None
    )

    data["skjevhet"] = (
        (sum((x - snitt) ** 3 for x in tall) / antall) / sd ** 3
        if sd > 0 else None
    )

    data["variasjonskoeffisient"] = (
        sd / abs(snitt) * 100 if snitt != 0 else None
    )

    data["mad"] = sum(abs(x - snitt) for x in tall) / antall

    # PERSENTILER

    for p in (5, 10, 90, 95):
        data[f"p{p}"] = persentil(tall, p)

    return data


def typetall_tekst(data):

    if (
        data["antall"] > 1
        and len(data["typetall"]) == len(data["frekvens"])
    ):
        return "Ingen (alle er unike)"

    return formater(data["typetall"])


def bygg_statistikkliste(data):

    """Returnerer liste med (navn, formatert verdi) basert på valgte funksjoner."""

    f = settings["features"]
    rader = []

    def legg(key, navn, verdi):

        if f.get(key):
            rader.append((navn, formater(verdi)))

    legg("antall", "Antall tall", data["antall"])
    legg("sum", "Sum", data["sum"])
    legg("gjennomsnitt", "Gjennomsnitt", data["gjennomsnitt"])
    legg("median", "Median", data["median"])
    legg("typetall", "Typetall", typetall_tekst(data))
    legg("minimum", "Laveste verdi", data["minimum"])
    legg("maksimum", "Høyeste verdi", data["maksimum"])
    legg(
        "variasjonsbredde",
        "Variasjonsbredde",
        data["variasjonsbredde"]
    )

    if f["quartiles"]:

        rader.extend([
            ("Q1", formater(data["q1"])),
            ("Q2", formater(data["q2"])),
            ("Q3", formater(data["q3"])),
            ("Kvartilbredde (IQR)", formater(data["iqr"]))
        ])

    if f["variance"]:

        rader.extend([
            ("Varians", formater(data["varians"])),
            ("Standardavvik", formater(data["standardavvik"]))
        ])

    if f["extra"]:

        rader.extend([
            (
                "Utvalgsstandardavvik",
                formater(data["utvalgs_std"])
            ),
            ("Standardfeil", formater(data["standardfeil"])),
            ("Geometrisk snitt", formater(data["geometrisk"])),
            ("Harmonisk snitt", formater(data["harmonisk"])),
            ("Skjevhet", formater(data["skjevhet"])),
            (
                "Variasjonskoeffisient (%)",
                formater(data["variasjonskoeffisient"])
            ),
            ("Gj.snittlig avvik", formater(data["mad"]))
        ])

    if f["percentiles"]:

        rader.extend([
            ("5. persentil", formater(data["p5"])),
            ("10. persentil", formater(data["p10"])),
            ("90. persentil", formater(data["p90"])),
            ("95. persentil", formater(data["p95"]))
        ])

    if f["outliers"]:

        rader.append((
            "Uteliggere",
            formater(data["uteliggere"])
        ))

    return rader


# ============================================================
# GLOBALE VARIABLER
# ============================================================

siste_resultat = None

root = None
style = None
canvas = None
main = None
main_window = None
scroll_container = None
entry = None
status_var = None
result_area = None
stats_frame = None
sorted_text = None
frekvens_tabell = None
histogram = None
boxplot_canvas = None
export_frame = None

dup_var = None
avrund_var = None
filt_min_var = None
filt_max_var = None


# ============================================================
# HOVEDPROGRAM
# ============================================================

def legg_i_historikk(tekst):

    if not settings["features"]["history"]:
        return

    if historikk and historikk[-1]["tekst"] == tekst:
        return

    historikk.append({
        "tid": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "tekst": tekst
    })

    del historikk[:-HISTORIKK_MAKS]

    lagre_historikk()


def sorter_tall(retning="stigende"):

    global siste_resultat

    input_text = entry.get().strip()

    if sjekk_easter_egg(input_text):
        return

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

    meldinger = []

    # FILTER

    try:

        tekst_min = filt_min_var.get().strip().replace(",", ".")
        tekst_maks = filt_max_var.get().strip().replace(",", ".")

        filter_min = float(tekst_min) if tekst_min else None
        filter_maks = float(tekst_maks) if tekst_maks else None

    except ValueError:

        messagebox.showerror(
            "Ugyldig filter",
            "Filterverdiene må være tall."
        )

        return

    for_filter = len(tall)

    if filter_min is not None:
        tall = [x for x in tall if x >= filter_min]

    if filter_maks is not None:
        tall = [x for x in tall if x <= filter_maks]

    if len(tall) < for_filter:
        meldinger.append(
            f"{for_filter - len(tall)} fjernet av filteret."
        )

    # AVRUNDING OG DUPLIKATER

    if avrund_var.get():
        tall = [float(math.floor(x + 0.5)) for x in tall]

    if dup_var.get():

        unike = list(dict.fromkeys(tall))

        if len(unike) < len(tall):
            meldinger.append(
                f"{len(tall) - len(unike)} duplikater fjernet."
            )

        tall = unike

    if not tall:

        messagebox.showerror(
            "Ingen tall igjen",
            "Filteret fjernet alle tallene."
        )

        return

    data = beregn_statistikk(tall)
    data["retning"] = retning

    if retning == "synkende":
        data["tall"].reverse()

    elif retning == "tilfeldig":
        random.shuffle(data["tall"])

    siste_resultat = data

    legg_i_historikk(input_text)

    vis_resultater()

    status = f"Ferdig. {len(tall)} tall behandlet."

    if ugyldige:
        status += f" {len(ugyldige)} ugyldige verdier ignorert."

    if meldinger:
        status += " " + " ".join(meldinger)

    status_var.set(status)


# ============================================================
# KNAPPER
# ============================================================

def lag_knapp(
    parent,
    tekst,
    funksjon,
    farge=None
):

    bakgrunn = farge or color("accent")

    if bakgrunn == color("panel_light"):
        tekstfarge = color("text")
    else:
        tekstfarge = "white"

    return tk.Button(
        parent,
        text=tekst,
        command=funksjon,
        bg=bakgrunn,
        fg=tekstfarge,
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

    verdier = bygg_statistikkliste(data)

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
            text=verdi,
            bg=color("panel_light"),
            fg=color("text"),
            font=font(settings["font_size"] + 2, True),
            wraplength=220,
            justify="left"
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
# BOKSPLOTT
# ============================================================

def tegn_boxplot(data):

    boxplot_canvas.delete("all")

    bredde = max(boxplot_canvas.winfo_width(), 400)
    hoyde = max(boxplot_canvas.winfo_height(), 110)

    if data["q1"] is None or data["minimum"] == data["maksimum"]:

        boxplot_canvas.create_text(
            bredde / 2,
            hoyde / 2,
            text="For få eller like verdier til å tegne boksplott",
            fill=color("muted"),
            font=font(10)
        )

        return

    lav = data["minimum"]
    hoy = data["maksimum"]

    margin = 40

    def x(verdi):
        return margin + (verdi - lav) / (hoy - lav) * (
            bredde - 2 * margin
        )

    midt = hoyde / 2 - 5

    normale = [
        v for v in data["tall"]
        if data["ut_lav"] <= v <= data["ut_hoy"]
    ]

    if normale:
        hvisker_lav = min(normale)
        hvisker_hoy = max(normale)
    else:
        hvisker_lav = data["q1"]
        hvisker_hoy = data["q3"]

    boxplot_canvas.create_line(
        x(hvisker_lav), midt, x(hvisker_hoy), midt,
        fill=color("muted"), width=2
    )

    for verdi in (hvisker_lav, hvisker_hoy):

        boxplot_canvas.create_line(
            x(verdi), midt - 10, x(verdi), midt + 10,
            fill=color("muted"), width=2
        )

    boxplot_canvas.create_rectangle(
        x(data["q1"]), midt - 18,
        x(data["q3"]), midt + 18,
        fill=color("accent"),
        outline=color("text")
    )

    boxplot_canvas.create_line(
        x(data["q2"]), midt - 18,
        x(data["q2"]), midt + 18,
        fill="white", width=3
    )

    for verdi in data["uteliggere"]:

        boxplot_canvas.create_oval(
            x(verdi) - 4, midt - 4,
            x(verdi) + 4, midt + 4,
            outline=color("red"),
            width=2
        )

    for verdi, tekst in (
        (lav, formater(lav)),
        (data["q2"], f"Median {formater(data['q2'])}"),
        (hoy, formater(hoy))
    ):

        boxplot_canvas.create_text(
            x(verdi),
            midt + 34,
            text=tekst,
            fill=color("muted"),
            font=font(8)
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

        liste = ", ".join(formater(x) for x in data["tall"])

        tekst += f"Tall ({data['retning']}): {liste}\n\n"

    tekst += "STATISTIKK\n"

    for navn, verdi in bygg_statistikkliste(data):
        tekst += f"{navn}: {verdi}\n"

    if features["frequency"]:

        tekst += "\nFREKVENSTABELL\n"

        for tall, antall in sorted(data["frekvens"].items()):

            prosent = antall / data["antall"] * 100

            tekst += (
                f"{formater(tall)}: {antall} "
                f"({prosent:.2f}%)\n"
            )

    return tekst


def kopier_resultater():

    if not settings["features"]["copy"]:
        return

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

    if not settings["features"]["export"]:
        return

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


def eksporter_csv():

    if not settings["features"]["csv"]:
        return

    if siste_resultat is None:
        messagebox.showwarning(
            "Ingen resultater",
            "Sorter tall først."
        )
        return

    fil = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[
            ("CSV-filer", "*.csv"),
            ("Alle filer", "*.*")
        ],
        title="Lagre som CSV"
    )

    if not fil:
        return

    data = siste_resultat

    try:

        with open(
            fil,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as f:

            skriver = csv.writer(f, delimiter=";")

            skriver.writerow(["Statistikk", "Verdi"])

            for navn, verdi in bygg_statistikkliste(data):
                skriver.writerow([navn, verdi])

            skriver.writerow([])
            skriver.writerow(["Tall", "Antall", "Prosent"])

            for tall, antall in sorted(data["frekvens"].items()):

                prosent = antall / data["antall"] * 100

                skriver.writerow([
                    formater(tall),
                    antall,
                    f"{prosent:.2f}".replace(".", ",")
                ])

        status_var.set("CSV-filen er lagret.")

    except OSError as error:

        messagebox.showerror("Eksportfeil", str(error))


def importer_fil():

    if not settings["features"]["import"]:
        return

    fil = filedialog.askopenfilename(
        title="Velg fil med tall",
        filetypes=[
            ("Tekst/CSV", "*.txt *.csv *.dat"),
            ("Alle filer", "*.*")
        ]
    )

    if not fil:
        return

    try:

        with open(
            fil,
            "r",
            encoding="utf-8-sig",
            errors="replace"
        ) as f:

            innhold = f.read()

    except OSError as error:

        messagebox.showerror("Importfeil", str(error))
        return

    funnet = re.findall(
        r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?",
        innhold
    )

    if not funnet:

        messagebox.showwarning(
            "Ingen tall",
            "Fant ingen tall i filen."
        )

        return

    if len(funnet) > MAX_TALL:

        funnet = funnet[:MAX_TALL]

        messagebox.showinfo(
            "Avkortet",
            f"Filen hadde for mange tall. "
            f"Bare de første {MAX_TALL} ble importert."
        )

    entry.delete(0, tk.END)
    entry.insert(0, " ".join(funnet))

    status_var.set(
        f"Importerte {len(funnet)} tall fra "
        f"{os.path.basename(fil)}."
    )


# ============================================================
# NULLSTILL
# ============================================================

def nullstill():

    global siste_resultat

    siste_resultat = None

    entry.delete(0, tk.END)

    dup_var.set(False)
    avrund_var.set(False)
    filt_min_var.set("")
    filt_max_var.set("")

    vis_resultater()

    status_var.set("Klar til å sortere nye tall.")


# ============================================================
# KALKULATOR
# ============================================================

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

KALK_FUNKSJONER = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    "radians": math.radians,
    "degrees": math.degrees,
    "pi": lambda: math.pi,
    "e": lambda: math.e
}

kalk_minne = {"ans": 0}


def sikker_beregning(uttrykk, ans=0):

    if len(uttrykk) > 200:
        raise ValueError("Uttrykket er for langt")

    tre = ast.parse(uttrykk, mode="eval")

    konstanter = {"pi": math.pi, "e": math.e, "ans": ans}

    def beregn(node):

        if isinstance(node, ast.Expression):
            return beregn(node.body)

        if isinstance(node, ast.Constant):

            if isinstance(node.value, bool):
                raise ValueError("Ugyldig verdi")

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Ugyldig verdi")

        if isinstance(node, ast.Name):

            if node.id in konstanter:
                return konstanter[node.id]

            raise ValueError("Ukjent navn")

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

            navn = node.func.id

            if navn not in KALK_FUNKSJONER:
                raise ValueError("Ukjent funksjon")

            if node.keywords:
                raise ValueError("Ugyldig argument")

            argumenter = [
                beregn(arg) for arg in node.args
            ]

            if navn in ("pi", "e"):

                if argumenter:
                    raise ValueError("Ingen argumenter tillatt")

                return KALK_FUNKSJONER[navn]()

            return KALK_FUNKSJONER[navn](*argumenter)

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

    window = nytt_vindu(
        "Kalkulator - Tall Sorterer",
        "400x700",
        (340, 560)
    )

    uttrykk_var = tk.StringVar()
    resultat_var = tk.StringVar(value="Klar")
    historie_var = tk.StringVar(value="")
    kalk_historie = []

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

    kalk_entry = tk.Entry(
        display,
        textvariable=uttrykk_var,
        justify="right",
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(20)
    )

    kalk_entry.pack(fill="x", ipady=12)
    kalk_entry.focus_set()

    tk.Label(
        display,
        textvariable=resultat_var,
        bg=color("panel"),
        fg=color("green"),
        font=font(12)
    ).pack(anchor="e", pady=(10, 0))

    tk.Label(
        display,
        textvariable=historie_var,
        bg=color("panel"),
        fg=color("muted"),
        font=font(8),
        justify="right"
    ).pack(anchor="e", pady=(6, 0))

    # BEREGNING

    def beregn():

        uttrykk = uttrykk_var.get().strip()

        if not uttrykk:
            return

        try:

            uttrykk_py = uttrykk.replace("^", "**")

            resultat = sikker_beregning(
                uttrykk_py,
                kalk_minne["ans"]
            )

            kalk_minne["ans"] = resultat

            resultat_var.set("= " + kalk_format(resultat))

            kalk_historie.append(
                f"{uttrykk} = {kalk_format(resultat)}"
            )

            historie_var.set("\n".join(kalk_historie[-3:]))

        except ZeroDivisionError:

            resultat_var.set("Kan ikke dele på null")

        except (
            ValueError, TypeError, SyntaxError,
            OverflowError, RecursionError
        ):

            resultat_var.set("Ugyldig regnestykke")

    # KNAPPFUNKSJONER

    def legg_til(verdi):

        uttrykk_var.set(
            uttrykk_var.get() + verdi
        )

        kalk_entry.icursor(tk.END)

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

            resultat = sikker_beregning(
                uttrykk,
                kalk_minne["ans"]
            )

            uttrykk_var.set(kalk_format(resultat))
            resultat_var.set("Resultatet er satt inn")

        except Exception:

            resultat_var.set("Kan ikke bruke resultatet")

    def send_til_tallfelt():

        try:

            uttrykk = uttrykk_var.get().replace("^", "**")

            resultat = sikker_beregning(
                uttrykk,
                kalk_minne["ans"]
            )

            gammel = entry.get().strip()

            entry.delete(0, tk.END)
            entry.insert(
                0,
                (gammel + " " if gammel else "")
                + kalk_format(resultat)
            )

            resultat_var.set("Lagt til i tallfeltet")

        except Exception:

            resultat_var.set("Kan ikke sende resultatet")

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
        ["sqrt(", "^", "pi()", "="],
        ["ans", "exp(", "ln(", "log("]
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

            er_lik = verdi == "="

            knapp = tk.Button(
                button_frame,
                text=verdi,
                command=lambda v=verdi: knappetrykk(v),
                bg=(
                    color("accent")
                    if er_lik
                    else color("panel_light")
                ),
                fg="white" if er_lik else color("text"),
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
        text="Funksjoner: sqrt, abs, round, sin, cos, tan, asin, "
             "acos, atan, log, ln, exp, floor, ceil, radians, "
             "degrees, pi, e, ans (forrige svar)",
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

    lag_knapp(
        extra,
        "Send til tallfeltet",
        send_til_tallfelt,
        color("panel_light")
    ).pack(fill="x", pady=(6, 0))

    window.bind("<Return>", lambda event: beregn())
    window.bind("<Escape>", lambda event: slett())


# ============================================================
# ENHETSOMREGNER
# ============================================================

ENHETER = {
    "Lengde": {
        "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
        "tomme": 0.0254, "fot": 0.3048, "yard": 0.9144,
        "engelsk mil": 1609.344, "nautisk mil": 1852.0,
        "norsk mil": 10000.0
    },
    "Vekt": {
        "mg": 1e-6, "g": 1e-3, "kg": 1.0, "tonn": 1000.0,
        "unse": 0.028349523125, "pund": 0.45359237,
        "stone": 6.35029318
    },
    "Volum": {
        "ml": 0.001, "cl": 0.01, "dl": 0.1, "liter": 1.0,
        "m³": 1000.0, "US gallon": 3.785411784,
        "US pint": 0.473176473
    },
    "Tid": {
        "ms": 0.001, "sekund": 1.0, "minutt": 60.0,
        "time": 3600.0, "døgn": 86400.0, "uke": 604800.0
    },
    "Hastighet": {
        "m/s": 1.0, "km/t": 1 / 3.6, "mph": 0.44704,
        "knop": 0.514444
    },
    "Temperatur": {"°C": None, "°F": None, "K": None}
}


def temp_til_celsius(verdi, enhet):

    if enhet == "°F":
        return (verdi - 32) * 5 / 9

    if enhet == "K":
        return verdi - 273.15

    return verdi


def temp_fra_celsius(verdi, enhet):

    if enhet == "°F":
        return verdi * 9 / 5 + 32

    if enhet == "K":
        return verdi + 273.15

    return verdi


def apne_omregner():

    if not settings["features"]["converter"]:
        return

    window = nytt_vindu(
        "Enhetsomregner",
        "420x420",
        (380, 380)
    )

    ramme = tk.Frame(
        window,
        bg=color("panel"),
        padx=18,
        pady=18
    )

    ramme.pack(fill="both", expand=True, padx=15, pady=15)

    kategori_var = tk.StringVar(value="Lengde")
    fra_var = tk.StringVar()
    til_var = tk.StringVar()
    verdi_var = tk.StringVar(value="1")
    resultat_var = tk.StringVar(value="")

    def etikett(tekst):

        tk.Label(
            ramme,
            text=tekst,
            bg=color("panel"),
            fg=color("muted"),
            font=font(9)
        ).pack(anchor="w", pady=(8, 2))

    etikett("Kategori")

    kategori_combo = ttk.Combobox(
        ramme,
        textvariable=kategori_var,
        values=list(ENHETER.keys()),
        state="readonly"
    )

    kategori_combo.pack(fill="x")

    etikett("Verdi")

    tk.Entry(
        ramme,
        textvariable=verdi_var,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(12)
    ).pack(fill="x", ipady=6)

    etikett("Fra")

    fra_combo = ttk.Combobox(
        ramme,
        textvariable=fra_var,
        state="readonly"
    )

    fra_combo.pack(fill="x")

    etikett("Til")

    til_combo = ttk.Combobox(
        ramme,
        textvariable=til_var,
        state="readonly"
    )

    til_combo.pack(fill="x")

    tk.Label(
        ramme,
        textvariable=resultat_var,
        bg=color("panel"),
        fg=color("green"),
        font=font(14, True),
        wraplength=340
    ).pack(pady=(18, 8))

    def omregn(*args):

        try:

            verdi = float(verdi_var.get().replace(",", "."))

            kategori = kategori_var.get()
            fra = fra_var.get()
            til = til_var.get()

            if kategori == "Temperatur":

                svar = temp_fra_celsius(
                    temp_til_celsius(verdi, fra),
                    til
                )

            else:

                tabell = ENHETER[kategori]

                svar = verdi * tabell[fra] / tabell[til]

            resultat_var.set(
                f"{formater(verdi)} {fra} = {kalk_format(svar)} {til}"
            )

        except (ValueError, KeyError, ZeroDivisionError):

            resultat_var.set("Ugyldig verdi")

    def bytt_kategori(*args):

        enheter = list(ENHETER[kategori_var.get()].keys())

        fra_combo.configure(values=enheter)
        til_combo.configure(values=enheter)

        fra_var.set(enheter[0])
        til_var.set(enheter[1] if len(enheter) > 1 else enheter[0])

        omregn()

    def send_til_tallfelt():

        tekst = resultat_var.get()

        if "=" not in tekst:
            return

        try:

            svar = tekst.split("=")[1].strip().split()[0]

            float(svar)

        except (ValueError, IndexError):
            return

        gammel = entry.get().strip()

        entry.delete(0, tk.END)
        entry.insert(0, (gammel + " " if gammel else "") + svar)

        status_var.set("Resultatet er lagt til i tallfeltet.")

    kategori_combo.bind("<<ComboboxSelected>>", bytt_kategori)
    fra_combo.bind("<<ComboboxSelected>>", omregn)
    til_combo.bind("<<ComboboxSelected>>", omregn)
    verdi_var.trace_add("write", omregn)

    lag_knapp(
        ramme,
        "Send til tallfeltet",
        send_til_tallfelt,
        color("accent")
    ).pack(fill="x")

    bytt_kategori()


# ============================================================
# TILFELDIGE TALL
# ============================================================

def apne_tilfeldig():

    if not settings["features"]["random"]:
        return

    window = nytt_vindu(
        "Tilfeldige tall",
        "380x420",
        (340, 400)
    )

    ramme = tk.Frame(
        window,
        bg=color("panel"),
        padx=18,
        pady=18
    )

    ramme.pack(fill="both", expand=True, padx=15, pady=15)

    antall_var = tk.StringVar(value="20")
    min_var = tk.StringVar(value="0")
    maks_var = tk.StringVar(value="100")
    heltall_var = tk.BooleanVar(value=True)
    auto_var = tk.BooleanVar(value=True)

    def felt(tekst, var):

        tk.Label(
            ramme,
            text=tekst,
            bg=color("panel"),
            fg=color("muted"),
            font=font(9)
        ).pack(anchor="w", pady=(8, 2))

        tk.Entry(
            ramme,
            textvariable=var,
            bg=color("panel_light"),
            fg=color("text"),
            insertbackground=color("text"),
            relief="flat",
            font=font(11)
        ).pack(fill="x", ipady=5)

    felt(f"Antall tall (1–{MAX_TALL})", antall_var)
    felt("Laveste verdi", min_var)
    felt("Høyeste verdi", maks_var)

    lag_sjekk(
        ramme,
        "Bare heltall",
        heltall_var,
        color("panel")
    ).pack(anchor="w", pady=(12, 0))

    lag_sjekk(
        ramme,
        "Sorter automatisk etterpå",
        auto_var,
        color("panel")
    ).pack(anchor="w")

    def generer():

        try:

            n = int(antall_var.get())
            lav = float(min_var.get().replace(",", "."))
            hoy = float(maks_var.get().replace(",", "."))

        except ValueError:

            messagebox.showerror(
                "Ugyldige verdier",
                "Kontroller antall og grenser.",
                parent=window
            )

            return

        if n < 1 or n > MAX_TALL:

            messagebox.showerror(
                "Ugyldig antall",
                f"Antall må være mellom 1 og {MAX_TALL}.",
                parent=window
            )

            return

        if lav > hoy:
            lav, hoy = hoy, lav

        if heltall_var.get():

            lav_i = math.ceil(lav)
            hoy_i = math.floor(hoy)

            if lav_i > hoy_i:

                messagebox.showerror(
                    "Ugyldig område",
                    "Det finnes ingen heltall i området.",
                    parent=window
                )

                return

            tall = [
                str(random.randint(lav_i, hoy_i))
                for _ in range(n)
            ]

        else:

            tall = [
                str(round(random.uniform(lav, hoy), 2))
                for _ in range(n)
            ]

        entry.delete(0, tk.END)
        entry.insert(0, " ".join(tall))

        status_var.set(f"Genererte {n} tilfeldige tall.")

        window.destroy()

        if auto_var.get():
            sorter_tall("stigende")

    lag_knapp(
        ramme,
        "Generer",
        generer,
        color("green")
    ).pack(fill="x", pady=(18, 0))

    window.bind("<Return>", lambda event: generer())


# ============================================================
# HISTORIKK
# ============================================================

def apne_historikk():

    if not settings["features"]["history"]:
        return

    window = nytt_vindu(
        "Historikk",
        "620x460",
        (480, 340)
    )

    tk.Label(
        window,
        text="TIDLIGERE INNDATA (dobbeltklikk for å laste inn)",
        bg=color("bg"),
        fg=color("text"),
        font=font(10, True)
    ).pack(anchor="w", padx=15, pady=(15, 8))

    ramme = tk.Frame(window, bg=color("panel"), padx=8, pady=8)
    ramme.pack(fill="both", expand=True, padx=15)

    liste = tk.Listbox(
        ramme,
        bg=color("panel_light"),
        fg=color("text"),
        selectbackground=color("accent"),
        relief="flat",
        font=font(9),
        activestyle="none"
    )

    rull = ttk.Scrollbar(ramme, command=liste.yview)
    liste.configure(yscrollcommand=rull.set)

    rull.pack(side="right", fill="y")
    liste.pack(side="left", fill="both", expand=True)

    def fyll():

        liste.delete(0, tk.END)

        for post in reversed(historikk):

            forkortet = post["tekst"]

            if len(forkortet) > 70:
                forkortet = forkortet[:67] + "..."

            liste.insert(tk.END, f"{post['tid']}   {forkortet}")

    def valgt_post():

        valg = liste.curselection()

        if not valg:
            return None

        return len(historikk) - 1 - valg[0]

    def last_inn(event=None):

        indeks = valgt_post()

        if indeks is None:
            return

        entry.delete(0, tk.END)
        entry.insert(0, historikk[indeks]["tekst"])

        status_var.set("Inndata lastet fra historikken.")

        window.destroy()

    def slett_valgt():

        indeks = valgt_post()

        if indeks is None:
            return

        del historikk[indeks]
        lagre_historikk()
        fyll()

    def tom_alt():

        if messagebox.askyesno(
            "Tøm historikk",
            "Vil du slette hele historikken?",
            parent=window
        ):

            historikk.clear()
            lagre_historikk()
            fyll()

    liste.bind("<Double-Button-1>", last_inn)

    knapper = tk.Frame(window, bg=color("bg"))
    knapper.pack(fill="x", padx=15, pady=15)

    lag_knapp(knapper, "Last inn", last_inn).pack(side="left")

    lag_knapp(
        knapper,
        "Slett valgt",
        slett_valgt,
        color("panel_light")
    ).pack(side="left", padx=8)

    lag_knapp(
        knapper,
        "Tøm alt",
        tom_alt,
        color("panel_light")
    ).pack(side="right")

    fyll()


# ============================================================
# HJELP OG OM
# ============================================================

HJELP_TEKST = [
    ("h1", "Velkommen til Tall Sorterer"),
    ("p", "Programmet sorterer tall og regner ut en rekke statistiske "
          "verdier. Alt vises i oversikten under tallfeltet.\n"),

    ("h2", "Slik bruker du programmet"),
    ("p", "1. Skriv inn tall i tallfeltet. Du kan skille dem med mellomrom, "
          "komma eller semikolon. Bruk punktum som desimaltegn.\n"
          "2. Trykk «Sorter stigende», «Sorter synkende» eller «Bland».\n"
          "3. Resultatene vises som kort, tabell, histogram og boksplott.\n"
          "4. Du kan kopiere eller eksportere resultatene som TXT eller CSV.\n"),

    ("h2", "Valg under tallfeltet"),
    ("p", "• Fjern duplikater: beholder bare ett eksemplar av hvert tall.\n"
          "• Avrund til heltall: runder alle tall til nærmeste heltall.\n"
          "• Filter fra/til: fjerner tall utenfor det området du velger.\n"),

    ("h2", "Statistikk forklart"),
    ("p", "• Gjennomsnitt: summen delt på antallet.\n"
          "• Median: midtverdien når tallene er sortert.\n"
          "• Typetall: tallet som forekommer oftest.\n"
          "• Kvartiler: Q1, Q2 (median) og Q3 deler dataene i fire deler.\n"
          "• IQR: Q3 minus Q1, bredden på de midterste 50 %.\n"
          "• Varians og standardavvik: hvor mye tallene varierer.\n"
          "• Utvalgsstandardavvik: bruker n−1 i stedet for n.\n"
          "• Standardfeil: utvalgsstandardavvik delt på √n.\n"
          "• Geometrisk og harmonisk snitt: krever at alle tall er positive.\n"
          "• Skjevhet: positiv betyr lang hale mot høye verdier.\n"
          "• Variasjonskoeffisient: standardavvik i prosent av snittet.\n"
          "• Persentiler: verdien under hvilken en gitt prosent av tallene ligger.\n"
          "• Uteliggere: verdier utenfor Q1 − 1,5·IQR og Q3 + 1,5·IQR.\n"),

    ("h2", "Verktøy"),
    ("p", "• Kalkulator: trygg regnemaskin med funksjoner og «ans».\n"
          "• Enhetsomregner: lengde, vekt, volum, tid, hastighet og temperatur.\n"
          "• Tilfeldige tall: lager en tallrekke for deg.\n"
          "• Importer: leser tall fra en tekst- eller CSV-fil.\n"
          "• Historikk: lagrer de siste inndataene dine.\n"),

    ("h2", "Hurtigtaster"),
    ("p", "Enter / Ctrl+Enter ........ Sorter stigende\n"
          "Ctrl+Shift+Enter ......... Sorter synkende\n"
          "Ctrl+B ................... Bland tallene\n"
          "Ctrl+L ................... Nullstill\n"
          "Ctrl+O ................... Importer fra fil\n"
          "Ctrl+S ................... Eksporter TXT\n"
          "Ctrl+Shift+C ............. Kopier resultater\n"
          "Ctrl+komma ............... Innstillinger\n"
          "Ctrl+ +  /  Ctrl+ − ...... Zoom inn / ut\n"
          "F1 ....................... Hjelp\n"
          "F2 ....................... Kalkulator\n"
          "F3 ....................... Tilfeldige tall\n"
          "F4 ....................... Historikk\n"
          "F5 ....................... Enhetsomregner\n"
          "F11 ...................... Fullskjerm\n"),

    ("h2", "Tips"),
    ("p", "• Du kan bytte tema under Vis → Tema.\n"
          "• Du kan skru av funksjoner du ikke trenger i innstillingene.\n"
          "• Programmet skjuler noen overraskelser. Prøv å skrive "
          "noen rare ting i tallfeltet, eller en gammel spillkode …\n")
]


def apne_hjelp():

    vindu = nytt_vindu(
        "Hjelp - Tall Sorterer",
        "760x680",
        (520, 400)
    )

    tekstfelt = tk.Text(
        vindu,
        wrap="word",
        bg=color("panel"),
        fg=color("text"),
        font=font(10),
        relief="flat",
        padx=18,
        pady=14
    )

    rull = ttk.Scrollbar(vindu, command=tekstfelt.yview)
    tekstfelt.configure(yscrollcommand=rull.set)

    rull.pack(side="right", fill="y")
    tekstfelt.pack(fill="both", expand=True)

    tekstfelt.tag_configure(
        "h1",
        font=font(15, True),
        foreground=color("accent"),
        spacing1=10,
        spacing3=6
    )

    tekstfelt.tag_configure(
        "h2",
        font=font(11, True),
        foreground=color("green"),
        spacing1=12,
        spacing3=4
    )

    tekstfelt.tag_configure("p", spacing3=4)

    for stil, tekst in HJELP_TEKST:
        tekstfelt.insert(tk.END, tekst + "\n", stil)

    tekstfelt.configure(state="disabled")


def vis_om():

    messagebox.showinfo(
        "Om Tall Sorterer",
        f"Tall Sorterer {VERSJON}\n\n"
        "Statistikk, analyse og tallbehandling.\n"
        "Laget med Python og Tkinter.\n\n"
        "Trykk F1 for hjelp."
    )


# ============================================================
# EASTER EGGS
# ============================================================

DISCO_FARGER = [
    "#FF006E", "#FB5607", "#FFBE0B", "#8338EC",
    "#3A86FF", "#06D6A0", "#EF476F", "#118AB2"
]


def vindu_lever(vindu):

    try:
        return bool(vindu.winfo_exists())

    except tk.TclError:
        return False


def animer(vindu, steg, intervall, antall):

    """Kjører en animasjon i et vindu og lukker det automatisk."""

    def loop(n=0):

        if not vindu_lever(vindu):
            return

        if n >= antall:
            vindu.destroy()
            return

        try:
            steg(n)

        except tk.TclError:
            return

        vindu.after(intervall, lambda: loop(n + 1))

    loop()


def lag_effektvindu(tittel, bredde, hoyde, bg="black"):

    vindu = tk.Toplevel(root)
    vindu.title(tittel)
    vindu.geometry(f"{bredde}x{hoyde}")
    vindu.configure(bg=bg)
    vindu.bind("<Escape>", lambda e: vindu.destroy())
    vindu.focus_force()

    return vindu


def egg_strobe():

    """Strobe med PETER ER EN IDIOT.

    Sakte blink (under 3 per sekund) og kort varighet, for å være
    skånsom mot personer som er følsomme for lysglimt.
    """

    vindu = tk.Toplevel(root)
    vindu.title("!!!")
    vindu.configure(bg="black")
    vindu.attributes("-topmost", True)

    try:
        vindu.attributes("-fullscreen", True)

    except tk.TclError:
        vindu.geometry(
            f"{root.winfo_screenwidth()}x"
            f"{root.winfo_screenheight()}+0+0"
        )

    flate = tk.Canvas(vindu, highlightthickness=0, bg="black")
    flate.pack(fill="both", expand=True)

    vindu.bind("<Escape>", lambda e: vindu.destroy())
    flate.bind("<Button-1>", lambda e: vindu.destroy())
    vindu.focus_force()

    def steg(n):

        paa = n % 2 == 0

        bakgrunn = "#E01010" if paa else "#101010"
        forgrunn = "#FFFFFF" if paa else "#FFE600"

        flate.configure(bg=bakgrunn)
        flate.delete("all")

        w = max(flate.winfo_width(), 400)
        h = max(flate.winfo_height(), 300)

        flate.create_text(
            w / 2, h / 2,
            text="PETER ER EN IDIOT",
            fill=forgrunn,
            font=(settings["font"], max(28, int(w / 16)), "bold"),
            width=w - 80,
            justify="center"
        )

        flate.create_text(
            w / 2, h - 40,
            text="Trykk ESC eller klikk for å lukke",
            fill=forgrunn,
            font=font(12)
        )

    animer(vindu, steg, 450, 14)


def egg_regnbue():

    vindu = lag_effektvindu("Tiril", 820, 320, "#0B0B12")

    flate = tk.Canvas(vindu, bg="#0B0B12", highlightthickness=0)
    flate.pack(fill="both", expand=True)

    tekst = "TIRIL KAN IKKE LESE"

    def steg(n):

        flate.delete("all")

        w = max(flate.winfo_width(), 600)
        h = max(flate.winfo_height(), 250)

        avstand = min(40, (w - 40) / len(tekst))
        start = (w - avstand * (len(tekst) - 1)) / 2

        for i, bokstav in enumerate(tekst):

            if bokstav == " ":
                continue

            y = h / 2 + math.sin(n * 0.25 + i * 0.5) * 35

            r, g, b = colorsys.hsv_to_rgb(
                (n * 0.02 + i / len(tekst)) % 1,
                0.8,
                1
            )

            farge = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

            flate.create_text(
                start + i * avstand, y,
                text=bokstav,
                fill=farge,
                font=(settings["font"], int(avstand * 0.9), "bold")
            )

        flate.create_text(
            w / 2, h - 25,
            text="(ESC for å lukke)",
            fill="#888888",
            font=font(9)
        )

    animer(vindu, steg, 50, 160)


def egg_konfetti():

    vindu = lag_effektvindu("Johan-Olai", 800, 520, "#101426")

    flate = tk.Canvas(vindu, bg="#101426", highlightthickness=0)
    flate.pack(fill="both", expand=True)

    farger = [
        "#FFD700", "#FF6B6B", "#4ECDC4", "#6C8CFF",
        "#FF9F1C", "#C77DFF", "#55D6A7"
    ]

    deler = [
        {
            "x": random.uniform(0, 800),
            "y": random.uniform(-500, 0),
            "vx": random.uniform(-1.5, 1.5),
            "vy": random.uniform(2, 6),
            "f": random.choice(farger),
            "s": random.randint(5, 11)
        }
        for _ in range(140)
    ]

    def steg(n):

        flate.delete("all")

        w = max(flate.winfo_width(), 600)
        h = max(flate.winfo_height(), 400)

        for d in deler:

            d["x"] += d["vx"]
            d["y"] += d["vy"]

            if d["y"] > h:
                d["y"] = random.uniform(-40, 0)
                d["x"] = random.uniform(0, w)

            flate.create_rectangle(
                d["x"], d["y"],
                d["x"] + d["s"], d["y"] + d["s"] * 0.6,
                fill=d["f"],
                outline=""
            )

        puls = 1 + 0.08 * math.sin(n * 0.2)

        flate.create_text(
            w / 2, h / 2 - 20,
            text="JOHAN-OLAI ER SMART",
            fill="#FFD700",
            font=(settings["font"], int(w / 20 * puls), "bold")
        )

        flate.create_text(
            w / 2, h / 2 + 50,
            text="IQ: 999+   ★ ★ ★",
            fill="white",
            font=font(18, True)
        )

    animer(vindu, steg, 33, 270)


def egg_matrix():

    vindu = lag_effektvindu("Matrix", 800, 520)

    flate = tk.Canvas(vindu, bg="black", highlightthickness=0)
    flate.pack(fill="both", expand=True)

    tegn = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&"
    kolonner = 50
    hoder = [random.randint(-30, 0) for _ in range(kolonner)]
    spor = []
    rad_hoyde = 18

    def steg(n):

        w = max(flate.winfo_width(), 600)
        h = max(flate.winfo_height(), 400)

        celle = w / kolonner

        nye = []

        for id_, alder in spor:

            if alder >= 14:
                flate.delete(id_)

            else:
                niva = max(40, 255 - alder * 18)
                flate.itemconfigure(id_, fill=f"#00{niva:02x}00")
                nye.append((id_, alder + 1))

        spor[:] = nye

        for k in range(kolonner):

            hoder[k] += 1

            if hoder[k] * rad_hoyde > h and random.random() > 0.9:
                hoder[k] = 0

            if 0 <= hoder[k] * rad_hoyde <= h + rad_hoyde:

                id_ = flate.create_text(
                    k * celle + celle / 2,
                    hoder[k] * rad_hoyde,
                    text=random.choice(tegn),
                    fill="#CCFFCC",
                    font=("Courier", 12, "bold")
                )

                spor.append((id_, 0))

    animer(vindu, steg, 60, 200)


def egg_disco():

    vindu = lag_effektvindu("Disco", 700, 420, "#000000")

    tk.Label(
        vindu,
        text="D I S C O !",
        bg="black",
        fg="white",
        font=font(20, True)
    ).pack(pady=8)

    rutenett = tk.Frame(vindu, bg="black")
    rutenett.pack(fill="both", expand=True, padx=8, pady=8)

    celler = []

    for r in range(6):

        rutenett.rowconfigure(r, weight=1)

        for c in range(10):

            rutenett.columnconfigure(c, weight=1)

            celle = tk.Label(rutenett, bg="#222222")
            celle.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
            celler.append(celle)

    def steg(n):

        # Bare noen få ruter endres om gangen (ingen full-skjerm-blink)

        for _ in range(8):
            random.choice(celler).configure(
                bg=random.choice(DISCO_FARGER)
            )

    animer(vindu, steg, 250, 48)



def egg_generell_animasjon(frase, tittel, beskrivelse):
    """Viser en animasjon med motiv som passer til den aktuelle hemmeligheten."""
    vindu = lag_effektvindu(f"Easter egg: {tittel}", 800, 540, "#071426")
    flate = tk.Canvas(vindu, bg="#071426", highlightthickness=0)
    flate.pack(fill="both", expand=True)

    tekst = (frase + " " + tittel + " " + beskrivelse).upper()

    # Velg en konkret scene ut fra temaet. Rekkefølgen er viktig for å unngå
    # at generelle ord (som «historie») overstyrer mer presise hendelser.
    scener = [
        (("MÅNELANDING", "APOLLO 11", "ROMKAPPLØPET", "APOLLO 13", "HUBBLE", "JAMES WEBB", "MARSROVER"), "space"),
        (("BERLINMUREN", "JERNTEPPET", "KALDE KRIGEN", "JERNTEPPET"), "wall"),
        (("FRANSKE REVOLUSJON", "BASTILLEN"), "revolution"),
        (("22 JULI", "TERRORANGREP", "9 11", "SEPTEMBER 2001", "ANDRE VERDENSKRIG", "D-DAGEN"), "memorial"),
        (("VIKING", "NANSEN", "AMUNDSEN", "SVALBARD", "POLAR"), "explorer"),
        (("SVARTEDAUDEN", "PEST", "PANDEMI", "COVID", "VAKSIN", "PENICILLIN", "HELSE"), "health"),
        (("KLIMA", "BÆREKRAFT", "FORNYBAR", "ENERGI", "ELEKTRISK BIL", "PARISAVTALEN", "TSJERNOBYL"), "climate"),
        (("SAMETING", "SAMEFOLK", "ALTAKONFLIKT", "SÁMI", "SAME"), "sami"),
        (("DEMOKRATI", "YTRINGSFRIHET", "EIDSVOLL", "MAGNA CARTA", "KVINNEBEVEG", "KVINNERS STEMMERETT", "STONEWALL", "RETTIGHET", "NOBELS FREDSPRIS", "NATO", "UKRAINA", "BREXIT", "UNIONSOPPLØSNINGEN", "NELSON MANDELA", "APARTHEID", "FN"), "civic"),
        (("CHATGPT", "KUNSTIG INTELLIGENS", "KI I", "DEEPFAKE", "ALGORITM", "KVANTEDATAMASKIN"), "ai"),
        (("INTERNETT", "WORLD WIDE WEB", "NETTVETT", "DIGITALT FOTSPOR", "PERSONVERN", "CYBERSIKKERHET", "PASSORD", "TOFAKTOR", "SOSIALE MEDIER", "FAKE NEWS", "KILDEKRITIKK"), "network"),
        (("DNA", "GENREDIGERING", "GENOM", "CRISPR"), "dna"),
        (("PYTHON", "LINUX", "OPEN SOURCE", "TRANSISTOR", "BINÆR", "NULL OG EN", "GUTENBERG"), "computing"),
        (("OL 1994", "PARIS 2024", "EUROPA 2024", "SPORT"), "sport"),
        (("HENRIK IBSEN", "EDVARD MUNCH", "RENESSANS", "MUSIKK", "DISCO"), "arts"),
        (("OLJEFUNN", "INDUSTRI", "ARBEIDER", "8 TIMERS", "JERNBAN", "FLY", "RADIO", "FJERNSYN", "MOBILTELEFON", "SMARTTELEFON"), "industry"),
        (("EUROEN", "VALUTA", "ØKONOMI"), "economy"),
    ]
    scene = "milestone"
    for nøkkelord, scene_navn in scener:
        if any(ord in tekst for ord in nøkkelord):
            scene = scene_navn
            break

    fargekart = {
        "space": ("#071426", "#8ED8FF", "#F7D774"),
        "wall": ("#171827", "#B9C4D0", "#F2C14E"),
        "revolution": ("#21151A", "#F04B55", "#F4D35E"),
        "memorial": ("#101B2B", "#D9E2F2", "#F5C76B"),
        "explorer": ("#102333", "#A8DADC", "#F1FAEE"),
        "health": ("#102A2A", "#72D6C9", "#F1FAEE"),
        "climate": ("#092A25", "#69D18B", "#F4D35E"),
        "sami": ("#14243A", "#E85D75", "#F4D35E"),
        "civic": ("#1B2035", "#8FB8ED", "#F4D35E"),
        "ai": ("#10162D", "#9B8CFF", "#55E6D0"),
        "network": ("#071D2B", "#45C4E8", "#A4F4D2"),
        "dna": ("#10202E", "#7DE2D1", "#E5B8F4"),
        "computing": ("#071A13", "#65E572", "#D8FF9A"),
        "sport": ("#10251C", "#F4D35E", "#F7FFF7"),
        "arts": ("#24182D", "#E0A5CF", "#F4D35E"),
        "industry": ("#22232A", "#F0A35E", "#D5DEE8"),
        "economy": ("#17291F", "#77D69B", "#F4D35E"),
        "milestone": ("#101522", "#6C8CFF", "#55D6A7"),
    }
    bg, aksent, lys = fargekart[scene]
    flate.configure(bg=bg)

    stjerner = [(random.random(), random.random(), random.uniform(1, 2.7)) for _ in range(65)]
    partikler = [{"x": random.random(), "y": random.random(),
                  "v": random.uniform(0.002, 0.008), "r": random.randint(2, 5)}
                 for _ in range(24)]

    def scene_tegn(n, w, h):
        cx, cy = w * .5, h * .43
        puls = 1 + .035 * math.sin(n * .10)
        # Diskré bakgrunnsstjerner/partikler – motivet er det sentrale.
        for x, y, r in stjerner:
            flate.create_oval(x*w-r, y*h-r, x*w+r, y*h+r, fill="#DCEBFF", outline="")

        if scene == "space":
            # Månelandskap, jordklode, stjerner og rakett som stiger.
            flate.create_oval(w*.68, h*.12, w*.86, h*.30, fill="#28618A", outline="#9AD9FF", width=2)
            flate.create_arc(w*.68, h*.12, w*.86, h*.30, start=75, extent=180, style="arc", outline="#D8F4FF", width=3)
            flate.create_oval(w*.08, h*.64, w*.92, h*1.12, fill="#A7A9B2", outline="#E7E8ED", width=2)
            for i in range(12):
                x = w*(.12 + i*.065); y = h*(.78 + .04*math.sin(i*2))
                flate.create_oval(x-5, y-3, x+5, y+3, fill="#777D89", outline="")
            ry = h*(.62 - (n % 90)/170)
            rx = w*.48
            flate.create_polygon(rx, ry-42, rx-17, ry+18, rx+17, ry+18, fill="#F1F4F8", outline=aksent, width=2)
            flate.create_polygon(rx-17, ry+5, rx-30, ry+25, rx-14, ry+20, fill="#E45B45", outline="")
            flate.create_polygon(rx+17, ry+5, rx+30, ry+25, rx+14, ry+20, fill="#E45B45", outline="")
            flate.create_oval(rx-6, ry-18, rx+6, ry-6, fill="#5AA9E6", outline="")
            flate.create_polygon(rx-8, ry+18, rx+8, ry+18, rx, ry+48+random.randint(0, 12), fill="#FFB347", outline="")
            flate.create_text(w*.22, h*.24, text="✦  APOLLO  ✦", fill=lys, font=("Arial", 15, "bold"))
        elif scene == "wall":
            # Betongmur som åpner seg, med frihetsflagg.
            gap = 20 + (1 + math.sin(n*.07))*70
            for side in (0, 1):
                x1 = w*(.12 if side == 0 else .56) + (-gap/2 if side == 0 else gap/2)
                x2 = x1 + w*.28
                flate.create_rectangle(x1, h*.30, x2, h*.72, fill="#858B98", outline="#D2D7DF", width=2)
                for yy in range(4):
                    for xx in range(3):
                        bx=x1+xx*(x2-x1)/3; by=h*.32+yy*h*.095
                        flate.create_rectangle(bx,by,bx+(x2-x1)/3-2,by+h*.085,outline="#555D6A")
            flate.create_smooth_line if False else None
            flate.create_oval(cx-15, h*.24-15, cx+15, h*.24+15, fill=lys, outline="")
            flate.create_line(cx, h*.25, cx, h*.48, fill=lys, width=4)
            flate.create_line(cx, h*.31, cx+42, h*.25, fill=aksent, width=3)
            flate.create_text(cx, h*.18, text="FRIHET", fill="#FFFFFF", font=("Arial", 18, "bold"))
        elif scene == "revolution":
            # Bastillen som silhuett, flagg og pulserende soloppgang.
            flate.create_rectangle(w*.25,h*.39,w*.75,h*.72,fill="#55515B",outline="#D5C3B0",width=2)
            for x in (.31,.44,.57,.70):
                flate.create_rectangle(w*x,h*.30,w*(x+.07),h*.43,fill="#77717B",outline="#D5C3B0")
            flate.create_line(cx,h*.29,cx,h*.12,fill=lys,width=3)
            flate.create_polygon(cx,h*.13,cx+70,h*.16,cx,h*.22,fill=aksent,outline="")
            flate.create_text(cx,h*.79,text="LIBERTÉ  •  ÉGALITÉ  •  FRATERNITÉ",fill="#FFFFFF",font=("Arial",13,"bold"))
        elif scene == "memorial":
            # Rolig minneslys og due – uten dramatiske eller grafiske elementer.
            flate.create_oval(cx-90,h*.27,cx+90,h*.65,outline="#52647E",width=2)
            flate.create_rectangle(cx-24,h*.53,cx+24,h*.70,fill="#D9E2F2",outline="")
            flate.create_polygon(cx-15,h*.53,cx,h*.38+8*math.sin(n*.12),cx+15,h*.53,fill="#F5C76B",outline="")
            flate.create_oval(cx-7,h*.46,cx+7,h*.55,fill="#FFF4C2",outline="")
            flate.create_oval(cx+65,h*.28,cx+115,h*.32,fill="#E7EEF8",outline="")
            flate.create_polygon(cx+75,h*.30,cx+45,h*.22,cx+60,h*.34,cx+35,h*.39,cx+86,h*.34,fill="#E7EEF8",outline="")
            flate.create_text(cx,h*.78,text="MINNE  •  DEMOKRATI  •  FELLESSKAP",fill="#E7EEF8",font=("Arial",13,"bold"))
        elif scene == "explorer":
            # Fjell, snø, ekspedisjonsflagg og en vandrende polfarer.
            flate.create_polygon(0,h*.72,w*.25,h*.25,w*.48,h*.72,fill="#607E91",outline="#C7E5F2")
            flate.create_polygon(w*.35,h*.72,w*.68,h*.18,w,h*.72,fill="#7896A8",outline="#DDF5FF")
            flate.create_polygon(w*.25,h*.25,w*.20,h*.38,w*.30,h*.36,fill="#F4FAFF",outline="")
            flate.create_polygon(w*.68,h*.18,w*.60,h*.34,w*.74,h*.32,fill="#F4FAFF",outline="")
            px=w*(.46+.05*math.sin(n*.08)); py=h*.57
            flate.create_oval(px-8,py-27,px+8,py-11,fill="#E8C7A0",outline="")
            flate.create_line(px,py-10,px,py+25,fill="#26384A",width=9)
            flate.create_line(px,py,px-13,py+17,fill="#26384A",width=4); flate.create_line(px,py,px+13,py+17,fill="#26384A",width=4)
            flate.create_line(px+5,py-7,px+27,py-30,fill=lys,width=2)
            flate.create_polygon(px+27,py-30,px+52,py-25,px+27,py-18,fill=aksent,outline="")
        elif scene == "health":
            # Pulsende medisinsk symbol, beskyttende skjold og viruspartikler.
            rr=65*puls
            flate.create_oval(cx-rr,cy-rr,cx+rr,cy+rr,outline=aksent,width=4)
            flate.create_rectangle(cx-13,cy-42,cx+13,cy+42,fill="#F5F8FC",outline="")
            flate.create_rectangle(cx-42,cy-13,cx+42,cy+13,fill="#F5F8FC",outline="")
            for i in range(12):
                a=i*math.tau/12+n*.018; x=cx+math.cos(a)*130; y=cy+math.sin(a)*90
                flate.create_oval(x-7,y-7,x+7,y+7,fill=lys,outline=aksent,width=1)
        elif scene == "climate":
            # Jordklode, blad og sol som beveger seg langs horisonten.
            r=100*puls
            flate.create_oval(cx-r,cy-r,cx+r,cy+r,fill="#236C78",outline="#9CE7D6",width=3)
            flate.create_arc(cx-r,cy-r,cx+r,cy+r,start=30+n%360,extent=115,style="arc",outline="#8DE0A6",width=5)
            flate.create_arc(cx-r*.7,cy-r*.7,cx+r*.7,cy+r*.7,start=190-n%360,extent=100,style="arc",outline="#8DE0A6",width=4)
            flate.create_oval(cx+95,cy-115,cx+145,cy-65,fill="#F4D35E",outline="")
            flate.create_oval(cx-35,cy-10,cx+35,cy+35,fill="#5DBB79",outline="")
            flate.create_line(cx,cy+28,cx+30,cy-8,fill="#D9FFE2",width=3)
            flate.create_text(cx,h*.75,text="JORDEN VÅR – FELLES ANSVAR",fill="#E7FFF1",font=("Arial",13,"bold"))
        elif scene == "sami":
            # Samisk-inspirert fargebånd og nordlys over fjell.
            for i,col in enumerate(("#2D6CDF","#E83E55","#F4D35E","#2D6CDF")):
                y=h*(.28+i*.09)+12*math.sin(n*.06+i)
                flate.create_arc(cx-190,y-85,cx+190,y+85,start=15,extent=150,style="arc",outline=col,width=13)
            flate.create_polygon(0,h*.74,w*.28,h*.43,w*.48,h*.74,fill="#263F58",outline="#8EB7C9")
            flate.create_polygon(w*.42,h*.74,w*.72,h*.36,w,h*.74,fill="#304B62",outline="#8EB7C9")
            flate.create_text(cx,h*.79,text="ÁRBEVIERRU  •  SPRÅK  •  KULTUR",fill="#FFFFFF",font=("Arial",13,"bold"))
        elif scene == "civic":
            # Stemmeseddel som glir ned i urne, med søyler som symboliserer institusjoner.
            flate.create_rectangle(cx-100,h*.43,cx+100,h*.70,fill="#34445F",outline="#C7D8F0",width=3)
            flate.create_polygon(cx-25,h*.43,cx+25,h*.43,cx+12,h*.49,cx-12,h*.49,fill=bg,outline="#DDE9F8")
            sy=h*(.22+(n%70)/220)
            flate.create_rectangle(cx-18,sy,cx+18,sy+48,fill="#FFFFFF",outline=aksent,width=2)
            flate.create_line(cx-8,sy+22,cx-1,sy+30,cx+11,sy+12,fill="#3A9D75",width=3)
            for x in (cx-155,cx+155):
                flate.create_rectangle(x-12,h*.30,x+12,h*.70,fill="#8FA8C8",outline="")
                flate.create_polygon(x-25,h*.30,x,h*.23,x+25,h*.30,fill=lys,outline="")
            flate.create_text(cx,h*.79,text="DELTAKELSE  •  RETTIGHETER  •  ANSVAR",fill="#FFFFFF",font=("Arial",12,"bold"))
        elif scene == "ai":
            # Nevralnett med lysende noder og forbindelser.
            layers=[(w*.25,3),(w*.43,4),(w*.62,4),(w*.79,2)]
            nodes=[]
            for li,(x,count) in enumerate(layers):
                for j in range(count):
                    y=h*(.30+j*.12+(li%2)*.035)+math.sin(n*.06+j+li)*7
                    nodes.append((x,y))
            for i,a in enumerate(nodes):
                for b in nodes[i+1:]:
                    if b[0]>a[0] and b[0]-a[0]<w*.23:
                        flate.create_line(a[0],a[1],b[0],b[1],fill="#414B83",width=1)
            for i,(x,y) in enumerate(nodes):
                rr=8+3*math.sin(n*.12+i)
                flate.create_oval(x-rr,y-rr,x+rr,y+rr,fill=aksent,outline=lys,width=2)
            flate.create_text(cx,h*.73,text="DATA  →  MODELL  →  SVAR",fill="#FFFFFF",font=("Arial",15,"bold"))
        elif scene == "network":
            # Nettverkspunkter sender en lysende datapuls mellom seg.
            nodes=[(w*.25,h*.34),(w*.48,h*.25),(w*.72,h*.35),(w*.32,h*.62),(w*.60,h*.66),(w*.82,h*.58)]
            for i,a in enumerate(nodes):
                for b in nodes[i+1:]:
                    if abs(a[0]-b[0])<w*.4:
                        flate.create_line(*a,*b,fill="#28647D",width=2)
            for i,(x,y) in enumerate(nodes):
                flate.create_oval(x-17,y-17,x+17,y+17,fill="#123D55",outline=aksent,width=3)
                flate.create_text(x,y,text="↔",fill=lys,font=("Arial",16,"bold"))
            pulse_x=w*(.18+((n%100)/100)*.65)
            flate.create_oval(pulse_x-7,cy-7,pulse_x+7,cy+7,fill="#FFFFFF",outline=aksent,width=2)
            flate.create_text(cx,h*.78,text="KOBLET SAMMEN",fill="#FFFFFF",font=("Arial",15,"bold"))
        elif scene == "dna":
            # Dobbelheliks som beveger seg oppover.
            for i in range(22):
                y=h*(.20+i*.025)
                x1=cx+75*math.sin(i*.48+n*.10); x2=cx-75*math.sin(i*.48+n*.10)
                flate.create_line(x1,y,x2,y,fill="#A5C8D8",width=2)
                flate.create_oval(x1-5,y-5,x1+5,y+5,fill=aksent,outline="")
                flate.create_oval(x2-5,y-5,x2+5,y+5,fill=lys,outline="")
            flate.create_text(cx,h*.78,text="GENETISK INFORMASJON",fill="#FFFFFF",font=("Arial",14,"bold"))
        elif scene == "computing":
            # Terminalvindu, binære tegn og en blinkende markør.
            flate.create_rectangle(w*.20,h*.24,w*.80,h*.70,fill="#07100C",outline=aksent,width=3)
            flate.create_rectangle(w*.20,h*.24,w*.80,h*.32,fill="#183B27",outline="")
            flate.create_text(w*.24,h*.28,text="●  ●  ●",fill=lys,font=("Arial",10,"bold"))
            for row in range(5):
                bits=" ".join(random.choice(("0","1")) for _ in range(18))
                flate.create_text(w*.25,h*(.38+row*.055),text=bits,anchor="w",fill=aksent,font=("Consolas",13))
            if n%2==0:
                flate.create_rectangle(w*.25,h*.68,w*.27,h*.70,fill="#FFFFFF",outline="")
        elif scene == "sport":
            # Ball i bevegelse mot mål / målstrek.
            flate.create_line(w*.18,h*.67,w*.82,h*.67,fill="#E7F3E9",width=4)
            flate.create_rectangle(w*.68,h*.37,w*.84,h*.67,outline="#FFFFFF",width=4)
            bx=w*(.25+(.42*((n%80)/80))); by=h*(.54-.12*math.sin((n%80)/80*math.pi))
            flate.create_oval(bx-22,by-22,bx+22,by+22,fill="#F7F7F7",outline="#263238",width=3)
            for a in range(5):
                aa=a*math.tau/5
                flate.create_oval(bx+math.cos(aa)*10-4,by+math.sin(aa)*10-4,bx+math.cos(aa)*10+4,by+math.sin(aa)*10+4,fill="#263238",outline="")
            flate.create_text(cx,h*.79,text="SAMHOLD  •  INNSATS  •  IDRETT",fill="#FFFFFF",font=("Arial",13,"bold"))
        elif scene == "arts":
            # Penselstrøk og noter som beveger seg over et lerret.
            flate.create_rectangle(w*.25,h*.25,w*.75,h*.67,fill="#33243B",outline="#E7C4E2",width=3)
            for i in range(7):
                x=w*(.32+i*.055); y=h*(.38+.13*math.sin(i+n*.07))
                flate.create_oval(x-13,y-13,x+13,y+13,fill=random.choice((aksent,lys,"#7EC8E3")),outline="")
            for i in range(3):
                x=w*(.40+i*.10); y=h*(.75+math.sin(n*.08+i)*8)
                flate.create_text(x,y,text="♫",fill=lys,font=("Arial",25,"bold"))
        elif scene == "industry":
            # Fabrikkhjul og damp – industri, transport og massemedier.
            flate.create_rectangle(w*.22,h*.47,w*.78,h*.72,fill="#424A55",outline="#C7D0DA",width=2)
            flate.create_polygon(w*.22,h*.47,w*.35,h*.35,w*.43,h*.47,w*.55,h*.34,w*.66,h*.47,fill="#596574",outline="#D5DEE8")
            for x in (w*.34,w*.51,w*.68):
                flate.create_rectangle(x-13,h*.22,x+13,h*.47,fill="#697684",outline="")
                puff_y=h*(.17-.03*math.sin(n*.1+x))
                flate.create_oval(x-20,puff_y-12,x+20,puff_y+12,outline="#C7D0DA",width=2)
            for x in (w*.38,w*.62):
                rr=24+4*math.sin(n*.12)
                flate.create_oval(x-rr,h*.58-rr,x+rr,h*.58+rr,outline=lys,width=4)
                flate.create_oval(x-5,h*.58-5,x+5,h*.58+5,fill=aksent,outline="")
        elif scene == "economy":
            # Mynt og stigende søylegraf – økonomi og felles valuta.
            for i,hh in enumerate((.18,.30,.42,.55,.68)):
                x=w*(.25+i*.11); top=h*(.70-hh*.45)
                flate.create_rectangle(x,h*.70,x+38,top,fill=aksent,outline=lys,width=1)
            rr=53+4*math.sin(n*.1)
            flate.create_oval(cx-rr,h*.18,cx+rr,h*.18+2*rr,fill="#D8B85B",outline="#FFF0A6",width=3)
            flate.create_text(cx,h*.18+rr,text="€",fill="#70551C",font=("Arial",42,"bold"))
        else:
            # Egen milepæl-scene: tidslinje, historisk årstall og bevegelig markør.
            flate.create_line(w*.18,h*.52,w*.82,h*.52,fill=aksent,width=5)
            for i in range(7):
                x=w*(.20+i*.10)
                flate.create_line(x,h*.48,x,h*.56,fill=lys,width=2)
                flate.create_oval(x-7,h*.52-7,x+7,h*.52+7,fill=lys,outline="")
            x=w*(.20+((n%120)/120)*.60)
            flate.create_oval(x-17,h*.52-17,x+17,h*.52+17,fill=aksent,outline="#FFFFFF",width=3)
            flate.create_text(cx,h*.30,text="EN VIKTIG MILEPÆL",fill="#FFFFFF",font=("Arial",18,"bold"))

    def steg(n):
        flate.delete("all")
        w=max(flate.winfo_width(),600); h=max(flate.winfo_height(),400)
        scene_tegn(n,w,h)
        flate.create_text(w/2,h*.86,text=tittel.upper(),fill="#FFFFFF",
                          font=(settings["font"],19,"bold"),width=w-50)
        flate.create_text(w/2,h*.92,text=beskrivelse,fill="#D0D9E8",
                          font=font(9),width=w-70,justify="center")
        flate.create_text(w/2,h-12,text="ESC for å lukke  •  Hemmelig frase: "+frase,
                          fill="#93A3B8",font=font(8))

    animer(vindu, steg, 65, 220)


# ============================================================
# EASTER EGGS – 100 HEMMELIGHETER + PROGRESJON
# ============================================================

EASTER_EGG_FILE = "tall_sorterer_easter_eggs.json"

# Phrase, title and short historical/social context.
# The first five preserve the original animated Easter eggs.
EASTER_EGG_DATA = [
    ("PETER ER DUM", "Peter", "En klassisk intern internett-spøk. Denne er med for tradisjonens skyld."),
    ("TIRIL KAN IKKE LESE", "Tiril i regnbue", "En fargerik, sprettende hyllest til leseglede – med et lite glimt i øyet."),
    ("JOHAN-OLAI ER SMART", "Johan-Olai", "En konfettifeiring av nysgjerrighet, læring og gode ideer."),
    ("MATRIX", "The Matrix", "Filmen The Matrix fra 1999 gjorde spørsmålet om simulert virkelighet til et kjent popkulturelt tema."),
    ("DISCO", "Disco", "Discomusikken preget dansegulv verden over på 1970-tallet."),
    ("MÅNELANDINGEN", "Månelandingen 1969", "Apollo 11 landet på månen 20. juli 1969. Neil Armstrong og Buzz Aldrin gikk på månens overflate."),
    ("BERLINMUREN", "Berlinmurens fall", "Berlinmuren åpnet 9. november 1989 og ble et sterkt symbol på slutten av den kalde krigen."),
    ("DEN KALDE KRIGEN", "Den kalde krigen", "Etter andre verdenskrig preget rivaliseringen mellom USA og Sovjetunionen internasjonal politikk i flere tiår."),
    ("INTERNETT", "Internett", "Internett utviklet seg fra forskningsnettverk til en global infrastruktur for kommunikasjon og informasjon."),
    ("KUNSTIG INTELLIGENS", "Kunstig intelligens", "KI brukes blant annet til språk, bildeanalyse, forskning og automatisering – og reiser viktige spørsmål om ansvar."),
    ("SOSIALE MEDIER", "Sosiale medier", "Sosiale medier har endret hvordan mennesker deler informasjon, bygger fellesskap og møter nyheter."),
    ("FAKE NEWS", "Desinformasjon", "Feilinformasjon og bevisst desinformasjon gjør kildekritikk viktigere enn noen gang."),
    ("KILDEKRITIKK", "Kildekritikk", "Sjekk hvem som står bak en påstand, hva dokumentasjonen er, og om flere uavhengige kilder bekrefter den."),
    ("KLIMAENDRINGER", "Klimaendringer", "Menneskeskapte utslipp av klimagasser bidrar til global oppvarming. Forskning og internasjonalt samarbeid står sentralt."),
    ("PARISAVTALEN", "Parisavtalen 2015", "Parisavtalen ble vedtatt i 2015 og har som mål å begrense den globale temperaturøkningen."),
    ("BÆREKRAFT", "Bærekraftig utvikling", "Bærekraft handler om å dekke dagens behov uten å ødelegge mulighetene for kommende generasjoner."),
    ("DEN INDUSTRIELLE REVOLUSJON", "Den industrielle revolusjon", "Industrialiseringen startet i Storbritannia på 1700-tallet og endret produksjon, arbeid og byliv."),
    ("TRYKKPRESSE", "Boktrykkerkunsten", "Johannes Gutenbergs trykketeknologi på 1400-tallet bidro til at bøker og ideer kunne spres i større omfang."),
    ("DEN FRANSKE REVOLUSJON", "Den franske revolusjon", "Revolusjonen startet i 1789 og utfordret enevelde og privilegiesamfunn med krav om frihet og politisk representasjon."),
    ("GRUNNLOVEN", "Norges grunnlov 1814", "Norges grunnlov ble vedtatt på Eidsvoll 17. mai 1814."),
    ("UNIONSOPPLØSNINGEN", "Unionsoppløsningen 1905", "Unionen mellom Norge og Sverige ble oppløst i 1905 etter en politisk prosess."),
    ("KVINNERS STEMMERETT", "Kvinners stemmerett", "Norge innførte allmenn stemmerett for kvinner ved stortingsvalg i 1913."),
    ("MENNESKERETTIGHETER", "Menneskerettighetene", "FNs verdenserklæring om menneskerettighetene ble vedtatt 10. desember 1948."),
    ("FN", "De forente nasjoner", "FN ble opprettet i 1945 for å fremme internasjonalt samarbeid, fred og sikkerhet."),
    ("ANDRE VERDENSKRIG", "Andre verdenskrig", "Andre verdenskrig varte fra 1939 til 1945 og fikk enorme konsekvenser for mennesker og samfunn."),
    ("D-DAGEN", "D-dagen 1944", "Den 6. juni 1944 gikk allierte styrker i land i Normandie i en stor operasjon under andre verdenskrig."),
    ("ROSA PARKS", "Rosa Parks", "Rosa Parks ble et viktig symbol i den amerikanske borgerrettighetsbevegelsen etter at hun nektet å gi fra seg bussetet sitt i 1955."),
    ("NELSON MANDELA", "Nelson Mandela", "Nelson Mandela ble Sør-Afrikas første svarte president i 1994 etter apartheidregimets fall."),
    ("APARTHEID", "Apartheid", "Apartheid var et system for institusjonalisert raseskille i Sør-Afrika, avskaffet gjennom en politisk overgang tidlig på 1990-tallet."),
    ("BORGERRETTIGHETER", "Borgerrettighetsbevegelsen", "Borgerrettighetsbevegelsen i USA arbeidet mot rasesegregering og diskriminering, særlig på 1950- og 1960-tallet."),
    ("TSJERNOBYL", "Tsjernobyl 1986", "Kjernekraftulykken i Tsjernobyl skjedde 26. april 1986 og fikk omfattende miljømessige og samfunnsmessige følger."),
    ("COVID 19", "Pandemien 2020", "COVID-19-pandemien førte til store endringer i helsevesen, skole, arbeidsliv og internasjonal reisevirksomhet."),
    ("VAKSINER", "Vaksinehistorie", "Vaksiner har forebygget alvorlig sykdom og vært avgjørende i kampen mot flere smittsomme sykdommer."),
    ("DNA", "DNA", "Oppdagelsen av DNA-strukturens dobbelheliks i 1953 ble et viktig vendepunkt i moderne biologi."),
    ("PENICILLIN", "Penicillin", "Alexander Fleming oppdaget penicillin i 1928. Antibiotika endret behandlingen av bakterielle infeksjoner."),
    ("TRANSISTOREN", "Transistoren", "Transistoren ble utviklet i 1947 og gjorde moderne elektronikk og datateknologi mulig i stadig mindre format."),
    ("WORLD WIDE WEB", "World Wide Web", "Tim Berners-Lee foreslo World Wide Web i 1989. Nettet gjorde det enklere å dele informasjon via lenker og nettsider."),
    ("SMARTTELEFON", "Smarttelefonen", "Smarttelefonen samlet kamera, kommunikasjon, kart og dataverktøy i én enhet og endret hverdagslivet."),
    ("ROMKAPPLØPET", "Romkappløpet", "Romkappløpet mellom USA og Sovjetunionen førte til store teknologiske fremskritt og kulminerte blant annet med Apollo 11."),
    ("HENRIK IBSEN", "Henrik Ibsen", "Henrik Ibsen er en av verdens mest spilte dramatikere. Et dukkehjem hadde premiere i 1879."),
    ("EDVARD MUNCH", "Edvard Munch", "Edvard Munchs Skrik fra 1893 er et av de mest kjente verkene i norsk kunsthistorie."),
    ("OL 1994", "Lillehammer-OL 1994", "Vinter-OL på Lillehammer i 1994 ble et stort norsk idretts- og kulturarrangement."),
    ("SAMETINGET", "Sametinget", "Sametinget i Norge åpnet i 1989 og er et folkevalgt organ for samene."),
    ("SAMEFOLKETS DAG", "Samenes nasjonaldag", "Samenes nasjonaldag feires 6. februar og markerer det første samiske landsmøtet i Trondheim i 1917."),
    ("ALTAKONFLIKTEN", "Alta-konflikten", "Alta-konflikten på 1970- og 1980-tallet ble et viktig vendepunkt for samisk politisk mobilisering og miljøkamp."),
    ("DEMOKRATI", "Demokrati", "Demokrati bygger på folkestyre, politisk deltakelse, rettigheter og institusjoner som begrenser makt."),
    ("YTRINGSFRIHET", "Ytringsfrihet", "Ytringsfrihet beskytter retten til å uttrykke meninger, samtidig som lover setter grenser for blant annet trusler og hatefulle ytringer."),
    ("PERSONVERN", "Personvern i den digitale tidsalderen", "Digitale tjenester samler ofte inn data. Personvern handler om kontroll, åpenhet og forsvarlig behandling av personopplysninger."),
    ("KVANTEDATAMASKIN", "Kvantedatamaskiner", "Kvantedatamaskiner bruker kvantemekaniske prinsipper og kan på enkelte problemtyper gi andre beregningsmuligheter enn klassiske datamaskiner."),
    ("FREMTIDEN", "Fremtiden", "Fremtiden formes av valgene vi tar innen teknologi, utdanning, demokrati, miljø og samarbeid.")

    ,("KUNSTIG INTELLIGENS 2026", "KI i 2026", "Kunstig intelligens er blitt en del av skole, arbeidsliv og forskning. Viktige temaer er åpenhet, personvern og menneskelig kontroll."),
    ("CHATGPT", "Samtaler med KI", "Språkmodeller kan hjelpe med å forklare, skrive og programmere, men svar bør vurderes kritisk og kontrolleres."),
    ("DEEPFAKE", "Deepfakes", "KI kan lage realistisk syntetisk lyd og video. Det gjør kildekontroll og tydelig merking stadig viktigere."),
    ("ALGORITMER", "Algoritmenes verden", "Algoritmer sorterer innhold, anbefaler videoer og påvirker hva vi ser på digitale plattformer."),
    ("DIGITALT FOTSPOR", "Det digitale fotsporet", "Søk, innlegg, bilder og appbruk kan etterlate digitale spor. Tenk gjennom hva du deler og hvem som får tilgang."),
    ("NETTVETT", "Nettvett", "Nettvett handler blant annet om respekt, personvern, kildekritikk og å tenke før man deler."),
    ("CYBERSIKKERHET", "Cybersikkerhet", "Cybersikkerhet beskytter systemer og informasjon mot digitale angrep, svindel og uautorisert tilgang."),
    ("PASSORD", "Passord og sikkerhet", "Unike passord og tofaktorautentisering reduserer risikoen for at uvedkommende får tilgang til kontoer."),
    ("TOFAKTOR", "Tofaktorautentisering", "Tofaktorautentisering krever en ekstra bekreftelse i tillegg til passordet og gir et ekstra sikkerhetslag."),
    ("BÆREKRAFTIG ENERGI", "Fornybar energi", "Sol-, vind- og vannkraft er viktige deler av omstillingen til energisystemer med lavere klimagassutslipp."),
    ("PARIS 2024", "Sommer-OL 2024", "Sommer-OL i Paris ble arrangert i 2024 og samlet utøvere fra hele verden."),
    ("EUROPA 2024", "Europamesterskapet 2024", "Fotball-EM for menn ble arrangert i Tyskland sommeren 2024."),
    ("UKRAINA 2022", "Fullskalainvasjonen av Ukraina", "Russlands fullskalainvasjon av Ukraina startet 24. februar 2022 og fikk store konsekvenser for europeisk sikkerhet."),
    ("9 11", "11. september 2001", "Terrorangrepene i USA 11. september 2001 endret internasjonal sikkerhetspolitikk og fikk store menneskelige konsekvenser."),
    ("EUROEN", "Euroen", "Euroen ble innført som kontovaluta i 1999 og som sedler og mynter i 2002 i mange europeiske land."),
    ("BREXIT", "Brexit", "Storbritannia forlot EU 31. januar 2020 etter folkeavstemningen i 2016."),
    ("NOBELS FREDSPRIS", "Nobels fredspris", "Nobels fredspris deles ut i Oslo og anerkjenner arbeid for fred og internasjonalt samarbeid."),
    ("OLJEFUNNET", "Norsk oljeeventyr", "Funnet av Ekofisk i 1969 ble starten på en omfattende norsk olje- og gassindustri."),
    ("22 JULI", "22. juli 2011", "Terrorangrepene 22. juli 2011 rammet regjeringskvartalet og Utøya. Dagen står som et viktig minne om demokrati og fellesskap."),
    ("EIDSVOLL", "Eidsvoll 1814", "Riksforsamlingen på Eidsvoll vedtok Norges grunnlov 17. mai 1814."),
    ("NANSEN", "Fridtjof Nansen", "Fridtjof Nansen var polfarer, forsker og humanitær. Han mottok Nobels fredspris i 1922."),
    ("AMUNDSEN", "Roald Amundsen", "Roald Amundsen ledet ekspedisjonen som nådde Sydpolen 14. desember 1911."),
    ("SVALBARD", "Svalbardtraktaten", "Svalbardtraktaten ble undertegnet i 1920 og fastsetter rammene for norsk suverenitet og andre lands rettigheter på øygruppen."),
    ("NATO", "NATO", "NATO ble grunnlagt i 1949 som en forsvarsallianse basert på kollektivt forsvar."),
    ("JERNTEPPET", "Jernteppet", "Uttrykket jernteppet beskrev Europas politiske og ideologiske deling under den kalde krigen."),
    ("GUTENBERG", "Johannes Gutenberg", "Gutenbergs trykketeknologi på 1400-tallet bidro til raskere spredning av bøker og kunnskap."),
    ("RENESSANSEN", "Renessansen", "Renessansen var en kulturell og intellektuell periode i Europa med fornyet interesse for antikkens kunst og kunnskap."),
    ("SVARTEDAUDEN", "Svartedauden", "Svartedauden nådde Norge omkring 1349 og førte til store demografiske og samfunnsmessige endringer."),
    ("VIKINGTIDEN", "Vikingtiden", "Vikingtiden i Skandinavia regnes vanligvis fra slutten av 700-tallet til midten av 1000-tallet."),
    ("MAGNA CARTA", "Magna Carta 1215", "Magna Carta ble forseglet i England i 1215 og ble senere et viktig symbol i utviklingen av rettsstatsprinsipper."),
    ("INDUSTRIARBEID", "Arbeiderbevegelsen", "Arbeiderbevegelsen arbeidet historisk for bedre lønns- og arbeidsvilkår, organisasjonsrett og politisk innflytelse."),
    ("8 TIMERS ARBEIDSDAG", "Åttetimersdagen", "Kampen for kortere arbeidsdag var en sentral del av arbeiderbevegelsens historie i mange land."),
    ("KVINNEBEVEGELSEN", "Kvinnebevegelsen", "Kvinnebevegelser har arbeidet for politiske, økonomiske og sosiale rettigheter og likestilling."),
    ("STONEWALL", "Stonewall-opprøret", "Hendelsene ved Stonewall Inn i 1969 ble et viktig vendepunkt i moderne LHBTQ+-historie."),
    ("APOLLO 13", "Apollo 13", "Apollo 13-ferden i 1970 ble avbrutt etter en alvorlig teknisk hendelse, og mannskapet kom trygt tilbake gjennom omfattende problemløsning."),
    ("HUBBLE", "Hubble-teleskopet", "Hubble-romteleskopet ble skutt opp i 1990 og har gitt viktige observasjoner av universet."),
    ("JAMES WEBB", "James Webb-teleskopet", "James Webb-romteleskopet ble skutt opp i 2021 og observerer universet i infrarødt lys."),
    ("MARSROVER", "Rover på Mars", "Roboter som Curiosity og Perseverance undersøker Mars og leter etter spor etter planetens geologiske og klimatiske historie."),
    ("GENREDIGERING", "CRISPR", "CRISPR-teknologi gjør det mulig å endre DNA mer presist og reiser viktige etiske spørsmål."),
    ("MENNESKEGENOMET", "Det menneskelige genomprosjektet", "Human Genome Project ble fullført i hovedsak i 2003 og kartla menneskets DNA-sekvens."),
    ("ELEKTRISK BIL", "Elektriske biler", "Elektriske biler har fått større utbredelse og er en viktig del av omstillingen i transportsektoren."),
    ("JERNBANEN", "Jernbanens gjennombrudd", "Jernbanen endret transport, handel og bosetting under industrialiseringen."),
    ("FLY", "Flygingens historie", "Brødrene Wright gjennomførte en kontrollert motorflyging i 1903, et viktig gjennombrudd i luftfartshistorien."),
    ("RADIO", "Radioens tidsalder", "Radio ble et sentralt massemedium på 1900-tallet for nyheter, underholdning og beredskap."),
    ("FJERNSYN", "Fjernsynet", "Fjernsynet endret nyhetsformidling og populærkultur gjennom 1900-tallet."),
    ("MOBILTELEFON", "Mobiltelefonens utvikling", "Mobiltelefonen utviklet seg fra enkle samtaleapparater til avanserte digitale verktøy."),
    ("OPEN SOURCE", "Åpen kildekode", "Åpen kildekode gjør programvare tilgjengelig for innsyn, bruk og videreutvikling under bestemte lisenser."),
    ("LINUX", "Linux", "Linux-kjernen ble først publisert i 1991 og er i dag grunnlag for mange operativsystemer og servere."),
    ("PYTHON", "Programmeringsspråket Python", "Python ble laget av Guido van Rossum og er kjent for lesbar syntaks og bred bruk innen blant annet dataanalyse."),
    ("NULL OG EN", "Det binære tallsystemet", "Datamaskiner representerer og behandler informasjon ved hjelp av binære verdier, ofte omtalt som null og én."),
]

# Progress is stored locally beside the program.
funnet_easter_eggs = set()

def last_easter_egg_fremgang():
    global funnet_easter_eggs
    try:
        if os.path.exists(EASTER_EGG_FILE):
            with open(EASTER_EGG_FILE, "r", encoding="utf-8") as fil:
                data = json.load(fil)
            if isinstance(data, list):
                gyldige = {rad[0] for rad in EASTER_EGG_DATA}
                funnet_easter_eggs = set(data) & gyldige
    except (OSError, json.JSONDecodeError, TypeError):
        funnet_easter_eggs = set()

def lagre_easter_egg_fremgang():
    try:
        with open(EASTER_EGG_FILE, "w", encoding="utf-8") as fil:
            json.dump(sorted(funnet_easter_eggs), fil, ensure_ascii=False, indent=2)
    except OSError:
        pass

def marker_easter_egg_funnet(frase):
    if frase not in funnet_easter_eggs:
        funnet_easter_eggs.add(frase)
        lagre_easter_egg_fremgang()

def vis_easter_egg_info(frase):
    rad = next((r for r in EASTER_EGG_DATA if r[0] == frase), None)
    if not rad:
        return
    _, tittel, beskrivelse = rad
    vindu = nytt_vindu(f"Du fant: {tittel}", "520x300", (420, 260))
    vindu.configure(bg=color("panel"))
    tk.Label(
        vindu, text="✦ HEMMELIGHET FUNNET ✦",
        bg=color("panel"), fg=color("green"), font=font(11, True)
    ).pack(pady=(24, 8))
    tk.Label(
        vindu, text=tittel, bg=color("panel"), fg=color("text"),
        font=font(20, True), wraplength=460, justify="center"
    ).pack(padx=20, pady=8)
    tk.Label(
        vindu, text=beskrivelse, bg=color("panel"), fg=color("muted"),
        font=font(10), wraplength=450, justify="center"
    ).pack(padx=25, pady=10)
    tk.Label(
        vindu, text=f"Samlet fremgang: {len(funnet_easter_eggs)} / 100",
        bg=color("panel"), fg=color("green"), font=font(10, True)
    ).pack(pady=(4, 16))
    lag_knapp(vindu, "Lukk", vindu.destroy, color("accent")).pack(pady=(0, 16))

def vis_easter_egg_fremgang(parent):
    total = len(EASTER_EGG_DATA)
    antall = len(funnet_easter_eggs)
    prosent = antall / total * 100
    tk.Label(
        parent, text="DIN EASTER EGG-FREMGANG",
        bg=color("panel"), fg=color("text"), font=font(14, True)
    ).pack(anchor="w", padx=16, pady=(16, 8))
    tk.Label(
        parent, text=f"{antall} av {total} hemmeligheter funnet  •  {prosent:.0f} %",
        bg=color("panel"), fg=color("green"), font=font(11, True)
    ).pack(anchor="w", padx=16, pady=(0, 8))
    bar = ttk.Progressbar(parent, maximum=total, value=antall, mode="determinate")
    bar.pack(fill="x", padx=16, pady=(0, 14))
    if antall == total:
        melding = "100 % – du har funnet alle hemmelighetene. Imponerende!"
    elif antall == 0:
        melding = "Ingen funnet ennå. Skriv inn en hemmelig frase i tallfeltet."
    else:
        melding = f"Du har funnet {antall}. Det finnes fortsatt {total - antall} å oppdage."
    tk.Label(
        parent, text=melding, bg=color("panel"), fg=color("muted"),
        font=font(9), wraplength=450, justify="left"
    ).pack(anchor="w", padx=16)
    if antall:
        tk.Label(
            parent, text="Sist oppdagede hemmeligheter:",
            bg=color("panel"), fg=color("text"), font=font(10, True)
        ).pack(anchor="w", padx=16, pady=(16, 4))
        for frase in [r[0] for r in EASTER_EGG_DATA if r[0] in funnet_easter_eggs][-8:]:
            tk.Label(
                parent, text="✓ " + frase, bg=color("panel"),
                fg=color("green"), font=font(9)
            ).pack(anchor="w", padx=22)

def vis_easter_egg_meny():
    if not settings["features"].get("fun", True):
        messagebox.showinfo("Easter eggs", "Easter eggs er deaktivert i innstillingene.")
        return

    vindu = nytt_vindu("Hemmelig meny – Easter eggs", "760x720", (580, 500))
    vindu.configure(bg=color("bg"))

    topp = tk.Frame(vindu, bg=color("bg"), padx=16, pady=12)
    topp.pack(fill="x")
    tk.Label(
        topp, text="✦ DEN HEMMELIGE MENYEN ✦",
        bg=color("bg"), fg=color("text"), font=font(17, True)
    ).pack(anchor="w")
    tk.Label(
        topp, text="100 skjulte fraser. Skriv en frase i tallfeltet for å låse opp hemmeligheten.",
        bg=color("bg"), fg=color("muted"), font=font(9), wraplength=620
    ).pack(anchor="w", pady=(4, 0))

    notebook = ttk.Notebook(vindu)
    notebook.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    alle_tab = tk.Frame(notebook, bg=color("panel"))
    fremgang_tab = tk.Frame(notebook, bg=color("panel"))
    notebook.add(alle_tab, text="Alle 100")
    notebook.add(fremgang_tab, text="Progresjon")

    # Scrollable list of all secrets.
    holder = tk.Frame(alle_tab, bg=color("panel"))
    holder.pack(fill="both", expand=True)
    liste_canvas = tk.Canvas(holder, bg=color("panel"), highlightthickness=0)
    scrollbar = ttk.Scrollbar(holder, orient="vertical", command=liste_canvas.yview)
    liste_frame = tk.Frame(liste_canvas, bg=color("panel"))
    liste_frame.bind(
        "<Configure>",
        lambda event: liste_canvas.configure(scrollregion=liste_canvas.bbox("all"))
    )
    liste_canvas.create_window((0, 0), window=liste_frame, anchor="nw")
    liste_canvas.configure(yscrollcommand=scrollbar.set)
    liste_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for indeks, (frase, tittel, beskrivelse) in enumerate(EASTER_EGG_DATA, 1):
        funnet = frase in funnet_easter_eggs
        rad = tk.Frame(liste_frame, bg=color("panel_light"), padx=10, pady=8)
        rad.pack(fill="x", padx=9, pady=4)
        status = "✓ FUNNET" if funnet else "🔒 IKKE FUNNET"
        statusfarge = color("green") if funnet else color("muted")
        tk.Label(
            rad, text=f"{indeks:02d}. {frase}", bg=color("panel_light"),
            fg=color("text"), font=font(9, True), anchor="w"
        ).pack(side="left", fill="x", expand=True)
        tk.Label(
            rad, text=status, bg=color("panel_light"), fg=statusfarge,
            font=font(8, True)
        ).pack(side="right")

    vis_easter_egg_fremgang(fremgang_tab)

    lag_knapp(
        vindu, "Lukk menyen", vindu.destroy, color("accent")
    ).pack(pady=(0, 12))

# Backwards-compatible animated eggs from the original program.
ORIGINAL_EGGS = {
    "PETER ER DUM": egg_strobe,
    "TIRIL KAN IKKE LESE": egg_regnbue,
    "JOHAN-OLAI ER SMART": egg_konfetti,
    "MATRIX": egg_matrix,
    "DISCO": egg_disco
}

def sjekk_easter_egg(tekst):
    if not settings["features"].get("fun", True):
        return False

    norm = " ".join(tekst.upper().split())

    # Secret menu keyword – this is not counted as one of the 50 eggs.
    if norm == "EASTER EGG":
        entry.delete(0, tk.END)
        status_var.set("Den hemmelige menyen er åpnet!")
        vis_easter_egg_meny()
        return True

    for frase, tittel, beskrivelse in EASTER_EGG_DATA:
        if norm == frase:
            entry.delete(0, tk.END)
            marker_easter_egg_funnet(frase)
            status_var.set(
                f"Easter egg funnet: {len(funnet_easter_eggs)} av 100!"
            )
            if frase in ORIGINAL_EGGS:
                ORIGINAL_EGGS[frase]()
            else:
                egg_generell_animasjon(frase, tittel, beskrivelse)
            return True

    return False


KONAMI = [
    "Up", "Up", "Down", "Down",
    "Left", "Right", "Left", "Right", "b", "a"
]

konami_pos = [0]


def egg_konami():

    status_var.set("KONAMI-KODE AKTIVERT! +30 liv")

    messagebox.showinfo(
        "KONAMI-KODE!",
        "Du har låst opp 30 ekstra liv!\n\n"
        "(Ikke at du trenger dem i et sorteringsprogram …)"
    )

    egg_disco()


def konami_tast(event):

    if not settings["features"].get("fun", True):
        return

    forventet = KONAMI[konami_pos[0]]

    if event.keysym.lower() == forventet.lower():

        konami_pos[0] += 1

        if konami_pos[0] == len(KONAMI):

            konami_pos[0] = 0
            egg_konami()

    else:

        konami_pos[0] = 1 if event.keysym == KONAMI[0] else 0


# ============================================================
# VIS RESULTATER
# ============================================================

def vis_resultater():

    global stats_frame
    global sorted_text
    global frekvens_tabell
    global histogram
    global boxplot_canvas

    for widget in result_area.winfo_children():
        widget.destroy()

    if siste_resultat is None:
        return

    data = siste_resultat
    features = settings["features"]

    # STATISTIKK

    statistikk_nokler = [
        "antall", "sum", "gjennomsnitt", "median", "typetall",
        "minimum", "maksimum", "variasjonsbredde", "quartiles",
        "variance", "extra", "percentiles", "outliers"
    ]

    har_statistikk = any(
        features.get(key, False)
        for key in statistikk_nokler
    )

    if har_statistikk:

        tk.Label(
            result_area,
            text="STATISTIKKOVERSIKT",
            bg=color("bg"),
            fg=color("text"),
            font=font(11, True)
        ).pack(anchor="w", pady=(5, 8))

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

        overskrift = {
            "stigende": "SORTERTE TALL (STIGENDE)",
            "synkende": "SORTERTE TALL (SYNKENDE)",
            "tilfeldig": "BLANDEDE TALL"
        }.get(data["retning"], "SORTERTE TALL")

        tk.Label(
            result_area,
            text=overskrift,
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

    # BOKSPLOTT

    if features["boxplot"]:

        boks = tk.Frame(
            result_area,
            bg=color("panel"),
            padx=12,
            pady=12
        )

        boks.pack(fill="x", pady=(15, 0))

        tk.Label(
            boks,
            text="BOKSPLOTT",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True)
        ).pack(anchor="w", pady=(0, 10))

        boxplot_canvas = tk.Canvas(
            boks,
            bg=color("panel"),
            highlightthickness=0,
            height=110
        )

        boxplot_canvas.pack(fill="x")

        boxplot_canvas.bind(
            "<Configure>",
            lambda event: tegn_boxplot(siste_resultat)
            if siste_resultat else None
        )

        tegn_boxplot(data)


# ============================================================
# TEMA OG VISNING
# ============================================================

def bruk_tema(navn):

    if navn not in THEMES:
        return

    for nokkel in FARGENOKLER:
        settings[nokkel] = THEMES[navn][nokkel]

    settings["theme"] = navn

    rebuild_interface()

    save_settings()

    status_var.set(f"Tema «{navn}» er aktivert.")


def zoom(endring):

    ny = settings["font_size"] + endring

    settings["font_size"] = max(8, min(20, ny))

    rebuild_interface()

    status_var.set(f"Skriftstørrelse: {settings['font_size']}")


def veksle_fullskjerm(event=None):

    root.attributes(
        "-fullscreen",
        not bool(root.attributes("-fullscreen"))
    )


def avslutt_fullskjerm(event=None):

    if root.attributes("-fullscreen"):
        root.attributes("-fullscreen", False)


def avslutt():

    lagre_historikk()
    root.destroy()


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
    window.geometry("650x820")
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

    def rull_innstillinger(event):

        if event.delta:
            settings_canvas.yview_scroll(
                -1 if event.delta > 0 else 1,
                "units"
            )

    window.bind("<MouseWheel>", rull_innstillinger)

    def seksjon(tittel):

        tk.Label(
            content,
            text=tittel,
            bg=color("bg"),
            fg=color("text"),
            font=font(12, True)
        ).pack(anchor="w", pady=(18, 8))

    def etikett(tekst):

        tk.Label(
            content,
            text=tekst,
            bg=color("bg"),
            fg=color("text"),
            font=font(9)
        ).pack(anchor="w")

    # TEMA

    seksjon("UTSEENDE OG FARGER")

    etikett("Fargetema")

    tema_var = tk.StringVar(value=settings["theme"])

    tema_combo = ttk.Combobox(
        content,
        textvariable=tema_var,
        values=list(THEMES.keys()),
        state="readonly"
    )

    tema_combo.pack(fill="x", pady=(5, 10))

    def velg_tema(event=None):

        bruk_tema(tema_var.get())

        window.destroy()

        apne_innstillinger()

    tema_combo.bind("<<ComboboxSelected>>", velg_tema)

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
                title=f"Velg {navn}",
                parent=window
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

    etikett("Skrifttype")

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

    etikett("Skriftstørrelse")

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

    etikett("Overskriftsstørrelse")

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

    seksjon("LAYOUT OG TALLFORMAT")

    etikett("Kolonner i statistikkoversikten")

    columns_var = tk.IntVar(
        value=settings["stats_columns"]
    )

    ttk.Combobox(
        content,
        textvariable=columns_var,
        values=[1, 2, 3, 4, 5],
        state="readonly"
    ).pack(fill="x", pady=(5, 10))

    etikett("Antall desimaler i resultatene")

    decimals_var = tk.IntVar(
        value=settings["decimals"]
    )

    tk.Spinbox(
        content,
        from_=0,
        to=10,
        textvariable=decimals_var,
        bg=color("panel_light"),
        fg=color("text"),
        relief="flat"
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
        "extra": "Utvidet statistikk (snitt, skjevhet, standardfeil …)",
        "percentiles": "Persentiler (5, 10, 90, 95)",
        "outliers": "Uteliggere",
        "frequency": "Frekvenstabell",
        "histogram": "Histogram",
        "boxplot": "Boksplott",
        "sorted_list": "Vis sorterte tall",
        "calculator": "Kalkulator",
        "converter": "Enhetsomregner",
        "random": "Tilfeldige tall",
        "import": "Importer fra fil",
        "history": "Historikk",
        "copy": "Kopier resultater",
        "export": "Eksporter TXT",
        "csv": "Eksporter CSV",
        "fun": "Moro-modus (skjulte overraskelser)"
    }

    feature_vars = {}

    groups = {
        "Statistiske beregninger": [
            "antall", "sum", "gjennomsnitt", "median",
            "typetall", "minimum", "maksimum", "variasjonsbredde"
        ],
        "Avanserte beregninger": [
            "quartiles", "variance", "extra",
            "percentiles", "outliers"
        ],
        "Visningsfunksjoner": [
            "frequency", "histogram", "boxplot", "sorted_list"
        ],
        "Verktøy": [
            "calculator", "converter", "random", "import",
            "history", "copy", "export", "csv"
        ],
        "Moro": [
            "fun"
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

            lag_sjekk(
                group_frame,
                feature_names[key],
                var,
                color("panel")
            ).pack(anchor="w", pady=2)

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

            settings["decimals"] = max(
                0,
                min(10, int(decimals_var.get()))
            )

        except (ValueError, tk.TclError):

            messagebox.showerror(
                "Ugyldige verdier",
                "Kontroller skriftstørrelse, kolonner og desimaler.",
                parent=window
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
# MENYLINJE
# ============================================================

def bygg_meny():

    f = settings["features"]

    meny = tk.Menu(root)

    # FIL

    fil = tk.Menu(meny, tearoff=0)

    if f["import"]:
        fil.add_command(
            label="Importer tall fra fil…",
            accelerator="Ctrl+O",
            command=importer_fil
        )

    if f["export"]:
        fil.add_command(
            label="Eksporter som TXT…",
            accelerator="Ctrl+S",
            command=eksporter_resultater
        )

    if f["csv"]:
        fil.add_command(
            label="Eksporter som CSV…",
            command=eksporter_csv
        )

    if f["copy"]:
        fil.add_command(
            label="Kopier resultater",
            accelerator="Ctrl+Shift+C",
            command=kopier_resultater
        )

    fil.add_separator()
    fil.add_command(label="Avslutt", command=avslutt)

    meny.add_cascade(label="Fil", menu=fil)

    # VERKTØY

    verktoy = tk.Menu(meny, tearoff=0)

    if f["calculator"]:
        verktoy.add_command(
            label="Kalkulator",
            accelerator="F2",
            command=apne_kalkulator
        )

    if f["random"]:
        verktoy.add_command(
            label="Tilfeldige tall…",
            accelerator="F3",
            command=apne_tilfeldig
        )

    if f["history"]:
        verktoy.add_command(
            label="Historikk",
            accelerator="F4",
            command=apne_historikk
        )

    if f["converter"]:
        verktoy.add_command(
            label="Enhetsomregner",
            accelerator="F5",
            command=apne_omregner
        )

    meny.add_cascade(label="Verktøy", menu=verktoy)

    # VIS

    vis = tk.Menu(meny, tearoff=0)

    tema_meny = tk.Menu(vis, tearoff=0)

    for navn in THEMES:
        tema_meny.add_command(
            label=navn,
            command=lambda n=navn: bruk_tema(n)
        )

    vis.add_cascade(label="Tema", menu=tema_meny)

    vis.add_command(
        label="Zoom inn",
        accelerator="Ctrl++",
        command=lambda: zoom(1)
    )

    vis.add_command(
        label="Zoom ut",
        accelerator="Ctrl+−",
        command=lambda: zoom(-1)
    )

    vis.add_command(
        label="Fullskjerm",
        accelerator="F11",
        command=veksle_fullskjerm
    )

    vis.add_separator()

    vis.add_command(
        label="Innstillinger…",
        accelerator="Ctrl+,",
        command=apne_innstillinger
    )

    meny.add_cascade(label="Vis", menu=vis)

    # HJELP

    hjelp = tk.Menu(meny, tearoff=0)

    hjelp.add_command(
        label="Hjelp og hurtigtaster",
        accelerator="F1",
        command=apne_hjelp
    )

    hjelp.add_command(label="Om programmet", command=vis_om)

    meny.add_cascade(label="Hjelp", menu=hjelp)

    root.configure(menu=meny)


# ============================================================
# BYGG HOVEDVINDU
# ============================================================

def rebuild_interface():

    global entry
    global status_var
    global result_area
    global export_frame

    # Husk tekst i tallfeltet

    gammel_tekst = ""

    if entry is not None:

        try:
            gammel_tekst = entry.get()

        except tk.TclError:
            gammel_tekst = ""

    # Oppdater bakgrunnsfarger

    root.configure(bg=color("bg"))
    scroll_container.configure(bg=color("bg"))
    canvas.configure(bg=color("bg"))
    main.configure(bg=color("bg"))

    oppdater_ttk()
    bygg_meny()

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

    # KNAPPER I OVERSKRIFTEN

    lag_knapp(
        header,
        "⚙ Innstillinger",
        apne_innstillinger,
        color("panel_light")
    ).pack(side="right", pady=5)

    lag_knapp(
        header,
        "? Hjelp",
        apne_hjelp,
        color("panel_light")
    ).pack(side="right", pady=5, padx=(0, 8))

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

    if gammel_tekst:
        entry.insert(0, gammel_tekst)

    entry.bind(
        "<KeyRelease>",
        lambda event: sjekk_easter_egg(entry.get())
    )

    entry.bind(
        "<Return>",
        lambda event: sorter_tall("stigende")
    )

    entry.focus_set()

    # VALG

    valg_rad = tk.Frame(
        input_frame,
        bg=color("panel")
    )

    valg_rad.pack(fill="x", pady=(10, 0))

    lag_sjekk(
        valg_rad,
        "Fjern duplikater",
        dup_var,
        color("panel")
    ).pack(side="left", padx=(0, 12))

    lag_sjekk(
        valg_rad,
        "Avrund til heltall",
        avrund_var,
        color("panel")
    ).pack(side="left", padx=(0, 12))

    tk.Label(
        valg_rad,
        text="Filter fra",
        bg=color("panel"),
        fg=color("muted"),
        font=font(9)
    ).pack(side="left")

    tk.Entry(
        valg_rad,
        textvariable=filt_min_var,
        width=7,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(9)
    ).pack(side="left", padx=(4, 8), ipady=3)

    tk.Label(
        valg_rad,
        text="til",
        bg=color("panel"),
        fg=color("muted"),
        font=font(9)
    ).pack(side="left")

    tk.Entry(
        valg_rad,
        textvariable=filt_max_var,
        width=7,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(9)
    ).pack(side="left", padx=(4, 0), ipady=3)

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
        "Bland",
        lambda: sorter_tall("tilfeldig"),
        color("panel_light")
    ).pack(side="left", padx=7)

    lag_knapp(
        button_frame,
        "Nullstill",
        nullstill,
        color("panel_light")
    ).pack(side="right")

    if settings["features"]["calculator"]:

        lag_knapp(
            button_frame,
            "Kalkulator",
            apne_kalkulator,
            color("panel_light")
        ).pack(side="right", padx=7)

    if settings["features"]["random"]:

        lag_knapp(
            button_frame,
            "Tilfeldige tall",
            apne_tilfeldig,
            color("panel_light")
        ).pack(side="right", padx=7)

    # RESULTATOMRÅDE

    result_area = tk.Frame(
        main,
        bg=color("bg")
    )

    result_area.pack(
        fill="both",
        expand=True
    )

    # EKSPORTKNAPPER

    f = settings["features"]

    if f["copy"] or f["export"] or f["csv"]:

        export_frame = tk.Frame(
            main,
            bg=color("bg")
        )

        export_frame.pack(
            fill="x",
            pady=(15, 5)
        )

        if f["copy"]:

            lag_knapp(
                export_frame,
                "Kopier resultater",
                kopier_resultater,
                color("panel_light")
            ).pack(side="left", padx=(0, 8))

        if f["export"]:

            lag_knapp(
                export_frame,
                "Eksporter TXT",
                eksporter_resultater,
                color("panel_light")
            ).pack(side="left", padx=(0, 8))

        if f["csv"]:

            lag_knapp(
                export_frame,
                "Eksporter CSV",
                eksporter_csv,
                color("panel_light")
            ).pack(side="left")

    # STATUS

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

dup_var = tk.BooleanVar(value=False)
avrund_var = tk.BooleanVar(value=False)
filt_min_var = tk.StringVar(value="")
filt_max_var = tk.StringVar(value="")

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

    try:

        if event.widget.winfo_toplevel() is not root:
            return

    except (AttributeError, KeyError, tk.TclError):
        return

    if event.delta:

        canvas.yview_scroll(
            -1 if event.delta > 0 else 1,
            "units"
        )


def scroll_opp(event):

    try:

        if event.widget.winfo_toplevel() is root:
            canvas.yview_scroll(-1, "units")

    except (AttributeError, KeyError, tk.TclError):
        pass


def scroll_ned(event):

    try:

        if event.widget.winfo_toplevel() is root:
            canvas.yview_scroll(1, "units")

    except (AttributeError, KeyError, tk.TclError):
        pass


canvas.bind_all("<MouseWheel>", musehjul)
canvas.bind_all("<Button-4>", scroll_opp)
canvas.bind_all("<Button-5>", scroll_ned)


# ============================================================
# TASTATURSNARVEIER
# ============================================================

root.bind("<Control-Return>", lambda event: sorter_tall("stigende"))
root.bind("<Control-Shift-Return>", lambda event: sorter_tall("synkende"))
root.bind("<Control-b>", lambda event: sorter_tall("tilfeldig"))
root.bind("<Control-l>", lambda event: nullstill())
root.bind("<Control-comma>", lambda event: apne_innstillinger())
root.bind("<Control-o>", lambda event: importer_fil())
root.bind("<Control-s>", lambda event: eksporter_resultater())
root.bind("<Control-C>", lambda event: kopier_resultater())
root.bind("<Control-plus>", lambda event: zoom(1))
root.bind("<Control-equal>", lambda event: zoom(1))
root.bind("<Control-minus>", lambda event: zoom(-1))
root.bind("<F1>", lambda event: apne_hjelp())
root.bind("<F2>", lambda event: apne_kalkulator())
root.bind("<F3>", lambda event: apne_tilfeldig())
root.bind("<F4>", lambda event: apne_historikk())
root.bind("<F5>", lambda event: apne_omregner())
root.bind("<F11>", veksle_fullskjerm)
root.bind("<Escape>", avslutt_fullskjerm)

root.bind_all("<Key>", konami_tast, add="+")

root.protocol("WM_DELETE_WINDOW", avslutt)


# ============================================================
# START PROGRAMMET
# ============================================================

last_easter_egg_fremgang()

oppdater_ttk()

rebuild_interface()

root.mainloop()