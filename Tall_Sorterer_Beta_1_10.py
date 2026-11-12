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

# Beta 1.10: standard library only (Tkinter is included with most Python installs).


# ============================================================
# INNSTILLINGER
# ============================================================

VERSJON = "Beta 1.10"
MAX_TALL = 999
HISTORIKK_MAKS = 30
SETTINGS_FILE = "tall_sorterer_settings.json"
HISTORY_FILE = "tall_sorterer_historikk.json"

FARGENOKLER = ["bg", "panel", "panel_light", "accent", "text", "muted", "green", "red"]

THEMES = {
    "Midnatt": {
        "bg": "#111318",
        "panel": "#1B1F29",
        "panel_light": "#242A36",
        "accent": "#6C8CFF",
        "text": "#F1F3F8",
        "muted": "#929BAD",
        "green": "#55D6A7",
        "red": "#FF7373",
    },
    "Lys": {
        "bg": "#F4F6FB",
        "panel": "#FFFFFF",
        "panel_light": "#E6EAF3",
        "accent": "#3D5AFE",
        "text": "#1B1F29",
        "muted": "#6B7385",
        "green": "#1E9E6A",
        "red": "#D93636",
    },
    "Hacker": {
        "bg": "#050805",
        "panel": "#0B140B",
        "panel_light": "#122012",
        "accent": "#1FA83A",
        "text": "#B6FFB6",
        "muted": "#5C9A5C",
        "green": "#39FF14",
        "red": "#FF4040",
    },
    "Solnedgang": {
        "bg": "#1E1220",
        "panel": "#2B1A2E",
        "panel_light": "#3A2440",
        "accent": "#FF7A59",
        "text": "#FFEFE6",
        "muted": "#C79AA8",
        "green": "#FFC857",
        "red": "#FF4D6D",
    },
    "Hav": {
        "bg": "#0B1B26",
        "panel": "#12293A",
        "panel_light": "#183649",
        "accent": "#2EC4B6",
        "text": "#E8F6F8",
        "muted": "#7FA3B0",
        "green": "#7BE0AD",
        "red": "#FF6B6B",
    },
}

DEFAULT_SETTINGS = {
    "theme": "Midnatt",
    "language": "nb",
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
        "fun": True,
    },
}


# ============================================================
# SPRÅKSTØTTE – OFFLINE / UTEN EKSTERNE PAKKER
# ============================================================

LANGUAGES = {
    "nb": "Norsk bokmål", "nn": "Norsk nynorsk", "en": "English",
    "de": "Deutsch", "fr": "Français", "es": "Español",
    "ar": "العربية", "sv": "Svenska", "da": "Dansk",
    "it": "Italiano", "pt": "Português", "nl": "Nederlands",
}

# Grensesnittordbok. Uoversatte fag-/easter-egg-tekster faller tilbake
# til bokmål, slik at programmet alltid viser forståelig tekst.
UI_TRANSLATIONS = {
    "nn": {
        "TALL SORTERER": "TAL SORTERER", "Statistikk, analyse og tallbehandling": "Statistikk, analyse og talhandsaming",
        "Innstillinger": "Innstillingar", "Hjelp": "Hjelp", "Språk": "Språk",
        "LEGG INN TALL": "LEGG INN TAL", "Sorter stigende": "Sorter stigande",
        "Sorter synkende": "Sorter synkande", "Bland": "Bland", "Nullstill": "Nullstill",
        "Kalkulator": "Kalkulator", "Tilfeldige tall": "Tilfeldige tal",
        "Kopier resultater": "Kopier resultat", "Eksporter TXT": "Eksporter TXT",
        "Eksporter CSV": "Eksporter CSV", "Matematisk ordbok": "Matematisk ordliste",
        "Tema": "Tema", "Vis": "Vis", "Verktøy": "Verktøy",
    },
    "en": {
        "TALL SORTERER": "NUMBER SORTER", "Statistikk, analyse og tallbehandling": "Statistics, analysis and number processing",
        "Innstillinger": "Settings", "Hjelp": "Help", "Språk": "Language",
        "LEGG INN TALL": "ENTER NUMBERS", "Sorter stigende": "Sort ascending",
        "Sorter synkende": "Sort descending", "Bland": "Shuffle", "Nullstill": "Reset",
        "Kalkulator": "Calculator", "Tilfeldige tall": "Random numbers",
        "Kopier resultater": "Copy results", "Eksporter TXT": "Export TXT",
        "Eksporter CSV": "Export CSV", "Matematisk ordbok": "Mathematics dictionary",
        "Tema": "Theme", "Vis": "View", "Verktøy": "Tools",
        "Skill tallene med mellomrom, komma eller semikolon.": "Separate numbers with spaces, commas or semicolons.",
        "Fjern duplikater": "Remove duplicates", "Avrund til heltall": "Round to integers",
        "Filter fra": "Filter from", "til": "to", "Sorter først": "Sort first",
        "Antall tall": "Number of values", "Sum": "Sum", "Gjennomsnitt": "Mean",
        "Median": "Median", "Typetall": "Mode", "Laveste verdi": "Minimum",
        "Høyeste verdi": "Maximum", "Variasjonsbredde": "Range",
        "Frekvenstabell": "Frequency table", "Historikk": "History",
        "Enhetsomregner": "Unit converter", "Easter eggs": "Easter eggs",
    },
    "de": {
        "TALL SORTERER": "ZAHLEN SORTIERER", "Statistikk, analyse og tallbehandling": "Statistik, Analyse und Zahlenverarbeitung",
        "Innstillinger": "Einstellungen", "Hjelp": "Hilfe", "Språk": "Sprache",
        "LEGG INN TALL": "ZAHLEN EINGEBEN", "Sorter stigende": "Aufsteigend sortieren",
        "Sorter synkende": "Absteigend sortieren", "Bland": "Mischen", "Nullstill": "Zurücksetzen",
        "Kalkulator": "Taschenrechner", "Tilfeldige tall": "Zufallszahlen",
        "Kopier resultater": "Ergebnisse kopieren", "Eksporter TXT": "TXT exportieren",
        "Eksporter CSV": "CSV exportieren", "Matematisk ordbok": "Mathematisches Wörterbuch",
        "Tema": "Design", "Vis": "Ansicht", "Verktøy": "Werkzeuge",
        "Fjern duplikater": "Duplikate entfernen", "Avrund til heltall": "Auf ganze Zahlen runden",
        "Gjennomsnitt": "Mittelwert", "Median": "Median", "Typetall": "Modalwert",
        "Laveste verdi": "Minimum", "Høyeste verdi": "Maximum",
    },
    "fr": {
        "TALL SORTERER": "TRIEUR DE NOMBRES", "Statistikk, analyse og tallbehandling": "Statistiques, analyse et traitement des nombres",
        "Innstillinger": "Paramètres", "Hjelp": "Aide", "Språk": "Langue",
        "LEGG INN TALL": "SAISIR DES NOMBRES", "Sorter stigende": "Trier par ordre croissant",
        "Sorter synkende": "Trier par ordre décroissant", "Bland": "Mélanger", "Nullstill": "Réinitialiser",
        "Kalkulator": "Calculatrice", "Tilfeldige tall": "Nombres aléatoires",
        "Kopier resultater": "Copier les résultats", "Eksporter TXT": "Exporter TXT",
        "Eksporter CSV": "Exporter CSV", "Matematisk ordbok": "Dictionnaire mathématique",
        "Tema": "Thème", "Vis": "Affichage", "Verktøy": "Outils",
        "Fjern duplikater": "Supprimer les doublons", "Avrund til heltall": "Arrondir aux entiers",
        "Gjennomsnitt": "Moyenne", "Median": "Médiane", "Typetall": "Mode",
    },
    "es": {
        "TALL SORTERER": "ORDENADOR DE NÚMEROS", "Statistikk, analyse og tallbehandling": "Estadística, análisis y procesamiento numérico",
        "Innstillinger": "Configuración", "Hjelp": "Ayuda", "Språk": "Idioma",
        "LEGG INN TALL": "INTRODUCIR NÚMEROS", "Sorter stigende": "Orden ascendente",
        "Sorter synkende": "Orden descendente", "Bland": "Mezclar", "Nullstill": "Restablecer",
        "Kalkulator": "Calculadora", "Tilfeldige tall": "Números aleatorios",
        "Kopier resultater": "Copiar resultados", "Eksporter TXT": "Exportar TXT",
        "Eksporter CSV": "Exportar CSV", "Matematisk ordbok": "Diccionario matemático",
        "Tema": "Tema", "Vis": "Ver", "Verktøy": "Herramientas",
        "Fjern duplikater": "Eliminar duplicados", "Avrund til heltall": "Redondear a enteros",
        "Gjennomsnitt": "Media", "Median": "Mediana", "Typetall": "Moda",
    },
    "ar": {
        "TALL SORTERER": "فرز الأرقام", "Statistikk, analyse og tallbehandling": "الإحصاء والتحليل ومعالجة الأرقام",
        "Innstillinger": "الإعدادات", "Hjelp": "مساعدة", "Språk": "اللغة",
        "LEGG INN TALL": "أدخل الأرقام", "Sorter stigende": "ترتيب تصاعدي",
        "Sorter synkende": "ترتيب تنازلي", "Bland": "خلط", "Nullstill": "إعادة ضبط",
        "Kalkulator": "آلة حاسبة", "Tilfeldige tall": "أرقام عشوائية",
        "Kopier resultater": "نسخ النتائج", "Eksporter TXT": "تصدير TXT",
        "Eksporter CSV": "تصدير CSV", "Matematisk ordbok": "قاموس الرياضيات",
        "Tema": "السمة", "Vis": "عرض", "Verktøy": "أدوات",
        "Gjennomsnitt": "المتوسط", "Median": "الوسيط", "Typetall": "المنوال",
    },
    "sv": {
        "TALL SORTERER": "TALSORTERARE", "Statistikk, analyse og tallbehandling": "Statistik, analys och talbehandling",
        "Innstillinger": "Inställningar", "Hjelp": "Hjälp", "Språk": "Språk",
        "LEGG INN TALL": "ANGE TAL", "Sorter stigende": "Sortera stigande",
        "Sorter synkende": "Sortera fallande", "Bland": "Blanda", "Nullstill": "Återställ",
        "Kalkulator": "Kalkylator", "Tilfeldige tall": "Slumptal",
        "Kopier resultater": "Kopiera resultat", "Eksporter TXT": "Exportera TXT",
        "Eksporter CSV": "Exportera CSV", "Matematisk ordbok": "Matematisk ordlista",
        "Tema": "Tema", "Vis": "Visa", "Verktøy": "Verktyg",
    },
    "da": {
        "TALL SORTERER": "TALSORTERER", "Statistikk, analyse og tallbehandling": "Statistik, analyse og talbehandling",
        "Innstillinger": "Indstillinger", "Hjelp": "Hjælp", "Språk": "Sprog",
        "LEGG INN TALL": "INDTAST TAL", "Sorter stigende": "Sorter stigende",
        "Sorter synkende": "Sorter faldende", "Bland": "Bland", "Nullstill": "Nulstil",
        "Kalkulator": "Lommeregner", "Tilfeldige tall": "Tilfældige tal",
        "Kopier resultater": "Kopiér resultater", "Eksporter TXT": "Eksportér TXT",
        "Eksporter CSV": "Eksportér CSV", "Matematisk ordbok": "Matematisk ordbog",
        "Tema": "Tema", "Vis": "Vis", "Verktøy": "Værktøjer",
    },
    "it": {
        "TALL SORTERER": "ORDINATORE DI NUMERI", "Statistikk, analyse og tallbehandling": "Statistiche, analisi ed elaborazione numerica",
        "Innstillinger": "Impostazioni", "Hjelp": "Aiuto", "Språk": "Lingua",
        "LEGG INN TALL": "INSERISCI NUMERI", "Sorter stigende": "Ordine crescente",
        "Sorter synkende": "Ordine decrescente", "Bland": "Mescola", "Nullstill": "Azzera",
        "Kalkulator": "Calcolatrice", "Tilfeldige tall": "Numeri casuali",
        "Kopier resultater": "Copia risultati", "Eksporter TXT": "Esporta TXT",
        "Eksporter CSV": "Esporta CSV", "Matematisk ordbok": "Dizionario matematico",
        "Tema": "Tema", "Vis": "Visualizza", "Verktøy": "Strumenti",
    },
    "pt": {
        "TALL SORTERER": "ORDENADOR DE NÚMEROS", "Statistikk, analyse og tallbehandling": "Estatística, análise e processamento numérico",
        "Innstillinger": "Configurações", "Hjelp": "Ajuda", "Språk": "Idioma",
        "LEGG INN TALL": "INTRODUZIR NÚMEROS", "Sorter stigende": "Ordenar crescente",
        "Sorter synkende": "Ordenar decrescente", "Bland": "Misturar", "Nullstill": "Repor",
        "Kalkulator": "Calculadora", "Tilfeldige tall": "Números aleatórios",
        "Kopier resultater": "Copiar resultados", "Eksporter TXT": "Exportar TXT",
        "Eksporter CSV": "Exportar CSV", "Matematisk ordbok": "Dicionário matemático",
        "Tema": "Tema", "Vis": "Ver", "Verktøy": "Ferramentas",
    },
    "nl": {
        "TALL SORTERER": "GETALLENSORTEERDER", "Statistikk, analyse og tallbehandling": "Statistiek, analyse en getalverwerking",
        "Innstillinger": "Instellingen", "Hjelp": "Help", "Språk": "Taal",
        "LEGG INN TALL": "VOER GETALLEN IN", "Sorter stigende": "Oplopend sorteren",
        "Sorter synkende": "Aflopend sorteren", "Bland": "Schudden", "Nullstill": "Wissen",
        "Kalkulator": "Rekenmachine", "Tilfeldige tall": "Willekeurige getallen",
        "Kopier resultater": "Resultaten kopiëren", "Eksporter TXT": "TXT exporteren",
        "Eksporter CSV": "CSV exporteren", "Matematisk ordbok": "Wiskundig woordenboek",
        "Tema": "Thema", "Vis": "Beeld", "Verktøy": "Hulpmiddelen",
    },
}

# Utvidede oversettelser av menypunkter.
UI_TRANSLATIONS.setdefault('nn', {}).update({'Fil': 'Fil', 'Rediger': 'Rediger', 'Vis': 'Vis', 'Hjelp': 'Hjelp', 'Avslutt': 'Avslutt', 'Importer tall fra fil…': 'Importer tal frå fil…', 'Eksporter som TXT…': 'Eksporter som TXT…', 'Eksporter som CSV…': 'Eksporter som CSV…', 'Zoom inn': 'Zoom inn', 'Zoom ut': 'Zoom ut', 'Fullskjerm': 'Fullskjerm', 'Innstillinger…': 'Innstillingar…', 'Hjelp og hurtigtaster': 'Hjelp og snøggtastar', 'Om programmet': 'Om programmet', 'Historikk': 'Historikk', 'Enhetsomregner': 'Einingomreknar', 'Tilfeldige tall…': 'Tilfeldige tal…', 'Matematisk ordbok…': 'Matematisk ordliste…'})
UI_TRANSLATIONS.setdefault('en', {}).update({'Fil': 'File', 'Rediger': 'Edit', 'Vis': 'View', 'Hjelp': 'Help', 'Avslutt': 'Exit', 'Importer tall fra fil…': 'Import numbers from file…', 'Eksporter som TXT…': 'Export as TXT…', 'Eksporter som CSV…': 'Export as CSV…', 'Zoom inn': 'Zoom in', 'Zoom ut': 'Zoom out', 'Fullskjerm': 'Fullscreen', 'Innstillinger…': 'Settings…', 'Hjelp og hurtigtaster': 'Help and shortcuts', 'Om programmet': 'About', 'Historikk': 'History', 'Enhetsomregner': 'Unit converter', 'Tilfeldige tall…': 'Random numbers…', 'Matematisk ordbok…': 'Math dictionary…'})
UI_TRANSLATIONS.setdefault('de', {}).update({'Fil': 'Datei', 'Rediger': 'Bearbeiten', 'Vis': 'Ansicht', 'Hjelp': 'Hilfe', 'Avslutt': 'Beenden', 'Importer tall fra fil…': 'Zahlen importieren…', 'Eksporter som TXT…': 'Als TXT exportieren…', 'Eksporter som CSV…': 'Als CSV exportieren…', 'Zoom inn': 'Vergrößern', 'Zoom ut': 'Verkleinern', 'Fullskjerm': 'Vollbild', 'Innstillinger…': 'Einstellungen…', 'Hjelp og hurtigtaster': 'Hilfe und Tastenkürzel', 'Om programmet': 'Über das Programm', 'Historikk': 'Verlauf', 'Enhetsomregner': 'Einheitenumrechner', 'Tilfeldige tall…': 'Zufallszahlen…', 'Matematisk ordbok…': 'Mathematisches Wörterbuch…'})
UI_TRANSLATIONS.setdefault('fr', {}).update({'Fil': 'Fichier', 'Rediger': 'Édition', 'Vis': 'Affichage', 'Hjelp': 'Aide', 'Avslutt': 'Quitter', 'Importer tall fra fil…': 'Importer des nombres…', 'Eksporter som TXT…': 'Exporter en TXT…', 'Eksporter som CSV…': 'Exporter en CSV…', 'Zoom inn': 'Agrandir', 'Zoom ut': 'Réduire', 'Fullskjerm': 'Plein écran', 'Innstillinger…': 'Paramètres…', 'Hjelp og hurtigtaster': 'Aide et raccourcis', 'Om programmet': 'À propos', 'Historikk': 'Historique', 'Enhetsomregner': 'Convertisseur d’unités', 'Tilfeldige tall…': 'Nombres aléatoires…', 'Matematisk ordbok…': 'Dictionnaire mathématique…'})
UI_TRANSLATIONS.setdefault('es', {}).update({'Fil': 'Archivo', 'Rediger': 'Editar', 'Vis': 'Ver', 'Hjelp': 'Ayuda', 'Avslutt': 'Salir', 'Importer tall fra fil…': 'Importar números…', 'Eksporter som TXT…': 'Exportar como TXT…', 'Eksporter som CSV…': 'Exportar como CSV…', 'Zoom inn': 'Acercar', 'Zoom ut': 'Alejar', 'Fullskjerm': 'Pantalla completa', 'Innstillinger…': 'Configuración…', 'Hjelp og hurtigtaster': 'Ayuda y atajos', 'Om programmet': 'Acerca del programa', 'Historikk': 'Historial', 'Enhetsomregner': 'Conversor de unidades', 'Tilfeldige tall…': 'Números aleatorios…', 'Matematisk ordbok…': 'Diccionario matemático…'})
UI_TRANSLATIONS.setdefault('ar', {}).update({'Fil': 'ملف', 'Rediger': 'تحرير', 'Vis': 'عرض', 'Hjelp': 'مساعدة', 'Avslutt': 'خروج', 'Importer tall fra fil…': 'استيراد الأرقام…', 'Eksporter som TXT…': 'تصدير TXT…', 'Eksporter som CSV…': 'تصدير CSV…', 'Zoom inn': 'تكبير', 'Zoom ut': 'تصغير', 'Fullskjerm': 'ملء الشاشة', 'Innstillinger…': 'الإعدادات…', 'Hjelp og hurtigtaster': 'المساعدة والاختصارات', 'Om programmet': 'حول البرنامج', 'Historikk': 'السجل', 'Enhetsomregner': 'محول الوحدات', 'Tilfeldige tall…': 'أرقام عشوائية…', 'Matematisk ordbok…': 'قاموس الرياضيات…'})
UI_TRANSLATIONS.setdefault('sv', {}).update({'Fil': 'Arkiv', 'Rediger': 'Redigera', 'Vis': 'Visa', 'Hjelp': 'Hjälp', 'Avslutt': 'Avsluta', 'Importer tall fra fil…': 'Importera tal…', 'Eksporter som TXT…': 'Exportera som TXT…', 'Eksporter som CSV…': 'Exportera som CSV…', 'Zoom inn': 'Zooma in', 'Zoom ut': 'Zooma ut', 'Fullskjerm': 'Helskärm', 'Innstillinger…': 'Inställningar…', 'Hjelp og hurtigtaster': 'Hjälp och kortkommandon', 'Om programmet': 'Om programmet', 'Historikk': 'Historik', 'Enhetsomregner': 'Enhetsomvandlare', 'Tilfeldige tall…': 'Slumptal…', 'Matematisk ordbok…': 'Matematisk ordlista…'})
UI_TRANSLATIONS.setdefault('da', {}).update({'Fil': 'Filer', 'Rediger': 'Rediger', 'Vis': 'Vis', 'Hjelp': 'Hjælp', 'Avslutt': 'Afslut', 'Importer tall fra fil…': 'Importér tal…', 'Eksporter som TXT…': 'Eksportér som TXT…', 'Eksporter som CSV…': 'Eksportér som CSV…', 'Zoom inn': 'Zoom ind', 'Zoom ut': 'Zoom ud', 'Fullskjerm': 'Fuldskærm', 'Innstillinger…': 'Indstillinger…', 'Hjelp og hurtigtaster': 'Hjælp og genveje', 'Om programmet': 'Om programmet', 'Historikk': 'Historik', 'Enhetsomregner': 'Enhedsomregner', 'Tilfeldige tall…': 'Tilfældige tal…', 'Matematisk ordbok…': 'Matematisk ordbog…'})
UI_TRANSLATIONS.setdefault('it', {}).update({'Fil': 'File', 'Rediger': 'Modifica', 'Vis': 'Visualizza', 'Hjelp': 'Aiuto', 'Avslutt': 'Esci', 'Importer tall fra fil…': 'Importa numeri…', 'Eksporter som TXT…': 'Esporta come TXT…', 'Eksporter som CSV…': 'Esporta come CSV…', 'Zoom inn': 'Ingrandisci', 'Zoom ut': 'Riduci', 'Fullskjerm': 'Schermo intero', 'Innstillinger…': 'Impostazioni…', 'Hjelp og hurtigtaster': 'Aiuto e scorciatoie', 'Om programmet': 'Informazioni', 'Historikk': 'Cronologia', 'Enhetsomregner': 'Convertitore di unità', 'Tilfeldige tall…': 'Numeri casuali…', 'Matematisk ordbok…': 'Dizionario matematico…'})
UI_TRANSLATIONS.setdefault('pt', {}).update({'Fil': 'Ficheiro', 'Rediger': 'Editar', 'Vis': 'Ver', 'Hjelp': 'Ajuda', 'Avslutt': 'Sair', 'Importer tall fra fil…': 'Importar números…', 'Eksporter som TXT…': 'Exportar como TXT…', 'Eksporter som CSV…': 'Exportar como CSV…', 'Zoom inn': 'Ampliar', 'Zoom ut': 'Reduzir', 'Fullskjerm': 'Ecrã inteiro', 'Innstillinger…': 'Configurações…', 'Hjelp og hurtigtaster': 'Ajuda e atalhos', 'Om programmet': 'Sobre o programa', 'Historikk': 'Histórico', 'Enhetsomregner': 'Conversor de unidades', 'Tilfeldige tall…': 'Números aleatórios…', 'Matematisk ordbok…': 'Dicionário matemático…'})
UI_TRANSLATIONS.setdefault('nl', {}).update({'Fil': 'Bestand', 'Rediger': 'Bewerken', 'Vis': 'Beeld', 'Hjelp': 'Help', 'Avslutt': 'Afsluiten', 'Importer tall fra fil…': 'Getallen importeren…', 'Eksporter som TXT…': 'Exporteren als TXT…', 'Eksporter som CSV…': 'Exporteren als CSV…', 'Zoom inn': 'Inzoomen', 'Zoom ut': 'Uitzoomen', 'Fullskjerm': 'Volledig scherm', 'Innstillinger…': 'Instellingen…', 'Hjelp og hurtigtaster': 'Help en sneltoetsen', 'Om programmet': 'Over het programma', 'Historikk': 'Geschiedenis', 'Enhetsomregner': 'Eenheden omrekenen', 'Tilfeldige tall…': 'Willekeurige getallen…', 'Matematisk ordbok…': 'Wiskundig woordenboek…'})


def tr(tekst):
    språk = settings.get("language", "nb")
    if språk == "nb":
        return tekst
    return UI_TRANSLATIONS.get(språk, {}).get(tekst, tekst)


def oversett_meny(meny):
    try:
        antall = meny.index("end")
        if antall is None:
            return
        for indeks in range(antall + 1):
            typ = meny.type(indeks)
            if typ in ("command", "cascade", "checkbutton", "radiobutton"):
                label = meny.entrycget(indeks, "label")
                # Keep the selected-language checkmark intact.
                prefix = "✓ " if label.startswith("✓ ") else ""
                ren = label[2:] if prefix else label
                oversatt = tr(ren)
                if oversatt != ren:
                    meny.entryconfigure(indeks, label=prefix + oversatt)
                if typ == "cascade":
                    try:
                        oversett_meny(meny.nametowidget(meny.entrycget(indeks, "menu")))
                    except (KeyError, tk.TclError):
                        pass
    except tk.TclError:
        pass

def velg_sprak(kode):
    if kode not in LANGUAGES:
        return
    settings["language"] = kode
    save_settings()
    rebuild_interface()
    status_var.set("Language changed." if kode == "en" else "Språk endret.")

def oversett_widget_tre(widget):
    """Oversetter synlige widget-etiketter etter at vinduet er bygget."""
    try:
        tekst = widget.cget("text")
        if tekst:
            ny = tr(tekst)
            if ny != tekst:
                widget.configure(text=ny)
    except (tk.TclError, TypeError):
        pass
    try:
        for barn in widget.winfo_children():
            oversett_widget_tre(barn)
    except tk.TclError:
        pass


settings = {}
historikk = []


def load_settings():

    global settings

    settings = json.loads(json.dumps(DEFAULT_SETTINGS))

    if os.path.exists(SETTINGS_FILE):

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:

                saved = json.load(file)

            for key in DEFAULT_SETTINGS:

                if key == "features":
                    settings["features"].update(saved.get("features", {}))

                elif key in saved:
                    settings[key] = saved[key]

        except (OSError, json.JSONDecodeError, AttributeError):
            pass


def save_settings():

    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:

            json.dump(settings, file, indent=4, ensure_ascii=False)

        return True

    except OSError:

        messagebox.showerror("Lagringsfeil", "Kunne ikke lagre innstillingene.")

        return False


def last_historikk():

    global historikk

    historikk = []

    if os.path.exists(HISTORY_FILE):

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:

                data = json.load(file)

            if isinstance(data, list):
                historikk = [
                    h
                    for h in data
                    if isinstance(h, dict) and "tekst" in h and "tid" in h
                ][-HISTORIKK_MAKS:]

        except (OSError, json.JSONDecodeError):
            historikk = []


def lagre_historikk():

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:

            json.dump(historikk[-HISTORIKK_MAKS:], file, indent=2, ensure_ascii=False)

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

    return (settings["font"], settings["title_size"], "bold")


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
        text=tr(tekst),
        variable=var,
        bg=bg,
        fg=color("text"),
        activebackground=bg,
        activeforeground=color("text"),
        selectcolor=color("panel_light"),
        font=font(9),
        highlightthickness=0,
        bd=0,
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

    return sortert[nedre] + (sortert[ovre] - sortert[nedre]) * (k - nedre)


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
        "retning": "stigende",
    }

    # KVARTILER

    if antall >= 2:

        midten = antall // 2

        nedre = tall[:midten]

        if antall % 2 == 0:
            ovre = tall[midten:]
        else:
            ovre = tall[midten + 1 :]

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
            x for x in tall if x < data["ut_lav"] or x > data["ut_hoy"]
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

    data["utvalgs_std"] = statistics.stdev(tall) if antall >= 2 else None

    data["standardfeil"] = (
        data["utvalgs_std"] / math.sqrt(antall)
        if data["utvalgs_std"] is not None
        else None
    )

    data["geometrisk"] = (
        math.exp(sum(math.log(x) for x in tall) / antall)
        if all(x > 0 for x in tall)
        else None
    )

    data["harmonisk"] = (
        antall / sum(1 / x for x in tall) if all(x > 0 for x in tall) else None
    )

    data["skjevhet"] = (
        (sum((x - snitt) ** 3 for x in tall) / antall) / sd ** 3 if sd > 0 else None
    )

    data["variasjonskoeffisient"] = sd / abs(snitt) * 100 if snitt != 0 else None

    data["mad"] = sum(abs(x - snitt) for x in tall) / antall

    # PERSENTILER

    for p in (5, 10, 90, 95):
        data[f"p{p}"] = persentil(tall, p)

    return data


def typetall_tekst(data):

    if data["antall"] > 1 and len(data["typetall"]) == len(data["frekvens"]):
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
    legg("variasjonsbredde", "Variasjonsbredde", data["variasjonsbredde"])

    if f["quartiles"]:

        rader.extend(
            [
                ("Q1", formater(data["q1"])),
                ("Q2", formater(data["q2"])),
                ("Q3", formater(data["q3"])),
                ("Kvartilbredde (IQR)", formater(data["iqr"])),
            ]
        )

    if f["variance"]:

        rader.extend(
            [
                ("Varians", formater(data["varians"])),
                ("Standardavvik", formater(data["standardavvik"])),
            ]
        )

    if f["extra"]:

        rader.extend(
            [
                ("Utvalgsstandardavvik", formater(data["utvalgs_std"])),
                ("Standardfeil", formater(data["standardfeil"])),
                ("Geometrisk snitt", formater(data["geometrisk"])),
                ("Harmonisk snitt", formater(data["harmonisk"])),
                ("Skjevhet", formater(data["skjevhet"])),
                ("Variasjonskoeffisient (%)", formater(data["variasjonskoeffisient"])),
                ("Gj.snittlig avvik", formater(data["mad"])),
            ]
        )

    if f["percentiles"]:

        rader.extend(
            [
                ("5. persentil", formater(data["p5"])),
                ("10. persentil", formater(data["p10"])),
                ("90. persentil", formater(data["p90"])),
                ("95. persentil", formater(data["p95"])),
            ]
        )

    if f["outliers"]:

        rader.append(("Uteliggere", formater(data["uteliggere"])))

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

    historikk.append(
        {"tid": datetime.now().strftime("%d.%m.%Y %H:%M:%S"), "tekst": tekst}
    )

    del historikk[:-HISTORIKK_MAKS]

    lagre_historikk()


def sorter_tall(retning="stigende"):

    global siste_resultat

    input_text = entry.get().strip()

    if sjekk_easter_egg(input_text):
        return

    if not input_text:

        messagebox.showwarning("Mangler tall", "Skriv inn noen tall først.")

        return

    tall = []
    ugyldige = []

    for verdi in input_text.replace(",", " ").replace(";", " ").split():

        try:

            tallverdi = float(verdi)

            if not math.isfinite(tallverdi):
                ugyldige.append(verdi)
                continue

            tall.append(tallverdi)

        except ValueError:
            ugyldige.append(verdi)

    if not tall:

        messagebox.showerror("Feil", "Ingen gyldige tall ble funnet.")

        return

    if len(tall) > MAX_TALL:

        messagebox.showwarning(
            "Maks antall", f"Du kan registrere maksimalt {MAX_TALL} tall."
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

        messagebox.showerror("Ugyldig filter", "Filterverdiene må være tall.")

        return

    for_filter = len(tall)

    if filter_min is not None:
        tall = [x for x in tall if x >= filter_min]

    if filter_maks is not None:
        tall = [x for x in tall if x <= filter_maks]

    if len(tall) < for_filter:
        meldinger.append(f"{for_filter - len(tall)} fjernet av filteret.")

    # AVRUNDING OG DUPLIKATER

    if avrund_var.get():
        tall = [float(math.floor(x + 0.5)) for x in tall]

    if dup_var.get():

        unike = list(dict.fromkeys(tall))

        if len(unike) < len(tall):
            meldinger.append(f"{len(tall) - len(unike)} duplikater fjernet.")

        tall = unike

    if not tall:

        messagebox.showerror("Ingen tall igjen", "Filteret fjernet alle tallene.")

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


def lag_knapp(parent, tekst, funksjon, farge=None):

    bakgrunn = farge or color("accent")

    if bakgrunn == color("panel_light"):
        tekstfarge = color("text")
    else:
        tekstfarge = "white"

    return tk.Button(
        parent,
        text=tr(tekst),
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
        cursor="hand2",
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

        kort = tk.Frame(stats_frame, bg=color("panel_light"), padx=12, pady=12)

        kort.grid(row=rad, column=kolonne, sticky="nsew", padx=5, pady=5)

        tk.Label(
            kort, text=navn, bg=color("panel_light"), fg=color("muted"), font=font(9)
        ).pack(anchor="w")

        tk.Label(
            kort,
            text=verdi,
            bg=color("panel_light"),
            fg=color("text"),
            font=font(settings["font_size"] + 2, True),
            wraplength=220,
            justify="left",
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
            "", "end", values=(formater(tall), antall, f"{prosent:.2f}%")
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
            font=font(11),
        )

        return

    antall_bins = min(10, max(2, int(antall ** 0.5)))

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
        margin, hoyde - margin, bredde - margin, hoyde - margin, fill=color("muted")
    )

    for i, verdi in enumerate(bins):

        stolkehoyde = (verdi / maks) * tilgjengelig_hoyde

        x1 = margin + i * stolkebredde + 3
        x2 = margin + (i + 1) * stolkebredde - 3

        y1 = hoyde - margin - stolkehoyde
        y2 = hoyde - margin

        histogram.create_rectangle(x1, y1, x2, y2, fill=color("accent"), outline="")

        histogram.create_text(
            (x1 + x2) / 2, y1 - 10, text=str(verdi), fill=color("text"), font=font(9)
        )

    histogram.create_text(
        bredde / 2,
        hoyde - 10,
        text=f"Verdiområde: {formater(lav)} – {formater(hoy)}",
        fill=color("muted"),
        font=font(9),
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
            font=font(10),
        )

        return

    lav = data["minimum"]
    hoy = data["maksimum"]

    margin = 40

    def x(verdi):
        return margin + (verdi - lav) / (hoy - lav) * (bredde - 2 * margin)

    midt = hoyde / 2 - 5

    normale = [v for v in data["tall"] if data["ut_lav"] <= v <= data["ut_hoy"]]

    if normale:
        hvisker_lav = min(normale)
        hvisker_hoy = max(normale)
    else:
        hvisker_lav = data["q1"]
        hvisker_hoy = data["q3"]

    boxplot_canvas.create_line(
        x(hvisker_lav), midt, x(hvisker_hoy), midt, fill=color("muted"), width=2
    )

    for verdi in (hvisker_lav, hvisker_hoy):

        boxplot_canvas.create_line(
            x(verdi), midt - 10, x(verdi), midt + 10, fill=color("muted"), width=2
        )

    boxplot_canvas.create_rectangle(
        x(data["q1"]),
        midt - 18,
        x(data["q3"]),
        midt + 18,
        fill=color("accent"),
        outline=color("text"),
    )

    boxplot_canvas.create_line(
        x(data["q2"]), midt - 18, x(data["q2"]), midt + 18, fill="white", width=3
    )

    for verdi in data["uteliggere"]:

        boxplot_canvas.create_oval(
            x(verdi) - 4,
            midt - 4,
            x(verdi) + 4,
            midt + 4,
            outline=color("red"),
            width=2,
        )

    for verdi, tekst in (
        (lav, formater(lav)),
        (data["q2"], f"Median {formater(data['q2'])}"),
        (hoy, formater(hoy)),
    ):

        boxplot_canvas.create_text(
            x(verdi), midt + 34, text=tekst, fill=color("muted"), font=font(8)
        )


# ============================================================
# SORTERTE TALL
# ============================================================


def vis_sorterte_tall(data):

    sorted_text.configure(state="normal")
    sorted_text.delete("1.0", tk.END)

    resultat = ", ".join(formater(x) for x in data["tall"])

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

            tekst += f"{formater(tall)}: {antall} " f"({prosent:.2f}%)\n"

    return tekst


def kopier_resultater():

    if not settings["features"]["copy"]:
        return

    tekst = lag_resultattekst()

    if not tekst:
        messagebox.showwarning("Ingen resultater", "Sorter tall først.")
        return

    root.clipboard_clear()
    root.clipboard_append(tekst)

    status_var.set("Resultatene er kopiert.")


def eksporter_resultater():

    if not settings["features"]["export"]:
        return

    tekst = lag_resultattekst()

    if not tekst:
        messagebox.showwarning("Ingen resultater", "Sorter tall først.")
        return

    fil = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Tekstfiler", "*.txt"), ("Alle filer", "*.*")],
        title="Lagre resultater",
    )

    if fil:

        try:

            with open(fil, "w", encoding="utf-8") as f:

                f.write(tekst)

            status_var.set("Resultatene er eksportert.")

        except OSError as error:

            messagebox.showerror("Eksportfeil", str(error))


def eksporter_csv():

    if not settings["features"]["csv"]:
        return

    if siste_resultat is None:
        messagebox.showwarning("Ingen resultater", "Sorter tall først.")
        return

    fil = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV-filer", "*.csv"), ("Alle filer", "*.*")],
        title="Lagre som CSV",
    )

    if not fil:
        return

    data = siste_resultat

    try:

        with open(fil, "w", encoding="utf-8-sig", newline="") as f:

            skriver = csv.writer(f, delimiter=";")

            skriver.writerow(["Statistikk", "Verdi"])

            for navn, verdi in bygg_statistikkliste(data):
                skriver.writerow([navn, verdi])

            skriver.writerow([])
            skriver.writerow(["Tall", "Antall", "Prosent"])

            for tall, antall in sorted(data["frekvens"].items()):

                prosent = antall / data["antall"] * 100

                skriver.writerow(
                    [formater(tall), antall, f"{prosent:.2f}".replace(".", ",")]
                )

        status_var.set("CSV-filen er lagret.")

    except OSError as error:

        messagebox.showerror("Eksportfeil", str(error))


def importer_fil():

    if not settings["features"]["import"]:
        return

    fil = filedialog.askopenfilename(
        title="Velg fil med tall",
        filetypes=[("Tekst/CSV", "*.txt *.csv *.dat"), ("Alle filer", "*.*")],
    )

    if not fil:
        return

    try:

        with open(fil, "r", encoding="utf-8-sig", errors="replace") as f:

            innhold = f.read()

    except OSError as error:

        messagebox.showerror("Importfeil", str(error))
        return

    funnet = re.findall(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", innhold)

    if not funnet:

        messagebox.showwarning("Ingen tall", "Fant ingen tall i filen.")

        return

    if len(funnet) > MAX_TALL:

        funnet = funnet[:MAX_TALL]

        messagebox.showinfo(
            "Avkortet",
            f"Filen hadde for mange tall. " f"Bare de første {MAX_TALL} ble importert.",
        )

    entry.delete(0, tk.END)
    entry.insert(0, " ".join(funnet))

    status_var.set(f"Importerte {len(funnet)} tall fra " f"{os.path.basename(fil)}.")


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
    ast.UAdd: operator.pos,
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
    "e": lambda: math.e,
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

            return OPERATORS[operator_type](venstre, hoyre)

        if isinstance(node, ast.UnaryOp):

            operator_type = type(node.op)

            if operator_type not in OPERATORS:
                raise ValueError("Ugyldig operasjon")

            return OPERATORS[operator_type](beregn(node.operand))

        if isinstance(node, ast.Call):

            if not isinstance(node.func, ast.Name):
                raise ValueError("Ugyldig funksjon")

            navn = node.func.id

            if navn not in KALK_FUNKSJONER:
                raise ValueError("Ukjent funksjon")

            if node.keywords:
                raise ValueError("Ugyldig argument")

            argumenter = [beregn(arg) for arg in node.args]

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

    window = nytt_vindu("Kalkulator - Tall Sorterer", "400x700", (340, 560))

    uttrykk_var = tk.StringVar()
    resultat_var = tk.StringVar(value="Klar")
    historie_var = tk.StringVar(value="")
    kalk_historie = []

    # DISPLAY

    display = tk.Frame(window, bg=color("panel"), padx=15, pady=15)

    display.pack(fill="x", padx=15, pady=15)

    kalk_entry = tk.Entry(
        display,
        textvariable=uttrykk_var,
        justify="right",
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(20),
    )

    kalk_entry.pack(fill="x", ipady=12)
    kalk_entry.focus_set()

    tk.Label(
        display,
        textvariable=resultat_var,
        bg=color("panel"),
        fg=color("green"),
        font=font(12),
    ).pack(anchor="e", pady=(10, 0))

    tk.Label(
        display,
        textvariable=historie_var,
        bg=color("panel"),
        fg=color("muted"),
        font=font(8),
        justify="right",
    ).pack(anchor="e", pady=(6, 0))

    # BEREGNING

    def beregn():

        uttrykk = uttrykk_var.get().strip()

        if not uttrykk:
            return

        try:

            uttrykk_py = uttrykk.replace("^", "**")

            resultat = sikker_beregning(uttrykk_py, kalk_minne["ans"])

            kalk_minne["ans"] = resultat

            resultat_var.set("= " + kalk_format(resultat))

            kalk_historie.append(f"{uttrykk} = {kalk_format(resultat)}")

            historie_var.set("\n".join(kalk_historie[-3:]))

        except ZeroDivisionError:

            resultat_var.set("Kan ikke dele på null")

        except (ValueError, TypeError, SyntaxError, OverflowError, RecursionError):

            resultat_var.set("Ugyldig regnestykke")

    # KNAPPFUNKSJONER

    def legg_til(verdi):

        uttrykk_var.set(uttrykk_var.get() + verdi)

        kalk_entry.icursor(tk.END)

    def slett():

        uttrykk_var.set("")
        resultat_var.set("Klar")

    def tilbake():

        uttrykk_var.set(uttrykk_var.get()[:-1])

    def bruk_resultat():

        try:

            uttrykk = uttrykk_var.get().replace("^", "**")

            resultat = sikker_beregning(uttrykk, kalk_minne["ans"])

            uttrykk_var.set(kalk_format(resultat))
            resultat_var.set("Resultatet er satt inn")

        except Exception:

            resultat_var.set("Kan ikke bruke resultatet")

    def send_til_tallfelt():

        try:

            uttrykk = uttrykk_var.get().replace("^", "**")

            resultat = sikker_beregning(uttrykk, kalk_minne["ans"])

            gammel = entry.get().strip()

            entry.delete(0, tk.END)
            entry.insert(0, (gammel + " " if gammel else "") + kalk_format(resultat))

            resultat_var.set("Lagt til i tallfeltet")

        except Exception:

            resultat_var.set("Kan ikke sende resultatet")

    # KNAPPEOPPSETT

    button_frame = tk.Frame(window, bg=color("bg"), padx=12)

    button_frame.pack(fill="both", expand=True)

    knapper = [
        ["C", "(", ")", "⌫"],
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "%", "+"],
        ["sqrt(", "^", "pi()", "="],
        ["ans", "exp(", "ln(", "log("],
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

        button_frame.rowconfigure(rad_index, weight=1)

        for kol_index, verdi in enumerate(rad):

            button_frame.columnconfigure(kol_index, weight=1)

            er_lik = verdi == "="

            knapp = tk.Button(
                button_frame,
                text=verdi,
                command=lambda v=verdi: knappetrykk(v),
                bg=(color("accent") if er_lik else color("panel_light")),
                fg="white" if er_lik else color("text"),
                activebackground="#5475E8",
                relief="flat",
                font=font(12, True),
            )

            knapp.grid(row=rad_index, column=kol_index, sticky="nsew", padx=3, pady=3)

    # EKSTRA FUNKSJONER

    extra = tk.Frame(window, bg=color("bg"), padx=15, pady=10)

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
        justify="left",
    ).pack(anchor="w")

    lag_knapp(extra, "Bruk resultat", bruk_resultat, color("green")).pack(
        fill="x", pady=(8, 0)
    )

    lag_knapp(
        extra, "Send til tallfeltet", send_til_tallfelt, color("panel_light")
    ).pack(fill="x", pady=(6, 0))

    window.bind("<Return>", lambda event: beregn())
    window.bind("<Escape>", lambda event: slett())


# ============================================================
# ENHETSOMREGNER
# ============================================================

ENHETER = {
    "Lengde": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "tomme": 0.0254,
        "fot": 0.3048,
        "yard": 0.9144,
        "engelsk mil": 1609.344,
        "nautisk mil": 1852.0,
        "norsk mil": 10000.0,
    },
    "Vekt": {
        "mg": 1e-6,
        "g": 1e-3,
        "kg": 1.0,
        "tonn": 1000.0,
        "unse": 0.028349523125,
        "pund": 0.45359237,
        "stone": 6.35029318,
    },
    "Volum": {
        "ml": 0.001,
        "cl": 0.01,
        "dl": 0.1,
        "liter": 1.0,
        "m³": 1000.0,
        "US gallon": 3.785411784,
        "US pint": 0.473176473,
    },
    "Tid": {
        "ms": 0.001,
        "sekund": 1.0,
        "minutt": 60.0,
        "time": 3600.0,
        "døgn": 86400.0,
        "uke": 604800.0,
    },
    "Hastighet": {"m/s": 1.0, "km/t": 1 / 3.6, "mph": 0.44704, "knop": 0.514444},
    "Temperatur": {"°C": None, "°F": None, "K": None},
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

    window = nytt_vindu("Enhetsomregner", "420x420", (380, 380))

    ramme = tk.Frame(window, bg=color("panel"), padx=18, pady=18)

    ramme.pack(fill="both", expand=True, padx=15, pady=15)

    kategori_var = tk.StringVar(value="Lengde")
    fra_var = tk.StringVar()
    til_var = tk.StringVar()
    verdi_var = tk.StringVar(value="1")
    resultat_var = tk.StringVar(value="")

    def etikett(tekst):

        tk.Label(
            ramme, text=tekst, bg=color("panel"), fg=color("muted"), font=font(9)
        ).pack(anchor="w", pady=(8, 2))

    etikett("Kategori")

    kategori_combo = ttk.Combobox(
        ramme, textvariable=kategori_var, values=list(ENHETER.keys()), state="readonly"
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
        font=font(12),
    ).pack(fill="x", ipady=6)

    etikett("Fra")

    fra_combo = ttk.Combobox(ramme, textvariable=fra_var, state="readonly")

    fra_combo.pack(fill="x")

    etikett("Til")

    til_combo = ttk.Combobox(ramme, textvariable=til_var, state="readonly")

    til_combo.pack(fill="x")

    tk.Label(
        ramme,
        textvariable=resultat_var,
        bg=color("panel"),
        fg=color("green"),
        font=font(14, True),
        wraplength=340,
    ).pack(pady=(18, 8))

    def omregn(*args):

        try:

            verdi = float(verdi_var.get().replace(",", "."))

            kategori = kategori_var.get()
            fra = fra_var.get()
            til = til_var.get()

            if kategori == "Temperatur":

                svar = temp_fra_celsius(temp_til_celsius(verdi, fra), til)

            else:

                tabell = ENHETER[kategori]

                svar = verdi * tabell[fra] / tabell[til]

            resultat_var.set(f"{formater(verdi)} {fra} = {kalk_format(svar)} {til}")

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

    lag_knapp(ramme, "Send til tallfeltet", send_til_tallfelt, color("accent")).pack(
        fill="x"
    )

    bytt_kategori()


# ============================================================
# TILFELDIGE TALL
# ============================================================


def apne_tilfeldig():

    if not settings["features"]["random"]:
        return

    window = nytt_vindu("Tilfeldige tall", "380x420", (340, 400))

    ramme = tk.Frame(window, bg=color("panel"), padx=18, pady=18)

    ramme.pack(fill="both", expand=True, padx=15, pady=15)

    antall_var = tk.StringVar(value="20")
    min_var = tk.StringVar(value="0")
    maks_var = tk.StringVar(value="100")
    heltall_var = tk.BooleanVar(value=True)
    auto_var = tk.BooleanVar(value=True)

    def felt(tekst, var):

        tk.Label(
            ramme, text=tekst, bg=color("panel"), fg=color("muted"), font=font(9)
        ).pack(anchor="w", pady=(8, 2))

        tk.Entry(
            ramme,
            textvariable=var,
            bg=color("panel_light"),
            fg=color("text"),
            insertbackground=color("text"),
            relief="flat",
            font=font(11),
        ).pack(fill="x", ipady=5)

    felt(f"Antall tall (1–{MAX_TALL})", antall_var)
    felt("Laveste verdi", min_var)
    felt("Høyeste verdi", maks_var)

    lag_sjekk(ramme, "Bare heltall", heltall_var, color("panel")).pack(
        anchor="w", pady=(12, 0)
    )

    lag_sjekk(ramme, "Sorter automatisk etterpå", auto_var, color("panel")).pack(
        anchor="w"
    )

    def generer():

        try:

            n = int(antall_var.get())
            lav = float(min_var.get().replace(",", "."))
            hoy = float(maks_var.get().replace(",", "."))

        except ValueError:

            messagebox.showerror(
                "Ugyldige verdier", "Kontroller antall og grenser.", parent=window
            )

            return

        if n < 1 or n > MAX_TALL:

            messagebox.showerror(
                "Ugyldig antall",
                f"Antall må være mellom 1 og {MAX_TALL}.",
                parent=window,
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
                    parent=window,
                )

                return

            tall = [str(random.randint(lav_i, hoy_i)) for _ in range(n)]

        else:

            tall = [str(round(random.uniform(lav, hoy), 2)) for _ in range(n)]

        entry.delete(0, tk.END)
        entry.insert(0, " ".join(tall))

        status_var.set(f"Genererte {n} tilfeldige tall.")

        window.destroy()

        if auto_var.get():
            sorter_tall("stigende")

    lag_knapp(ramme, "Generer", generer, color("green")).pack(fill="x", pady=(18, 0))

    window.bind("<Return>", lambda event: generer())


# ============================================================
# HISTORIKK
# ============================================================


def apne_historikk():

    if not settings["features"]["history"]:
        return

    window = nytt_vindu("Historikk", "620x460", (480, 340))

    tk.Label(
        window,
        text="TIDLIGERE INNDATA (dobbeltklikk for å laste inn)",
        bg=color("bg"),
        fg=color("text"),
        font=font(10, True),
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
        activestyle="none",
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
            "Tøm historikk", "Vil du slette hele historikken?", parent=window
        ):

            historikk.clear()
            lagre_historikk()
            fyll()

    liste.bind("<Double-Button-1>", last_inn)

    knapper = tk.Frame(window, bg=color("bg"))
    knapper.pack(fill="x", padx=15, pady=15)

    lag_knapp(knapper, "Last inn", last_inn).pack(side="left")

    lag_knapp(knapper, "Slett valgt", slett_valgt, color("panel_light")).pack(
        side="left", padx=8
    )

    lag_knapp(knapper, "Tøm alt", tom_alt, color("panel_light")).pack(side="right")

    fyll()


# ============================================================
# HJELP OG OM
# ============================================================

HJELP_TEKST = [
    ("h1", "Velkommen til Tall Sorterer"),
    (
        "p",
        "Programmet sorterer tall og regner ut en rekke statistiske "
        "verdier. Alt vises i oversikten under tallfeltet.\n",
    ),
    ("h2", "Slik bruker du programmet"),
    (
        "p",
        "1. Skriv inn tall i tallfeltet. Du kan skille dem med mellomrom, "
        "komma eller semikolon. Bruk punktum som desimaltegn.\n"
        "2. Trykk «Sorter stigende», «Sorter synkende» eller «Bland».\n"
        "3. Resultatene vises som kort, tabell, histogram og boksplott.\n"
        "4. Du kan kopiere eller eksportere resultatene som TXT eller CSV.\n",
    ),
    ("h2", "Valg under tallfeltet"),
    (
        "p",
        "• Fjern duplikater: beholder bare ett eksemplar av hvert tall.\n"
        "• Avrund til heltall: runder alle tall til nærmeste heltall.\n"
        "• Filter fra/til: fjerner tall utenfor det området du velger.\n",
    ),
    ("h2", "Statistikk forklart"),
    (
        "p",
        "• Gjennomsnitt: summen delt på antallet.\n"
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
        "• Uteliggere: verdier utenfor Q1 − 1,5·IQR og Q3 + 1,5·IQR.\n",
    ),
    ("h2", "Verktøy"),
    (
        "p",
        "• Kalkulator: trygg regnemaskin med funksjoner og «ans».\n"
        "• Enhetsomregner: lengde, vekt, volum, tid, hastighet og temperatur.\n"
        "• Tilfeldige tall: lager en tallrekke for deg.\n"
        "• Importer: leser tall fra en tekst- eller CSV-fil.\n"
        "• Historikk: lagrer de siste inndataene dine.\n",
    ),
    ("h2", "Hurtigtaster"),
    (
        "p",
        "Enter / Ctrl+Enter ........ Sorter stigende\n"
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
        "F11 ...................... Fullskjerm\n",
    ),
    ("h2", "Tips"),
    (
        "p",
        "• Du kan bytte tema under Vis → Tema.\n"
        "• Du kan skru av funksjoner du ikke trenger i innstillingene.\n"
        "• Programmet skjuler noen overraskelser. Prøv å skrive "
        "noen rare ting i tallfeltet, eller en gammel spillkode …\n",
    ),
]


def apne_hjelp():

    vindu = nytt_vindu("Hjelp - Tall Sorterer", "760x680", (520, 400))

    tekstfelt = tk.Text(
        vindu,
        wrap="word",
        bg=color("panel"),
        fg=color("text"),
        font=font(10),
        relief="flat",
        padx=18,
        pady=14,
    )

    rull = ttk.Scrollbar(vindu, command=tekstfelt.yview)
    tekstfelt.configure(yscrollcommand=rull.set)

    rull.pack(side="right", fill="y")
    tekstfelt.pack(fill="both", expand=True)

    tekstfelt.tag_configure(
        "h1", font=font(15, True), foreground=color("accent"), spacing1=10, spacing3=6
    )

    tekstfelt.tag_configure(
        "h2", font=font(11, True), foreground=color("green"), spacing1=12, spacing3=4
    )

    tekstfelt.tag_configure("p", spacing3=4)

    for stil, tekst in HJELP_TEKST:
        tekstfelt.insert(tk.END, tekst + "\n", stil)

    tekstfelt.configure(state="disabled")


def vis_om():

    messagebox.showinfo(
        "Om Tall Sorterer",
        f"Tall Sorterer {VERSJON}\n\n"
        "Statistikk, analyse, graftegning og matematikkverktøy.\n"
        "Inneholder verktøy for R1/R2-matematikk og en matematisk ordbok.\n"
        "Laget med Python og Tkinter.\n\n"
        "Hjelpemiddelbruk: Programmet kan brukes på del 2 av matematikkprøver når\n"
        "lærerens/skolens regler tillater slike digitale hjelpemidler. Det er ikke\n"
        "automatisk godkjent på alle prøver eller eksamener; kontroller alltid\n"
        "reglene som gjelder for den aktuelle vurderingen.\n\n"
        "Trykk F1 for hjelp.",
    )


# ============================================================
# EASTER EGGS
# ============================================================

DISCO_FARGER = [
    "#FF006E",
    "#FB5607",
    "#FFBE0B",
    "#8338EC",
    "#3A86FF",
    "#06D6A0",
    "#EF476F",
    "#118AB2",
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
            f"{root.winfo_screenwidth()}x" f"{root.winfo_screenheight()}+0+0"
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
            w / 2,
            h / 2,
            text="PETER ER EN IDIOT",
            fill=forgrunn,
            font=(settings["font"], max(28, int(w / 16)), "bold"),
            width=w - 80,
            justify="center",
        )

        flate.create_text(
            w / 2,
            h - 40,
            text="Trykk ESC eller klikk for å lukke",
            fill=forgrunn,
            font=font(12),
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

            r, g, b = colorsys.hsv_to_rgb((n * 0.02 + i / len(tekst)) % 1, 0.8, 1)

            farge = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

            flate.create_text(
                start + i * avstand,
                y,
                text=bokstav,
                fill=farge,
                font=(settings["font"], int(avstand * 0.9), "bold"),
            )

        flate.create_text(
            w / 2, h - 25, text="(ESC for å lukke)", fill="#888888", font=font(9)
        )

    animer(vindu, steg, 50, 160)


def egg_konfetti():

    vindu = lag_effektvindu("Johan-Olai", 800, 520, "#101426")

    flate = tk.Canvas(vindu, bg="#101426", highlightthickness=0)
    flate.pack(fill="both", expand=True)

    farger = [
        "#FFD700",
        "#FF6B6B",
        "#4ECDC4",
        "#6C8CFF",
        "#FF9F1C",
        "#C77DFF",
        "#55D6A7",
    ]

    deler = [
        {
            "x": random.uniform(0, 800),
            "y": random.uniform(-500, 0),
            "vx": random.uniform(-1.5, 1.5),
            "vy": random.uniform(2, 6),
            "f": random.choice(farger),
            "s": random.randint(5, 11),
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
                d["x"],
                d["y"],
                d["x"] + d["s"],
                d["y"] + d["s"] * 0.6,
                fill=d["f"],
                outline="",
            )

        puls = 1 + 0.08 * math.sin(n * 0.2)

        flate.create_text(
            w / 2,
            h / 2 - 20,
            text="JOHAN-OLAI ER SMART",
            fill="#FFD700",
            font=(settings["font"], int(w / 20 * puls), "bold"),
        )

        flate.create_text(
            w / 2,
            h / 2 + 50,
            text="IQ: 999+   ★ ★ ★",
            fill="white",
            font=font(18, True),
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
                    font=("Courier", 12, "bold"),
                )

                spor.append((id_, 0))

    animer(vindu, steg, 60, 200)


def egg_disco():

    vindu = lag_effektvindu("Disco", 700, 420, "#000000")

    tk.Label(
        vindu, text="D I S C O !", bg="black", fg="white", font=font(20, True)
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
            random.choice(celler).configure(bg=random.choice(DISCO_FARGER))

    animer(vindu, steg, 250, 48)


# Hver hemmelighet har sin egen illustrasjon, fargepalett og bevegelsesprofil.
# Symbolene er bevisst ulike; bevegelsen er valgt for å passe til motivet.
EGG_SCENER = {
    "MÅNELANDINGEN": ("🚀", "#071426", "#F7D774", "#8ED8FF", "launch"),
    "BERLINMUREN": ("🧱", "#171827", "#F2C14E", "#B9C4D0", "open"),
    "DEN KALDE KRIGEN": ("☢", "#111827", "#E76F51", "#9DB4C0", "orbit"),
    "INTERNETT": ("🌐", "#071D2B", "#45C4E8", "#A4F4D2", "orbit"),
    "KUNSTIG INTELLIGENS": ("🧠", "#10162D", "#9B8CFF", "#55E6D0", "pulse"),
    "SOSIALE MEDIER": ("💬", "#24152F", "#FF5D8F", "#70D6FF", "float"),
    "FAKE NEWS": ("📰", "#251B16", "#F4A261", "#F8EDE3", "flip"),
    "KILDEKRITIKK": ("🔎", "#182331", "#F4D35E", "#E8F1F2", "scan"),
    "KLIMAENDRINGER": ("🌍", "#092A25", "#69D18B", "#F4D35E", "orbit"),
    "PARISAVTALEN": ("🤝", "#102A27", "#69D18B", "#D9F99D", "join"),
    "BÆREKRAFT": ("♻", "#102A1D", "#62C370", "#D7F9C5", "rotate"),
    "DEN INDUSTRIELLE REVOLUSJON": ("⚙", "#25252A", "#F0A35E", "#D5DEE8", "gear"),
    "TRYKKPRESSE": ("📚", "#241C16", "#C99A5B", "#F3E9D2", "stamp"),
    "DEN FRANSKE REVOLUSJON": ("🏰", "#21151A", "#F04B55", "#F4D35E", "rise"),
    "GRUNNLOVEN": ("📜", "#211D17", "#D8B56D", "#FFF0C2", "unroll"),
    "UNIONSOPPLØSNINGEN": ("🇳🇴", "#14243A", "#E85D75", "#F4D35E", "wave"),
    "KVINNERS STEMMERETT": ("🗳", "#24172B", "#C77DFF", "#F4D35E", "drop"),
    "MENNESKERETTIGHETER": ("⚖", "#182238", "#8FB8ED", "#F4D35E", "balance"),
    "FN": ("🕊", "#10233A", "#7DB7E8", "#F5F7FA", "fly"),
    "ANDRE VERDENSKRIG": ("🕯", "#151923", "#D9E2F2", "#F5C76B", "flicker"),
    "D-DAGEN": ("⛴", "#172735", "#A8DADC", "#F1FAEE", "cross"),
    "ROSA PARKS": ("🚌", "#251D19", "#D7A86E", "#F4E1C1", "drive"),
    "NELSON MANDELA": ("🔓", "#17291F", "#77D69B", "#F4D35E", "unlock"),
    "APARTHEID": ("🚧", "#24191A", "#E76F51", "#F4D35E", "separate"),
    "BORGERRETTIGHETER": ("✊", "#251A22", "#D98CB3", "#F4D35E", "raise"),
    "TSJERNOBYL": ("☢", "#172019", "#A5C66B", "#F4D35E", "warning"),
    "COVID 19": ("🦠", "#102A2A", "#72D6C9", "#F1FAEE", "drift"),
    "VAKSINER": ("💉", "#102A2A", "#72D6C9", "#F1FAEE", "protect"),
    "DNA": ("🧬", "#10202E", "#7DE2D1", "#E5B8F4", "helix"),
    "PENICILLIN": ("🧫", "#102A2A", "#72D6C9", "#F1FAEE", "grow"),
    "TRANSISTOREN": ("🔌", "#071A13", "#65E572", "#D8FF9A", "spark"),
    "WORLD WIDE WEB": ("🕸", "#071D2B", "#45C4E8", "#A4F4D2", "connect"),
    "SMARTTELEFON": ("📱", "#151A2B", "#7AA2F7", "#E6EEFF", "notify"),
    "ROMKAPPLØPET": ("🛰", "#071426", "#8ED8FF", "#F7D774", "orbit"),
    "HENRIK IBSEN": ("🎭", "#24182D", "#E0A5CF", "#F4D35E", "curtain"),
    "EDVARD MUNCH": ("😱", "#281A24", "#F08A70", "#F8D49D", "wave"),
    "OL 1994": ("⛷", "#10251C", "#F4D35E", "#F7FFF7", "ski"),
    "SAMETINGET": ("🏛", "#14243A", "#E85D75", "#F4D35E", "rise"),
    "SAMEFOLKETS DAG": ("☀", "#14243A", "#E85D75", "#F4D35E", "sunrise"),
    "ALTAKONFLIKTEN": ("🌊", "#102333", "#A8DADC", "#F1FAEE", "surge"),
    "DEMOKRATI": ("🗳", "#1B2035", "#8FB8ED", "#F4D35E", "vote"),
    "YTRINGSFRIHET": ("📣", "#1B2035", "#8FB8ED", "#F4D35E", "sound"),
    "PERSONVERN": ("🔐", "#101B2B", "#8FB8ED", "#D9E2F2", "shield"),
    "KVANTEDATAMASKIN": ("⚛", "#10162D", "#9B8CFF", "#55E6D0", "quantum"),
    "FREMTIDEN": ("🔮", "#15162B", "#A78BFA", "#67E8F9", "portal"),
    "KUNSTIG INTELLIGENS 2026": ("🤖", "#10162D", "#9B8CFF", "#55E6D0", "robot"),
    "CHATGPT": ("💡", "#10162D", "#9B8CFF", "#55E6D0", "chat"),
    "DEEPFAKE": ("🎭", "#24182D", "#E0A5CF", "#F4D35E", "morph"),
    "ALGORITMER": ("🔀", "#071D2B", "#45C4E8", "#A4F4D2", "sort"),
    "DIGITALT FOTSPOR": ("👣", "#071D2B", "#45C4E8", "#A4F4D2", "footsteps"),
    "NETTVETT": ("🛡", "#10233A", "#7DB7E8", "#F5F7FA", "guard"),
    "CYBERSIKKERHET": ("🖥", "#071A13", "#65E572", "#D8FF9A", "firewall"),
    "PASSORD": ("🔑", "#101B2B", "#8FB8ED", "#D9E2F2", "key"),
    "TOFAKTOR": ("🔒", "#101B2B", "#8FB8ED", "#D9E2F2", "doublelock"),
    "BÆREKRAFTIG ENERGI": ("☀", "#092A25", "#69D18B", "#F4D35E", "solar"),
    "PARIS 2024": ("🏅", "#10251C", "#F4D35E", "#F7FFF7", "podium"),
    "EUROPA 2024": ("⚽", "#10251C", "#F4D35E", "#F7FFF7", "football"),
    "UKRAINA 2022": ("🌻", "#182238", "#F4D35E", "#6AA9E9", "sunflower"),
    "9 11": ("🕊", "#101B2B", "#D9E2F2", "#F5C76B", "memorial"),
    "EUROEN": ("€", "#17291F", "#77D69B", "#F4D35E", "coin"),
    "BREXIT": ("🚪", "#182238", "#8FB8ED", "#F4D35E", "exit"),
    "NOBELS FREDSPRIS": ("🏅", "#17291F", "#77D69B", "#F4D35E", "medal"),
    "OLJEFUNNET": ("🛢", "#22232A", "#F0A35E", "#D5DEE8", "drill"),
    "22 JULI": ("🌹", "#101B2B", "#D9E2F2", "#F5C76B", "rose"),
    "EIDSVOLL": ("📜", "#211D17", "#D8B56D", "#FFF0C2", "constitution"),
    "NANSEN": ("🧭", "#102333", "#A8DADC", "#F1FAEE", "compass"),
    "AMUNDSEN": ("🏔", "#102333", "#A8DADC", "#F1FAEE", "southpole"),
    "SVALBARD": ("🐻‍❄️", "#102333", "#A8DADC", "#F1FAEE", "ice"),
    "NATO": ("⭐", "#14243A", "#7DB7E8", "#F5F7FA", "alliance"),
    "JERNTEPPET": ("🪟", "#171827", "#B9C4D0", "#F2C14E", "curtain"),
    "GUTENBERG": ("📖", "#241C16", "#C99A5B", "#F3E9D2", "pages"),
    "RENESSANSEN": ("🎨", "#24182D", "#E0A5CF", "#F4D35E", "paint"),
    "SVARTEDAUDEN": ("⏳", "#211B24", "#A8A0B5", "#E6D5B8", "hourglass"),
    "VIKINGTIDEN": ("🛶", "#102333", "#A8DADC", "#F1FAEE", "sail"),
    "MAGNA CARTA": ("⚖", "#211D17", "#D8B56D", "#FFF0C2", "seal"),
    "INDUSTRIARBEID": ("🔧", "#22232A", "#F0A35E", "#D5DEE8", "wrench"),
    "8 TIMERS ARBEIDSDAG": ("🕗", "#22232A", "#F0A35E", "#D5DEE8", "clock"),
    "KVINNEBEVEGELSEN": ("⚖", "#24172B", "#C77DFF", "#F4D35E", "scales"),
    "STONEWALL": ("🏳️‍🌈", "#24172B", "#C77DFF", "#F4D35E", "pride"),
    "APOLLO 13": ("🧑‍🚀", "#071426", "#8ED8FF", "#F7D774", "capsule"),
    "HUBBLE": ("🔭", "#071426", "#8ED8FF", "#F7D774", "telescope"),
    "JAMES WEBB": ("🔬", "#071426", "#8ED8FF", "#F7D774", "mirror"),
    "MARSROVER": ("🤖", "#281C18", "#E58B55", "#F4D9B5", "rover"),
    "GENREDIGERING": ("✂", "#10202E", "#7DE2D1", "#E5B8F4", "scissors"),
    "MENNESKEGENOMET": ("🧬", "#10202E", "#7DE2D1", "#E5B8F4", "genome"),
    "ELEKTRISK BIL": ("🚗", "#10251C", "#69D18B", "#F4D35E", "electriccar"),
    "JERNBANEN": ("🚂", "#22232A", "#F0A35E", "#D5DEE8", "train"),
    "FLY": ("✈", "#102333", "#A8DADC", "#F1FAEE", "airplane"),
    "RADIO": ("📻", "#241C16", "#C99A5B", "#F3E9D2", "waves"),
    "FJERNSYN": ("📺", "#151A2B", "#7AA2F7", "#E6EEFF", "screen"),
    "MOBILTELEFON": ("☎", "#151A2B", "#7AA2F7", "#E6EEFF", "ring"),
    "OPEN SOURCE": ("🧩", "#071A13", "#65E572", "#D8FF9A", "assemble"),
    "LINUX": ("🐧", "#071A13", "#65E572", "#D8FF9A", "penguin"),
    "PYTHON": ("🐍", "#071A13", "#65E572", "#D8FF9A", "snake"),
    "NULL OG EN": ("01", "#071A13", "#65E572", "#D8FF9A", "binary"),
    'TUNG TUNG TUNG SAHUR': ('🥁', '#160F25', '#F0A6FF', '#FFE7A8', "brainrot_01"),
    'TRALALERO TRALALA': ('🦈', '#061B2C', '#42D9F5', '#E9FBFF', "brainrot_02"),
    'BOMBARDIRO CROCODILO': ('🐊', '#24110E', '#FF8B5C', '#FFE0A8', "brainrot_03"),
    'BONECA AMBALABU': ('🪆', '#20152C', '#D9A7FF', '#FFF0F7', "brainrot_04"),
    'LIRILI LARILA': ('🌵', '#122719', '#83D98C', '#F3F0A0', "brainrot_05"),
    'BRR BRR PATAPIM': ('🌳', '#10251D', '#6CD7A5', '#E6FFD8', "brainrot_06"),
    'CAPPUCCINO ASSASSINO': ('☕', '#2A160F', '#C78A5B', '#FFF1D0', "brainrot_07"),
    'BALLERINA CAPPUCCINA': ('🩰', '#26172B', '#FF9BD2', '#FFF0F8', "brainrot_08"),
    'CHIMPANZINI BANANINI': ('🍌', '#20200D', '#E6D65A', '#F5F1B8', "brainrot_09"),
    'BOMBOMBINI GUSINI': ('🪿', '#17212C', '#C9D7E8', '#FFFFFF', "brainrot_10"),
    'TRIPPI TROPPI': ('🌀', '#160F25', '#F0A6FF', '#FFE7A8', "brainrot_11"),
    'FRIGO CAMelo': ('🐪', '#061B2C', '#42D9F5', '#E9FBFF', "brainrot_12"),
    'GANGSTER FOOTERA': ('⚽', '#24110E', '#FF8B5C', '#FFE0A8', "brainrot_13"),
    'ORANGUTINI ANANASINI': ('🍍', '#20152C', '#D9A7FF', '#FFF0F7', "brainrot_14"),
    'LA VACA SATURNO SATURNITA': ('🪐', '#122719', '#83D98C', '#F3F0A0', "brainrot_15"),
    'Brr ES TEH PATIPUM': ('🫖', '#10251D', '#6CD7A5', '#E6FFD8', "brainrot_16"),
    'GIRAFFA CELESTE': ('🦒', '#2A160F', '#C78A5B', '#FFF1D0', "brainrot_17"),
    'TRULIMERO TRULICINA': ('🎭', '#26172B', '#FF9BD2', '#FFF0F8', "brainrot_18"),
    'TIGRULLINI WATERMELINI': ('🍉', '#20200D', '#E6D65A', '#F5F1B8', "brainrot_19"),
    'BOBRITO BANDITO': ('🦫', '#17212C', '#C9D7E8', '#FFFFFF', "brainrot_20"),
    'GLORBO FRUTTODRILLO': ('🍇', '#160F25', '#F0A6FF', '#FFE7A8', "brainrot_21"),
    'SPIONIRO GOLUBIRO': ('🕊', '#061B2C', '#42D9F5', '#E9FBFF', "brainrot_22"),
    'ZIBRA ZUBRA ZIBRALINA': ('🦓', '#24110E', '#FF8B5C', '#FFE0A8', "brainrot_23"),
    'TATATATA SAHUR': ('🥁', '#20152C', '#D9A7FF', '#FFF0F7', "brainrot_24"),
    'BONECA SPAGHETTI': ('🍝', '#122719', '#83D98C', '#F3F0A0', "brainrot_25"),
    'POT HOTSPOT': ('🍲', '#10251D', '#6CD7A5', '#E6FFD8', "brainrot_26"),
    'TRALALERO AQUATICO': ('🌊', '#2A160F', '#C78A5B', '#FFF1D0', "brainrot_27"),
    'CAPPUCCINO DISCO': ('🪩', '#26172B', '#FF9BD2', '#FFF0F8', "brainrot_28"),
    'BANANINI LASAGNINI': ('🍌', '#20200D', '#E6D65A', '#F5F1B8', "brainrot_29"),
    'CROCODILO BOMBARDINO': ('🎺', '#17212C', '#C9D7E8', '#FFFFFF', "brainrot_30"),
    'PENGUINO CACTUSINO': ('🐧', '#160F25', '#F0A6FF', '#FFE7A8', "brainrot_31"),
    'ESPRESSONA SIGNORA': ('☕', '#061B2C', '#42D9F5', '#E9FBFF', "brainrot_32"),
    'MACCHIATONE BALERONE': ('🎼', '#24110E', '#FF8B5C', '#FFE0A8', "brainrot_33"),
    'RINOCERONTE TOASTINO': ('🦏', '#20152C', '#D9A7FF', '#FFF0F7', "brainrot_34"),
    'TORTUGA NUCLEARA': ('🐢', '#122719', '#83D98C', '#F3F0A0', "brainrot_35"),
    'PAPPAGALLO BANANALLO': ('🦜', '#10251D', '#6CD7A5', '#E6FFD8', "brainrot_36"),
    'SPAGHETTI TORNADINI': ('🌪', '#2A160F', '#C78A5B', '#FFF1D0', "brainrot_37"),
    'MOZZARELLA DRAMMATICA': ('🧀', '#26172B', '#FF9BD2', '#FFF0F8', "brainrot_38"),
    'GATTO LAMPADINO': ('💡', '#20200D', '#E6D65A', '#F5F1B8', "brainrot_39"),
    'RANOCCHIO PIANINO': ('🐸', '#17212C', '#C9D7E8', '#FFFFFF', "brainrot_40"),
    'PIZZA ROTOLINO': ('🍕', '#160F25', '#F0A6FF', '#FFE7A8', "brainrot_41"),
    'TUBARONE MACCHINONE': ('⚙', '#061B2C', '#42D9F5', '#E9FBFF', "brainrot_42"),
    'PULCINO BANANOSO': ('🐥', '#24110E', '#FF8B5C', '#FFE0A8', "brainrot_43"),
    'MELONI BALLOONI': ('🍈', '#20152C', '#D9A7FF', '#FFF0F7', "brainrot_44"),
    'SAXOFONO CAFFEINO': ('🎷', '#122719', '#83D98C', '#F3F0A0', "brainrot_45"),
    'TROMBONI LIMONI': ('🎺', '#10251D', '#6CD7A5', '#E6FFD8', "brainrot_46"),
    'TUBATINO BASSOTTO': ('🎵', '#2A160F', '#C78A5B', '#FFF1D0', "brainrot_47"),
    'RAVIOLI VOLANTI': ('🥟', '#26172B', '#FF9BD2', '#FFF0F8', "brainrot_48"),
    'GNOCCHI COSMICI': ('🥔', '#20200D', '#E6D65A', '#F5F1B8', "brainrot_49"),
    'PAPPARDELLE SUPREME': ('🍝', '#17212C', '#C9D7E8', '#FFFFFF', "brainrot_50"),
}


def egg_generell_animasjon(frase, tittel, beskrivelse):
    """Spiller en dedikert, frase-spesifikk animasjon for hemmeligheten."""
    symbol, bg, aksent, lys, bevegelse = EGG_SCENER.get(
        frase, ("✦", "#071426", "#6C8CFF", "#DCEBFF", "pulse")
    )
    vindu = lag_effektvindu(f"Easter egg: {tittel}", 800, 540, bg)
    flate = tk.Canvas(vindu, bg=bg, highlightthickness=0)
    flate.pack(fill="both", expand=True)
    partikler = [
        [random.uniform(0.08, 0.92), random.uniform(0.16, 0.72), random.uniform(1.5, 4)]
        for _ in range(24)
    ]

    def steg(n):
        flate.delete("all")
        w, h = max(flate.winfo_width(), 600), max(flate.winfo_height(), 400)
        cx, cy = w * 0.5, h * 0.43
        t = n * 0.055
        # Hver scene får et eget bakteppe med partikler som følger motivet.
        for i, p in enumerate(partikler):
            p[1] += 0.0015 + (i % 4) * 0.00035
            if p[1] > 0.76:
                p[1] = 0.14
                p[0] = random.uniform(0.08, 0.92)
            rr = p[2] * (1 + 0.18 * math.sin(t + i))
            flate.create_oval(
                p[0] * w - rr,
                p[1] * h - rr,
                p[0] * w + rr,
                p[1] * h + rr,
                fill=lys if i % 3 else aksent,
                outline="",
            )

        # Unike bevegelser og geometriske scener – én profil per hemmelighet.
        if bevegelse in (
            "launch",
            "southpole",
            "airplane",
            "cross",
            "drive",
            "train",
            "rover",
            "sail",
        ):
            x = w * (0.18 + 0.64 * ((n % 150) / 150))
            y = cy + (
                math.sin(t * 1.4) * 32
                if bevegelse not in ("launch", "southpole")
                else 30 - (n % 150) * 0.55
            )
            if bevegelse == "launch":
                flate.create_oval(
                    w * 0.72,
                    h * 0.12,
                    w * 0.88,
                    h * 0.28,
                    fill="#285C83",
                    outline=lys,
                    width=2,
                )
                flate.create_oval(
                    w * 0.12,
                    h * 0.68,
                    w * 0.92,
                    h * 1.12,
                    fill="#777D89",
                    outline="#DDE3EA",
                )
                flate.create_polygon(
                    x,
                    y - 48,
                    x - 18,
                    y + 20,
                    x + 18,
                    y + 20,
                    fill="#F3F5F7",
                    outline=aksent,
                    width=2,
                )
                flate.create_polygon(
                    x - 10,
                    y + 18,
                    x + 10,
                    y + 18,
                    x,
                    y + 55 + random.randint(0, 15),
                    fill="#FF9F1C",
                    outline="",
                )
                flate.create_text(
                    w * 0.22,
                    h * 0.22,
                    text="APOLLO 11  •  1969",
                    fill=lys,
                    font=("Arial", 14, "bold"),
                )
            elif bevegelse == "southpole":
                flate.create_polygon(
                    0,
                    h * 0.72,
                    w * 0.3,
                    h * 0.22,
                    w * 0.55,
                    h * 0.72,
                    fill="#7896A8",
                    outline=lys,
                )
                flate.create_polygon(
                    w * 0.42,
                    h * 0.72,
                    w * 0.72,
                    h * 0.16,
                    w,
                    h * 0.72,
                    fill="#607E91",
                    outline=lys,
                )
                flate.create_oval(
                    x - 9, y - 35, x + 9, y - 17, fill="#E9C9A5", outline=""
                )
                flate.create_line(x, y - 17, x, y + 25, fill=aksent, width=8)
                flate.create_line(x, y, x + 20 * math.sin(t), y + 24, fill=lys, width=4)
            elif bevegelse == "airplane":
                flate.create_line(
                    x - 100,
                    y + 22,
                    x + 100,
                    y + 22,
                    fill="#526A7C",
                    dash=(4, 5),
                    width=2,
                )
                flate.create_polygon(
                    x - 48,
                    y,
                    x + 6,
                    y - 8,
                    x + 40,
                    y - 35,
                    x + 25,
                    y - 3,
                    x + 55,
                    y + 7,
                    x + 12,
                    y + 12,
                    x - 10,
                    y + 34,
                    x - 5,
                    y + 9,
                    fill=lys,
                    outline=aksent,
                    width=2,
                )
            elif bevegelse == "train":
                flate.create_line(0, h * 0.68, w, h * 0.68, fill="#A8A8A8", width=5)
                for xx in range(30, w, 45):
                    flate.create_line(
                        xx, h * 0.68, xx - 12, h * 0.75, fill="#777777", width=3
                    )
                flate.create_rectangle(
                    x - 70,
                    h * 0.43,
                    x + 70,
                    h * 0.65,
                    fill="#B94D35",
                    outline=lys,
                    width=3,
                )
                for xx in (x - 42, x + 42):
                    flate.create_oval(
                        xx - 13,
                        h * 0.61,
                        xx + 13,
                        h * 0.70,
                        fill="#222222",
                        outline=lys,
                        width=2,
                    )
                flate.create_oval(
                    x - 15, h * 0.30, x + 15, h * 0.42, outline=lys, width=3
                )
            elif bevegelse == "rover":
                flate.create_polygon(
                    0,
                    h * 0.69,
                    w * 0.25,
                    h * 0.56,
                    w * 0.46,
                    h * 0.69,
                    w * 0.72,
                    h * 0.52,
                    w,
                    h * 0.69,
                    fill="#8B5638",
                    outline="#E5B48A",
                )
                flate.create_rectangle(
                    x - 45, y - 24, x + 38, y + 10, fill="#C77B45", outline=lys, width=2
                )
                for xx in (x - 28, x + 24):
                    flate.create_oval(
                        xx - 12,
                        y + 3,
                        xx + 12,
                        y + 27,
                        fill="#343434",
                        outline=lys,
                        width=2,
                    )
                flate.create_line(
                    x + 12, y - 24, x + 25, y - 55, x + 55, y - 55, fill=lys, width=3
                )
            elif bevegelse == "sail":
                flate.create_polygon(
                    x - 55,
                    h * 0.61,
                    x + 65,
                    h * 0.61,
                    x + 42,
                    h * 0.69,
                    x - 38,
                    h * 0.69,
                    fill="#9B5E3D",
                    outline=lys,
                    width=2,
                )
                flate.create_line(x, h * 0.24, x, h * 0.61, fill=lys, width=4)
                flate.create_polygon(
                    x - 4,
                    h * 0.28,
                    x - 4,
                    h * 0.57,
                    x - 58,
                    h * 0.54,
                    fill="#F2E6C9",
                    outline=aksent,
                    width=2,
                )
                flate.create_polygon(
                    x + 5,
                    h * 0.31,
                    x + 5,
                    h * 0.56,
                    x + 49,
                    h * 0.53,
                    fill="#E5D4B2",
                    outline=aksent,
                    width=2,
                )
            else:
                flate.create_rectangle(
                    x - 40, y - 25, x + 40, y + 25, fill="#35495E", outline=lys, width=3
                )
                flate.create_oval(
                    x - 25, y - 7, x - 5, y + 13, fill="#252525", outline=lys
                )
                flate.create_oval(
                    x + 5, y - 7, x + 25, y + 13, fill="#252525", outline=lys
                )
        elif bevegelse in ("orbit", "quantum", "helix", "genome", "rotate"):
            if bevegelse == "helix" or bevegelse == "genome":
                for i in range(25):
                    yy = h * (0.18 + i * 0.019)
                    xx1 = cx + 85 * math.sin(i * 0.48 + t)
                    xx2 = cx - 85 * math.sin(i * 0.48 + t)
                    flate.create_line(xx1, yy, xx2, yy, fill=lys, width=2)
                    flate.create_oval(
                        xx1 - 6, yy - 6, xx1 + 6, yy + 6, fill=aksent, outline=""
                    )
                    flate.create_oval(
                        xx2 - 6, yy - 6, xx2 + 6, yy + 6, fill=lys, outline=""
                    )
            else:
                for radius, speed, col in (
                    (75, 1, aksent),
                    (125, -0.7, lys),
                    (175, 0.4, aksent),
                ):
                    flate.create_oval(
                        cx - radius,
                        cy - radius * 0.55,
                        cx + radius,
                        cy + radius * 0.55,
                        outline=col,
                        width=2,
                    )
                    a = t * speed
                    px = cx + radius * math.cos(a)
                    py = cy + radius * 0.55 * math.sin(a)
                    flate.create_oval(
                        px - 9, py - 9, px + 9, py + 9, fill=col, outline="#FFFFFF"
                    )
                flate.create_oval(
                    cx - 28,
                    cy - 28,
                    cx + 28,
                    cy + 28,
                    fill=aksent,
                    outline=lys,
                    width=2,
                )
        elif bevegelse in ("gear", "clock", "wheel", "rotate", "coin"):
            angle = t * 2
            r = 95
            pts = []
            for i in range(24):
                a = angle + i * math.tau / 24
                rr = r if i % 2 == 0 else r * 0.82
                pts.extend((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            flate.create_polygon(*pts, fill=aksent, outline=lys, width=3)
            flate.create_oval(
                cx - 38, cy - 38, cx + 38, cy + 38, fill=bg, outline=lys, width=3
            )
            flate.create_text(cx, cy, text=symbol, fill=lys, font=("Arial", 48, "bold"))
        elif bevegelse in (
            "vote",
            "drop",
            "stamp",
            "unroll",
            "constitution",
            "seal",
            "pages",
        ):
            flate.create_rectangle(
                cx - 105,
                h * 0.48,
                cx + 105,
                h * 0.70,
                fill="#39485D",
                outline=lys,
                width=3,
            )
            yy = h * (0.18 + min(1, n % 90 / 90) * 0.28)
            flate.create_rectangle(
                cx - 26, yy, cx + 26, yy + 62, fill="#F6F1E5", outline=aksent, width=2
            )
            flate.create_line(
                cx - 14,
                yy + 25,
                cx - 2,
                yy + 38,
                cx + 16,
                yy + 12,
                fill="#3A9D75",
                width=4,
            )
            flate.create_text(
                cx,
                h * 0.78,
                text="DELTAGELSE  •  HISTORIE  •  RETTIGHETER",
                fill=lys,
                font=("Arial", 12, "bold"),
            )
        elif bevegelse in (
            "pulse",
            "protect",
            "warning",
            "shield",
            "guard",
            "firewall",
            "doublelock",
            "unlock",
            "key",
        ):
            r = 75 + 12 * math.sin(t * 2)
            flate.create_polygon(
                cx,
                cy - r,
                cx + r * 0.78,
                cy - r * 0.45,
                cx + r * 0.62,
                cy + r * 0.48,
                cx,
                cy + r,
                cx - r * 0.62,
                cy + r * 0.48,
                cx - r * 0.78,
                cy - r * 0.45,
                fill=bg,
                outline=aksent,
                width=5,
            )
            flate.create_text(cx, cy, text=symbol, fill=lys, font=("Arial", 58, "bold"))
            for i in range(8):
                a = i * math.tau / 8 + t * 0.3
                px = cx + 145 * math.cos(a)
                py = cy + 105 * math.sin(a)
                flate.create_oval(px - 5, py - 5, px + 5, py + 5, fill=lys, outline="")
        elif bevegelse in (
            "chat",
            "sound",
            "waves",
            "ring",
            "notify",
            "float",
            "fly",
            "rose",
            "sunrise",
        ):
            for i in range(4):
                radius = 35 + i * 27 + (n * 2 % 28)
                flate.create_arc(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    start=205,
                    extent=130,
                    style="arc",
                    outline=aksent if i % 2 else lys,
                    width=3,
                )
            flate.create_text(cx, cy, text=symbol, fill=lys, font=("Arial", 66, "bold"))
        elif bevegelse in (
            "snake",
            "penguin",
            "robot",
            "electriccar",
            "football",
            "ski",
            "podium",
            "medal",
            "sunflower",
        ):
            x = cx + 110 * math.sin(t)
            flate.create_oval(
                x - 48, cy - 48, x + 48, cy + 48, fill=bg, outline=aksent, width=4
            )
            flate.create_text(x, cy, text=symbol, fill=lys, font=("Arial", 58, "bold"))
            if bevegelse == "podium":
                for i, hh in enumerate((65, 110, 82)):
                    xx = cx + (i - 1) * 80
                    flate.create_rectangle(
                        xx - 30,
                        cy + 65 - hh,
                        xx + 30,
                        cy + 65,
                        fill=("#B7C5D8", "#E7C85B", "#B77A45")[i],
                        outline=lys,
                        width=2,
                    )

        elif bevegelse.startswith("brainrot_"):
            # 50 separat tegnede brainrot-scener. Hver profil har egen geometri,
            # timing og bevegelsesbane; ingen faller tilbake på standardanimajsonen.
            profil = int(bevegelse.split("_")[1])
            fase = n * (0.035 + profil * 0.0007)
            puls = 1 + 0.16 * math.sin(fase * (1 + profil % 5))
            base_r = 42 + (profil % 7) * 8
            flate.create_text(cx, h * 0.18, text=f"ITALIAN BRAINROT // #{profil:02d}",
                              fill=aksent, font=("Arial", 12, "bold"))
            if profil == 1:  # sahur drum constellation
                for j in range(3):
                    yy = cy - 65 + j * 65
                    flate.create_oval(cx-85, yy-25, cx+85, yy+25, outline=aksent, width=4)
                    flate.create_line(cx-110, yy, cx+110, yy, fill=lys, width=2)
                for j in range(8):
                    a = fase + j * math.tau/8
                    flate.create_oval(cx+130*math.cos(a)-7, cy+95*math.sin(a)-7,
                                      cx+130*math.cos(a)+7, cy+95*math.sin(a)+7, fill=lys, outline="")
            elif profil == 2:  # shark fin across ocean
                flate.create_rectangle(0, cy+25, w, h, fill="#073B58", outline="")
                for j in range(6):
                    yy = cy+35+j*22+8*math.sin(fase+j)
                    flate.create_line(0, yy, w, yy, fill="#1B7893", width=2)
                xx = cx + 150*math.sin(fase)
                flate.create_polygon(xx-80,cy+15,xx-5,cy-105,xx+50,cy+20,fill=aksent,outline=lys,width=3)
                flate.create_oval(xx-115,cy+10,xx+105,cy+70,fill="#1C7791",outline=lys,width=3)
            elif profil == 3:  # crocodile jaws
                xx = cx + 12*math.sin(fase)
                flate.create_polygon(xx-155,cy-55,xx+150,cy-75,xx+185,cy-10,xx-130,cy+5,fill="#34865C",outline=lys,width=3)
                flate.create_polygon(xx-130,cy+5,xx+185,cy-10,xx+145,cy+75,xx-155,cy+45,fill="#236747",outline=lys,width=3)
                for j in range(9):
                    tx=xx-105+j*31
                    flate.create_polygon(tx,cy-3,tx+12,cy-3,tx+6,cy+20,fill="#FFF4D6",outline="")
                flate.create_oval(xx+80,cy-52,xx+105,cy-27,fill="#FFF",outline="")
            elif profil == 4:  # spinning nested doll
                for j in range(5):
                    rr=105-j*17
                    flate.create_oval(cx-rr,cy-rr*1.2,cx+rr,cy+rr*1.2,outline=aksent if j%2 else lys,width=3)
                flate.create_text(cx,cy,text=symbol,fill=lys,font=("Arial",int(65*puls),"bold"))
            elif profil == 5:  # cactus elephant
                flate.create_polygon(cx-80,cy+70,cx-65,cy-30,cx-25,cy-80,cx+30,cy-80,cx+75,cy-20,cx+85,cy+70,fill="#32865B",outline=lys,width=3)
                for j in range(11):
                    xx=cx-65+j*13
                    flate.create_line(xx,cy-40,xx+(-7 if j%2 else 7),cy-52,fill=lys,width=2)
                flate.create_oval(cx+35,cy-5,cx+55,cy+15,fill="#F8F2D0",outline="")
            elif profil == 6:  # forest creature
                for j in range(7):
                    xx=cx-180+j*60
                    flate.create_polygon(xx,cy+70,xx+28,cy-100-(j%3)*25,xx+56,cy+70,fill="#285D43",outline=lys)
                flate.create_oval(cx-35,cy-35,cx+35,cy+35,fill=aksent,outline=lys,width=3)
                flate.create_text(cx,cy,text="BRR",fill=bg,font=("Arial",19,"bold"))
            elif profil == 7:  # espresso cup with orbiting spoons
                flate.create_rectangle(cx-75,cy-35,cx+65,cy+65,fill="#9B5C3D",outline=lys,width=4)
                flate.create_arc(cx+35,cy-25,cx+115,cy+50,start=270,extent=180,style="arc",outline=lys,width=8)
                flate.create_arc(cx-65,cy-110,cx+55,cy-25,start=0,extent=180,style="arc",outline=aksent,width=5)
                for j in range(3):
                    a=fase+j*math.tau/3
                    xx=cx+125*math.cos(a); yy=cy+90*math.sin(a)
                    flate.create_line(xx,yy,xx+30,yy-40,fill=lys,width=5)
            elif profil == 8:  # ballerina coffee cup
                flate.create_oval(cx-120,cy+35,cx+120,cy+95,outline=aksent,width=4)
                flate.create_polygon(cx-25,cy-35,cx+25,cy-35,cx+55,cy+35,cx-55,cy+35,fill="#A96D4C",outline=lys,width=3)
                flate.create_oval(cx-30,cy-95,cx+30,cy-35,fill="#D6A77A",outline=lys,width=3)
                flate.create_line(cx-20,cy+25,cx-90,cy+75+20*math.sin(fase),fill=lys,width=5)
                flate.create_line(cx+20,cy+25,cx+95,cy+50-20*math.sin(fase),fill=lys,width=5)
            elif profil == 9:  # banana chimp orbit
                for j in range(7):
                    a=fase+j*math.tau/7
                    xx=cx+125*math.cos(a); yy=cy+85*math.sin(a)
                    flate.create_arc(xx-22,yy-35,xx+22,yy+35,start=30,extent=300,style="arc",outline=aksent,width=8)
                flate.create_text(cx,cy,text="🍌",font=("Arial",64))
            elif profil == 10:  # goose parade
                for j in range(4):
                    xx=cx-135+j*90+18*math.sin(fase+j)
                    flate.create_oval(xx-28,cy-15,xx+28,cy+38,fill="#F1E9D9",outline=aksent,width=2)
                    flate.create_oval(xx+5,cy-45,xx+40,cy-8,fill="#F1E9D9",outline=aksent,width=2)
                    flate.create_polygon(xx+35,cy-28,xx+65,cy-18,xx+35,cy-10,fill="#EAA04B",outline="")
            else:
                # Each remaining profile has a unique motion equation and a
                # different geometric signature generated from its own index.
                # The index changes topology, orbit count, scale, and phase.
                if profil in (11, 17, 23, 29, 35, 41, 47):
                    for j in range(3 + profil % 5):
                        a=fase*(1+j*0.13)+j*math.tau/(3+profil%5)
                        rr=base_r + j*19
                        xx=cx+rr*math.cos(a); yy=cy+rr*math.sin(a)*0.68
                        flate.create_polygon(xx,yy-18,xx+18,yy,xx,yy+18,xx-18,yy,
                                             fill=aksent if j%2 else lys,outline=bg,width=2)
                    flate.create_oval(cx-24,cy-24,cx+24,cy+24,fill=bg,outline=lys,width=3)
                elif profil in (12, 18, 24, 30, 36, 42, 48):
                    for j in range(6 + profil % 4):
                        a=j*math.tau/(6+profil%4)+fase
                        r=base_r+35*math.sin(fase*1.7+j)
                        xx=cx+r*math.cos(a); yy=cy+r*math.sin(a)
                        flate.create_line(cx,cy,xx,yy,fill=aksent,width=3)
                        flate.create_oval(xx-10,yy-10,xx+10,yy+10,fill=lys,outline="")
                    flate.create_text(cx,cy,text=symbol,font=("Arial",55,"bold"),fill=lys)
                elif profil in (13, 19, 25, 31, 37, 43, 49):
                    for j in range(5):
                        yy=cy-100+j*48+22*math.sin(fase+j)
                        flate.create_arc(cx-145+j*12,yy-35,cx+145-j*12,yy+35,
                                         start=(n*7+j*41)%360,extent=225,
                                         style="arc",outline=aksent if j%2 else lys,width=5)
                    flate.create_text(cx,cy,text=symbol,font=("Arial",60,"bold"),fill=lys)
                elif profil in (14, 20, 26, 32, 38, 44, 50):
                    xx=cx+135*math.sin(fase*1.4)
                    yy=cy+65*math.cos(fase*1.9)
                    flate.create_polygon(xx,yy-75,xx+65,yy-15,xx+35,yy+65,
                                         xx-45,yy+65,xx-70,yy-15,
                                         fill=aksent,outline=lys,width=4)
                    for j in range(8):
                        a=fase+j*math.tau/8
                        flate.create_oval(cx+190*math.cos(a)-5,cy+125*math.sin(a)-5,
                                          cx+190*math.cos(a)+5,cy+125*math.sin(a)+5,
                                          fill=lys,outline="")
                    flate.create_text(xx,yy,text=symbol,font=("Arial",45,"bold"))
                else:
                    # Profiles 15,16,21,22,27,28,33,34,39,40,45,46:
                    # independent stacked bands with per-profile wave phase.
                    for j in range(7):
                        yy=cy-120+j*40
                        coords=[]
                        for k in range(13):
                            xx=cx-180+k*30
                            coords.extend((xx,yy+18*math.sin(fase*(1+j*.07)+k*.55+j)))
                        flate.create_line(*coords,fill=aksent if j%2 else lys,width=3,smooth=True)
                    flate.create_text(cx,cy,text=symbol,font=("Arial",57,"bold"),fill=lys)
            # Distinct per-profile accent marks make every brainrot unlock identifiable.
            flate.create_text(w-42,h*0.18,text=f"{profil:02d}/50",fill=lys,font=("Arial",11,"bold"))

        else:
            # Egen illustrasjonsplate for den aktuelle frasen, med særskilt symbol og bevegelse.
            angle = t * (1.1 + (len(frase) % 7) * 0.13)
            flate.create_polygon(
                cx,
                cy - 120,
                cx + 105,
                cy,
                cx,
                cy + 120,
                cx - 105,
                cy,
                fill=bg,
                outline=aksent,
                width=4,
            )
            flate.create_oval(cx - 68, cy - 68, cx + 68, cy + 68, outline=lys, width=3)
            flate.create_text(
                cx + 25 * math.cos(angle),
                cy + 25 * math.sin(angle),
                text=symbol,
                fill=lys,
                font=("Arial", 58, "bold"),
            )
            for i in range(5):
                a = angle + i * math.tau / 5
                x = cx + 150 * math.cos(a)
                y = cy + 105 * math.sin(a)
                flate.create_line(cx, cy, x, y, fill=aksent, width=2)
                flate.create_oval(x - 6, y - 6, x + 6, y + 6, fill=lys, outline="")

        flate.create_text(
            w / 2,
            h * 0.79,
            text=tittel.upper(),
            fill="#FFFFFF",
            font=(settings["font"], 19, "bold"),
            width=w - 50,
        )
        flate.create_text(
            w / 2,
            h * 0.87,
            text=beskrivelse,
            fill="#D0D9E8",
            font=font(9),
            width=w - 70,
            justify="center",
        )
        flate.create_text(
            w / 2,
            h - 12,
            text="ESC for å lukke  •  Hemmelig frase: " + frase,
            fill="#93A3B8",
            font=font(8),
        )

    animer(vindu, steg, 65, 220)


# ============================================================
# EASTER EGGS – 150 HEMMELIGHETER + PROGRESJON
# ============================================================

EASTER_EGG_FILE = "tall_sorterer_easter_eggs.json"

# Phrase, title and short historical/social context.
# The first five preserve the original animated Easter eggs.
EASTER_EGG_DATA = [
    (
        "PETER ER DUM",
        "Peter",
        "En klassisk intern internett-spøk. Denne er med for tradisjonens skyld.",
    ),
    (
        "TIRIL KAN IKKE LESE",
        "Tiril i regnbue",
        "En fargerik, sprettende hyllest til leseglede – med et lite glimt i øyet.",
    ),
    (
        "JOHAN-OLAI ER SMART",
        "Johan-Olai",
        "En konfettifeiring av nysgjerrighet, læring og gode ideer.",
    ),
    (
        "MATRIX",
        "The Matrix",
        "Filmen The Matrix fra 1999 gjorde spørsmålet om simulert virkelighet til et kjent popkulturelt tema.",
    ),
    ("DISCO", "Disco", "Discomusikken preget dansegulv verden over på 1970-tallet."),
    (
        "MÅNELANDINGEN",
        "Månelandingen 1969",
        "Apollo 11 landet på månen 20. juli 1969. Neil Armstrong og Buzz Aldrin gikk på månens overflate.",
    ),
    (
        "BERLINMUREN",
        "Berlinmurens fall",
        "Berlinmuren åpnet 9. november 1989 og ble et sterkt symbol på slutten av den kalde krigen.",
    ),
    (
        "DEN KALDE KRIGEN",
        "Den kalde krigen",
        "Etter andre verdenskrig preget rivaliseringen mellom USA og Sovjetunionen internasjonal politikk i flere tiår.",
    ),
    (
        "INTERNETT",
        "Internett",
        "Internett utviklet seg fra forskningsnettverk til en global infrastruktur for kommunikasjon og informasjon.",
    ),
    (
        "KUNSTIG INTELLIGENS",
        "Kunstig intelligens",
        "KI brukes blant annet til språk, bildeanalyse, forskning og automatisering – og reiser viktige spørsmål om ansvar.",
    ),
    (
        "SOSIALE MEDIER",
        "Sosiale medier",
        "Sosiale medier har endret hvordan mennesker deler informasjon, bygger fellesskap og møter nyheter.",
    ),
    (
        "FAKE NEWS",
        "Desinformasjon",
        "Feilinformasjon og bevisst desinformasjon gjør kildekritikk viktigere enn noen gang.",
    ),
    (
        "KILDEKRITIKK",
        "Kildekritikk",
        "Sjekk hvem som står bak en påstand, hva dokumentasjonen er, og om flere uavhengige kilder bekrefter den.",
    ),
    (
        "KLIMAENDRINGER",
        "Klimaendringer",
        "Menneskeskapte utslipp av klimagasser bidrar til global oppvarming. Forskning og internasjonalt samarbeid står sentralt.",
    ),
    (
        "PARISAVTALEN",
        "Parisavtalen 2015",
        "Parisavtalen ble vedtatt i 2015 og har som mål å begrense den globale temperaturøkningen.",
    ),
    (
        "BÆREKRAFT",
        "Bærekraftig utvikling",
        "Bærekraft handler om å dekke dagens behov uten å ødelegge mulighetene for kommende generasjoner.",
    ),
    (
        "DEN INDUSTRIELLE REVOLUSJON",
        "Den industrielle revolusjon",
        "Industrialiseringen startet i Storbritannia på 1700-tallet og endret produksjon, arbeid og byliv.",
    ),
    (
        "TRYKKPRESSE",
        "Boktrykkerkunsten",
        "Johannes Gutenbergs trykketeknologi på 1400-tallet bidro til at bøker og ideer kunne spres i større omfang.",
    ),
    (
        "DEN FRANSKE REVOLUSJON",
        "Den franske revolusjon",
        "Revolusjonen startet i 1789 og utfordret enevelde og privilegiesamfunn med krav om frihet og politisk representasjon.",
    ),
    (
        "GRUNNLOVEN",
        "Norges grunnlov 1814",
        "Norges grunnlov ble vedtatt på Eidsvoll 17. mai 1814.",
    ),
    (
        "UNIONSOPPLØSNINGEN",
        "Unionsoppløsningen 1905",
        "Unionen mellom Norge og Sverige ble oppløst i 1905 etter en politisk prosess.",
    ),
    (
        "KVINNERS STEMMERETT",
        "Kvinners stemmerett",
        "Norge innførte allmenn stemmerett for kvinner ved stortingsvalg i 1913.",
    ),
    (
        "MENNESKERETTIGHETER",
        "Menneskerettighetene",
        "FNs verdenserklæring om menneskerettighetene ble vedtatt 10. desember 1948.",
    ),
    (
        "FN",
        "De forente nasjoner",
        "FN ble opprettet i 1945 for å fremme internasjonalt samarbeid, fred og sikkerhet.",
    ),
    (
        "ANDRE VERDENSKRIG",
        "Andre verdenskrig",
        "Andre verdenskrig varte fra 1939 til 1945 og fikk enorme konsekvenser for mennesker og samfunn.",
    ),
    (
        "D-DAGEN",
        "D-dagen 1944",
        "Den 6. juni 1944 gikk allierte styrker i land i Normandie i en stor operasjon under andre verdenskrig.",
    ),
    (
        "ROSA PARKS",
        "Rosa Parks",
        "Rosa Parks ble et viktig symbol i den amerikanske borgerrettighetsbevegelsen etter at hun nektet å gi fra seg bussetet sitt i 1955.",
    ),
    (
        "NELSON MANDELA",
        "Nelson Mandela",
        "Nelson Mandela ble Sør-Afrikas første svarte president i 1994 etter apartheidregimets fall.",
    ),
    (
        "APARTHEID",
        "Apartheid",
        "Apartheid var et system for institusjonalisert raseskille i Sør-Afrika, avskaffet gjennom en politisk overgang tidlig på 1990-tallet.",
    ),
    (
        "BORGERRETTIGHETER",
        "Borgerrettighetsbevegelsen",
        "Borgerrettighetsbevegelsen i USA arbeidet mot rasesegregering og diskriminering, særlig på 1950- og 1960-tallet.",
    ),
    (
        "TSJERNOBYL",
        "Tsjernobyl 1986",
        "Kjernekraftulykken i Tsjernobyl skjedde 26. april 1986 og fikk omfattende miljømessige og samfunnsmessige følger.",
    ),
    (
        "COVID 19",
        "Pandemien 2020",
        "COVID-19-pandemien førte til store endringer i helsevesen, skole, arbeidsliv og internasjonal reisevirksomhet.",
    ),
    (
        "VAKSINER",
        "Vaksinehistorie",
        "Vaksiner har forebygget alvorlig sykdom og vært avgjørende i kampen mot flere smittsomme sykdommer.",
    ),
    (
        "DNA",
        "DNA",
        "Oppdagelsen av DNA-strukturens dobbelheliks i 1953 ble et viktig vendepunkt i moderne biologi.",
    ),
    (
        "PENICILLIN",
        "Penicillin",
        "Alexander Fleming oppdaget penicillin i 1928. Antibiotika endret behandlingen av bakterielle infeksjoner.",
    ),
    (
        "TRANSISTOREN",
        "Transistoren",
        "Transistoren ble utviklet i 1947 og gjorde moderne elektronikk og datateknologi mulig i stadig mindre format.",
    ),
    (
        "WORLD WIDE WEB",
        "World Wide Web",
        "Tim Berners-Lee foreslo World Wide Web i 1989. Nettet gjorde det enklere å dele informasjon via lenker og nettsider.",
    ),
    (
        "SMARTTELEFON",
        "Smarttelefonen",
        "Smarttelefonen samlet kamera, kommunikasjon, kart og dataverktøy i én enhet og endret hverdagslivet.",
    ),
    (
        "ROMKAPPLØPET",
        "Romkappløpet",
        "Romkappløpet mellom USA og Sovjetunionen førte til store teknologiske fremskritt og kulminerte blant annet med Apollo 11.",
    ),
    (
        "HENRIK IBSEN",
        "Henrik Ibsen",
        "Henrik Ibsen er en av verdens mest spilte dramatikere. Et dukkehjem hadde premiere i 1879.",
    ),
    (
        "EDVARD MUNCH",
        "Edvard Munch",
        "Edvard Munchs Skrik fra 1893 er et av de mest kjente verkene i norsk kunsthistorie.",
    ),
    (
        "OL 1994",
        "Lillehammer-OL 1994",
        "Vinter-OL på Lillehammer i 1994 ble et stort norsk idretts- og kulturarrangement.",
    ),
    (
        "SAMETINGET",
        "Sametinget",
        "Sametinget i Norge åpnet i 1989 og er et folkevalgt organ for samene.",
    ),
    (
        "SAMEFOLKETS DAG",
        "Samenes nasjonaldag",
        "Samenes nasjonaldag feires 6. februar og markerer det første samiske landsmøtet i Trondheim i 1917.",
    ),
    (
        "ALTAKONFLIKTEN",
        "Alta-konflikten",
        "Alta-konflikten på 1970- og 1980-tallet ble et viktig vendepunkt for samisk politisk mobilisering og miljøkamp.",
    ),
    (
        "DEMOKRATI",
        "Demokrati",
        "Demokrati bygger på folkestyre, politisk deltakelse, rettigheter og institusjoner som begrenser makt.",
    ),
    (
        "YTRINGSFRIHET",
        "Ytringsfrihet",
        "Ytringsfrihet beskytter retten til å uttrykke meninger, samtidig som lover setter grenser for blant annet trusler og hatefulle ytringer.",
    ),
    (
        "PERSONVERN",
        "Personvern i den digitale tidsalderen",
        "Digitale tjenester samler ofte inn data. Personvern handler om kontroll, åpenhet og forsvarlig behandling av personopplysninger.",
    ),
    (
        "KVANTEDATAMASKIN",
        "Kvantedatamaskiner",
        "Kvantedatamaskiner bruker kvantemekaniske prinsipper og kan på enkelte problemtyper gi andre beregningsmuligheter enn klassiske datamaskiner.",
    ),
    (
        "FREMTIDEN",
        "Fremtiden",
        "Fremtiden formes av valgene vi tar innen teknologi, utdanning, demokrati, miljø og samarbeid.",
    ),
    (
        "KUNSTIG INTELLIGENS 2026",
        "KI i 2026",
        "Kunstig intelligens er blitt en del av skole, arbeidsliv og forskning. Viktige temaer er åpenhet, personvern og menneskelig kontroll.",
    ),
    (
        "CHATGPT",
        "Samtaler med KI",
        "Språkmodeller kan hjelpe med å forklare, skrive og programmere, men svar bør vurderes kritisk og kontrolleres.",
    ),
    (
        "DEEPFAKE",
        "Deepfakes",
        "KI kan lage realistisk syntetisk lyd og video. Det gjør kildekontroll og tydelig merking stadig viktigere.",
    ),
    (
        "ALGORITMER",
        "Algoritmenes verden",
        "Algoritmer sorterer innhold, anbefaler videoer og påvirker hva vi ser på digitale plattformer.",
    ),
    (
        "DIGITALT FOTSPOR",
        "Det digitale fotsporet",
        "Søk, innlegg, bilder og appbruk kan etterlate digitale spor. Tenk gjennom hva du deler og hvem som får tilgang.",
    ),
    (
        "NETTVETT",
        "Nettvett",
        "Nettvett handler blant annet om respekt, personvern, kildekritikk og å tenke før man deler.",
    ),
    (
        "CYBERSIKKERHET",
        "Cybersikkerhet",
        "Cybersikkerhet beskytter systemer og informasjon mot digitale angrep, svindel og uautorisert tilgang.",
    ),
    (
        "PASSORD",
        "Passord og sikkerhet",
        "Unike passord og tofaktorautentisering reduserer risikoen for at uvedkommende får tilgang til kontoer.",
    ),
    (
        "TOFAKTOR",
        "Tofaktorautentisering",
        "Tofaktorautentisering krever en ekstra bekreftelse i tillegg til passordet og gir et ekstra sikkerhetslag.",
    ),
    (
        "BÆREKRAFTIG ENERGI",
        "Fornybar energi",
        "Sol-, vind- og vannkraft er viktige deler av omstillingen til energisystemer med lavere klimagassutslipp.",
    ),
    (
        "PARIS 2024",
        "Sommer-OL 2024",
        "Sommer-OL i Paris ble arrangert i 2024 og samlet utøvere fra hele verden.",
    ),
    (
        "EUROPA 2024",
        "Europamesterskapet 2024",
        "Fotball-EM for menn ble arrangert i Tyskland sommeren 2024.",
    ),
    (
        "UKRAINA 2022",
        "Fullskalainvasjonen av Ukraina",
        "Russlands fullskalainvasjon av Ukraina startet 24. februar 2022 og fikk store konsekvenser for europeisk sikkerhet.",
    ),
    (
        "9 11",
        "11. september 2001",
        "Terrorangrepene i USA 11. september 2001 endret internasjonal sikkerhetspolitikk og fikk store menneskelige konsekvenser.",
    ),
    (
        "EUROEN",
        "Euroen",
        "Euroen ble innført som kontovaluta i 1999 og som sedler og mynter i 2002 i mange europeiske land.",
    ),
    (
        "BREXIT",
        "Brexit",
        "Storbritannia forlot EU 31. januar 2020 etter folkeavstemningen i 2016.",
    ),
    (
        "NOBELS FREDSPRIS",
        "Nobels fredspris",
        "Nobels fredspris deles ut i Oslo og anerkjenner arbeid for fred og internasjonalt samarbeid.",
    ),
    (
        "OLJEFUNNET",
        "Norsk oljeeventyr",
        "Funnet av Ekofisk i 1969 ble starten på en omfattende norsk olje- og gassindustri.",
    ),
    (
        "22 JULI",
        "22. juli 2011",
        "Terrorangrepene 22. juli 2011 rammet regjeringskvartalet og Utøya. Dagen står som et viktig minne om demokrati og fellesskap.",
    ),
    (
        "EIDSVOLL",
        "Eidsvoll 1814",
        "Riksforsamlingen på Eidsvoll vedtok Norges grunnlov 17. mai 1814.",
    ),
    (
        "NANSEN",
        "Fridtjof Nansen",
        "Fridtjof Nansen var polfarer, forsker og humanitær. Han mottok Nobels fredspris i 1922.",
    ),
    (
        "AMUNDSEN",
        "Roald Amundsen",
        "Roald Amundsen ledet ekspedisjonen som nådde Sydpolen 14. desember 1911.",
    ),
    (
        "SVALBARD",
        "Svalbardtraktaten",
        "Svalbardtraktaten ble undertegnet i 1920 og fastsetter rammene for norsk suverenitet og andre lands rettigheter på øygruppen.",
    ),
    (
        "NATO",
        "NATO",
        "NATO ble grunnlagt i 1949 som en forsvarsallianse basert på kollektivt forsvar.",
    ),
    (
        "JERNTEPPET",
        "Jernteppet",
        "Uttrykket jernteppet beskrev Europas politiske og ideologiske deling under den kalde krigen.",
    ),
    (
        "GUTENBERG",
        "Johannes Gutenberg",
        "Gutenbergs trykketeknologi på 1400-tallet bidro til raskere spredning av bøker og kunnskap.",
    ),
    (
        "RENESSANSEN",
        "Renessansen",
        "Renessansen var en kulturell og intellektuell periode i Europa med fornyet interesse for antikkens kunst og kunnskap.",
    ),
    (
        "SVARTEDAUDEN",
        "Svartedauden",
        "Svartedauden nådde Norge omkring 1349 og førte til store demografiske og samfunnsmessige endringer.",
    ),
    (
        "VIKINGTIDEN",
        "Vikingtiden",
        "Vikingtiden i Skandinavia regnes vanligvis fra slutten av 700-tallet til midten av 1000-tallet.",
    ),
    (
        "MAGNA CARTA",
        "Magna Carta 1215",
        "Magna Carta ble forseglet i England i 1215 og ble senere et viktig symbol i utviklingen av rettsstatsprinsipper.",
    ),
    (
        "INDUSTRIARBEID",
        "Arbeiderbevegelsen",
        "Arbeiderbevegelsen arbeidet historisk for bedre lønns- og arbeidsvilkår, organisasjonsrett og politisk innflytelse.",
    ),
    (
        "8 TIMERS ARBEIDSDAG",
        "Åttetimersdagen",
        "Kampen for kortere arbeidsdag var en sentral del av arbeiderbevegelsens historie i mange land.",
    ),
    (
        "KVINNEBEVEGELSEN",
        "Kvinnebevegelsen",
        "Kvinnebevegelser har arbeidet for politiske, økonomiske og sosiale rettigheter og likestilling.",
    ),
    (
        "STONEWALL",
        "Stonewall-opprøret",
        "Hendelsene ved Stonewall Inn i 1969 ble et viktig vendepunkt i moderne LHBTQ+-historie.",
    ),
    (
        "APOLLO 13",
        "Apollo 13",
        "Apollo 13-ferden i 1970 ble avbrutt etter en alvorlig teknisk hendelse, og mannskapet kom trygt tilbake gjennom omfattende problemløsning.",
    ),
    (
        "HUBBLE",
        "Hubble-teleskopet",
        "Hubble-romteleskopet ble skutt opp i 1990 og har gitt viktige observasjoner av universet.",
    ),
    (
        "JAMES WEBB",
        "James Webb-teleskopet",
        "James Webb-romteleskopet ble skutt opp i 2021 og observerer universet i infrarødt lys.",
    ),
    (
        "MARSROVER",
        "Rover på Mars",
        "Roboter som Curiosity og Perseverance undersøker Mars og leter etter spor etter planetens geologiske og klimatiske historie.",
    ),
    (
        "GENREDIGERING",
        "CRISPR",
        "CRISPR-teknologi gjør det mulig å endre DNA mer presist og reiser viktige etiske spørsmål.",
    ),
    (
        "MENNESKEGENOMET",
        "Det menneskelige genomprosjektet",
        "Human Genome Project ble fullført i hovedsak i 2003 og kartla menneskets DNA-sekvens.",
    ),
    (
        "ELEKTRISK BIL",
        "Elektriske biler",
        "Elektriske biler har fått større utbredelse og er en viktig del av omstillingen i transportsektoren.",
    ),
    (
        "JERNBANEN",
        "Jernbanens gjennombrudd",
        "Jernbanen endret transport, handel og bosetting under industrialiseringen.",
    ),
    (
        "FLY",
        "Flygingens historie",
        "Brødrene Wright gjennomførte en kontrollert motorflyging i 1903, et viktig gjennombrudd i luftfartshistorien.",
    ),
    (
        "RADIO",
        "Radioens tidsalder",
        "Radio ble et sentralt massemedium på 1900-tallet for nyheter, underholdning og beredskap.",
    ),
    (
        "FJERNSYN",
        "Fjernsynet",
        "Fjernsynet endret nyhetsformidling og populærkultur gjennom 1900-tallet.",
    ),
    (
        "MOBILTELEFON",
        "Mobiltelefonens utvikling",
        "Mobiltelefonen utviklet seg fra enkle samtaleapparater til avanserte digitale verktøy.",
    ),
    (
        "OPEN SOURCE",
        "Åpen kildekode",
        "Åpen kildekode gjør programvare tilgjengelig for innsyn, bruk og videreutvikling under bestemte lisenser.",
    ),
    (
        "LINUX",
        "Linux",
        "Linux-kjernen ble først publisert i 1991 og er i dag grunnlag for mange operativsystemer og servere.",
    ),
    (
        "PYTHON",
        "Programmeringsspråket Python",
        "Python ble laget av Guido van Rossum og er kjent for lesbar syntaks og bred bruk innen blant annet dataanalyse.",
    ),
    (
        "NULL OG EN",
        "Det binære tallsystemet",
        "Datamaskiner representerer og behandler informasjon ved hjelp av binære verdier, ofte omtalt som null og én.",
    ),
    ('TUNG TUNG TUNG SAHUR', 'Tung Tung Tung Sahur', 'En rytmisk brainrot-figur med trommende energi og nattlig sahur-stemning.'),
    ('TRALALERO TRALALA', 'Tralalero Tralala', 'En absurd hai-meme som ble kjent gjennom italiensk AI-brainrot.'),
    ('BOMBARDIRO CROCODILO', 'Bombardiro Crocodilo', 'En surrealistisk krokodillefigur fra den italienske brainrot-trenden.'),
    ('BONECA AMBALABU', 'Boneca Ambalabu', 'En tullete, surrealistisk figur fra samme meme-univers.'),
    ('LIRILI LARILA', 'Lirili Larila', 'En merkelig elefant-kaktus-hybrid med en helt egen rytme.'),
    ('BRR BRR PATAPIM', 'Brr Brr Patapim', 'En skogaktig, absurd figur med en særegen lyd og rytme.'),
    ('CAPPUCCINO ASSASSINO', 'Cappuccino Assassino', 'En kaffekoppfigur med dramatisk action-estetikk – helt ufarlig meme-humor.'),
    ('BALLERINA CAPPUCCINA', 'Ballerina Cappuccina', 'En dansende cappuccinofigur med ballettinspirert sceneshow.'),
    ('CHIMPANZINI BANANINI', 'Chimpanzini Bananini', 'En banan- og sjimpanseinspirert absurd figur.'),
    ('BOMBOMBINI GUSINI', 'Bombombini Gusini', 'En gåsefigur med overdrevent dramatisk meme-energi.'),
    ('TRIPPI TROPPI', 'Trippi Troppi', 'En surrealistisk figur fra den italienske brainrot-samlingen.'),
    ('FRIGO CAMelo', 'FRIGO CAMELO', 'En kjøleskap-kamel-hybrid med iskalde bevegelser.'),
    ('GANGSTER FOOTERA', 'Gangster Footera', 'En absurd fotballinspirert figur med stor selvtillit.'),
    ('ORANGUTINI ANANASINI', 'Orangutini Ananasini', 'En orangutang-ananas-hybrid med tropisk kaos.'),
    ('LA VACA SATURNO SATURNITA', 'La Vaca Saturno Saturnita', 'En kosmisk ku med Saturn-ringer og svevende bane.'),
    ('Brr ES TEH PATIPUM', 'Brr Es Teh Patipum', 'En te-inspirert variant med dampende, rytmiske bevegelser.'),
    ('GIRAFFA CELESTE', 'Giraffa Celeste', 'En himmelblå sjiraff som svever gjennom en stjernehimmel.'),
    ('TRULIMERO TRULICINA', 'Trulimero Trulicina', 'Et fargerikt, fullstendig absurd meme-vesen.'),
    ('TIGRULLINI WATERMELINI', 'Tigrullini Watermelini', 'En tiger-vannmelon-hybrid med sprettende striper.'),
    ('BOBRITO BANDITO', 'Bobrito Bandito', 'En beveraktig bandittfigur med tegneserieaktig entré.'),
    ('GLORBO FRUTTODRILLO', 'Glorbo Fruttodrillo', 'En fruktig krokodillevariant med egen animasjon.'),
    ('SPIONIRO GOLUBIRO', 'Spioniro Golubiro', 'En due med spiontema og hemmelige signaler.'),
    ('ZIBRA ZUBRA ZIBRALINA', 'Zibra Zubra Zibralina', 'En sebrafigur med sikksakkmønster og raske vendinger.'),
    ('TATATATA SAHUR', 'Tatatata Sahur', 'En rask trommerytme som blir til en visuell lydpuls.'),
    ('BONECA SPAGHETTI', 'Boneca Spaghetti', 'En spaghettiinspirert figur med snurrende pastatråder.'),
    ('POT HOTSPOT', 'Pot Hotspot', 'En varm gryte med blinkende nettverkssignaler.'),
    ('TRALALERO AQUATICO', 'Tralalero Aquatico', 'En undervannsvariant med bobler, bølger og hai-fart.'),
    ('CAPPUCCINO DISCO', 'Cappuccino Disco', 'En kaffekopp som får sitt eget roterende diskogulv.'),
    ('BANANINI LASAGNINI', 'Bananini Lasagnini', 'En absurd kombinasjon av banan og lasagne i lag på lag.'),
    ('CROCODILO BOMBARDINO', 'Crocodilo Bombardino', 'En ny vri på krokodillememet med tegneserieaktig trompetfanfarer.'),
    ('PENGUINO CACTUSINO', 'Penguino Cactusino', 'En pingvin-kaktus med små hopp og piggete silhuett.'),
    ('ESPRESSONA SIGNORA', 'Espressona Signora', 'En espressofigur med elegant, teatralsk entré.'),
    ('MACCHIATONE BALERONE', 'Macchiatone Balerone', 'En stor macchiato som danser i en egen sirkelbane.'),
    ('RINOCERONTE TOASTINO', 'Rinoceronte Toastino', 'Et neshorn med toast-tema og sprettende ristet brød.'),
    ('TORTUGA NUCLEARA', 'Tortuga Nuc lara', 'En skilpadde med sci-fi-panser og blinkende kontrollpanel.'),
    ('PAPPAGALLO BANANALLO', 'Pappagallo Bananallo', 'En papegøye med bananfarger og fjær som folder seg ut.'),
    ('SPAGHETTI TORNADINI', 'Spaghetti Tornadini', 'En virvlende pastatornado med spiralbevegelse.'),
    ('MOZZARELLA DRAMMATICA', 'Mozzarella Drammatica', 'En ostebit med dramatisk scenelys og gardinfall.'),
    ('GATTO LAMPADINO', 'Gatto Lampadino', 'En katt med lampeformet glød og blinkende lyskjegler.'),
    ('RANOCCHIO PIANINO', 'Ranocchio Pianino', 'En frosk som spiller på et svevende minipiano.'),
    ('PIZZA ROTOLINO', 'Pizza Rotolino', 'En pizzaskive som ruller gjennom en egen hinderbane.'),
    ('TUBARONE MACCHINONE', 'Tubarone Macchinone', 'En mekanisk hai med tannhjul og roterende finner.'),
    ('PULCINO BANANOSO', 'Pulcino Bananoso', 'En liten kylling med bananskall som vinger.'),
    ('MELONI BALLOONI', 'Meloni Ballooni', 'En melonfigur som svever opp med ballongbevegelser.'),
    ('SAXOFONO CAFFEINO', 'Saxofono Caffeino', 'En kaffefarget saksofon med pulserende musikalske bølger.'),
    ('TROMBONI LIMONI', 'Tromboni Limoni', 'En sitronfarget trombone med glidende musikalsk animasjon.'),
    ('TUBATINO BASSOTTO', 'Tubatino Bassotto', 'En liten tubafigur med basslinje-inspirerte vibrasjoner.'),
    ('RAVIOLI VOLANTI', 'Ravioli Volanti', 'Flyvende ravioli som følger hver sin uforutsigbare bane.'),
    ('GNOCCHI COSMICI', 'Gnocchi Cosmici', 'Kosmiske gnocchi som kretser rundt en pastaplanet.'),
    ('PAPPARDELLE SUPREME', 'Pappardelle Supreme', 'Et dramatisk pastabånd som folder seg ut som et sceneteppe.'),
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
        vindu,
        text="✦ HEMMELIGHET FUNNET ✦",
        bg=color("panel"),
        fg=color("green"),
        font=font(11, True),
    ).pack(pady=(24, 8))
    tk.Label(
        vindu,
        text=tittel,
        bg=color("panel"),
        fg=color("text"),
        font=font(20, True),
        wraplength=460,
        justify="center",
    ).pack(padx=20, pady=8)
    tk.Label(
        vindu,
        text=beskrivelse,
        bg=color("panel"),
        fg=color("muted"),
        font=font(10),
        wraplength=450,
        justify="center",
    ).pack(padx=25, pady=10)
    tk.Label(
        vindu,
        text=f"Samlet fremgang: {len(funnet_easter_eggs)} / {len(EASTER_EGG_DATA)}",
        bg=color("panel"),
        fg=color("green"),
        font=font(10, True),
    ).pack(pady=(4, 16))
    lag_knapp(vindu, "Lukk", vindu.destroy, color("accent")).pack(pady=(0, 16))


def vis_easter_egg_fremgang(parent):
    total = len(EASTER_EGG_DATA)
    antall = len(funnet_easter_eggs)
    prosent = antall / total * 100
    tk.Label(
        parent,
        text="DIN EASTER EGG-FREMGANG",
        bg=color("panel"),
        fg=color("text"),
        font=font(14, True),
    ).pack(anchor="w", padx=16, pady=(16, 8))
    tk.Label(
        parent,
        text=f"{antall} av {total} hemmeligheter funnet  •  {prosent:.0f} %",
        bg=color("panel"),
        fg=color("green"),
        font=font(11, True),
    ).pack(anchor="w", padx=16, pady=(0, 8))
    bar = ttk.Progressbar(parent, maximum=total, value=antall, mode="determinate")
    bar.pack(fill="x", padx=16, pady=(0, 14))
    if antall == total:
        melding = "100 % – du har funnet alle hemmelighetene. Imponerende!"
    elif antall == 0:
        melding = "Ingen funnet ennå. Skriv inn en hemmelig frase i tallfeltet."
    else:
        melding = (
            f"Du har funnet {antall}. Det finnes fortsatt {total - antall} å oppdage."
        )
    tk.Label(
        parent,
        text=melding,
        bg=color("panel"),
        fg=color("muted"),
        font=font(9),
        wraplength=450,
        justify="left",
    ).pack(anchor="w", padx=16)
    if antall:
        tk.Label(
            parent,
            text="Sist oppdagede hemmeligheter:",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True),
        ).pack(anchor="w", padx=16, pady=(16, 4))
        for frase in [r[0] for r in EASTER_EGG_DATA if r[0] in funnet_easter_eggs][-8:]:
            tk.Label(
                parent,
                text="✓ " + frase,
                bg=color("panel"),
                fg=color("green"),
                font=font(9),
            ).pack(anchor="w", padx=22)


def vis_easter_egg_meny():
    if not settings["features"].get("fun", True):
        messagebox.showinfo(
            "Easter eggs", "Easter eggs er deaktivert i innstillingene."
        )
        return

    vindu = nytt_vindu("Hemmelig meny – Easter eggs", "760x720", (580, 500))
    vindu.configure(bg=color("bg"))

    topp = tk.Frame(vindu, bg=color("bg"), padx=16, pady=12)
    topp.pack(fill="x")
    tk.Label(
        topp,
        text="✦ DEN HEMMELIGE MENYEN ✦",
        bg=color("bg"),
        fg=color("text"),
        font=font(17, True),
    ).pack(anchor="w")
    tk.Label(
        topp,
        text=f"{len(EASTER_EGG_DATA)} skjulte fraser – hver med sin egen tematiske animasjon og illustrasjon. Skriv en frase i tallfeltet for å låse den opp.",
        bg=color("bg"),
        fg=color("muted"),
        font=font(9),
        wraplength=620,
    ).pack(anchor="w", pady=(4, 0))

    notebook = ttk.Notebook(vindu)
    notebook.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    alle_tab = tk.Frame(notebook, bg=color("panel"))
    fremgang_tab = tk.Frame(notebook, bg=color("panel"))
    notebook.add(alle_tab, text=f"Alle {len(EASTER_EGG_DATA)}")
    notebook.add(fremgang_tab, text="Progresjon")

    # Scrollable list of all secrets.
    holder = tk.Frame(alle_tab, bg=color("panel"))
    holder.pack(fill="both", expand=True)
    liste_canvas = tk.Canvas(holder, bg=color("panel"), highlightthickness=0)
    scrollbar = ttk.Scrollbar(holder, orient="vertical", command=liste_canvas.yview)
    liste_frame = tk.Frame(liste_canvas, bg=color("panel"))
    liste_frame.bind(
        "<Configure>",
        lambda event: liste_canvas.configure(scrollregion=liste_canvas.bbox("all")),
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
            rad,
            text=f"{indeks:02d}. {frase}",
            bg=color("panel_light"),
            fg=color("text"),
            font=font(9, True),
            anchor="w",
        ).pack(side="left", fill="x", expand=True)
        tk.Label(
            rad,
            text=status,
            bg=color("panel_light"),
            fg=statusfarge,
            font=font(8, True),
        ).pack(side="right")

    vis_easter_egg_fremgang(fremgang_tab)

    lag_knapp(vindu, "Lukk menyen", vindu.destroy, color("accent")).pack(pady=(0, 12))


# Backwards-compatible animated eggs from the original program.
ORIGINAL_EGGS = {
    "PETER ER DUM": egg_strobe,
    "TIRIL KAN IKKE LESE": egg_regnbue,
    "JOHAN-OLAI ER SMART": egg_konfetti,
    "MATRIX": egg_matrix,
    "DISCO": egg_disco,
}

# ============================================================
# HEMMELIG SPILLMENY – 6 SMÅ ARKADESPILL
# Åpnes ved å skrive: INGENTING Å SE HER
# ============================================================

SPILL_BG = "#10151f"
SPILL_PANEL = "#1b2636"
SPILL_FG = "#f2f5fa"
SPILL_ACCENT = "#65d6ad"


def spill_vindu(tittel, bredde=640, hoyde=480):
    vindu = tk.Toplevel(root)
    vindu.title(tittel)
    vindu.geometry(f"{bredde}x{hoyde}")
    vindu.resizable(False, False)
    vindu.configure(bg=SPILL_BG)
    vindu.transient(root)
    vindu.grab_set()
    return vindu


def start_space_invaders():
    w = spill_vindu("Space Invaders", 540, 590)
    c = tk.Canvas(w, width=500, height=500, bg="#070b18", highlightthickness=0)
    c.pack(pady=10)
    info = tk.Label(
        w,
        text="← / → eller A / D: flytt  •  Mellomrom: skyt  •  R: omstart",
        bg=SPILL_BG,
        fg=SPILL_FG,
    )
    info.pack()
    state = {
        "x": 250,
        "shots": [],
        "enemies": [],
        "score": 0,
        "lives": 3,
        "direction": 1,
        "over": False,
        "after": None,
        "cooldown": 0,
    }

    def reset():
        state.update(
            x=250,
            shots=[],
            enemies=[],
            score=0,
            lives=3,
            direction=1,
            over=False,
            cooldown=0,
        )
        wave()
        frame()

    def wave():
        state["enemies"] = [
            [65 + col * 62, 55 + row * 42, 1] for row in range(3) for col in range(6)
        ]

    def key(e):
        k = e.keysym.lower()
        if k == "r":
            reset()
            return
        if state["over"]:
            return
        if k in ("left", "a"):
            state["x"] = max(20, state["x"] - 24)
        elif k in ("right", "d"):
            state["x"] = min(480, state["x"] + 24)
        elif k == "space" and state["cooldown"] <= 0:
            state["shots"].append([state["x"], 440])
            state["cooldown"] = 10

    def frame():
        if not w.winfo_exists():
            return
        if state["over"]:
            return
        state["cooldown"] = max(0, state["cooldown"] - 1)
        enemies = state["enemies"]
        if enemies:
            edge = (
                max(e[0] for e in enemies)
                if state["direction"] > 0
                else min(e[0] for e in enemies)
            )
            if edge > 470 or edge < 30:
                state["direction"] *= -1
                for enemy in enemies:
                    enemy[1] += 18
            for enemy in enemies:
                enemy[0] += state["direction"] * 1.4
        for shot in state["shots"]:
            shot[1] -= 8
        state["shots"] = [a for a in state["shots"] if a[1] > 5]
        hit_shots = set()
        hit_enemies = set()
        for si, shot in enumerate(state["shots"]):
            for ei, enemy in enumerate(enemies):
                if abs(shot[0] - enemy[0]) < 17 and abs(shot[1] - enemy[1]) < 15:
                    hit_shots.add(si)
                    hit_enemies.add(ei)
                    state["score"] += 10
                    break
        state["shots"] = [v for i, v in enumerate(state["shots"]) if i not in hit_shots]
        state["enemies"] = [v for i, v in enumerate(enemies) if i not in hit_enemies]
        if not state["enemies"]:
            wave()
        if any(e[1] > 420 for e in state["enemies"]):
            state["over"] = True
        c.delete("all")
        for i in range(35):
            x = (i * 137) % 500
            y = (i * 83) % 470
            c.create_oval(x, y, x + 2, y + 2, fill="#56627c", outline="")
        c.create_rectangle(
            state["x"] - 16, 455, state["x"] + 16, 472, fill="#62e6c4", outline=""
        )
        c.create_rectangle(
            state["x"] - 4, 445, state["x"] + 4, 460, fill="#b8fff0", outline=""
        )
        for x, y in state["shots"]:
            c.create_rectangle(x - 2, y - 8, x + 2, y + 5, fill="#ffe36e", outline="")
        for x, y, _ in state["enemies"]:
            c.create_rectangle(
                x - 13, y - 9, x + 13, y + 9, fill="#a77cff", outline="#e0d2ff"
            )
            c.create_rectangle(x - 8, y - 3, x - 4, y + 1, fill="#101522", outline="")
            c.create_rectangle(x + 4, y - 3, x + 8, y + 1, fill="#101522", outline="")
        c.create_text(
            12,
            12,
            anchor="nw",
            text=f"POENG {state['score']}",
            fill="white",
            font=("Consolas", 12, "bold"),
        )
        if state["over"]:
            c.create_text(
                250,
                250,
                text="GAME OVER  •  R = NY RUNDE",
                fill="white",
                font=("Segoe UI", 17, "bold"),
            )
        else:
            state["after"] = w.after(30, frame)
        info.config(
            text=f"Poeng: {state['score']}  •  ←/→ eller A/D  •  Mellomrom skyter  •  R omstart"
        )

    w.bind("<Key>", key)
    w.focus_force()
    wave()
    frame()


def start_minesweeper():
    w = spill_vindu("Minesweeper", 430, 520)
    size, mine_count = 9, 10
    board = [[0 for _ in range(size)] for _ in range(size)]
    mines = set(
        random.sample([(x, y) for y in range(size) for x in range(size)], mine_count)
    )
    revealed, flags = set(), set()
    buttons = {}
    status = tk.Label(
        w, text="Venstreklikk: åpne  •  Høyreklikk: flagg", bg=SPILL_BG, fg=SPILL_FG
    )
    status.pack(pady=10)
    grid = tk.Frame(w, bg=SPILL_BG)
    grid.pack(padx=12, pady=8)
    for y in range(size):
        for x in range(size):
            board[y][x] = sum(
                (x + dx, y + dy) in mines
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                if (dx or dy) and 0 <= x + dx < size and 0 <= y + dy < size
            )

    def finish(won):
        for (x, y), b in buttons.items():
            if (x, y) in mines:
                b.config(text="✹", bg="#7b3544", fg="white")
            b.config(state="disabled")
        status.config(
            text="Du klarte det!" if won else "Bom! Prøv igjen med nytt brett."
        )

    def open_cell(x, y):
        if (x, y) in revealed or (x, y) in flags:
            return
        if (x, y) in mines:
            revealed.add((x, y))
            finish(False)
            return
        stack = [(x, y)]
        while stack:
            a, b = stack.pop()
            if (
                (a, b) in revealed
                or (a, b) in mines
                or not (0 <= a < size and 0 <= b < size)
            ):
                continue
            revealed.add((a, b))
            if board[b][a] == 0:
                stack.extend(
                    (a + dx, b + dy)
                    for dx in (-1, 0, 1)
                    for dy in (-1, 0, 1)
                    if dx or dy
                )
        for (a, b), btn in buttons.items():
            if (a, b) in revealed:
                val = board[b][a]
                btn.config(
                    text=str(val) if val else "",
                    bg="#34445c",
                    relief="sunken",
                    state="disabled",
                    disabledforeground=[
                        "#dce6f2",
                        "#72c7ff",
                        "#78df9b",
                        "#ffbd68",
                        "#ff7b88",
                    ][min(val, 4)],
                )
        if len(revealed) == size * size - mine_count:
            finish(True)

    def toggle_flag(x, y):
        if (x, y) in revealed:
            return
        if (x, y) in flags:
            flags.remove((x, y))
            buttons[x, y].config(text="")
        else:
            flags.add((x, y))
            buttons[x, y].config(text="⚑", fg="#ffd36a")
        status.config(
            text=f"Flagg: {len(flags)}/{mine_count}  •  Venstreklikk åpner, høyreklikk flagger"
        )

    for y in range(size):
        for x in range(size):
            b = tk.Button(
                grid,
                text="",
                width=3,
                height=1,
                font=("Consolas", 12, "bold"),
                bg="#26364b",
                fg="white",
                relief="raised",
                command=lambda a=x, b=y: open_cell(a, b),
            )
            b.grid(row=y, column=x, padx=1, pady=1)
            b.bind("<Button-3>", lambda e, a=x, b=y: (toggle_flag(a, b), "break"))
            buttons[x, y] = b

    tk.Button(
        w,
        text="Nytt brett",
        command=lambda: (w.destroy(), start_minesweeper()),
        bg="#34445c",
        fg="white",
        relief="flat",
        padx=16,
        pady=7,
    ).pack(pady=12)


def start_doom_arena():
    """Originalt, ikke-grafisk retro labyrintspill inspirert av 90-talls FPS."""
    w = spill_vindu("DOOM: Pixel Maze", 620, 500)
    width, height = 580, 390
    c = tk.Canvas(w, width=width, height=height, bg="#090b12", highlightthickness=0)
    c.pack(pady=8)
    info = tk.Label(
        w,
        text="WASD: gå  •  ←/→: snu  •  Mellomrom: zap roboter  •  R: start på nytt",
        bg=SPILL_BG,
        fg=SPILL_FG,
    )
    info.pack(pady=(0, 8))
    world = [
        "##########",
        "#........#",
        "#..##....#",
        "#........#",
        "#....#...#",
        "#........#",
        "#..##....#",
        "#........#",
        "#........#",
        "##########",
    ]
    start_enemies = [(6.5, 1.8), (7.5, 4.5), (2.5, 7.5), (7.5, 8.0)]
    st = {
        "x": 1.7,
        "y": 1.7,
        "angle": 0.0,
        "score": 0,
        "shots": 0,
        "enemies": [],
        "flash": 0,
        "over": False,
        "after": None,
    }
    fov = math.radians(62)

    def reset():
        st.update(
            x=1.7,
            y=1.7,
            angle=0.0,
            score=0,
            shots=0,
            enemies=[list(v) for v in start_enemies],
            flash=0,
            over=False,
        )
        frame()

    def wall(x, y):
        ix, iy = int(x), int(y)
        return (
            iy < 0
            or iy >= len(world)
            or ix < 0
            or ix >= len(world[0])
            or world[iy][ix] == "#"
        )

    def move(dx, dy):
        nx, ny = st["x"] + dx, st["y"] + dy
        if not wall(nx + (0.16 if dx > 0 else -0.16 if dx < 0 else 0), st["y"]):
            st["x"] = nx
        if not wall(st["x"], ny + (0.16 if dy > 0 else -0.16 if dy < 0 else 0)):
            st["y"] = ny

    def key(e):
        k = e.keysym.lower()
        if k == "r":
            reset()
            return
        if st["over"]:
            return
        if k in ("left",):
            st["angle"] -= 0.14
        elif k in ("right",):
            st["angle"] += 0.14
        elif k in ("w", "up"):
            move(math.cos(st["angle"]) * 0.20, math.sin(st["angle"]) * 0.20)
        elif k in ("s", "down"):
            move(-math.cos(st["angle"]) * 0.16, -math.sin(st["angle"]) * 0.16)
        elif k == "a":
            move(
                math.cos(st["angle"] - math.pi / 2) * 0.16,
                math.sin(st["angle"] - math.pi / 2) * 0.16,
            )
        elif k == "d":
            move(
                math.cos(st["angle"] + math.pi / 2) * 0.16,
                math.sin(st["angle"] + math.pi / 2) * 0.16,
            )
        elif k == "space":
            fire()

    def clear_path(ex, ey):
        dist = math.hypot(ex - st["x"], ey - st["y"])
        steps = max(1, int(dist / 0.06))
        for i in range(1, steps):
            t = i / steps
            if wall(st["x"] + (ex - st["x"]) * t, st["y"] + (ey - st["y"]) * t):
                return False
        return True

    def fire():
        if st["over"]:
            return
        st["shots"] += 1
        candidates = []
        for i, enemy in enumerate(st["enemies"]):
            dx, dy = enemy[0] - st["x"], enemy[1] - st["y"]
            dist = math.hypot(dx, dy)
            diff = (math.atan2(dy, dx) - st["angle"] + math.pi) % (
                2 * math.pi
            ) - math.pi
            if abs(diff) < 0.13 and dist < 8 and clear_path(*enemy):
                candidates.append((dist, i))
        if candidates:
            _, idx = min(candidates)
            st["enemies"].pop(idx)
            st["score"] += 100
        st["flash"] = 3
        if not st["enemies"]:
            st["over"] = True

    def frame():
        if not w.winfo_exists():
            return
        c.delete("all")
        c.create_rectangle(0, 0, width, height // 2, fill="#171a2b", outline="")
        c.create_rectangle(0, height // 2, width, height, fill="#302a2a", outline="")
        rays, depth = 145, []
        for i in range(rays):
            ray_angle = st["angle"] - fov / 2 + fov * i / (rays - 1)
            d = 0.04
            while d < 12 and not wall(
                st["x"] + math.cos(ray_angle) * d, st["y"] + math.sin(ray_angle) * d
            ):
                d += 0.035
            corrected = max(0.1, d * math.cos(ray_angle - st["angle"]))
            depth.append(corrected)
            h = min(height, 290 / corrected)
            shade = max(35, int(150 / (1 + corrected * 0.22)))
            color = f"#{shade:02x}{int(shade*0.72):02x}{int(shade*0.48):02x}"
            x1 = i * width / rays
            x2 = (i + 1) * width / rays + 1
            c.create_rectangle(
                x1, height / 2 - h / 2, x2, height / 2 + h / 2, fill=color, outline=""
            )
        # Tegn robotene som enkle, fiktive pikselfigurer, sortert bakerst først.
        visible = []
        for ex, ey in st["enemies"]:
            dx, dy = ex - st["x"], ey - st["y"]
            dist = math.hypot(dx, dy)
            diff = (math.atan2(dy, dx) - st["angle"] + math.pi) % (
                2 * math.pi
            ) - math.pi
            if abs(diff) < fov / 2 and dist > 0.2:
                sx = (0.5 + diff / fov) * width
                ray_i = max(0, min(rays - 1, int(sx / width * rays)))
                if clear_path(ex, ey) and dist < depth[ray_i] + 0.25:
                    visible.append((dist, sx))
        for dist, sx in sorted(visible, reverse=True):
            size = min(150, 100 / dist)
            y = height / 2
            c.create_rectangle(
                sx - size * 0.30,
                y - size * 0.38,
                sx + size * 0.30,
                y + size * 0.40,
                fill="#694b8f",
                outline="#c8a7ff",
                width=2,
            )
            c.create_rectangle(
                sx - size * 0.23,
                y - size * 0.55,
                sx + size * 0.23,
                y - size * 0.20,
                fill="#9b78c4",
                outline="#e4d4ff",
            )
            c.create_rectangle(
                sx - size * 0.15,
                y - size * 0.43,
                sx - size * 0.04,
                y - size * 0.34,
                fill="#ffdc78",
                outline="",
            )
            c.create_rectangle(
                sx + size * 0.04,
                y - size * 0.43,
                sx + size * 0.15,
                y - size * 0.34,
                fill="#ffdc78",
                outline="",
            )
            c.create_rectangle(
                sx - size * 0.18,
                y + size * 0.12,
                sx - size * 0.06,
                y + size * 0.32,
                fill="#45335e",
                outline="",
            )
            c.create_rectangle(
                sx + size * 0.06,
                y + size * 0.12,
                sx + size * 0.18,
                y + size * 0.32,
                fill="#45335e",
                outline="",
            )
        # Siktemerke og HUD.
        c.create_line(
            width / 2 - 8,
            height / 2,
            width / 2 + 8,
            height / 2,
            fill="#e9f4e8",
            width=2,
        )
        c.create_line(
            width / 2,
            height / 2 - 8,
            width / 2,
            height / 2 + 8,
            fill="#e9f4e8",
            width=2,
        )
        c.create_rectangle(0, height - 34, width, height, fill="#111827", outline="")
        c.create_text(
            12,
            height - 17,
            anchor="w",
            text=f"ENERGI 100   ROBOTER {len(st['enemies'])}   POENG {st['score']}",
            fill="#9ef0d2",
            font=("Consolas", 12, "bold"),
        )
        if st["flash"]:
            c.create_rectangle(
                width / 2 - 28,
                height - 65,
                width / 2 + 28,
                height - 35,
                fill="#d4e4f2",
                outline="#ffffff",
            )
            st["flash"] -= 1
        if st["over"]:
            msg = "LABYRINT RYDDET!" if not st["enemies"] else "FERDIG"
            c.create_rectangle(
                100, 145, 480, 235, fill="#101522", outline="#9ef0d2", width=2
            )
            c.create_text(
                width / 2, 175, text=msg, fill="#9ef0d2", font=("Consolas", 21, "bold")
            )
            c.create_text(
                width / 2,
                207,
                text="Trykk R for å spille igjen",
                fill="white",
                font=("Segoe UI", 11),
            )
        info.config(
            text="WASD: gå  •  ←/→: snu  •  Mellomrom: zap robot  •  R: start på nytt"
        )
        if not st["over"]:
            st["after"] = w.after(35, frame)

    w.bind("<Key>", key)
    w.focus_force()
    reset()


def vis_spillmeny():
    vindu = spill_vindu("INGENTING Å SE HER – Spillrom", 620, 700)
    tk.Label(
        vindu,
        text="ARKADEROMMET",
        bg=SPILL_BG,
        fg=SPILL_FG,
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=(18, 3))
    tk.Label(
        vindu,
        text="Ni små spill gjemt inne i Tall Sorterer.",
        bg=SPILL_BG,
        fg="#aab6c8",
        font=("Segoe UI", 10),
    ).pack(pady=(0, 10))

    outer = tk.Frame(vindu, bg=SPILL_BG)
    outer.pack(fill="both", expand=True, padx=22, pady=4)
    canvas = tk.Canvas(outer, bg=SPILL_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    ramme = tk.Frame(canvas, bg=SPILL_BG)
    ramme.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=ramme, anchor="nw", width=550)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    spill = [
        ("TETRIS", "Stable fallende blokker – piltaster og mellomrom.", start_tetris),
        ("PIXEL RUNNER", "Sidescroller – hopp over hindringer.", start_sidescroller),
        ("SNAKE", "Spis prikker og unngå vegger og egen hale.", start_snake),
        ("PONG", "Klassisk bordtennis mot datamaskinen.", start_pong),
        ("BREAKOUT", "Knus klossene med ballen.", start_breakout),
        ("MEMORY", "Finn alle parene med færrest mulig trekk.", start_memory),
        (
            "SPACE INVADERS",
            "Forsvar basen mot bølger av romvesener.",
            start_space_invaders,
        ),
        ("MINESWEEPER", "Åpne trygge ruter og flagg minene.", start_minesweeper),
        (
            "DOOM: PIXEL MAZE",
            "Retro førstepersons labyrint med roboter. WASD/piler + mellomrom.",
            start_doom_arena,
        ),
    ]
    for navn, tekst, funksjon in spill:
        kort = tk.Frame(ramme, bg=SPILL_PANEL, padx=14, pady=9)
        kort.pack(fill="x", pady=4)
        rad = tk.Frame(kort, bg=SPILL_PANEL)
        rad.pack(fill="x")
        tk.Label(
            rad,
            text=navn,
            bg=SPILL_PANEL,
            fg=SPILL_ACCENT,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        tk.Button(
            rad,
            text="SPILL",
            command=funksjon,
            bg="#34445c",
            fg="white",
            activebackground="#49617e",
            activeforeground="white",
            relief="flat",
            padx=16,
            cursor="hand2",
        ).pack(side="right")
        tk.Label(
            kort,
            text=tekst,
            bg=SPILL_PANEL,
            fg="#b7c2d2",
            font=("Segoe UI", 9),
            wraplength=470,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

    tk.Button(
        vindu,
        text="Lukk spillrom",
        command=vindu.destroy,
        bg="#34445c",
        fg="white",
        activebackground="#49617e",
        relief="flat",
        padx=18,
        pady=7,
    ).pack(pady=12)


def start_tetris():
    w = spill_vindu("Tetris", 360, 570)
    cw, ch, cell = 300, 500, 25
    c = tk.Canvas(w, width=cw, height=ch, bg="#080d16", highlightthickness=0)
    c.pack(pady=12)
    status = tk.Label(
        w, text="Piltaster: flytt/roter  •  Mellomrom: slipp", bg=SPILL_BG, fg=SPILL_FG
    )
    status.pack()
    cols, rows = 12, 20
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    colors = [
        "#42d6c5",
        "#4d7cff",
        "#ffad42",
        "#ffe05b",
        "#a66bff",
        "#58d68d",
        "#ff6685",
    ]
    shapes = [
        [[1, 1, 1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[1, 1], [1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[0, 1, 0], [1, 1, 1]],
        [[1, 1, 0], [0, 1, 1]],
    ]
    state = {"piece": None, "x": 4, "y": 0, "score": 0, "over": False, "after": None}

    def new_piece():
        idx = random.randrange(len(shapes))
        state.update(piece=[row[:] for row in shapes[idx]], x=4, y=0, color=colors[idx])
        if collision(state["piece"], state["x"], state["y"]):
            state["over"] = True
            status.config(
                text=f"Spillet er over – poeng: {state['score']}  •  Trykk R for nytt spill"
            )

    def collision(piece, x, y):
        for py, row in enumerate(piece):
            for px, val in enumerate(row):
                if val:
                    xx, yy = x + px, y + py
                    if (
                        xx < 0
                        or xx >= cols
                        or yy >= rows
                        or (yy >= 0 and board[yy][xx])
                    ):
                        return True
        return False

    def draw():
        c.delete("all")
        for yy in range(rows):
            for xx in range(cols):
                if board[yy][xx]:
                    c.create_rectangle(
                        xx * cell + 1,
                        yy * cell + 1,
                        (xx + 1) * cell - 1,
                        (yy + 1) * cell - 1,
                        fill=board[yy][xx],
                        outline="",
                    )
        if state["piece"]:
            for py, row in enumerate(state["piece"]):
                for px, val in enumerate(row):
                    if val:
                        c.create_rectangle(
                            (state["x"] + px) * cell + 1,
                            (state["y"] + py) * cell + 1,
                            (state["x"] + px + 1) * cell - 1,
                            (state["y"] + py + 1) * cell - 1,
                            fill=state["color"],
                            outline="",
                        )
        c.create_text(
            8,
            8,
            anchor="nw",
            text=f"POENG: {state['score']}",
            fill="white",
            font=("Consolas", 10, "bold"),
        )

    def tick():
        if not w.winfo_exists() or state["over"]:
            return
        if not collision(state["piece"], state["x"], state["y"] + 1):
            state["y"] += 1
        else:
            for py, row in enumerate(state["piece"]):
                for px, val in enumerate(row):
                    if val and state["y"] + py >= 0:
                        board[state["y"] + py][state["x"] + px] = state["color"]
            full = [i for i, row in enumerate(board) if all(row)]
            for i in reversed(full):
                board.pop(i)
                board.insert(0, [0] * cols)
            state["score"] += [0, 100, 300, 500, 800][min(len(full), 4)]
            new_piece()
        draw()
        state["after"] = w.after(420, tick)

    def key(e):
        k = e.keysym.lower()
        if k == "r":
            for row in board:
                row[:] = [0] * cols
            state.update(score=0, over=False)
            new_piece()
            draw()
            tick()
            return
        if state["over"]:
            return
        if k in ("left", "right"):
            nx = state["x"] + (-1 if k == "left" else 1)
            if not collision(state["piece"], nx, state["y"]):
                state["x"] = nx
        elif k == "down":
            if not collision(state["piece"], state["x"], state["y"] + 1):
                state["y"] += 1
                state["score"] += 1
        elif k == "up":
            rotated = [list(row) for row in zip(*state["piece"][::-1])]
            if not collision(rotated, state["x"], state["y"]):
                state["piece"] = rotated
        elif k == "space":
            while not collision(state["piece"], state["x"], state["y"] + 1):
                state["y"] += 1
        draw()

    w.bind("<Key>", key)
    w.focus_force()
    new_piece()
    draw()
    tick()


def start_sidescroller():
    w = spill_vindu("Pixel Runner – Sidescroller", 720, 390)
    c = tk.Canvas(w, width=680, height=300, bg="#9bd8ef", highlightthickness=0)
    c.pack(pady=12)
    tk.Label(
        w, text="Mellomrom / ↑ = hopp  •  R = start på nytt", bg=SPILL_BG, fg=SPILL_FG
    ).pack()
    ground = 250
    player = {"y": ground - 34, "vy": 0, "air": False}
    obstacles = []
    state = {"score": 0, "over": False, "after": None, "speed": 7}

    def reset():
        c.delete("all")
        obstacles.clear()
        player.update(y=ground - 34, vy=0, air=False)
        state.update(score=0, over=False, speed=7)
        frame()

    def jump(e=None):
        if state["over"]:
            reset()
        elif not player["air"]:
            player["vy"] = -14
            player["air"] = True

    def frame():
        if not w.winfo_exists():
            return
        c.delete("all")
        c.create_rectangle(0, ground, 680, 300, fill="#4e9b5b", outline="")
        c.create_line(0, ground, 680, ground, fill="#285d3c", width=4)
        player["vy"] += 0.8
        player["y"] += player["vy"]
        if player["y"] >= ground - 34:
            player.update(y=ground - 34, vy=0, air=False)
        px1, py1, px2, py2 = 85, player["y"], 119, player["y"] + 34
        c.create_rectangle(
            px1, py1, px2, py2, fill="#ffcf4a", outline="#28364a", width=2
        )
        if random.random() < 0.035 and (not obstacles or obstacles[-1][0] < 480):
            obstacles.append([690, random.choice([28, 38, 48])])
        for ob in obstacles:
            ob[0] -= state["speed"]
        obstacles[:] = [o for o in obstacles if o[0] > -30]
        for ox, oh in obstacles:
            c.create_rectangle(
                ox,
                ground - oh,
                ox + 22,
                ground,
                fill="#e75b55",
                outline="#8f302d",
                width=2,
            )
            if px2 > ox + 3 and px1 < ox + 19 and py2 > ground - oh + 3:
                state["over"] = True
        state["score"] += 1
        state["speed"] = min(13, 7 + state["score"] // 700)
        c.create_text(
            12,
            12,
            anchor="nw",
            text=f"DISTANSE  {state['score']//5}",
            fill="#173047",
            font=("Consolas", 13, "bold"),
        )
        if state["over"]:
            c.create_text(
                340,
                120,
                text="GAME OVER",
                fill="#9b2635",
                font=("Segoe UI", 28, "bold"),
            )
            c.create_text(
                340,
                160,
                text="Trykk mellomrom for å prøve igjen",
                fill="#173047",
                font=("Segoe UI", 12),
            )
        else:
            state["after"] = w.after(30, frame)

    w.bind("<space>", jump)
    w.bind("<Up>", jump)
    w.bind("r", lambda e: reset())
    w.focus_force()
    frame()


def start_snake():
    w = spill_vindu("Snake", 430, 490)
    cell = 20
    cols = 20
    rows = 20
    c = tk.Canvas(
        w, width=cols * cell, height=rows * cell, bg="#0b1118", highlightthickness=0
    )
    c.pack(pady=12)
    info = tk.Label(
        w,
        text="Piltaster styrer slangen  •  R starter på nytt",
        bg=SPILL_BG,
        fg=SPILL_FG,
    )
    info.pack()
    state = {
        "snake": [(9, 10), (8, 10), (7, 10)],
        "dir": (1, 0),
        "food": (14, 10),
        "over": False,
        "after": None,
        "score": 0,
    }

    def reset():
        state.update(
            snake=[(9, 10), (8, 10), (7, 10)],
            dir=(1, 0),
            food=(14, 10),
            over=False,
            score=0,
        )
        draw()
        tick()

    def key(e):
        dirs = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}
        if e.keysym.lower() == "r":
            reset()
            return
        d = dirs.get(e.keysym)
        if d and d != (-state["dir"][0], -state["dir"][1]):
            state["dir"] = d

    def draw():
        c.delete("all")
        for x, y in state["snake"]:
            c.create_rectangle(
                x * cell + 1,
                y * cell + 1,
                (x + 1) * cell - 1,
                (y + 1) * cell - 1,
                fill="#52d69a",
                outline="",
            )
        x, y = state["food"]
        c.create_oval(
            x * cell + 3,
            y * cell + 3,
            (x + 1) * cell - 3,
            (y + 1) * cell - 3,
            fill="#ff647c",
            outline="",
        )
        info.config(
            text=f"Poeng: {state['score']}   •   Piltaster styrer   •   R starter på nytt"
        )
        if state["over"]:
            c.create_text(
                200, 200, text="GAME OVER", fill="white", font=("Segoe UI", 24, "bold")
            )

    def tick():
        if not w.winfo_exists() or state["over"]:
            return
        x, y = state["snake"][0]
        dx, dy = state["dir"]
        head = (x + dx, y + dy)
        if (
            head[0] < 0
            or head[0] >= cols
            or head[1] < 0
            or head[1] >= rows
            or head in state["snake"][:-1]
        ):
            state["over"] = True
            draw()
            return
        state["snake"].insert(0, head)
        if head == state["food"]:
            state["score"] += 10
            empty = [
                (a, b)
                for a in range(cols)
                for b in range(rows)
                if (a, b) not in state["snake"]
            ]
            if empty:
                state["food"] = random.choice(empty)
        else:
            state["snake"].pop()
        draw()
        state["after"] = w.after(max(65, 125 - state["score"] // 5), tick)

    w.bind("<Key>", key)
    w.focus_force()
    draw()
    tick()


def start_pong():
    w = spill_vindu("Pong", 650, 440)
    c = tk.Canvas(w, width=620, height=360, bg="#080d16", highlightthickness=0)
    c.pack(pady=12)
    info = tk.Label(
        w,
        text="W/S eller ↑/↓ styrer venstre racket. Høyre racket styres av datamaskinen.",
        bg=SPILL_BG,
        fg=SPILL_FG,
    )
    info.pack()
    st = {
        "py": 150,
        "ey": 150,
        "x": 310,
        "y": 180,
        "vx": 4,
        "vy": 3,
        "score": 0,
        "opp": 0,
        "after": None,
    }

    def key(e):
        if e.keysym.lower() == "w" or e.keysym == "Up":
            st["py"] = max(5, st["py"] - 25)
        if e.keysym.lower() == "s" or e.keysym == "Down":
            st["py"] = min(295, st["py"] + 25)

    def frame():
        if not w.winfo_exists():
            return
        st["x"] += st["vx"]
        st["y"] += st["vy"]
        if st["y"] < 8 or st["y"] > 352:
            st["vy"] *= -1
        if 35 < st["x"] < 48 and st["py"] - 5 < st["y"] < st["py"] + 75:
            st["vx"] = abs(st["vx"]) * 1.04
        if 572 < st["x"] < 585 and st["ey"] - 5 < st["y"] < st["ey"] + 75:
            st["vx"] = -abs(st["vx"]) * 1.04
        st["ey"] += max(-4, min(4, st["y"] - (st["ey"] + 37)))
        if st["x"] < 0:
            st["opp"] += 1
            st.update(x=310, y=180, vx=4, vy=3)
        if st["x"] > 620:
            st["score"] += 1
            st.update(x=310, y=180, vx=-4, vy=3)
        c.delete("all")
        c.create_line(310, 0, 310, 360, fill="#314052", dash=(5, 7))
        c.create_rectangle(30, st["py"], 43, st["py"] + 75, fill="#5de0b2", outline="")
        c.create_rectangle(
            577, st["ey"], 590, st["ey"] + 75, fill="#ffbd59", outline=""
        )
        c.create_oval(
            st["x"] - 7, st["y"] - 7, st["x"] + 7, st["y"] + 7, fill="white", outline=""
        )
        c.create_text(
            270, 20, text=st["score"], fill="white", font=("Consolas", 18, "bold")
        )
        c.create_text(
            350, 20, text=st["opp"], fill="white", font=("Consolas", 18, "bold")
        )
        info.config(
            text=f"Du {st['score']} – Datamaskin {st['opp']}   •   W/S eller ↑/↓"
        )
        st["after"] = w.after(20, frame)

    w.bind("<Key>", key)
    w.focus_force()
    frame()


def start_breakout():
    w = spill_vindu("Breakout", 620, 510)
    c = tk.Canvas(w, width=580, height=430, bg="#0b101a", highlightthickness=0)
    c.pack(pady=10)
    info = tk.Label(
        w, text="← / → flytter brettet. R starter på nytt.", bg=SPILL_BG, fg=SPILL_FG
    )
    info.pack()
    st = {
        "px": 250,
        "x": 290,
        "y": 350,
        "vx": 3,
        "vy": -4,
        "bricks": [],
        "score": 0,
        "lives": 3,
        "over": False,
        "after": None,
    }

    def setup():
        st.update(
            px=250,
            x=290,
            y=350,
            vx=3,
            vy=-4,
            score=0,
            lives=3,
            over=False,
            bricks=[(25 + x * 76, 35 + y * 25) for y in range(5) for x in range(7)],
        )

    def key(e):
        if e.keysym.lower() == "r":
            setup()
            draw()
            frame()
            return
        if e.keysym == "Left":
            st["px"] = max(0, st["px"] - 28)
        if e.keysym == "Right":
            st["px"] = min(500, st["px"] + 28)

    def draw():
        c.delete("all")
        for i, (x, y) in enumerate(st["bricks"]):
            c.create_rectangle(
                x,
                y,
                x + 65,
                y + 17,
                fill=["#ff687a", "#ffad55", "#f3d45c", "#5bd6a4", "#6a9cff"][i % 5],
                outline="",
            )
        c.create_rectangle(
            st["px"], 395, st["px"] + 80, 407, fill="#e9f1ff", outline=""
        )
        c.create_oval(
            st["x"] - 7,
            st["y"] - 7,
            st["x"] + 7,
            st["y"] + 7,
            fill="#6de4c0",
            outline="",
        )
        info.config(text=f"Poeng: {st['score']}   •   Liv: {st['lives']}   •   ← / →")
        if st["over"]:
            c.create_text(
                290,
                220,
                text="FERDIG!  Trykk R",
                fill="white",
                font=("Segoe UI", 22, "bold"),
            )

    def frame():
        if not w.winfo_exists() or st["over"]:
            return
        st["x"] += st["vx"]
        st["y"] += st["vy"]
        if st["x"] < 7 or st["x"] > 573:
            st["vx"] *= -1
        if st["y"] < 7:
            st["vy"] *= -1
        if (
            380 < st["y"] < 405
            and st["px"] - 7 < st["x"] < st["px"] + 87
            and st["vy"] > 0
        ):
            st["vy"] *= -1
        hit = None
        for b in st["bricks"]:
            bx, by = b
            if bx - 7 < st["x"] < bx + 72 and by - 7 < st["y"] < by + 24:
                hit = b
                break
        if hit:
            st["bricks"].remove(hit)
            st["vy"] *= -1
            st["score"] += 10
        if st["y"] > 430:
            st["lives"] -= 1
            if st["lives"] <= 0:
                st["over"] = True
            else:
                st.update(x=290, y=350, vx=3, vy=-4)
        if not st["bricks"]:
            st["over"] = True
        draw()
        if not st["over"]:
            st["after"] = w.after(16, frame)

    setup()
    w.bind("<Key>", key)
    w.focus_force()
    draw()
    frame()


def start_memory():
    w = spill_vindu("Memory", 460, 520)
    symbols = ["★", "♫", "☀", "♞", "♦", "☂", "☕", "⚡"] * 2
    random.shuffle(symbols)
    state = {"open": [], "matched": set(), "moves": 0, "locked": False}
    top = tk.Label(
        w,
        text="Finn alle de åtte parene",
        bg=SPILL_BG,
        fg=SPILL_FG,
        font=("Segoe UI", 15, "bold"),
    )
    top.pack(pady=12)
    grid = tk.Frame(w, bg=SPILL_BG)
    grid.pack(padx=18, pady=8)
    buttons = []

    def update():
        top.config(text=f"Trekk: {state['moves']}   •   Par: {len(state['matched'])}/8")

    def flip(i):
        if state["locked"] or i in state["matched"] or i in state["open"]:
            return
        buttons[i].config(text=symbols[i], fg=SPILL_FG, bg="#405a78")
        state["open"].append(i)
        if len(state["open"]) == 2:
            state["moves"] += 1
            a, b = state["open"]
            if symbols[a] == symbols[b]:
                state["matched"].update((a, b))
                state["open"] = []
            else:
                state["locked"] = True

                def hide():
                    if not w.winfo_exists():
                        return
                    for j in (a, b):
                        buttons[j].config(text="?", bg="#26364b")
                    state["open"] = []
                    state["locked"] = False
                    update()

                w.after(750, hide)
        update()
        if len(state["matched"]) == 16:
            top.config(text=f"Du fant alle parene på {state['moves']} trekk!")

    for i in range(16):
        b = tk.Button(
            grid,
            text="?",
            width=7,
            height=3,
            font=("Segoe UI", 16, "bold"),
            bg="#26364b",
            fg=SPILL_FG,
            activebackground="#405a78",
            relief="flat",
            command=lambda j=i: flip(j),
        )
        b.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        buttons.append(b)
    tk.Button(
        w,
        text="Bland på nytt",
        command=lambda: (w.destroy(), start_memory()),
        bg="#34445c",
        fg="white",
        relief="flat",
        padx=15,
        pady=7,
    ).pack(pady=12)


# ============================================================
# BETA 1.8 – EKSTRA SPILLBIBLIOTEK OG R-MATEMATIKK
# ============================================================

EKSTRA_SPILL = [
    ("Asteroid Patrol", "Styr et romskip og unngå asteroider.", "dodge"),
    ("Robot Defense", "Forsvar basen mot roboter som nærmer seg.", "target"),
    ("Ghost Hunt", "Finn spøkelsene før tiden går ut.", "whack"),
    (
        "Deep Space Rescue",
        "Naviger gjennom rommet og samle redningskapsler.",
        "collect",
    ),
    ("Frog Crossing", "Kryss trafikkerte veier uten å bli truffet.", "lanes"),
    ("Tunnel Rush", "Unngå veggene i en stadig smalere tunnel.", "dodge"),
    ("Cave Flyer", "Fly gjennom en grotte med skiftende åpning.", "fly"),
    ("Volcano Escape", "Hopp mellom plattformer mens lavaen stiger.", "platform"),
    ("Tower Climber", "Klatre oppover og unngå fallende hindringer.", "climb"),
    ("Micro Maze", "Finn veien gjennom en tilfeldig labyrint.", "maze"),
    ("Circuit Connect", "Koble start og mål med færrest mulig trekk.", "connect"),
    ("Cargo Sorter", "Sorter pakker etter riktig kategori.", "sort"),
    ("Potion Mixer", "Bland ingredienser i riktig rekkefølge.", "sequence"),
    ("Bubble Pop", "Sprekk bobler før de når toppen.", "click"),
    ("Ninja Fruit", "Klikk fruktene og unngå bombene.", "click"),
    ("Target Practice", "Treff bevegelige mål med museklikk.", "target"),
    ("Stack Master", "Stable blokker så presist som mulig.", "stack"),
    ("Moon Lander", "Land romfartøyet med lav nok hastighet.", "lander"),
    ("Treasure Diver", "Samle skatter og pass deg for farer under vann.", "collect"),
    ("Crystal Cavern", "Samle krystaller i en grotte.", "maze"),
    ("Pixel Golf", "Juster vinkel og kraft for å få ballen i hullet.", "golf"),
    ("Paper Plane", "Fly papirflyet gjennom ringene.", "fly"),
    ("Color Switch", "Trykk når figuren matcher fargen.", "color"),
    ("Quick Math", "Løs regnestykker mot klokken.", "math"),
    ("Number Guess", "Gjett det skjulte tallet med færrest forsøk.", "guess"),
    ("Word Scramble", "Sett bokstavene sammen til riktig ord.", "word"),
    ("Simon Sequence", "Husk og gjenta en stadig lengre sekvens.", "simon"),
    ("Lights Out", "Slå av alle lysene på brettet.", "lights"),
    ("2048 Mini", "Slå sammen like tall og nå 2048.", "2048"),
    ("Sudoku Mini", "Fyll inn et lite 4×4 sudoku-brett.", "sudoku"),
    ("Paddle Panic", "Hold ballen i spill med en bevegelig plate.", "paddle"),
    ("Orbit Defender", "Forsvar planeten fra innkommende objekter.", "orbit"),
    ("Magnet Maze", "Bruk magnetkraft til å flytte en kule til målet.", "maze"),
    ("Bridge Builder", "Bygg en bro som tåler den angitte belastningen.", "bridge"),
    ("Pattern Finder", "Finn neste ledd i en mønsterrekke.", "pattern"),
    ("Binary Breaker", "Konverter binærtall til desimaltall.", "binary"),
    ("Fraction Frenzy", "Velg riktig brøk før tiden går ut.", "fraction"),
    (
        "Periodic Table Dash",
        "Finn grunnstoffet ut fra symbol eller atomnummer.",
        "chem",
    ),
    ("Soundless DJ", "Husk og gjenta rytmemønstre visuelt.", "simon"),
    ("Star Cartographer", "Koble stjerner i riktig konstellasjon.", "connect"),
]


def start_ekstra_spill(navn, beskrivelse, modus):
    """Selvstendige minispill med felles vindusramme og modusspesifikk spillmekanikk."""
    w = spill_vindu(navn, 620, 560)
    c = tk.Canvas(w, width=580, height=390, bg="#0a1220", highlightthickness=0)
    c.pack(padx=10, pady=8)
    status = tk.Label(w, text=beskrivelse, bg=SPILL_BG, fg=SPILL_FG, wraplength=560)
    status.pack(pady=5)
    panel = tk.Frame(w, bg=SPILL_BG)
    panel.pack(pady=5)
    st = {
        "score": 0,
        "time": 30,
        "running": True,
        "pos": 0,
        "tries": 0,
        "target": random.randint(1, 30),
        "seq": [],
        "step": 0,
        "cells": [],
        "player": (1, 1),
        "items": [],
        "vx": 3,
        "vy": 2,
        "x": 280,
        "y": 190,
        "lives": 3,
    }
    c.create_text(
        290, 24, text=navn.upper(), fill="#75e5c1", font=("Consolas", 18, "bold")
    )

    def finish(msg):
        st["running"] = False
        c.create_rectangle(
            70, 135, 510, 270, fill="#17263a", outline="#75e5c1", width=2
        )
        c.create_text(290, 175, text=msg, fill="white", font=("Segoe UI", 19, "bold"))
        c.create_text(
            290,
            215,
            text=f"Poeng: {st['score']}   •   Trykk NY RUNDE",
            fill="#a9c7df",
            font=("Segoe UI", 11),
        )

    def button(text, cmd):
        tk.Button(
            panel,
            text=text,
            command=cmd,
            bg="#34445c",
            fg="white",
            activebackground="#49617e",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=3)

    def restart():
        for child in panel.winfo_children():
            child.destroy()
        c.delete("all")
        st.update(
            score=0,
            time=30,
            running=True,
            pos=0,
            tries=0,
            target=random.randint(1, 30),
            seq=[],
            step=0,
            cells=[],
            player=(1, 1),
            items=[],
            x=280,
            y=190,
            lives=3,
        )
        run_game()

    def run_game():
        c.delete("all")
        c.create_text(
            290, 24, text=navn.upper(), fill="#75e5c1", font=("Consolas", 18, "bold")
        )
        if modus in ("dodge", "fly", "lander", "paddle", "orbit"):
            st["items"] = [
                [
                    random.randint(20, 560),
                    random.randint(-360, -20),
                    random.randint(8, 18),
                ]
                for _ in range(9)
            ]
            st["x"], st["y"] = 290, 330

            def key(e):
                if e.keysym in ("Left", "a"):
                    st["x"] = max(20, st["x"] - 22)
                if e.keysym in ("Right", "d"):
                    st["x"] = min(560, st["x"] + 22)
                if e.keysym in ("Up", "space"):
                    st["y"] = max(65, st["y"] - 18)
                if e.keysym in ("Down", "s"):
                    st["y"] = min(365, st["y"] + 18)

            w.bind("<Key>", key)
            w.focus_force()

            def tick():
                if not w.winfo_exists() or not st["running"]:
                    return
                c.delete("all")
                c.create_text(
                    12,
                    12,
                    anchor="nw",
                    text=f"Poeng {st['score']}  •  Liv {st['lives']}",
                    fill="white",
                )
                c.create_oval(
                    st["x"] - 12,
                    st["y"] - 12,
                    st["x"] + 12,
                    st["y"] + 12,
                    fill="#65d6ad",
                    outline="white",
                )
                for ob in st["items"]:
                    ob[1] += 5
                    c.create_oval(
                        ob[0] - ob[2],
                        ob[1] - ob[2],
                        ob[0] + ob[2],
                        ob[1] + ob[2],
                        fill="#ffb454",
                        outline="",
                    )
                    if math.hypot(ob[0] - st["x"], ob[1] - st["y"]) < ob[2] + 12:
                        st["lives"] -= 1
                        ob[1] = -30
                    if ob[1] > 410:
                        ob[1] = -random.randint(30, 250)
                        ob[0] = random.randint(20, 560)
                        st["score"] += 1
                if st["lives"] <= 0:
                    finish("SPILLET ER OVER")
                else:
                    w.after(35, tick)

            tick()
        elif modus in ("target", "whack", "click", "collect"):
            st["target_pos"] = [random.randint(50, 530), random.randint(80, 350)]

            def hit():
                if not st["running"]:
                    return
                st["score"] += 1
                st["target_pos"] = [random.randint(45, 535), random.randint(80, 350)]
                draw_target()

            def draw_target():
                c.delete("all")
                c.create_text(
                    290,
                    24,
                    text=f"TREFF MÅL  •  POENG {st['score']}",
                    fill="white",
                    font=("Consolas", 15, "bold"),
                )
                x, y = st["target_pos"]
                c.create_oval(
                    x - 22,
                    y - 22,
                    x + 22,
                    y + 22,
                    fill="#e65e78",
                    outline="white",
                    width=2,
                )
                c.create_oval(x - 8, y - 8, x + 8, y + 8, fill="#ffe27a", outline="")

            def click(e):
                x, y = st["target_pos"]
                if math.hypot(e.x - x, e.y - y) < 25:
                    hit()

            c.bind("<Button-1>", click)
            draw_target()

            def countdown():
                if not w.winfo_exists() or not st["running"]:
                    return
                st["time"] -= 1
                status.config(text=f"Tid igjen: {st['time']} sekunder • Klikk på målet")
                if st["time"] <= 0:
                    finish("TIDEN ER UTE")
                else:
                    w.after(1000, countdown)

            countdown()
        elif modus in (
            "math",
            "guess",
            "binary",
            "fraction",
            "pattern",
            "word",
            "chem",
        ):
            if modus == "guess":
                q = f"Gjett tallet mellom 1 og 30. (Mål: {st['target']})"
                answer = st["target"]
            elif modus == "binary":
                answer = random.randint(2, 63)
                q = f"Hva er {answer:b}₂ i titallssystemet?"
            elif modus == "fraction":
                a, b, d = (
                    random.randint(1, 8),
                    random.randint(2, 9),
                    random.randint(2, 9),
                )
                answer = round(a / b + d / b, 4)
                q = f"Hva er {a}/{b} + {d}/{b}? (desimaltall)"
            elif modus == "pattern":
                a = random.randint(1, 8)
                step = random.randint(2, 6)
                answer = a + step * 4
                q = f"Hvilket tall mangler? {a}, {a+step}, {a+2*step}, ?, {a+4*step}"
            elif modus == "word":
                word = random.choice(["MATTE", "TALL", "KODE", "SPILL", "ROMSKIP"])
                answer = word
                q = "Skriv ordet riktig: " + " ".join(
                    random.sample(list(word), len(word))
                )
            elif modus == "chem":
                pairs = [
                    ("H", "Hydrogen"),
                    ("O", "Oksygen"),
                    ("C", "Karbon"),
                    ("Fe", "Jern"),
                    ("Au", "Gull"),
                    ("Na", "Natrium"),
                ]
                sym, answer = random.choice(pairs)
                q = f"Hvilket grunnstoff har symbolet {sym}?"
            else:
                a, b = random.randint(2, 20), random.randint(2, 20)
                op = random.choice(["+", "−", "×"])
                answer = a + b if op == "+" else a - b if op == "−" else a * b
                q = f"Regn ut: {a} {op} {b}"
            tk.Label(
                panel, text=q, bg=SPILL_BG, fg="white", font=("Segoe UI", 12, "bold")
            ).pack(side="left", padx=4)
            ent = tk.Entry(panel, width=12, font=("Consolas", 12))
            ent.pack(side="left", padx=4)
            ent.focus_set()

            def submit():
                raw = ent.get().strip()
                try:
                    ok = (
                        (abs(float(raw) - float(answer)) < 1e-4)
                        if isinstance(answer, (int, float))
                        else raw.upper() == str(answer).upper()
                    )
                except Exception:
                    ok = False
                if ok:
                    st["score"] += 1
                    status.config(text=f"Riktig! Poeng: {st['score']}")
                    restart()
                else:
                    status.config(text="Ikke helt riktig – prøv igjen.")

            button("Svar", submit)
        elif modus in ("sequence", "simon"):
            colors = ["RØD", "BLÅ", "GRØNN", "GUL"]
            st["seq"] = [
                random.choice(colors) for _ in range(4 if modus == "sequence" else 3)
            ]
            tk.Label(panel, text="Husk sekvensen:", bg=SPILL_BG, fg="white").pack(
                side="left"
            )
            shown = tk.Label(
                panel,
                text="  →  ".join(st["seq"]),
                bg=SPILL_BG,
                fg="#ffd36a",
                font=("Consolas", 12, "bold"),
            )
            shown.pack(side="left")

            def hide():
                shown.config(text="?  ?  ?  ?")

            w.after(2200, hide)
            ent = tk.Entry(panel, width=25)
            ent.pack(side="left")

            def check():
                if ent.get().upper().replace(",", " ").split() == st["seq"]:
                    st["score"] = 10
                    finish("PERFEKT HUKOMMELSE!")
                else:
                    finish("SEKVENSEN VAR: " + " – ".join(st["seq"]))

            button("Kontroller", check)
        elif modus in (
            "maze",
            "connect",
            "lights",
            "2048",
            "sudoku",
            "sort",
            "bridge",
            "stack",
            "golf",
            "platform",
            "climb",
            "lanes",
        ):
            # Distinct rule/puzzle panels, with stateful user actions and score.
            prompts = {
                "maze": "Finn utgangen: velg riktig retning i labyrinten.",
                "connect": "Koble sammen start og mål ved å velge 1–4.",
                "lights": "Slå av lysene: velg tallene som er tent.",
                "2048": "Velg to like tall for å slå dem sammen.",
                "sudoku": "Hvilket tall mangler i raden 1, 2, 4, ?",
                "sort": "Sorter tallene fra minst til størst.",
                "bridge": "Broen tåler 20 kg per planke. Velg antall planker for 75 kg.",
                "stack": "Stable blokkene i riktig rekkefølge: liten til stor.",
                "golf": "Velg slagstyrke (1–10) for å nå 70 meter.",
                "platform": "Velg riktig plattform: 1, 3, 5, ?",
                "climb": "Klatre: velg neste trinn i 2, 4, 8, 16, ?",
                "lanes": "Unngå trafikken: velg trygg bane 1, 2 eller 3.",
            }
            q = prompts[modus]
            tk.Label(panel, text=q, bg=SPILL_BG, fg="white", wraplength=500).pack(
                side="left", padx=4
            )
            ent = tk.Entry(panel, width=12)
            ent.pack(side="left")
            expected = {
                "maze": "ØST",
                "connect": "3",
                "lights": "2",
                "2048": "4",
                "sudoku": "3",
                "sort": "1 2 3 4",
                "bridge": "4",
                "stack": "1 2 3",
                "golf": "7",
                "platform": "7",
                "climb": "32",
                "lanes": "2",
            }[modus]

            def check():
                if ent.get().strip().upper() == expected:
                    finish("OPPGAVE KLART!")
                else:
                    status.config(text="Prøv igjen – les oppgaven nøye.")

            button("Kontroller", check)
        else:
            c.create_text(
                290,
                180,
                text=beskrivelse,
                fill="white",
                font=("Segoe UI", 14),
                width=460,
            )
            button(
                "Få poeng",
                lambda: (
                    st.update(score=st["score"] + 1),
                    status.config(text=f"Poeng: {st['score']}"),
                ),
            )
        button("Ny runde", restart)

    run_game()


def start_pocket_creatures():
    """Originalt skapningssamlerspill inspirert av monster-samlersjangeren."""
    w = spill_vindu("Pocket Creatures – Ekspedisjon", 620, 600)
    creatures = [
        {"name": "Flamling", "type": "Ild", "hp": 28, "atk": 9, "skill": "Gnistsalve"},
        {"name": "Mossel", "type": "Natur", "hp": 36, "atk": 7, "skill": "Rotgrep"},
        {"name": "Bølvi", "type": "Vann", "hp": 32, "atk": 8, "skill": "Bølgeslag"},
        {"name": "Voltass", "type": "Lyn", "hp": 25, "atk": 11, "skill": "Lynpuls"},
        {"name": "Steinok", "type": "Jord", "hp": 42, "atk": 6, "skill": "Steinras"},
        {"name": "Skyra", "type": "Luft", "hp": 27, "atk": 10, "skill": "Vindstøt"},
    ]
    team = [dict(random.choice(creatures))]
    coins = 0
    area = 0
    head = tk.Label(
        w,
        text="POCKET CREATURES",
        bg=SPILL_BG,
        fg="#ffd36a",
        font=("Segoe UI", 20, "bold"),
    )
    head.pack(pady=12)
    desc = tk.Label(
        w,
        text="Utforsk områder, møt ville skapninger og bygg laget ditt.",
        bg=SPILL_BG,
        fg=SPILL_FG,
        wraplength=560,
    )
    desc.pack(pady=5)
    stats = tk.Label(w, text="", bg=SPILL_BG, fg="#8fe0c2", font=("Consolas", 11))
    stats.pack(pady=5)
    log = tk.Text(
        w,
        width=66,
        height=13,
        bg="#0a1220",
        fg="#eaf0f8",
        insertbackground="white",
        wrap="word",
        state="disabled",
    )
    log.pack(padx=14, pady=8)
    actions = tk.Frame(w, bg=SPILL_BG)
    actions.pack(pady=8)

    def say(t):
        log.config(state="normal")
        log.insert("end", t + "\n")
        log.see("end")
        log.config(state="disabled")

    def update():
        stats.config(
            text=f"Område {area+1}  •  Lag: {len(team)}/4  •  Utforskningsmerker: {coins}"
        )

    def explore():
        nonlocal area
        area += 1
        wild = dict(random.choice(creatures))
        wild["hp"] += area * 2
        say(
            f"Du utforsker område {area}. En vill {wild['name']} ({wild['type']}) dukker opp!"
        )

        def battle():
            nonlocal coins
            player = team[0]
            php = player["hp"]
            whp = wild["hp"]
            say(f"Kamp: {player['name']} mot {wild['name']}!")

            def turn():
                nonlocal php, whp, coins
                if php <= 0:
                    say("Du trekker deg tilbake. Laget trenger hvile.")
                    return
                if whp <= 0:
                    say(f"{wild['name']} er beseiret. Du får et merke.")
                    coins += 1
                    if len(team) < 4 and random.random() < 0.75:
                        team.append(dict(wild))
                        say(f"{wild['name']} blir med på laget!")
                    update()
                    return
                whp -= player["atk"]
                say(
                    f"{player['name']} bruker {player['skill']} ({player['atk']} skade). Vill HP: {max(0,whp)}"
                )
                if whp > 0:
                    php -= wild["atk"]
                    say(f"{wild['name']} svarer. Din HP: {max(0,php)}")
                update()
                if whp <= 0 or php <= 0:
                    turn_result()

            def turn_result():
                if whp <= 0:
                    say(f"Seier! {wild['name']} er slått.")
                    coins += 1
                    if len(team) < 4 and random.random() < 0.75:
                        team.append(dict(wild))
                        say(f"{wild['name']} slutter seg til laget.")
                    update()
                elif php <= 0:
                    say("Kampen er tapt. Prøv et annet område senere.")

            tk.Button(
                actions,
                text="Angrip",
                command=turn,
                bg="#34445c",
                fg="white",
                relief="flat",
                padx=18,
            ).pack(side="left", padx=4)

        tk.Button(
            actions,
            text="Møt utfordringen",
            command=battle,
            bg="#345b50",
            fg="white",
            relief="flat",
            padx=12,
        ).pack(side="left", padx=4)
        update()

    def heal():
        for p in team:
            p["hp"] = max(p["hp"], 30)
        say("Laget har fått hvile. HP er gjenopprettet.")
        update()

    tk.Button(
        actions,
        text="Utforsk",
        command=explore,
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=18,
    ).pack(side="left", padx=4)
    tk.Button(
        actions,
        text="Hvil laget",
        command=heal,
        bg="#34445c",
        fg="white",
        relief="flat",
        padx=12,
    ).pack(side="left", padx=4)
    update()
    say("Velkommen! Trykk Utforsk for å begynne eventyret.")


def vis_spillmeny():
    vindu = spill_vindu("INGENTING Å SE HER – Spillbibliotek", 720, 760)
    tk.Label(
        vindu,
        text="SPILLBIBLIOTEK",
        bg=SPILL_BG,
        fg=SPILL_ACCENT,
        font=("Segoe UI", 23, "bold"),
    ).pack(pady=(14, 2))
    tk.Label(
        vindu, text="50 spill • Velg et spill for å starte", bg=SPILL_BG, fg="#aab6c8"
    ).pack(pady=(0, 10))
    outer = tk.Frame(vindu, bg=SPILL_BG)
    outer.pack(fill="both", expand=True, padx=18, pady=4)
    canvas = tk.Canvas(outer, bg=SPILL_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg=SPILL_BG)
    frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=frame, anchor="nw", width=650)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    existing = [
        ("Tetris", "Stable fallende blokker.", start_tetris),
        ("Pixel Runner", "Sidescroller med hopp.", start_sidescroller),
        ("Snake", "Spis og voks uten å treffe deg selv.", start_snake),
        ("Pong", "Bordtennis mot datamaskinen.", start_pong),
        ("Breakout", "Knus klosser med ballen.", start_breakout),
        ("Memory", "Finn like kort.", start_memory),
        ("Space Invaders", "Forsvar basen mot romvesener.", start_space_invaders),
        ("Minesweeper", "Finn trygge ruter.", start_minesweeper),
        ("DOOM: Pixel Maze", "Retroinspirert labyrint-FPS.", start_doom_arena),
        (
            "Pocket Creatures",
            "Utforsk, fang og tren originale skapninger.",
            start_pocket_creatures,
        ),
    ]
    games = existing + [
        (n, d, lambda n=n, d=d, m=m: start_ekstra_spill(n, d, m))
        for n, d, m in EKSTRA_SPILL
    ]
    for i, (name, desc, fn) in enumerate(games, 1):
        card = tk.Frame(frame, bg=SPILL_PANEL, padx=12, pady=7)
        card.pack(fill="x", pady=3)
        tk.Label(
            card,
            text=f"{i:02d}. {name}",
            bg=SPILL_PANEL,
            fg=SPILL_ACCENT,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")
        tk.Button(
            card,
            text="SPILL",
            command=fn,
            bg="#34445c",
            fg="white",
            relief="flat",
            padx=13,
        ).pack(side="right")
        tk.Label(
            card,
            text=desc,
            bg=SPILL_PANEL,
            fg="#b7c2d2",
            font=("Segoe UI", 9),
            wraplength=500,
            justify="left",
        ).pack(anchor="w")
    tk.Button(
        vindu,
        text="Lukk spillbibliotek",
        command=vindu.destroy,
        bg="#34445c",
        fg="white",
        relief="flat",
        padx=18,
        pady=7,
    ).pack(pady=10)


# ---------------------- R-MATEMATIKK -------------------------


def safe_function_eval(expr, x):
    """Sikker evaluering av matematiske uttrykk med x som variabel."""
    allowed = {
        "x": x,
        "pi": math.pi,
        "e": math.e,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "sqrt": math.sqrt,
        "log": math.log,
        "ln": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
        "factorial": math.factorial,
    }
    tree = ast.parse(expr.replace("^", "**"), mode="eval")

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if (
            isinstance(node, ast.Name)
            and node.id in allowed
            and not callable(allowed[node.id])
        ):
            return allowed[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in (
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Pow,
            ast.Mod,
        ):
            a, b = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Div):
                return a / b
            if isinstance(node.op, ast.Pow):
                return a ** b
            return a % b
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return ev(node.operand) * (1 if isinstance(node.op, ast.UAdd) else -1)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in allowed
            and callable(allowed[node.func.id])
        ):
            return allowed[node.func.id](*(ev(a) for a in node.args))
        raise ValueError(
            "Uttrykket inneholder en funksjon eller operator som ikke er tillatt."
        )

    return float(ev(tree))


def _solve_linear(A, b):
    n = len(b)
    M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-12:
            raise ValueError("Systemet har ingen entydig løsning.")
        M[col], M[pivot] = M[pivot], M[col]
        q = M[col][col]
        M[col] = [v / q for v in M[col]]
        for r in range(n):
            if r != col:
                q = M[r][col]
                M[r] = [M[r][j] - q * M[col][j] for j in range(n + 1)]
    return [M[i][-1] for i in range(n)]


def apne_r_matte():
    w = tk.Toplevel(root)
    w.title("R-matematikk – Analyseverktøy")
    w.geometry("900x720")
    w.configure(bg=SPILL_BG)
    w.transient(root)
    tk.Label(
        w,
        text="R-MATEMATIKK",
        bg=SPILL_BG,
        fg=SPILL_ACCENT,
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=(12, 2))
    tk.Label(
        w,
        text="Funksjonsanalyse • derivasjon • integrasjon • regresjon • sannsynlighet • vektorer",
        bg=SPILL_BG,
        fg="#aab6c8",
    ).pack(pady=(0, 8))
    nb = ttk.Notebook(w)
    nb.pack(fill="both", expand=True, padx=12, pady=10)

    def page(title):
        f = tk.Frame(nb, bg=SPILL_BG)
        nb.add(f, text=title)
        return f

    def field(parent, label, default):
        row = tk.Frame(parent, bg=SPILL_BG)
        row.pack(fill="x", padx=14, pady=5)
        tk.Label(row, text=label, width=27, anchor="w", bg=SPILL_BG, fg=SPILL_FG).pack(
            side="left"
        )
        e = tk.Entry(row, font=("Consolas", 11), width=36)
        e.insert(0, default)
        e.pack(side="left", fill="x", expand=True)
        return e

    def output(parent):
        box = tk.Text(
            parent,
            height=13,
            bg="#0a1220",
            fg="#eaf0f8",
            insertbackground="white",
            wrap="word",
        )
        box.pack(fill="both", expand=True, padx=14, pady=8)
        return box

    def show(box, fn):
        try:
            result = fn()
            box.delete("1.0", "end")
            box.insert("end", str(result))
        except Exception as ex:
            messagebox.showerror("Beregning kunne ikke utføres", str(ex), parent=w)

    f = page("Funksjon")
    expr = field(f, "Funksjon f(x) =", "x^3 - 3*x^2 + 2")
    x0 = field(f, "Punkt x₀ =", "2")
    h = field(f, "Steglengde h =", "0.001")
    box = output(f)

    def analyse():
        ex = expr.get()
        x = float(x0.get())
        step = float(h.get())
        if step <= 0:
            raise ValueError("h må være positiv.")
        fx = safe_function_eval(ex, x)
        der = (safe_function_eval(ex, x + step) - safe_function_eval(ex, x - step)) / (
            2 * step
        )
        sec = (
            safe_function_eval(ex, x + step) - 2 * fx + safe_function_eval(ex, x - step)
        ) / (step * step)
        return f"f(x) = {ex}\nf({x}) = {fx:.10g}\nNumerisk f'({x}) ≈ {der:.10g}\nNumerisk f''({x}) ≈ {sec:.10g}\n\nDerivasjon er beregnet med sentraldifferanse."

    tk.Button(
        f,
        text="Analyser funksjon",
        command=lambda: show(box, analyse),
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(pady=4)

    f = page("Integral og nullpunkt")
    ex2 = field(f, "Funksjon f(x) =", "sin(x)")
    aa = field(f, "Nedre grense a =", "0")
    bb = field(f, "Øvre grense b =", "3.14159")
    n = field(f, "Delintervaller (partall) =", "1000")
    box2 = output(f)

    def integ():
        ex = ex2.get()
        a = float(aa.get())
        b = float(bb.get())
        N = int(n.get())
        if N < 2 or N % 2:
            raise ValueError("Antall delintervaller må være et positivt partall.")
        dx = (b - a) / N
        total = safe_function_eval(ex, a) + safe_function_eval(ex, b)
        for i in range(1, N):
            total += (4 if i % 2 else 2) * safe_function_eval(ex, a + i * dx)
        integral = total * dx / 3
        lo, hi = a, b
        flo = safe_function_eval(ex, lo)
        fhi = safe_function_eval(ex, hi)
        if flo * fhi > 0:
            rootmsg = "Nullpunkt: ikke garantert i intervallet (endepunktene har samme fortegn)."
        else:
            for _ in range(80):
                mid = (lo + hi) / 2
                fm = safe_function_eval(ex, mid)
                if flo * fm <= 0:
                    hi = mid
                    fhi = fm
                else:
                    lo = mid
                    flo = fm
            rootmsg = f"Nullpunkt med halveringsmetoden: x ≈ {(lo+hi)/2:.10g}"
        return f"Simpsons integral ≈ {integral:.12g}\n{rootmsg}\nMetode: sammensatt Simpsons regel."

    tk.Button(
        f,
        text="Beregn integral og nullpunkt",
        command=lambda: show(box2, integ),
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(pady=4)

    f = page("Regresjon")
    data = field(f, "Punktliste x,y (semikolon) =", "1,2; 2,3; 3,5; 4,8; 5,11")
    degree = field(f, "Polynomgrad (1 eller 2) =", "2")
    box3 = output(f)

    def regression():
        pts = []
        for pair in data.get().split(";"):
            x, y = map(float, pair.split(","))
            pts.append((x, y))
        d = int(degree.get())
        if d not in (1, 2) or len(pts) < d + 1:
            raise ValueError("Velg grad 1 eller 2 og oppgi nok punkter.")
        m = d + 1
        A = [[sum(x ** (i + j) for x, y in pts) for j in range(m)] for i in range(m)]
        B = [sum(y * x ** i for x, y in pts) for i in range(m)]
        coef = _solve_linear(A, B)
        pred = [sum(coef[i] * x ** i for i in range(m)) for x, y in pts]
        mean = sum(y for x, y in pts) / len(pts)
        ssr = sum((y - p) ** 2 for (x, y), p in zip(pts, pred))
        sst = sum((y - mean) ** 2 for x, y in pts)
        r2 = 1 - ssr / sst if sst else 1
        return (
            "Koeffisienter fra konstantledd og oppover: "
            + ", ".join(f"a{i}={v:.8g}" for i, v in enumerate(coef))
            + f"\nR² = {r2:.8f}\nResidualkvadratsum = {ssr:.8g}"
        )

    tk.Button(
        f,
        text="Tilpass regresjonsmodell",
        command=lambda: show(box3, regression),
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(pady=4)

    f = page("Sannsynlighet")
    prob = field(f, "Suksess-sannsynlighet p =", "0.35")
    trials = field(f, "Antall forsøk n =", "10")
    successes = field(f, "Antall treff k =", "4")
    box4 = output(f)

    def binomial():
        p0 = float(prob.get())
        N = int(trials.get())
        k = int(successes.get())
        if not 0 <= p0 <= 1 or N < 0 or not 0 <= k <= N:
            raise ValueError("Krev 0 ≤ p ≤ 1 og 0 ≤ k ≤ n.")
        from math import comb

        pk = comb(N, k) * p0 ** k * (1 - p0) ** (N - k)
        cdf = sum(comb(N, j) * p0 ** j * (1 - p0) ** (N - j) for j in range(k + 1))
        return f"X ~ Bin(n={N}, p={p0})\nP(X = {k}) = {pk:.10g}\nP(X ≤ {k}) = {cdf:.10g}\nE(X) = np = {N*p0:.8g}\nVar(X) = np(1-p) = {N*p0*(1-p0):.8g}\nσ = {math.sqrt(N*p0*(1-p0)):.8g}"

    tk.Button(
        f,
        text="Beregn binomisk sannsynlighet",
        command=lambda: show(box4, binomial),
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(pady=4)

    f = page("Vektorer")
    va = field(f, "Vektor a (komma) =", "2,3,1")
    vb = field(f, "Vektor b (komma) =", "4,1,5")
    box5 = output(f)

    def vectors():
        a = list(map(float, va.get().split(",")))
        b = list(map(float, vb.get().split(",")))
        if len(a) != len(b) or not a:
            raise ValueError("Vektorene må ha samme dimensjon.")
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb_ = math.sqrt(sum(y * y for y in b))
        angle = (
            math.degrees(math.acos(max(-1, min(1, dot / (na * nb_)))))
            if na and nb_
            else float("nan")
        )
        return f"a + b = {[x+y for x,y in zip(a,b)]}\na − b = {[x-y for x,y in zip(a,b)]}\na · b = {dot}\n|a| = {na:.8g}\n|b| = {nb_:.8g}\nVinkel = {angle:.8g}°"

    tk.Button(
        f,
        text="Beregn vektoroperasjoner",
        command=lambda: show(box5, vectors),
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(pady=4)

    f = page("Rekker")
    a0 = field(f, "Første ledd a₁ =", "3")
    ratio = field(f, "Kvotient / differanse r =", "2")
    count = field(f, "Antall ledd n =", "10")
    kind = field(f, "Type (A=aritmetisk, G=geometrisk) =", "G")
    box6 = output(f)

    def series():
        a = float(a0.get())
        r = float(ratio.get())
        N = int(count.get())
        typ = kind.get().upper()
        if N < 1 or N > 100000:
            raise ValueError("n må være mellom 1 og 100000.")
        vals = [a + i * r if typ == "A" else a * (r ** i) for i in range(N)]
        return f"De første leddene: {vals[:30]}{' ...' if N>30 else ''}\nS_n = {sum(vals):.12g}\na_n = {vals[-1]:.12g}\nType: {'aritmetisk' if typ=='A' else 'geometrisk'}"

    tk.Button(
        f,
        text="Beregn rekken",
        command=lambda: show(box6, series),
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(pady=4)

    f = page("Likninger og økonomi")
    qa = field(f, "Andregrad a =", "1")
    qb = field(f, "Andregrad b =", "-5")
    qc = field(f, "Andregrad c =", "6")
    qbox = output(f)

    def quadratic():
        a = float(qa.get())
        b = float(qb.get())
        c = float(qc.get())
        if abs(a) < 1e-15:
            raise ValueError("a kan ikke være 0 i en andregradslikning.")
        disc = b * b - 4 * a * c
        if disc < 0:
            return f"Diskriminant D = {disc:.10g}\nIngen reelle røtter.\nKomplekse røtter: {(-b/(2*a)):.8g} ± {math.sqrt(-disc)/(2*a):.8g}i"
        r1 = (-b + math.sqrt(disc)) / (2 * a)
        r2 = (-b - math.sqrt(disc)) / (2 * a)
        return f"{a}x² + ({b})x + ({c}) = 0\nDiskriminant D = {disc:.10g}\nx₁ = {r1:.10g}\nx₂ = {r2:.10g}"

    tk.Button(
        f,
        text="Løs andregradslikning",
        command=lambda: show(qbox, quadratic),
        bg="#345b50",
        fg="white",
        relief="flat",
        pady=7,
    ).pack(pady=4)
    principal = field(f, "Startkapital K₀ =", "10000")
    rate = field(f, "Årlig rente/vekst (%) =", "4")
    years = field(f, "Antall år =", "8")
    deposits = field(f, "Innskudd per år (slutt) =", "0")
    econbox = output(f)

    def finance():
        k = float(principal.get())
        r = float(rate.get()) / 100
        n = int(years.get())
        dep = float(deposits.get())
        if n < 0 or n > 10000 or r <= -1:
            raise ValueError("Antall år må være ≥ 0 og rente større enn -100 %. ")
        total = k * (1 + r) ** n + (dep * ((1 + r) ** n - 1) / r if r else dep * n)
        return f"Sluttverdi etter {n} år: {total:.2f}\nStartkapitalens verdi: {k*(1+r)**n:.2f}\nInnskuddenes verdi: {total-k*(1+r)**n:.2f}\nModell: årlig rentes rente og innskudd ved slutten av hvert år."

    tk.Button(
        f,
        text="Beregn rentes rente og sparing",
        command=lambda: show(econbox, finance),
        bg="#345b50",
        fg="white",
        relief="flat",
        pady=7,
    ).pack(pady=4)

    f = page("Beskrivende statistikk")
    sample = field(f, "Datasett (komma/blank) =", "4, 7, 7, 9, 12, 15, 18")
    sbox = output(f)

    def descriptives():
        vals = [float(x) for x in sample.get().replace(",", " ").split()]
        if not vals:
            raise ValueError("Skriv inn minst ett tall.")
        vals.sort()
        n0 = len(vals)
        mean = statistics.mean(vals)
        med = statistics.median(vals)
        try:
            modes = statistics.multimode(vals)
        except Exception:
            modes = []
        return f"Antall: {n0}\nSum: {sum(vals):.10g}\nGjennomsnitt: {mean:.10g}\nMedian: {med:.10g}\nTypetall: {modes}\nMinimum: {min(vals):.10g}\nMaksimum: {max(vals):.10g}\nVariasjonsbredde: {max(vals)-min(vals):.10g}\nKvartiler (Q1, Q2, Q3): {statistics.quantiles(vals,n=4,method='inclusive') if n0>=2 else 'for få observasjoner'}\nPopulasjonsvarians: {statistics.pvariance(vals):.10g}\nPopulasjonsstandardavvik: {statistics.pstdev(vals):.10g}\nUtvalgsstandardavvik: {statistics.stdev(vals):.10g if n0>=2 else float('nan')}"

    tk.Button(
        f,
        text="Analyser datasett",
        command=lambda: show(sbox, descriptives),
        bg="#345b50",
        fg="white",
        relief="flat",
        pady=7,
    ).pack(pady=4)

    f = page("Verktøykasse")
    tk.Label(
        f,
        text="Flere R1/R2-verktøy",
        bg=SPILL_BG,
        fg=SPILL_ACCENT,
        font=("Segoe UI", 14, "bold"),
    ).pack(pady=12)
    tk.Label(
        f,
        text="Numerisk derivasjon • Simpsons integrasjon • halveringsmetode • polynomregresjon grad 1–2 • binomisk fordeling • vektoroperasjoner • aritmetiske og geometriske rekker.\n\nFunksjonsuttrykk støtter +, −, ×, /, potens, parenteser og sin, cos, tan, sqrt, log, log10, exp, abs, pi og e. Bruk * for multiplikasjon og ** eller ^ for potens.",
        bg=SPILL_BG,
        fg=SPILL_FG,
        justify="left",
        wraplength=760,
    ).pack(padx=20, pady=10)


# ---------------------- GRAFTEGNER -------------------------
def apne_graftegner():
    w = tk.Toplevel(root)
    w.title("Graftegner – Sorterer Beta 1.10")
    w.geometry("1000x760")
    w.configure(bg=SPILL_BG)
    w.transient(root)
    top = tk.Frame(w, bg=SPILL_BG)
    top.pack(fill="x", padx=12, pady=10)
    tk.Label(top, text="f(x) =", bg=SPILL_BG, fg=SPILL_FG).pack(side="left")
    expr = tk.Entry(top, width=30, font=("Consolas", 12))
    expr.insert(0, "x^2 - 4")
    expr.pack(side="left", padx=6)
    tk.Label(top, text="x-min", bg=SPILL_BG, fg=SPILL_FG).pack(side="left")
    xmin = tk.Entry(top, width=7)
    xmin.insert(0, "-10")
    xmin.pack(side="left", padx=3)
    tk.Label(top, text="x-max", bg=SPILL_BG, fg=SPILL_FG).pack(side="left")
    xmax = tk.Entry(top, width=7)
    xmax.insert(0, "10")
    xmax.pack(side="left", padx=3)
    tk.Label(top, text="y-min", bg=SPILL_BG, fg=SPILL_FG).pack(side="left")
    ymin = tk.Entry(top, width=7)
    ymin.insert(0, "-10")
    ymin.pack(side="left", padx=3)
    tk.Label(top, text="y-max", bg=SPILL_BG, fg=SPILL_FG).pack(side="left")
    ymax = tk.Entry(top, width=7)
    ymax.insert(0, "10")
    ymax.pack(side="left", padx=3)
    canvas = tk.Canvas(w, bg="#0a1220", highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=12, pady=8)
    status = tk.Label(
        w,
        text="Skriv uttrykk med x. Eksempel: sin(x), e^x, log(x), sqrt(x). Vinkler i radianer.",
        bg=SPILL_BG,
        fg="#aab6c8",
    )
    status.pack(fill="x", padx=14, pady=(0, 8))

    def draw(event=None):
        try:
            a, b, c, d = map(float, (xmin.get(), xmax.get(), ymin.get(), ymax.get()))
            if not a < b or not c < d:
                raise ValueError("Minste verdi må være mindre enn største verdi.")
            W = max(canvas.winfo_width(), 300)
            H = max(canvas.winfo_height(), 200)
            X = lambda x: (x - a) / (b - a) * W
            Y = lambda y: H - (y - c) / (d - c) * H
            canvas.delete("all")
            # grid, axes and labels
            for i in range(11):
                xx = a + (b - a) * i / 10
                yy = c + (d - c) * i / 10
                canvas.create_line(X(xx), 0, X(xx), H, fill="#243247")
                canvas.create_line(0, Y(yy), W, Y(yy), fill="#243247")
                canvas.create_text(
                    X(xx) + 2,
                    H - 12,
                    text=f"{xx:.3g}",
                    fill="#8b9bb2",
                    anchor="s",
                    font=("Segoe UI", 8),
                )
                canvas.create_text(
                    4,
                    Y(yy) - 2,
                    text=f"{yy:.3g}",
                    fill="#8b9bb2",
                    anchor="nw",
                    font=("Segoe UI", 8),
                )
            if c <= 0 <= d:
                canvas.create_line(0, Y(0), W, Y(0), fill="#d8e1ef", width=1.5)
            if a <= 0 <= b:
                canvas.create_line(X(0), 0, X(0), H, fill="#d8e1ef", width=1.5)
            pts = []
            valid = 0
            for i in range(1201):
                x = a + (b - a) * i / 1200
                try:
                    y = safe_function_eval(expr.get(), x)
                    if math.isfinite(y) and c - 5 * (d - c) <= y <= d + 5 * (d - c):
                        pts.extend((X(x), Y(y)))
                        valid += 1
                    else:
                        if len(pts) >= 4:
                            canvas.create_line(
                                *pts, fill="#61d6ad", width=2, smooth=False
                            )
                        pts = []
                except Exception:
                    if len(pts) >= 4:
                        canvas.create_line(*pts, fill="#61d6ad", width=2, smooth=False)
                    pts = []
            if len(pts) >= 4:
                canvas.create_line(*pts, fill="#61d6ad", width=2, smooth=False)
            status.config(
                text=f"Tegnet f(x) = {expr.get()} · {valid} gyldige beregningspunkter · vinkler i radianer"
            )
        except Exception as ex:
            messagebox.showerror("Graftegner", str(ex), parent=w)

    tk.Button(
        top,
        text="Tegn graf",
        command=draw,
        bg="#345b50",
        fg="white",
        relief="flat",
        padx=12,
    ).pack(side="left", padx=8)
    canvas.bind("<Configure>", lambda e: draw() if expr.get().strip() else None)
    w.after(150, draw)


# ---------------------- MATEMATISK ORDBOK -------------------------
MATTE_ORD = {
    "Absoluttverdi": "Avstanden fra et tall til null på tallinja. |x| er alltid 0 eller positiv.",
    "Asymptote": "En linje som en graf nærmer seg når x eller y går mot en bestemt verdi eller uendelig.",
    "Derivert": "Et mål på momentan vekstfart. f'(x) beskriver stigningstallet til tangenten.",
    "Derivasjon": "Regneoperasjonen som finner den deriverte funksjonen.",
    "Diskriminant": "Uttrykket b² − 4ac i en andregradslikning. Fortegnet avgjør antall reelle røtter.",
    "Eksponentialfunksjon": "En funksjon der variabelen står i eksponenten, for eksempel f(x)=a·b^x.",
    "Funksjon": "En regel som knytter hver tillatte x-verdi til nøyaktig én y-verdi.",
    "Gjennomsnittlig vekstfart": "Endring i funksjonsverdi delt på endring i x: (f(b)-f(a))/(b-a).",
    "Integral": "Et matematisk mål på akkumulert størrelse; bestemt integral kan tolkes som fortegnet areal.",
    "Kontinuitet": "En funksjon er kontinuerlig dersom grafen kan tegnes lokalt uten hopp eller brudd.",
    "Logaritme": "Den inverse operasjonen til potensregning. log_b(x)=y betyr at b^y=x.",
    "Maksimumspunkt": "Et punkt der funksjonen har en lokal eller global største verdi.",
    "Minimumspunkt": "Et punkt der funksjonen har en lokal eller global minste verdi.",
    "Nullpunkt": "En x-verdi der f(x)=0; grafen krysser eller berører x-aksen.",
    "Normalfordeling": "En symmetrisk sannsynlighetsfordeling med klokkeform, bestemt av μ og σ.",
    "Parameter": "En fast størrelse som bestemmer egenskapene til en modell eller funksjon.",
    "Regresjon": "Metode for å tilpasse en matematisk modell til observerte datapunkter.",
    "Residual": "Forskjellen mellom observert verdi og modellens beregnede verdi.",
    "Standardavvik": "Et mål på spredningen rundt gjennomsnittet; kvadratroten av variansen.",
    "Tangent": "En linje som har samme stigningstall som grafen i et bestemt punkt.",
    "Vendepunkt": "Et punkt der grafen skifter krumning; ofte der f'' skifter fortegn.",
    "Vekstfaktor": "Faktoren en størrelse multipliseres med per periode. Ved p prosent vekst er den 1+p/100.",
    "Varians": "Gjennomsnittet av de kvadrerte avvikene fra forventningsverdien eller gjennomsnittet.",
    "Vektor": "En størrelse med retning og lengde, ofte skrevet som en koordinatliste.",
    "Konfidensintervall": "Et intervall beregnet fra data som ved en valgt metode har en bestemt dekningsgrad.",
    "Korrelasjon": "Et mål på styrken og retningen til en statistisk sammenheng mellom variabler.",
    "Stigningstall": "Endringen i y delt på endringen i x for en rett linje.",
    "Sannsynlighet": "Et tall mellom 0 og 1 som beskriver hvor sannsynlig en hendelse er.",
    "Binomisk fordeling": "Fordeling for antall treff i n uavhengige forsøk med samme treff-sannsynlighet p.",
    "Geometrisk rekke": "En rekke der hvert ledd fås ved å multiplisere det forrige med en fast kvotient.",
    "Sentralmål": "Median, Typetall og Gjennomsnitt.",
    "Breddemål/Spredningsmål": "Mål som beskriver hvor spredt observasjonene er, for eksempel variasjonsbredde, kvartilbredde, varians og standardavvik.",
    "Gjennomsnitt": "Alle verdiene lagt sammen og delt på antallet verdier.",
    "Median": "Den midterste verdien i et sortert datasett. Ved et partall antall observasjoner er medianen gjennomsnittet av de to midterste verdiene.",
    "Typetall": "Verdien som forekommer oftest i datasettet. Det kan finnes flere typetall.",

    "Addisjon": "Regneoperasjonen der to eller flere tall legges sammen. Symbolet er +.",
    "Subtraksjon": "Regneoperasjonen der én verdi trekkes fra en annen. Symbolet er −.",
    "Multiplikasjon": "Gjentatt addisjon eller skalering. Symbolet er × eller ·.",
    "Divisjon": "Fordeling i like store deler eller måling av hvor mange ganger en verdi går opp i en annen.",
    "Brøk": "Et tall skrevet som teller delt på nevner. Nevneren kan ikke være null.",
    "Teller": "Tallet over brøkstreken; viser hvor mange deler som er med.",
    "Nevner": "Tallet under brøkstreken; viser hvor mange like deler helheten er delt i.",
    "Prosent": "En andel per hundre. 25 % betyr 25 av 100.",
    "Promille": "En andel per tusen. 5 ‰ betyr 5 av 1000.",
    "Potens": "En kort skrivemåte for gjentatt multiplikasjon, for eksempel 2³ = 2·2·2.",
    "Grunntall": "Tallet som opphøyes i en potens.",
    "Eksponent": "Tallet som angir hvor mange ganger grunntallet brukes som faktor.",
    "Kvadratrot": "Det ikke-negative tallet som ganget med seg selv gir tallet under rottegnet.",
    "Kubikkrot": "Tallet som opphøyd i tredje gir tallet under rottegnet.",
    "Likning": "Et matematisk utsagn med en ukjent størrelse og et likhetstegn.",
    "Ulikhet": "Et matematisk utsagn som sammenligner størrelser med <, >, ≤ eller ≥.",
    "Variabel": "Et symbol, ofte x eller y, som representerer en verdi som kan variere.",
    "Konstant": "En fast verdi som ikke endres i uttrykket eller modellen.",
    "Koordinatsystem": "Et system med akser som brukes til å plassere punkter ved hjelp av koordinater.",
    "X-akse": "Den vannrette aksen i et vanlig todimensjonalt koordinatsystem.",
    "Y-akse": "Den loddrette aksen i et vanlig todimensjonalt koordinatsystem.",
    "Origo": "Skjæringspunktet mellom aksene, vanligvis punktet (0, 0).",
    "Lineær funksjon": "En funksjon på formen f(x)=ax+b. Grafen er en rett linje.",
    "Andregradsfunksjon": "En funksjon på formen f(x)=ax²+bx+c, der a ikke er null.",
    "Polynom": "Et uttrykk som består av ledd med konstanter og ikke-negative heltallspotenser av variabler.",
    "Rasjonal funksjon": "En funksjon som kan skrives som forholdet mellom to polynomer.",
    "Asymptote": "En linje som en graf nærmer seg når x eller y går mot en bestemt verdi eller uendelig.",
    "Grenseverdi": "Verdien en funksjon nærmer seg når variabelen går mot en bestemt verdi.",
    "Derivasjonsregel": "En regel som gjør det mulig å finne den deriverte uten å bruke definisjonen direkte.",
    "Produktregelen": "Regel for derivasjon av et produkt: (fg)' = f'g + fg'.",
    "Kvotientregelen": "Regel for derivasjon av en brøk av funksjoner.",
    "Kjerneregel": "Regel for derivasjon av sammensatte funksjoner: deriver ytre funksjon og gang med indre derivert.",
    "Antiderivert": "En funksjon F der F'(x)=f(x).",
    "Bestemt integral": "Integral med nedre og øvre grense; måler akkumulert nettoareal.",
    "Ubestemt integral": "Mengden av alle antideriverte til en funksjon, inkludert integrasjonskonstanten.",
    "Aritmetisk følge": "En tallfølge der differansen mellom to påfølgende ledd er konstant.",
    "Geometrisk følge": "En tallfølge der forholdet mellom to påfølgende ledd er konstant.",
    "Rekke": "Summen av leddene i en tallfølge.",
    "Uendelig rekke": "En sum med uendelig mange ledd; den kan konvergere eller divergere.",
    "Konvergens": "At en følge eller rekke nærmer seg en endelig grenseverdi.",
    "Divergens": "At en følge eller rekke ikke nærmer seg en endelig grenseverdi.",
    "Utvalg": "En del av en populasjon som undersøkes for å si noe om helheten.",
    "Populasjon": "Hele gruppen eller mengden som en statistisk undersøkelse handler om.",
    "Variabeltype": "Beskriver hvilken type data en variabel inneholder, for eksempel kategorier eller tall.",
    "Kategorisk variabel": "En variabel som beskriver grupper eller egenskaper, ikke en målt tallstørrelse.",
    "Kontinuerlig variabel": "En tallvariabel som i prinsippet kan ha alle verdier i et intervall.",
    "Diskret variabel": "En variabel som bare kan ha bestemte, adskilte verdier.",
    "Frekvens": "Hvor mange ganger en bestemt verdi eller kategori forekommer.",
    "Relativ frekvens": "Frekvensen delt på totalt antall observasjoner, ofte oppgitt i prosent.",
    "Kumulativ frekvens": "Summen av frekvensene opp til og med en bestemt verdi.",
    "Kvartil": "En verdi som deler sorterte data i fire omtrent like store deler.",
    "Persentil": "En verdi som angir hvor stor prosentandel av observasjonene som ligger på eller under verdien.",
    "Interkvartilbredde": "Forskjellen mellom tredje og første kvartil, Q3 − Q1.",
    "Utligger": "En observasjon som ligger uvanlig langt fra resten av datasettet.",
    "Standardfeil": "Et mål på usikkerheten i et estimat, ofte standardavviket til utvalgsfordelingen.",
    "Korrelasjonskoeffisient": "Et tall mellom −1 og 1 som beskriver retning og styrke i en lineær sammenheng.",
    "Kausalitet": "Et årsaksforhold der en endring i én faktor bidrar til en endring i en annen.",
    "Regresjonslinje": "En linje som modellerer sammenhengen mellom to variabler ved regresjon.",
    "Residualplott": "Et diagram over residualene som brukes til å vurdere om en regresjonsmodell passer.",
    "Normalisering": "En omforming av data til en felles skala eller standardisert form.",
    "Z-skår": "Antall standardavvik en observasjon ligger over eller under gjennomsnittet.",
    "Standardisering": "Omforming av verdier slik at de får gjennomsnitt 0 og standardavvik 1.",
    "Sannsynlighetsrom": "Mengden av alle mulige utfall i et sannsynlighetsforsøk.",
    "Hendelse": "En delmengde av utfallsrommet; ett eller flere mulige utfall.",
    "Komplementær hendelse": "Hendelsen at en bestemt hendelse ikke skjer.",
    "Uavhengige hendelser": "Hendelser der kunnskap om den ene ikke endrer sannsynligheten for den andre.",
    "Betinget sannsynlighet": "Sannsynligheten for en hendelse gitt at en annen hendelse har inntruffet.",
    "Forventningsverdi": "Det langsiktige gjennomsnittet som forventes i et tilfeldig forsøk.",
    "Standardavvik": "Et mål på spredningen rundt gjennomsnittet; kvadratroten av variansen.",
    "Variasjonskoeffisient": "Standardavvik delt på absolutt gjennomsnitt, ofte uttrykt i prosent.",
    "Harmonisk gjennomsnitt": "Antall observasjoner delt på summen av de inverse verdiene; nyttig for visse rater.",
    "Geometrisk gjennomsnitt": "N-te rot av produktet av n positive observasjoner; nyttig for vekstrater.",
    "Skjevhet": "Et mål på asymmetri i en fordeling.",
    "Median absolutt avvik": "Et robust spredningsmål basert på medianen av absolutte avvik fra medianen.",
    "IQR-metoden": "En vanlig metode for å flagge uteliggere utenfor Q1−1,5·IQR og Q3+1,5·IQR.",
}


def apne_matteordbok():
    w = tk.Toplevel(root)
    w.title("Matematisk ordbok")
    w.geometry("780x650")
    w.configure(bg=SPILL_BG)
    w.transient(root)
    tk.Label(
        w,
        text="MATEMATISK ORDBOK",
        bg=SPILL_BG,
        fg=SPILL_ACCENT,
        font=("Segoe UI", 20, "bold"),
    ).pack(pady=12)
    search = tk.Entry(w, font=("Segoe UI", 12))
    search.pack(fill="x", padx=14, pady=6)
    search.insert(0, "Søk etter begrep …")
    body = tk.Frame(w, bg=SPILL_BG)
    body.pack(fill="both", expand=True, padx=14, pady=8)
    lb = tk.Listbox(
        body,
        width=28,
        bg="#0a1220",
        fg="#eaf0f8",
        selectbackground="#345b50",
        font=("Segoe UI", 10),
    )
    lb.pack(side="left", fill="y")
    txt = tk.Text(
        body,
        bg="#0a1220",
        fg="#eaf0f8",
        wrap="word",
        font=("Segoe UI", 11),
        padx=12,
        pady=12,
    )
    txt.pack(side="left", fill="both", expand=True, padx=(8, 0))

    def refresh(*_):
        q = search.get().casefold()
        lb.delete(0, "end")
        for term in sorted(MATTE_ORD):
            if q in term.casefold() or q in MATTE_ORD[term].casefold():
                lb.insert("end", term)
        if lb.size():
            lb.selection_set(0)
            show_term()

    def show_term(event=None):
        sel = lb.curselection()
        if not sel:
            return
        term = lb.get(sel[0])
        txt.delete("1.0", "end")
        txt.insert("end", term + "\n\n" + MATTE_ORD[term])

    lb.bind("<<ListboxSelect>>", show_term)
    search.bind("<KeyRelease>", refresh)
    refresh()


def sjekk_easter_egg(tekst):
    if not settings["features"].get("fun", True):
        return False

    norm = " ".join(tekst.upper().split())

    # Hemmelig spillrom – åpnes med den eksakte frasen.
    if norm == "INGENTING Å SE HER":
        entry.delete(0, tk.END)
        status_var.set("Du fant spillrommet.")
        vis_spillmeny()
        return True

    # Secret menu keyword – this is not counted as one of the 100 eggs.
    if norm == "EASTER EGG":
        entry.delete(0, tk.END)
        status_var.set("Den hemmelige menyen er åpnet!")
        vis_easter_egg_meny()
        return True

    for frase, tittel, beskrivelse in EASTER_EGG_DATA:
        if norm == frase:
            entry.delete(0, tk.END)
            marker_easter_egg_funnet(frase)
            status_var.set(f"Easter egg funnet: {len(funnet_easter_eggs)} av {len(EASTER_EGG_DATA)}!")
            if frase in ORIGINAL_EGGS:
                ORIGINAL_EGGS[frase]()
            else:
                egg_generell_animasjon(frase, tittel, beskrivelse)
            return True

    return False


KONAMI = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right", "b", "a"]

konami_pos = [0]


def egg_konami():

    status_var.set("KONAMI-KODE AKTIVERT! +30 liv")

    messagebox.showinfo(
        "KONAMI-KODE!",
        "Du har låst opp 30 ekstra liv!\n\n"
        "(Ikke at du trenger dem i et sorteringsprogram …)",
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
        "antall",
        "sum",
        "gjennomsnitt",
        "median",
        "typetall",
        "minimum",
        "maksimum",
        "variasjonsbredde",
        "quartiles",
        "variance",
        "extra",
        "percentiles",
        "outliers",
    ]

    har_statistikk = any(features.get(key, False) for key in statistikk_nokler)

    if har_statistikk:

        tk.Label(
            result_area,
            text="STATISTIKKOVERSIKT",
            bg=color("bg"),
            fg=color("text"),
            font=font(11, True),
        ).pack(anchor="w", pady=(5, 8))

        stats_frame = tk.Frame(result_area, bg=color("bg"))

        stats_frame.pack(fill="x", pady=(0, 15))

        vis_statistikk(data)

    # SORTERTE TALL

    if features["sorted_list"]:

        overskrift = {
            "stigende": "SORTERTE TALL (STIGENDE)",
            "synkende": "SORTERTE TALL (SYNKENDE)",
            "tilfeldig": "BLANDEDE TALL",
        }.get(data["retning"], "SORTERTE TALL")

        tk.Label(
            result_area,
            text=overskrift,
            bg=color("bg"),
            fg=color("text"),
            font=font(11, True),
        ).pack(anchor="w", pady=(5, 8))

        sorted_panel = tk.Frame(result_area, bg=color("panel"), padx=12, pady=12)

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
            pady=8,
        )

        sorted_text.pack(fill="x")

        vis_sorterte_tall(data)

    # NEDRE OMRÅDE

    lower = tk.Frame(result_area, bg=color("bg"))

    lower.pack(fill="both", expand=True)

    # FREKVENSTABELL

    if features["frequency"]:

        left = tk.Frame(lower, bg=color("panel"), padx=12, pady=12)

        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        tk.Label(
            left,
            text="FREKVENSTABELL",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True),
        ).pack(anchor="w", pady=(0, 10))

        table_frame = tk.Frame(left, bg=color("panel"))

        table_frame.pack(fill="both", expand=True)

        frekvens_tabell = ttk.Treeview(
            table_frame,
            columns=("tall", "antall", "prosent"),
            show="headings",
            height=10,
        )

        table_scroll = ttk.Scrollbar(
            table_frame, orient="vertical", command=frekvens_tabell.yview
        )

        frekvens_tabell.configure(yscrollcommand=table_scroll.set)

        table_scroll.pack(side="right", fill="y")

        frekvens_tabell.pack(side="left", fill="both", expand=True)

        for column, title in [
            ("tall", "Tall"),
            ("antall", "Antall"),
            ("prosent", "Prosent"),
        ]:

            frekvens_tabell.heading(column, text=title)

            frekvens_tabell.column(column, width=90, anchor="center")

        vis_frekvens(data)

    # HISTOGRAM

    if features["histogram"]:

        right = tk.Frame(lower, bg=color("panel"), padx=12, pady=12)

        right.pack(side="right", fill="both", expand=True, padx=(6, 0))

        tk.Label(
            right,
            text="HISTOGRAM",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True),
        ).pack(anchor="w", pady=(0, 10))

        histogram = tk.Canvas(
            right, bg=color("panel"), highlightthickness=0, height=220
        )

        histogram.pack(fill="both", expand=True)

        histogram.bind(
            "<Configure>",
            lambda event: tegn_histogram(siste_resultat) if siste_resultat else None,
        )

        tegn_histogram(data)

    # BOKSPLOTT

    if features["boxplot"]:

        boks = tk.Frame(result_area, bg=color("panel"), padx=12, pady=12)

        boks.pack(fill="x", pady=(15, 0))

        tk.Label(
            boks,
            text="BOKSPLOTT",
            bg=color("panel"),
            fg=color("text"),
            font=font(10, True),
        ).pack(anchor="w", pady=(0, 10))

        boxplot_canvas = tk.Canvas(
            boks, bg=color("panel"), highlightthickness=0, height=110
        )

        boxplot_canvas.pack(fill="x")

        boxplot_canvas.bind(
            "<Configure>",
            lambda event: tegn_boxplot(siste_resultat) if siste_resultat else None,
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

    root.attributes("-fullscreen", not bool(root.attributes("-fullscreen")))


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

    outer = tk.Frame(window, bg=color("bg"))

    outer.pack(fill="both", expand=True)

    settings_canvas = tk.Canvas(outer, bg=color("bg"), highlightthickness=0)

    settings_scroll = ttk.Scrollbar(
        outer, orient="vertical", command=settings_canvas.yview
    )

    settings_canvas.configure(yscrollcommand=settings_scroll.set)

    settings_scroll.pack(side="right", fill="y")

    settings_canvas.pack(side="left", fill="both", expand=True)

    content = tk.Frame(settings_canvas, bg=color("bg"), padx=20, pady=20)

    content_id = settings_canvas.create_window((0, 0), window=content, anchor="nw")

    content.bind(
        "<Configure>",
        lambda event: settings_canvas.configure(
            scrollregion=settings_canvas.bbox("all")
        ),
    )

    settings_canvas.bind(
        "<Configure>",
        lambda event: settings_canvas.itemconfigure(content_id, width=event.width),
    )

    def rull_innstillinger(event):

        if event.delta:
            settings_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    window.bind("<MouseWheel>", rull_innstillinger)

    def seksjon(tittel):

        tk.Label(
            content, text=tittel, bg=color("bg"), fg=color("text"), font=font(12, True)
        ).pack(anchor="w", pady=(18, 8))

    def etikett(tekst):

        tk.Label(
            content, text=tekst, bg=color("bg"), fg=color("text"), font=font(9)
        ).pack(anchor="w")

    # TEMA

    seksjon("UTSEENDE OG FARGER")

    etikett("Fargetema")

    tema_var = tk.StringVar(value=settings["theme"])

    tema_combo = ttk.Combobox(
        content, textvariable=tema_var, values=list(THEMES.keys()), state="readonly"
    )

    tema_combo.pack(fill="x", pady=(5, 10))

    def velg_tema(event=None):

        bruk_tema(tema_var.get())

        window.destroy()

        apne_innstillinger()

    tema_combo.bind("<<ComboboxSelected>>", velg_tema)

    # FARGER

    def fargerad(navn, key):

        rad = tk.Frame(content, bg=color("bg"))

        rad.pack(fill="x", pady=4)

        tk.Label(rad, text=navn, bg=color("bg"), fg=color("text"), font=font(9)).pack(
            side="left"
        )

        def velg():

            valgt = colorchooser.askcolor(
                color=settings[key], title=f"Velg {navn}", parent=window
            )

            if valgt and valgt[1]:

                settings[key] = valgt[1]
                knapp.configure(bg=valgt[1])

        knapp = tk.Button(rad, bg=settings[key], width=8, relief="flat", command=velg)

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

    font_var = tk.StringVar(value=settings["font"])

    font_combo = ttk.Combobox(
        content,
        textvariable=font_var,
        values=sorted(set(tkfont.families(root))),
        state="readonly",
    )

    font_combo.pack(fill="x", pady=(5, 10))

    etikett("Skriftstørrelse")

    font_size_var = tk.IntVar(value=settings["font_size"])

    tk.Spinbox(
        content,
        from_=8,
        to=20,
        textvariable=font_size_var,
        bg=color("panel_light"),
        fg=color("text"),
        relief="flat",
    ).pack(fill="x", pady=(5, 10))

    etikett("Overskriftsstørrelse")

    title_size_var = tk.IntVar(value=settings["title_size"])

    tk.Spinbox(
        content,
        from_=16,
        to=40,
        textvariable=title_size_var,
        bg=color("panel_light"),
        fg=color("text"),
        relief="flat",
    ).pack(fill="x", pady=(5, 10))

    # LAYOUT

    seksjon("LAYOUT OG TALLFORMAT")

    etikett("Kolonner i statistikkoversikten")

    columns_var = tk.IntVar(value=settings["stats_columns"])

    ttk.Combobox(
        content, textvariable=columns_var, values=[1, 2, 3, 4, 5], state="readonly"
    ).pack(fill="x", pady=(5, 10))

    etikett("Antall desimaler i resultatene")

    decimals_var = tk.IntVar(value=settings["decimals"])

    tk.Spinbox(
        content,
        from_=0,
        to=10,
        textvariable=decimals_var,
        bg=color("panel_light"),
        fg=color("text"),
        relief="flat",
    ).pack(fill="x", pady=(5, 10))

    # FUNKSJONSVALG

    seksjon("VELG FUNKSJONER")

    tk.Label(
        content,
        text="Bestem hvilke beregninger og verktøy som skal være aktive.",
        bg=color("bg"),
        fg=color("muted"),
        font=font(9),
        wraplength=500,
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
        "fun": "Moro-modus (skjulte overraskelser)",
    }

    feature_vars = {}

    groups = {
        "Statistiske beregninger": [
            "antall",
            "sum",
            "gjennomsnitt",
            "median",
            "typetall",
            "minimum",
            "maksimum",
            "variasjonsbredde",
        ],
        "Avanserte beregninger": [
            "quartiles",
            "variance",
            "extra",
            "percentiles",
            "outliers",
        ],
        "Visningsfunksjoner": ["frequency", "histogram", "boxplot", "sorted_list"],
        "Verktøy": [
            "calculator",
            "converter",
            "random",
            "import",
            "history",
            "copy",
            "export",
            "csv",
        ],
        "Moro": ["fun"],
    }

    for group_name, keys in groups.items():

        group_frame = tk.Frame(content, bg=color("panel"), padx=12, pady=10)

        group_frame.pack(fill="x", pady=5)

        tk.Label(
            group_frame,
            text=group_name,
            bg=color("panel"),
            fg=color("accent"),
            font=font(9, True),
        ).pack(anchor="w", pady=(0, 5))

        for key in keys:

            var = tk.BooleanVar(value=settings["features"][key])

            feature_vars[key] = var

            lag_sjekk(group_frame, feature_names[key], var, color("panel")).pack(
                anchor="w", pady=2
            )

    def velg_alle():

        for var in feature_vars.values():
            var.set(True)

    def fjern_alle():

        for var in feature_vars.values():
            var.set(False)

    selection_buttons = tk.Frame(content, bg=color("bg"))

    selection_buttons.pack(fill="x", pady=10)

    lag_knapp(selection_buttons, "Velg alle", velg_alle, color("panel_light")).pack(
        side="left", padx=(0, 5)
    )

    lag_knapp(selection_buttons, "Fjern alle", fjern_alle, color("panel_light")).pack(
        side="left"
    )

    # LAGRE INNSTILLINGER

    seksjon("LAGRE INNSTILLINGER")

    def bruk_innstillinger():

        try:

            settings["font"] = font_var.get()

            settings["font_size"] = max(8, min(20, int(font_size_var.get())))

            settings["title_size"] = max(16, min(40, int(title_size_var.get())))

            settings["stats_columns"] = max(1, min(5, int(columns_var.get())))

            settings["decimals"] = max(0, min(10, int(decimals_var.get())))

        except (ValueError, tk.TclError):

            messagebox.showerror(
                "Ugyldige verdier",
                "Kontroller skriftstørrelse, kolonner og desimaler.",
                parent=window,
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

                status_var.set("Innstillingene er lagret.")

                window.destroy()

    def standardinnstillinger():

        global settings

        settings = json.loads(json.dumps(DEFAULT_SETTINGS))

        save_settings()

        window.destroy()

        rebuild_interface()

        status_var.set("Standardinnstillinger gjenopprettet.")

    buttons = tk.Frame(content, bg=color("bg"))

    buttons.pack(fill="x", pady=(10, 25))

    lag_knapp(buttons, "Bruk", bruk_innstillinger).pack(side="left", padx=(0, 5))

    lag_knapp(buttons, "Lagre og lukk", lagre_og_lukk, color("green")).pack(
        side="left", padx=5
    )

    lag_knapp(buttons, "Standard", standardinnstillinger, color("panel_light")).pack(
        side="right"
    )


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
            label="Importer tall fra fil…", accelerator="Ctrl+O", command=importer_fil
        )

    if f["export"]:
        fil.add_command(
            label="Eksporter som TXT…",
            accelerator="Ctrl+S",
            command=eksporter_resultater,
        )

    if f["csv"]:
        fil.add_command(label="Eksporter som CSV…", command=eksporter_csv)

    if f["copy"]:
        fil.add_command(
            label="Kopier resultater",
            accelerator="Ctrl+Shift+C",
            command=kopier_resultater,
        )

    fil.add_separator()
    fil.add_command(label="Avslutt", command=avslutt)

    meny.add_cascade(label="Fil", menu=fil)

    # VERKTØY

    verktoy = tk.Menu(meny, tearoff=0)

    if f["calculator"]:
        verktoy.add_command(
            label="Kalkulator", accelerator="F2", command=apne_kalkulator
        )

    if f["random"]:
        verktoy.add_command(
            label="Tilfeldige tall…", accelerator="F3", command=apne_tilfeldig
        )

    if f["history"]:
        verktoy.add_command(label="Historikk", accelerator="F4", command=apne_historikk)

    if f["converter"]:
        verktoy.add_command(
            label="Enhetsomregner", accelerator="F5", command=apne_omregner
        )

    verktoy.add_separator()
    verktoy.add_command(
        label="R-matematikk – analyseverktøy…",
        accelerator="Ctrl+R",
        command=apne_r_matte,
    )
    verktoy.add_command(label="Graftegner…", command=apne_graftegner)
    verktoy.add_command(label="Matematisk ordbok…", command=apne_matteordbok)


    meny.add_cascade(label=tr("Verktøy"), menu=verktoy)

    # SPRÅK – lagres lokalt og beholdes ved neste oppstart.
    sprak_meny = tk.Menu(meny, tearoff=0)
    for kode, navn in LANGUAGES.items():
        markering = "✓ " if settings.get("language", "nb") == kode else ""
        sprak_meny.add_command(
            label=markering + navn,
            command=lambda k=kode: velg_sprak(k),
        )
    meny.add_cascade(label=tr("Språk"), menu=sprak_meny)

    # VIS

    vis = tk.Menu(meny, tearoff=0)

    tema_meny = tk.Menu(vis, tearoff=0)

    for navn in THEMES:
        tema_meny.add_command(label=navn, command=lambda n=navn: bruk_tema(n))

    vis.add_cascade(label="Tema", menu=tema_meny)

    vis.add_command(label="Zoom inn", accelerator="Ctrl++", command=lambda: zoom(1))

    vis.add_command(label="Zoom ut", accelerator="Ctrl+−", command=lambda: zoom(-1))

    vis.add_command(label="Fullskjerm", accelerator="F11", command=veksle_fullskjerm)

    vis.add_separator()

    vis.add_command(
        label="Innstillinger…", accelerator="Ctrl+,", command=apne_innstillinger
    )

    meny.add_cascade(label="Vis", menu=vis)

    # HJELP

    hjelp = tk.Menu(meny, tearoff=0)

    hjelp.add_command(
        label="Hjelp og hurtigtaster", accelerator="F1", command=apne_hjelp
    )

    hjelp.add_command(label="Om programmet", command=vis_om)

    meny.add_cascade(label="Hjelp", menu=hjelp)

    root.configure(menu=meny)
    oversett_meny(meny)


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

    header = tk.Frame(main, bg=color("bg"))

    header.pack(fill="x")

    title_frame = tk.Frame(header, bg=color("bg"))

    title_frame.pack(side="left")

    tk.Label(
        title_frame,
        text="TALL SORTERER",
        bg=color("bg"),
        fg=color("text"),
        font=title_font(),
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Statistikk, analyse og tallbehandling",
        bg=color("bg"),
        fg=color("muted"),
        font=font(9),
    ).pack(anchor="w", pady=(2, 15))

    # KNAPPER I OVERSKRIFTEN

    lag_knapp(header, "⚙ Innstillinger", apne_innstillinger, color("panel_light")).pack(
        side="right", pady=5
    )

    lag_knapp(header, "? Hjelp", apne_hjelp, color("panel_light")).pack(
        side="right", pady=5, padx=(0, 8)
    )

    # INPUTPANEL

    input_frame = tk.Frame(main, bg=color("panel"), padx=18, pady=15)

    input_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        input_frame,
        text=f"LEGG INN TALL (MAKS {MAX_TALL})",
        bg=color("panel"),
        fg=color("text"),
        font=font(10, True),
    ).pack(anchor="w")

    tk.Label(
        input_frame,
        text="Skill tallene med mellomrom, komma eller semikolon.",
        bg=color("panel"),
        fg=color("muted"),
        font=font(9),
    ).pack(anchor="w", pady=(3, 10))

    entry = tk.Entry(
        input_frame,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(12),
        borderwidth=0,
    )

    entry.pack(fill="x", ipady=12)

    if gammel_tekst:
        entry.insert(0, gammel_tekst)

    entry.bind("<KeyRelease>", lambda event: sjekk_easter_egg(entry.get()))

    entry.bind("<Return>", lambda event: sorter_tall("stigende"))

    entry.focus_set()

    # VALG

    valg_rad = tk.Frame(input_frame, bg=color("panel"))

    valg_rad.pack(fill="x", pady=(10, 0))

    lag_sjekk(valg_rad, "Fjern duplikater", dup_var, color("panel")).pack(
        side="left", padx=(0, 12)
    )

    lag_sjekk(valg_rad, "Avrund til heltall", avrund_var, color("panel")).pack(
        side="left", padx=(0, 12)
    )

    tk.Label(
        valg_rad, text="Filter fra", bg=color("panel"), fg=color("muted"), font=font(9)
    ).pack(side="left")

    tk.Entry(
        valg_rad,
        textvariable=filt_min_var,
        width=7,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(9),
    ).pack(side="left", padx=(4, 8), ipady=3)

    tk.Label(
        valg_rad, text="til", bg=color("panel"), fg=color("muted"), font=font(9)
    ).pack(side="left")

    tk.Entry(
        valg_rad,
        textvariable=filt_max_var,
        width=7,
        bg=color("panel_light"),
        fg=color("text"),
        insertbackground=color("text"),
        relief="flat",
        font=font(9),
    ).pack(side="left", padx=(4, 0), ipady=3)

    # KNAPPER

    button_frame = tk.Frame(input_frame, bg=color("panel"))

    button_frame.pack(fill="x", pady=(12, 0))

    lag_knapp(button_frame, "Sorter stigende", lambda: sorter_tall("stigende")).pack(
        side="left", padx=(0, 7)
    )

    lag_knapp(
        button_frame,
        "Sorter synkende",
        lambda: sorter_tall("synkende"),
        color("panel_light"),
    ).pack(side="left", padx=7)

    lag_knapp(
        button_frame, "Bland", lambda: sorter_tall("tilfeldig"), color("panel_light")
    ).pack(side="left", padx=7)

    lag_knapp(button_frame, "Nullstill", nullstill, color("panel_light")).pack(
        side="right"
    )

    if settings["features"]["calculator"]:

        lag_knapp(
            button_frame, "Kalkulator", apne_kalkulator, color("panel_light")
        ).pack(side="right", padx=7)

    if settings["features"]["random"]:

        lag_knapp(
            button_frame, "Tilfeldige tall", apne_tilfeldig, color("panel_light")
        ).pack(side="right", padx=7)

    # RESULTATOMRÅDE

    result_area = tk.Frame(main, bg=color("bg"))

    result_area.pack(fill="both", expand=True)

    # EKSPORTKNAPPER

    f = settings["features"]

    if f["copy"] or f["export"] or f["csv"]:

        export_frame = tk.Frame(main, bg=color("bg"))

        export_frame.pack(fill="x", pady=(15, 5))

        if f["copy"]:

            lag_knapp(
                export_frame,
                "Kopier resultater",
                kopier_resultater,
                color("panel_light"),
            ).pack(side="left", padx=(0, 8))

        if f["export"]:

            lag_knapp(
                export_frame,
                "Eksporter TXT",
                eksporter_resultater,
                color("panel_light"),
            ).pack(side="left", padx=(0, 8))

        if f["csv"]:

            lag_knapp(
                export_frame, "Eksporter CSV", eksporter_csv, color("panel_light")
            ).pack(side="left")

    # STATUS

    tk.Label(
        main, textvariable=status_var, bg=color("bg"), fg=color("green"), font=font(9)
    ).pack(anchor="w", pady=(8, 0))

    # VIS TIDLIGERE RESULTATER

    if siste_resultat is not None:
        vis_resultater()

    oversett_widget_tre(main)
    root.title(tr("Tall Sorterer – Beta 1.10"))

    root.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox("all"))


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
        borderwidth=0,
    )

    style.configure(
        "Treeview.Heading",
        background=color("panel"),
        foreground=color("text"),
        font=font(10, True),
        relief="flat",
    )

    style.map(
        "Treeview",
        background=[("selected", color("accent"))],
        foreground=[("selected", "white")],
    )


# ============================================================
# HOVEDVINDU OG SCROLLBAR
# ============================================================

root = tk.Tk()

root.title("Tall Sorterer – Beta 1.10")
root.geometry("1100x850")
root.minsize(750, 600)
root.configure(bg=color("bg"))

style = ttk.Style()
style.theme_use("clam")

status_var = tk.StringVar(value="Klar til å sortere nye tall.")

dup_var = tk.BooleanVar(value=False)
avrund_var = tk.BooleanVar(value=False)
filt_min_var = tk.StringVar(value="")
filt_max_var = tk.StringVar(value="")

scroll_container = tk.Frame(root, bg=color("bg"))

scroll_container.pack(fill="both", expand=True)

canvas = tk.Canvas(scroll_container, bg=color("bg"), highlightthickness=0)

canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)

scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

main = tk.Frame(canvas, bg=color("bg"), padx=25, pady=20)

main_window = canvas.create_window((0, 0), window=main, anchor="nw")


# ============================================================
# SCROLLFUNKSJONER
# ============================================================


def oppdater_scroll(event=None):

    canvas.configure(scrollregion=canvas.bbox("all"))


def tilpass_bredde(event):

    canvas.itemconfigure(main_window, width=event.width)


main.bind("<Configure>", oppdater_scroll)

canvas.bind("<Configure>", tilpass_bredde)


def musehjul(event):

    try:

        if event.widget.winfo_toplevel() is not root:
            return

    except (AttributeError, KeyError, tk.TclError):
        return

    if event.delta:

        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")


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

root.title("Sorterer – Beta 1.10")
root.bind("<Control-r>", lambda e: apne_r_matte())
root.bind("<Control-g>", lambda e: apne_graftegner())
root.bind("<Control-d>", lambda e: apne_matteordbok())

root.mainloop()
