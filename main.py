#!/usr/bin/env python3
"""
Eplan Label Tool by Wolfs-TS - Improved UI (ES / EN / NL)
- Panel detection from Groepscode only
- Automatic blank marker filtering
- Language selector
- Responsive two-pane layout (no clipping on smaller screens)
"""

import sys
import os
import subprocess
import glob
import re
import tempfile
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

print(sys.version)
print("Current working directory:", os.getcwd())

# ============== TRANSLATIONS ==============

translations = {
    "nl": {
        "app_title": "Eplan Label Tool by Wolfs-TS — v3 (Groepscode + Filter blanco)",
        "load_btn": "📁 Laad projectmap (TXT)",
        "project_lbl": "Project:",
        "no_project": "..Geen map geladen..",
        "status_ready": "Klaar. Laad een projectmap om te beginnen.",
        "kast_section": "KASTEN EN ONDERDELEN",
        "groepscode": "Groepscode",
        "onderdelen_norm": "Onderdelen (normaal)",
        "onderdelen_lpc": "Onderdelen LPC (directe print)",
        "onderdelen_label": "Onderdelen volgens labeling (R02)",
        "onderdelen_tech": "Onderdelen - Technische waarde",
        "legends": "Legends",
        "klemmen_section": "KLEMMEN",
        "klemmenstrook": "Klemmenstrook",
        "klemmen_los": "Klemmen (losse klemmen)",
        "kabels_section": "KABELS",
        "kabels_0_10": "Kabels 0-10 mm",
        "kabels_10_100": "Kabels 10-100 mm",
        "generate_btn": "▶  GEN ETIKETTEN GENEREREN",
        "panels_section": "Gedetecteerde kasten (uit Groepscode)",
        "panels_info": "De kasten worden automatisch uit het Groepscode bestand gehaald.\nSelecteer welke kasten je wilt meenemen (standaard = alle).",
        "select_all": "Alles selecteren",
        "select_none": "Niets selecteren",
        "apply_filter": "Alleen geselecteerde kasten exporteren\n(lege/markerloze regels worden automatisch verwijderd)",
        "detect_btn": "🔄 Detecteren / Vernieuwen",
        "footer": "Lege markers (alleen ;;;) worden automatisch gefilterd. Tijdelijke bestanden in TEMP.",
        "msg_no_files": "Geen bestanden geladen",
        "msg_select_folder_first": "Selecteer eerst de projectmap met de TXT bestanden.",
        "msg_nothing_selected": "Niets te doen",
        "msg_select_at_least_one": "Selecteer minstens één type label.",
        "msg_done_title": "Proces voltooid",
        "msg_done_body": "{launched} van {total} MPrintPRO processen gestart.\n\nFilter op kasten: {filter_text}",
        "msg_filter_no_results": "Geen regels gevonden",
        "msg_filter_fallback": "Geen regels gevonden voor de geselecteerde kasten.\nHet volledige bestand wordt gebruikt.",
        "filter_yes": "Ja",
        "filter_no": "Nee (alle kasten)",
        "lang_label": "Taal:",
    },
    "en": {
        "app_title": "Eplan Label Tool by Wolfs-TS — v3 (Groepscode + Blank Filter)",
        "load_btn": "📁 Load project folder (TXT)",
        "project_lbl": "Project:",
        "no_project": "..No folder loaded..",
        "status_ready": "Ready. Load a project folder to start.",
        "kast_section": "CABINETS AND PARTS",
        "groepscode": "Group code",
        "onderdelen_norm": "Parts (normal)",
        "onderdelen_lpc": "Parts LPC (direct print)",
        "onderdelen_label": "Parts according to labeling (R02)",
        "onderdelen_tech": "Parts - Technical value",
        "legends": "Legends",
        "klemmen_section": "TERMINALS",
        "klemmenstrook": "Terminal strips",
        "klemmen_los": "Terminals (individual)",
        "kabels_section": "CABLES",
        "kabels_0_10": "Cables 0-10 mm",
        "kabels_10_100": "Cables 10-100 mm",
        "generate_btn": "▶  GENERATE SELECTED LABELS",
        "panels_section": "Detected panels (from Groepscode)",
        "panels_info": "Panels are automatically read from the Groepscode file.\nSelect which panels to include (default = all).",
        "select_all": "Select all",
        "select_none": "Select none",
        "apply_filter": "Export only selected panels\n(blank/empty marker lines are automatically removed)",
        "detect_btn": "🔄 Detect / Refresh",
        "footer": "Empty markers (only ;;;) are automatically filtered. Temp files saved in TEMP folder.",
        "msg_no_files": "No files loaded",
        "msg_select_folder_first": "Please select the project folder with the TXT files first.",
        "msg_nothing_selected": "Nothing to do",
        "msg_select_at_least_one": "Select at least one label type.",
        "msg_done_title": "Process completed",
        "msg_done_body": "{launched} of {total} MPrintPRO processes started.\n\nPanel filter: {filter_text}",
        "msg_filter_no_results": "No lines found",
        "msg_filter_fallback": "No lines found for the selected panels.\nThe full file will be used.",
        "filter_yes": "Yes",
        "filter_no": "No (all panels)",
        "lang_label": "Language:",
    },
    "es": {
        "app_title": "Herramienta de Etiquetas Eplan por Wolfs-TS — v3 (Groepscode + Filtro blanco)",
        "load_btn": "📁 Cargar carpeta del proyecto (TXT)",
        "project_lbl": "Proyecto:",
        "no_project": "..Ninguna carpeta cargada..",
        "status_ready": "Listo. Carga una carpeta de proyecto para comenzar.",
        "kast_section": "CUADROS Y COMPONENTES",
        "groepscode": "Código de grupo",
        "onderdelen_norm": "Componentes (normal)",
        "onderdelen_lpc": "Componentes LPC (impresión directa)",
        "onderdelen_label": "Componentes según etiquetado (R02)",
        "onderdelen_tech": "Componentes - Valor técnico",
        "legends": "Leyendas",
        "klemmen_section": "BORNES",
        "klemmenstrook": "Tiras de bornes",
        "klemmen_los": "Bornes (individuales)",
        "kabels_section": "CABLES",
        "kabels_0_10": "Cables 0-10 mm",
        "kabels_10_100": "Cables 10-100 mm",
        "generate_btn": "▶  GENERAR ETIQUETAS SELECCIONADAS",
        "panels_section": "Cuadros detectados (desde Groepscode)",
        "panels_info": "Los cuadros se leen automáticamente del archivo Groepscode.\nSelecciona cuáles quieres incluir (por defecto = todos).",
        "select_all": "Seleccionar todos",
        "select_none": "Seleccionar ninguno",
        "apply_filter": "Exportar solo los cuadros seleccionados\n(las líneas vacías/marcadores en blanco se eliminan automáticamente)",
        "detect_btn": "🔄 Detectar / Actualizar",
        "footer": "Los marcadores vacíos (solo ;;;) se filtran automáticamente. Archivos temporales en TEMP.",
        "msg_no_files": "Sin archivos cargados",
        "msg_select_folder_first": "Primero selecciona la carpeta del proyecto con los archivos TXT.",
        "msg_nothing_selected": "Nada que hacer",
        "msg_select_at_least_one": "Selecciona al menos un tipo de etiqueta.",
        "msg_done_title": "Proceso completado",
        "msg_done_body": "Se lanzaron {launched} de {total} procesos de MPrintPRO.\n\nFiltro de cuadros: {filter_text}",
        "msg_filter_no_results": "Sin resultados",
        "msg_filter_fallback": "No se encontraron líneas para los cuadros seleccionados.\nSe usará el archivo completo.",
        "filter_yes": "Sí",
        "filter_no": "No (todos los cuadros)",
        "lang_label": "Idioma:",
    }
}

current_lang = "nl"


def t(key):
    return translations.get(current_lang, translations["nl"]).get(key, key)


# ============== GLOBALS ==============

loaded_files = {}
detected_panels = []
panel_listbox = None

# Widgets updated by language/resize handlers
root = None
open_btn = None
FilenameTitle_label = None
Filename_label = None
action_btn = None
right_frame = None
footer = None
status_var = None
info_label = None
lang_label_widget = None

status_groep = None
status_kabels = None
status_klemmen = None
status_klemmenstrook = None
status_legends = None
status_onderdelen = None

# label option widgets for live translation
lbl_kast_section = None
chk_groep = None
chk_onderdelen = None
chk_onderdelen_lpc = None
chk_onderdelen_lbl = None
chk_onderdelen_tw = None
chk_legends = None
lbl_klemmen_section = None
chk_klemmenstrook = None
chk_klemmen = None
lbl_kabels_section = None
chk_kab10 = None
chk_kab100 = None
btn_select_all = None
btn_select_none = None
chk_use_filter = None
btn_detect = None

project_loaded = False


# ============== MPrintPRO HELPERS ==============


def StartMprintPro(misFile, sourcefile):
    command = [
        r'C:\Program Files (x86)\weidmueller\mprintpro\bin\MPrintPRO.exe',
        sourcefile,
        f'-ImportFilter:{misFile}'
    ]
    print(f"Executing command: {' '.join(command)}")
    subprocess.Popen(command)


def StartMprintProDirect(misFile, sourcefile):
    command = [
        r'C:\Program Files (x86)\weidmueller\mprintpro\bin\MPrintPRO.exe',
        sourcefile,
        f'-ImportFilter:{misFile}',
        "-p"
    ]
    print(f"Executing command: {' '.join(command)}")
    subprocess.Popen(command)


# ============== FILTERING LOGIC ==============


def create_filtered_temp(source_path, selected_panels):
    """Create a temporary file with only relevant lines.
    - Removes completely empty lines and blank markers
    - Applies panel filter if active
    """
    if not selected_panels:
        try:
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                all_lines = f.readlines()

            keep_lines = []
            for line in all_lines:
                stripped = line.strip()
                if not stripped or stripped.replace(';', '').strip() == '':
                    continue
                if stripped.count(';') >= 6 and len(stripped.replace(';', '').strip()) < 8:
                    continue
                keep_lines.append(line)

            tmp_path = os.path.join(tempfile.gettempdir(), "eplan_labels_filtered.txt")
            with open(tmp_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.writelines(keep_lines)
            return tmp_path
        except Exception:
            return source_path

    try:
        with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()

        keep_lines = []
        for line in all_lines:
            stripped = line.strip()
            if not stripped or stripped.replace(';', '').strip() == '':
                continue
            if stripped.count(';') >= 6 and len(stripped.replace(';', '').strip()) < 8:
                continue

            line_u = stripped.upper()
            match = False
            for pan in selected_panels:
                if re.search(rf'(^|[;+= \t]){re.escape(pan.upper())}($|[; \t\n])', line_u):
                    match = True
                    break
            if match:
                keep_lines.append(line)

        if len(keep_lines) == 0:
            messagebox.showwarning(t("msg_filter_no_results"), t("msg_filter_fallback"))
            return source_path

        tmp_path = os.path.join(tempfile.gettempdir(), "eplan_labels_filtered.txt")
        with open(tmp_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.writelines(keep_lines)

        return tmp_path

    except Exception:
        return source_path


# ============== PANEL DETECTION ==============


def detect_and_update_panels():
    global detected_panels, panel_listbox

    panel_set = set()
    groep_path = loaded_files.get('groep')

    if groep_path and os.path.exists(groep_path):
        try:
            with open(groep_path, 'r', encoding='utf-8', errors='ignore') as fh:
                for ln in fh:
                    p = ln.strip()
                    if p and 2 <= len(p) <= 25:
                        panel_set.add(p)
        except Exception as ex:
            print("Error reading Groepscode file:", ex)

    detected_panels = sorted(panel_set)

    if panel_listbox is not None:
        panel_listbox.delete(0, tk.END)
        for p in detected_panels:
            panel_listbox.insert(tk.END, p)
        if detected_panels:
            panel_listbox.select_set(0, tk.END)


# ============== MAIN GENERATE FUNCTION ==============


def generate_labels():
    if not loaded_files:
        messagebox.showwarning(t("msg_no_files"), t("msg_select_folder_first"))
        return

    jobs = []
    if var_groep.get() and loaded_files.get('groep'):
        jobs.append(("Groepscode", "groep", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Groepcode.mis", False))
    if var_onderdelen.get() and loaded_files.get('onderdelen'):
        jobs.append(("Onderdelen", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Onderdelen R10.mis", False))
    if var_onderdelen_lpc.get() and loaded_files.get('onderdelen'):
        jobs.append(("Onderdelen LPC", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Onderdelen_LPC.mis", True))
    if var_onderdelen_lbl.get() and loaded_files.get('onderdelen'):
        jobs.append(("Onderdelen Label", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Onderdelen_VolgensLabelR02.mis", False))
    if var_onderdelen_tw.get() and loaded_files.get('onderdelen'):
        jobs.append(("Onderdelen Tech", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_OnderdelenR02.mis", False))
    if var_legends.get() and loaded_files.get('legends'):
        jobs.append(("Legends", "legends", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Legends R10.mis", False))
    if var_klemmenstrook.get() and loaded_files.get('klemmenstrook'):
        jobs.append(("Klemmenstrook", "klemmenstrook", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klemmenstrook R10.mis", False))
    if var_klemmen.get() and loaded_files.get('klemmen'):
        jobs.append(("Klemmen", "klemmen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klem R10.mis", False))
    if var_kab10.get() and loaded_files.get('kabels'):
        jobs.append(("Kabels 0-10mm", "kabels", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 0-10mm R10.mis", False))
    if var_kab100.get() and loaded_files.get('kabels'):
        jobs.append(("Kabels 10-100mm", "kabels", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 10-100 mm R10.mis", False))

    if not jobs:
        messagebox.showinfo(t("msg_nothing_selected"), t("msg_select_at_least_one"))
        return

    sel_panels = []
    if var_use_filter.get():
        sel = panel_listbox.curselection() if panel_listbox else ()
        if sel:
            sel_panels = [panel_listbox.get(i) for i in sel]

    use_filter = len(sel_panels) > 0

    launched = 0
    for display_name, src_key, mis_path, direct in jobs:
        src = loaded_files.get(src_key)
        if not src:
            continue

        work_file = create_filtered_temp(src, sel_panels) if use_filter else src
        tempname = str(work_file).replace('/', '\\')

        try:
            if direct:
                StartMprintProDirect(mis_path, tempname)
            else:
                StartMprintPro(mis_path, tempname)
            launched += 1
        except Exception as e:
            print(f"Error launching {display_name}: {e}")

    filter_text = (
        f"{t('filter_yes')} ({', '.join(sel_panels[:4])}{'...' if len(sel_panels) > 4 else ''})"
        if use_filter else t("filter_no")
    )
    messagebox.showinfo(
        t("msg_done_title"),
        t("msg_done_body").format(launched=launched, total=len(jobs), filter_text=filter_text)
    )


# ============== LOAD PROJECT FOLDER ==============


def update_loaded_indicators():
    status_map = {
        'groep': status_groep,
        'kabels': status_kabels,
        'klemmen': status_klemmen,
        'klemmenstrook': status_klemmenstrook,
        'legends': status_legends,
        'onderdelen': status_onderdelen
    }
    for key, lbl in status_map.items():
        if loaded_files.get(key):
            lbl.config(text=f"✓ {key.upper()}", bg="#90EE90", fg="black")
        else:
            lbl.config(text=f"✗ {key.upper()}", bg="#FFCCCB", fg="black")


def load_project_folder():
    folder = filedialog.askdirectory(title="Select the project folder containing Eplan TXT files")
    if not folder:
        return

    global loaded_files, project_loaded
    loaded_files = {}

    candidates = glob.glob(os.path.join(folder, "*R0*.txt")) or glob.glob(os.path.join(folder, "*.txt"))

    patterns = {
        'groep': 'GROEPSCODE',
        'kabels': 'KABELS',
        'klemmenstrook': 'KLEMMENSTROOK',
        'klemmen': 'KLEMMEN',
        'legends': 'LEGENDS',
        'onderdelen': 'ONDERDEEL'
    }

    for txt_path in candidates:
        base_upper = os.path.basename(txt_path).upper()
        for key, keyword in patterns.items():
            if keyword in base_upper:
                if key == 'klemmen' and 'STROOK' in base_upper:
                    continue
                if key == 'klemmenstrook' and 'STROOK' not in base_upper:
                    continue
                if key not in loaded_files:
                    loaded_files[key] = txt_path
                break

    update_loaded_indicators()
    detect_and_update_panels()

    project_name = os.path.basename(folder)
    Filename_label.config(text=f"Project: {project_name} ({len(loaded_files)} files)")
    status_var.set(f"Folder loaded: {project_name}")
    project_loaded = True


# ============== LANGUAGE HANDLING ==============


def refresh_ui_texts():
    root.title(t("app_title"))
    open_btn.config(text=t("load_btn"))
    FilenameTitle_label.config(text=t("project_lbl"))
    action_btn.config(text=t("generate_btn"))
    right_frame.config(text=t("panels_section"))
    footer.config(text=t("footer"))
    lang_label_widget.config(text=t("lang_label"))

    lbl_kast_section.config(text=t("kast_section"))
    chk_groep.config(text=t("groepscode"))
    chk_onderdelen.config(text=t("onderdelen_norm"))
    chk_onderdelen_lpc.config(text=t("onderdelen_lpc"))
    chk_onderdelen_lbl.config(text=t("onderdelen_label"))
    chk_onderdelen_tw.config(text=t("onderdelen_tech"))
    chk_legends.config(text=t("legends"))

    lbl_klemmen_section.config(text=t("klemmen_section"))
    chk_klemmenstrook.config(text=t("klemmenstrook"))
    chk_klemmen.config(text=t("klemmen_los"))

    lbl_kabels_section.config(text=t("kabels_section"))
    chk_kab10.config(text=t("kabels_0_10"))
    chk_kab100.config(text=t("kabels_10_100"))

    info_label.config(text=t("panels_info"))
    btn_select_all.config(text=t("select_all"))
    btn_select_none.config(text=t("select_none"))
    chk_use_filter.config(text=t("apply_filter"))
    btn_detect.config(text=t("detect_btn"))

    if not project_loaded:
        Filename_label.config(text=t("no_project"))
        status_var.set(t("status_ready"))

    update_wraps()


def change_language(new_lang):
    global current_lang
    current_lang = new_lang
    refresh_ui_texts()


def on_lang_change(event):
    val = lang_combo.get()
    if val == "Nederlands":
        change_language("nl")
    elif val == "English":
        change_language("en")
    elif val == "Español":
        change_language("es")


# ============== RESPONSIVE HELPERS ==============


def update_wraps():
    if info_label is not None and right_frame is not None:
        wrap = max(260, right_frame.winfo_width() - 40)
        info_label.config(wraplength=wrap)


def on_resize(event):
    if event.widget is root:
        update_wraps()


# ============== GUI ==============

root = tk.Tk()
root.geometry("1180x760")
root.minsize(980, 620)
root.wm_title(t("app_title"))

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(2, weight=1)

status_var = tk.StringVar(value=t("status_ready"))
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.grid(row=1, column=0, sticky="ew")

# Top bar
top_bar = tk.Frame(frame)
top_bar.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)

top_bar.columnconfigure(0, weight=1)

open_btn = tk.Button(
    top_bar,
    text=t("load_btn"),
    command=load_project_folder,
    bg="#4CAF50",
    fg="white",
    font=("calibre", 11, "bold"),
    padx=15,
    pady=6
)
open_btn.pack(side=tk.LEFT, padx=10)

FilenameTitle_label = tk.Label(top_bar, text=t("project_lbl"), font=('calibre', 10, 'bold'))
FilenameTitle_label.pack(side=tk.LEFT, padx=(20, 5))

Filename_label = tk.Label(top_bar, text=t("no_project"), font=('calibre', 10))
Filename_label.pack(side=tk.LEFT)

lang_frame = tk.Frame(top_bar)
lang_frame.pack(side=tk.RIGHT, padx=15)
lang_label_widget = tk.Label(lang_frame, text=t("lang_label"), font=('calibre', 9, 'bold'))
lang_label_widget.pack(side=tk.LEFT)
lang_combo = ttk.Combobox(lang_frame, values=["Nederlands", "English", "Español"], state="readonly", width=13)
lang_combo.set("Nederlands")
lang_combo.pack(side=tk.LEFT, padx=5)
lang_combo.bind("<<ComboboxSelected>>", on_lang_change)

# File status indicators
status_frame = tk.Frame(frame)
status_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=3)
status_groep = tk.Label(status_frame, text="✗ GROEP", width=12, relief=tk.GROOVE)
status_kabels = tk.Label(status_frame, text="✗ KABELS", width=12, relief=tk.GROOVE)
status_klemmen = tk.Label(status_frame, text="✗ KLEMMEN", width=12, relief=tk.GROOVE)
status_klemmenstrook = tk.Label(status_frame, text="✗ KLEMMENSTR", width=14, relief=tk.GROOVE)
status_legends = tk.Label(status_frame, text="✗ LEGENDS", width=12, relief=tk.GROOVE)
status_onderdelen = tk.Label(status_frame, text="✗ ONDERDELEN", width=14, relief=tk.GROOVE)
for lbl in [status_groep, status_kabels, status_klemmen, status_klemmenstrook, status_legends, status_onderdelen]:
    lbl.pack(side=tk.LEFT, padx=3)

# Main split
main_paned = tk.PanedWindow(frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
main_paned.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5)

left_frame = tk.LabelFrame(main_paned, text=t("kast_section"), padx=10, pady=8)
main_paned.add(left_frame, minsize=340, width=430)

lbl_kast_section = tk.Label(left_frame, text=t("kast_section"), font=('calibre', 10, 'bold'), fg="#2E86AB")
lbl_kast_section.pack(anchor="w", pady=(5, 2))

var_groep = tk.BooleanVar(value=True)
chk_groep = ttk.Checkbutton(left_frame, text=t("groepscode"), variable=var_groep)
chk_groep.pack(anchor="w")

var_onderdelen = tk.BooleanVar(value=True)
chk_onderdelen = ttk.Checkbutton(left_frame, text=t("onderdelen_norm"), variable=var_onderdelen)
chk_onderdelen.pack(anchor="w")

var_onderdelen_lpc = tk.BooleanVar(value=False)
chk_onderdelen_lpc = ttk.Checkbutton(left_frame, text=t("onderdelen_lpc"), variable=var_onderdelen_lpc)
chk_onderdelen_lpc.pack(anchor="w")

var_onderdelen_lbl = tk.BooleanVar(value=False)
chk_onderdelen_lbl = ttk.Checkbutton(left_frame, text=t("onderdelen_label"), variable=var_onderdelen_lbl)
chk_onderdelen_lbl.pack(anchor="w")

var_onderdelen_tw = tk.BooleanVar(value=False)
chk_onderdelen_tw = ttk.Checkbutton(left_frame, text=t("onderdelen_tech"), variable=var_onderdelen_tw)
chk_onderdelen_tw.pack(anchor="w")

var_legends = tk.BooleanVar(value=True)
chk_legends = ttk.Checkbutton(left_frame, text=t("legends"), variable=var_legends)
chk_legends.pack(anchor="w")

lbl_klemmen_section = tk.Label(left_frame, text=t("klemmen_section"), font=('calibre', 10, 'bold'), fg="#2E86AB")
lbl_klemmen_section.pack(anchor="w", pady=(12, 2))

var_klemmenstrook = tk.BooleanVar(value=True)
chk_klemmenstrook = ttk.Checkbutton(left_frame, text=t("klemmenstrook"), variable=var_klemmenstrook)
chk_klemmenstrook.pack(anchor="w")

var_klemmen = tk.BooleanVar(value=True)
chk_klemmen = ttk.Checkbutton(left_frame, text=t("klemmen_los"), variable=var_klemmen)
chk_klemmen.pack(anchor="w")

lbl_kabels_section = tk.Label(left_frame, text=t("kabels_section"), font=('calibre', 10, 'bold'), fg="#2E86AB")
lbl_kabels_section.pack(anchor="w", pady=(12, 2))

var_kab10 = tk.BooleanVar(value=True)
chk_kab10 = ttk.Checkbutton(left_frame, text=t("kabels_0_10"), variable=var_kab10)
chk_kab10.pack(anchor="w")

var_kab100 = tk.BooleanVar(value=True)
chk_kab100 = ttk.Checkbutton(left_frame, text=t("kabels_10_100"), variable=var_kab100)
chk_kab100.pack(anchor="w")

action_btn = tk.Button(
    left_frame,
    text=t("generate_btn"),
    command=generate_labels,
    bg="#FF6B35",
    fg="white",
    font=("calibre", 13, "bold"),
    padx=20,
    pady=12,
    relief=tk.RAISED
)
action_btn.pack(pady=20, fill=tk.X)

# Right pane
right_frame = tk.LabelFrame(main_paned, text=t("panels_section"), padx=10, pady=8)
main_paned.add(right_frame, minsize=320, width=420)

info_label = tk.Label(right_frame, text=t("panels_info"), justify=tk.LEFT, font=('calibre', 9), anchor="w")
info_label.pack(anchor="w", pady=(0, 6), fill="x")

list_container = tk.Frame(right_frame)
list_container.pack(fill=tk.BOTH, expand=True)

panel_listbox = tk.Listbox(
    list_container,
    selectmode=tk.MULTIPLE,
    height=16,
    width=34,
    exportselection=False,
    bg="#F8F9FA",
    font=('calibre', 10)
)
panel_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=panel_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
panel_listbox.config(yscrollcommand=scrollbar.set)

btn_frame = tk.Frame(right_frame)
btn_frame.pack(fill=tk.X, pady=6)

btn_select_all = ttk.Button(btn_frame, text=t("select_all"), width=18, command=lambda: panel_listbox.select_set(0, tk.END))
btn_select_all.pack(side=tk.LEFT, padx=3)

btn_select_none = ttk.Button(btn_frame, text=t("select_none"), width=18, command=lambda: panel_listbox.selection_clear(0, tk.END))
btn_select_none.pack(side=tk.LEFT, padx=3)

var_use_filter = tk.BooleanVar(value=False)
chk_use_filter = ttk.Checkbutton(right_frame, text=t("apply_filter"), variable=var_use_filter)
chk_use_filter.pack(anchor="w", pady=4, fill="x")

btn_detect = ttk.Button(right_frame, text=t("detect_btn"), command=detect_and_update_panels)
btn_detect.pack(pady=4, fill=tk.X)

footer = tk.Label(frame, text=t("footer"), font=('calibre', 8), fg="gray")
footer.grid(row=3, column=0, columnspan=3, sticky="w", pady=5)

# Keyboard shortcuts
root.bind('<Control-o>', lambda e: load_project_folder())
root.bind('<F5>', lambda e: detect_and_update_panels())
root.bind('<Return>', lambda e: generate_labels())
root.bind('<Configure>', on_resize)

# Initialize layout-dependent wrapping after first draw
root.after(100, update_wraps)

root.mainloop()
