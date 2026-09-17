#!/usr/bin/env python3
"""
Eplan Label Tool by Wolfs-TS
Improved by Lira Sobrino Rodríguez
"""

import sys
import os
import subprocess
import glob
import re
import tempfile
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog

print(sys.version)
print("Current working directory:", os.getcwd())

# ============================================================
# TRANSLATIONS
# ============================================================
# All translatable strings are centralized in this dictionary.
# The current language is controlled by `current_lang` and helper `t(key)`.
translations = {
    "nl": {
        "app_title": "Eplan Label Tool by Wolfs-TS",
        "load_btn": "📁 Laad projectmap (TXT)",
        "load_project_btn": "🔎 Project laden",
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

        "menu_settings": "Instellingen",
        "menu_open_settings": "Instellingen openen",
        "menu_manual_update": "Handmatige update",
        "menu_auto_update": "Automatische update",

        "settings_title": "Instellingen",
        "settings_main_folder": "Hoofdprojectmap:",
        "settings_browse": "Bladeren...",
        "settings_legacy_selection": "Legacy-selectie activeren",
        "settings_save": "Opslaan",
        "settings_cancel": "Annuleren",
        "settings_saved": "Instellingen opgeslagen.",

        "msg_settings_missing_title": "Hoofdprojectmap ontbreekt",
        "msg_settings_missing": "Stel eerst een hoofdprojectmap in via Instellingen.",
        "msg_project_number_title": "Project laden",
        "msg_project_number_prompt": "Voer projectnummer in (bijv. 123):",
        "msg_project_not_found_title": "Project niet gevonden",
        "msg_project_not_found": "Geen map gevonden die start met '{project_number}' in de hoofdprojectmap.",
        "msg_drawings_missing_title": "Map ontbreekt",
        "msg_drawings_missing": "De map 'Tekeningen' is niet gevonden in: {project_path}",
        "msg_revision_missing_title": "Revisie ontbreekt",
        "msg_revision_missing": "Geen revisiemappen gevonden (R###) in: {drawings_path}",
        "msg_labels_missing_title": "Labels map ontbreekt",
        "msg_labels_missing": "De map 'labels' is niet gevonden in: {revision_path}",
        "msg_loaded_from_project": "Project geladen via nummer: {project_number} (revisie {revision_name})",
        "msg_no_matching_txt_title": "Geen bruikbare TXT bestanden",
        "msg_no_matching_txt": "Er zijn wel TXT bestanden gevonden, maar geen bekende Eplan bestandsnamen (GROEPSCODE/KABELS/KLEMMEN/etc).",
        "msg_select_txt_for_folder": "Selecteer één Eplan TXT-bestand uit de projectmap",
        "msg_folder_loaded": "Map geladen: {project_name}",
        "msg_manual_update_title": "Handmatige update",
        "msg_auto_update_title": "Automatische update",
        "msg_update_handler_missing": "Deze update-optie is nog niet beschikbaar.",
        "cabinet_markers": "Kastmarkeringen",
        "component_markers": "Componentmarkeringen",
        "terminal_markers": "Klemmenmarkeringen",
        "cable_markers": "Kabelmarkeringen"
    },
    "en": {
        "app_title": "Eplan Label Tool by Wolfs-TS — v4 (Project loader + settings)",
        "load_btn": "📁 Load project folder (TXT)",
        "load_project_btn": "🔎 Load project",
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

        "menu_settings": "Settings",
        "menu_open_settings": "Open settings",
        "menu_manual_update": "Manual update",
        "menu_auto_update": "Auto update",

        "settings_title": "Settings",
        "settings_main_folder": "Main project folder:",
        "settings_browse": "Browse...",
        "settings_legacy_selection": "Enable legacy selection",
        "settings_save": "Save",
        "settings_cancel": "Cancel",
        "settings_saved": "Settings saved.",

        "msg_settings_missing_title": "Main project folder missing",
        "msg_settings_missing": "Please configure the main project folder first in Settings.",
        "msg_project_number_title": "Load project",
        "msg_project_number_prompt": "Enter project number (e.g. 123):",
        "msg_project_not_found_title": "Project not found",
        "msg_project_not_found": "No folder found starting with '{project_number}' inside the main project folder.",
        "msg_drawings_missing_title": "Folder missing",
        "msg_drawings_missing": "The folder 'Tekeningen' was not found in: {project_path}",
        "msg_revision_missing_title": "Revision missing",
        "msg_revision_missing": "No revision folders found (R###) in: {drawings_path}",
        "msg_labels_missing_title": "Labels folder missing",
        "msg_labels_missing": "The folder 'labels' was not found in: {revision_path}",
        "msg_loaded_from_project": "Project loaded by number: {project_number} (revision {revision_name})",
        "msg_no_matching_txt_title": "No usable TXT files",
        "msg_no_matching_txt": "TXT files were found, but no known Eplan filenames matched (GROEPSCODE/KABELS/KLEMMEN/etc).",
        "msg_select_txt_for_folder": "Select one Eplan TXT file from the project folder",
        "msg_folder_loaded": "Folder loaded: {project_name}",
        "msg_manual_update_title": "Manual update",
        "msg_auto_update_title": "Auto update",
        "msg_update_handler_missing": "This update option is not available yet.",
        "cabinet_markers": "Cabinet markers",
        "component_markers": "Component markers",
        "terminal_markers": "Terminal markers",
        "cable_markers": "Cable markers"
    },
    "es": {
        "app_title": "Herramienta de Etiquetas Eplan por Wolfs-TS — v4 (Cargador de proyecto + ajustes)",
        "load_btn": "📁 Cargar carpeta del proyecto (TXT)",
        "load_project_btn": "🔎 Cargar proyecto",
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

        "menu_settings": "Ajustes",
        "menu_open_settings": "Abrir ajustes",
        "menu_manual_update": "Actualización manual",
        "menu_auto_update": "Actualización automática",

        "settings_title": "Ajustes",
        "settings_main_folder": "Carpeta principal de proyectos:",
        "settings_browse": "Examinar...",
        "settings_legacy_selection": "Activar selección heredada",
        "settings_save": "Guardar",
        "settings_cancel": "Cancelar",
        "settings_saved": "Ajustes guardados.",

        "msg_settings_missing_title": "Falta la carpeta principal",
        "msg_settings_missing": "Primero configura la carpeta principal en Ajustes.",
        "msg_project_number_title": "Cargar proyecto",
        "msg_project_number_prompt": "Introduce el número de proyecto (p. ej. 123):",
        "msg_project_not_found_title": "Proyecto no encontrado",
        "msg_project_not_found": "No se encontró ninguna carpeta que empiece por '{project_number}' dentro de la carpeta principal.",
        "msg_drawings_missing_title": "Falta carpeta",
        "msg_drawings_missing": "La carpeta 'Tekeningen' no se encontró en: {project_path}",
        "msg_revision_missing_title": "Falta revisión",
        "msg_revision_missing": "No se encontraron carpetas de revisión (R###) en: {drawings_path}",
        "msg_labels_missing_title": "Falta carpeta labels",
        "msg_labels_missing": "La carpeta 'labels' no se encontró en: {revision_path}",
        "msg_loaded_from_project": "Proyecto cargado por número: {project_number} (revisión {revision_name})",
        "msg_no_matching_txt_title": "No hay TXT utilizables",
        "msg_no_matching_txt": "Se encontraron TXT, pero no coinciden con nombres Eplan conocidos (GROEPSCODE/KABELS/KLEMMEN/etc).",
        "msg_select_txt_for_folder": "Selecciona un archivo TXT de Eplan de la carpeta del proyecto",
        "msg_folder_loaded": "Carpeta cargada: {project_name}",
        "msg_manual_update_title": "Actualización manual",
        "msg_auto_update_title": "Actualización automática",
        "msg_update_handler_missing": "Esta opción de actualización todavía no está disponible.",
        "cabinet_markers": "Marcadores de armarios",
        "component_markers": "Marcadores de componentes",
        "terminal_markers": "Marcadores de bornes",
        "cable_markers": "Marcadores de cables"
    }
}

# Default language is Dutch.
current_lang = "nl"


# Translation helper.
def t(key):
    return translations.get(current_lang, translations["nl"]).get(key, key)


# ============================================================
# GLOBALS
# ============================================================
loaded_files = {}
detected_panels = []
panel_listbox = None

# App settings (persisted in a local JSON file next to this script).
settings = {
    "main_project_folder": "",
    "legacy_selection": False
}
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

# Widgets updated by language/resize handlers
root = None
open_btn = None
load_project_btn = None
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

# Label option widgets for live translation
lbl_kast_section = None
chk_groep = None
chk_cabinet_markers = None
chk_component_markers = None
chk_terminal_markers = None
chk_cable_markers = None
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
selection_mode_frame = None
legacy_options_frame = None

project_loaded = False


# ============================================================
# SETTINGS HELPERS
# ============================================================
# These functions handle loading/saving the app configuration.
def load_settings_from_disk():
    """Load settings.json if present. If invalid/missing, keep defaults."""
    global settings
    if not os.path.exists(SETTINGS_FILE):
        return

    try:
        import json
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            settings["main_project_folder"] = str(data.get("main_project_folder", "")).strip()
            settings["legacy_selection"] = bool(data.get("legacy_selection", False))
    except Exception as ex:
        print("Could not load settings:", ex)


def save_settings_to_disk():
    """Persist settings to settings.json."""
    try:
        import json
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception as ex:
        messagebox.showerror("Error", f"Could not save settings: {ex}")


def open_settings_window():
    """Open a small modal settings window to edit the main project folder."""
    win = tk.Toplevel(root)
    win.title(t("settings_title"))
    win.geometry("720x170")
    win.minsize(600, 150)
    win.transient(root)
    win.grab_set()

    container = tk.Frame(win, padx=12, pady=12)
    container.pack(fill=tk.BOTH, expand=True)

    tk.Label(container, text=t("settings_main_folder"), font=('calibre', 10, 'bold')).grid(row=0, column=0, sticky="w")

    folder_var = tk.StringVar(value=settings.get("main_project_folder", ""))
    entry = tk.Entry(container, textvariable=folder_var)
    entry.grid(row=1, column=0, sticky="ew", pady=(6, 0))

    def browse_folder():
        selected = filedialog.askdirectory(title=t("settings_main_folder"))
        if selected:
            folder_var.set(selected)

    browse_btn = ttk.Button(container, text=t("settings_browse"), command=browse_folder)
    browse_btn.grid(row=1, column=1, padx=(8, 0), sticky="ew")

    legacy_var = tk.BooleanVar(value=settings.get("legacy_selection", False))
    legacy_chk = ttk.Checkbutton(container, text=t("settings_legacy_selection"), variable=legacy_var)
    legacy_chk.grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))

    def do_save():
        settings["main_project_folder"] = folder_var.get().strip()
        settings["legacy_selection"] = legacy_var.get()
        save_settings_to_disk()
        apply_selection_mode_ui()
        messagebox.showinfo(t("settings_title"), t("settings_saved"))
        win.destroy()

    btns = tk.Frame(container)
    btns.grid(row=3, column=0, columnspan=2, sticky="e", pady=(14, 0))

    ttk.Button(btns, text=t("settings_cancel"), command=win.destroy).pack(side=tk.RIGHT, padx=(8, 0))
    ttk.Button(btns, text=t("settings_save"), command=do_save).pack(side=tk.RIGHT)

    container.columnconfigure(0, weight=1)


def run_manual_update():
    """Run manual update handler when available; otherwise show a safe placeholder."""
    handler = globals().get("manual_update")
    if callable(handler):
        handler()
        return
    messagebox.showinfo(t("msg_manual_update_title"), t("msg_update_handler_missing"))


def run_auto_update():
    """Run auto update handler when available; otherwise show a safe placeholder."""
    handler = globals().get("auto_update")
    if callable(handler):
        handler()
        return
    messagebox.showinfo(t("msg_auto_update_title"), t("msg_update_handler_missing"))


# ============================================================
# MPRINTPRO HELPERS
# ============================================================
def StartMprintPro(misFile, sourcefile):
    """Launch MPrintPRO with a filter script and source file."""
    command = [
        r'C:\Program Files (x86)\weidmueller\mprintpro\bin\MPrintPRO.exe',
        sourcefile,
        f'-ImportFilter:{misFile}'
    ]
    print(f"Executing command: {' '.join(command)}")
    subprocess.Popen(command)


def StartMprintProDirect(misFile, sourcefile):
    """Launch MPrintPRO in direct print mode (-p)."""
    command = [
        r'C:\Program Files (x86)\weidmueller\mprintpro\bin\MPrintPRO.exe',
        sourcefile,
        f'-ImportFilter:{misFile}',
        "-p"
    ]
    print(f"Executing command: {' '.join(command)}")
    subprocess.Popen(command)


# ============================================================
# FILTERING LOGIC
# ============================================================
def create_filtered_temp(source_path, selected_panels):
    """Create a temporary filtered file.

    Behavior:
    - Removes empty lines and blank marker rows.
    - If selected_panels is not empty, keeps only lines that match those panels.
    - Falls back to original file on read/write errors.
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


# ============================================================
# PANEL DETECTION
# ============================================================
def detect_and_update_panels():
    """Read panel names from the loaded groepscode file and refresh listbox."""
    global detected_panels, panel_listbox

    panel_set = set()
    groep_path = loaded_files.get('groep')

    if groep_path and os.path.exists(groep_path):
        try:
            with open(groep_path, 'r', encoding='utf-8', errors='ignore') as fh:
                for ln in fh:
                    p = ln.strip()
                    if p and 2 <= len(p) <= 25 and not is_revision_header_line(p):
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


# ============================================================
# MAIN GENERATE FUNCTION
# ============================================================
def generate_labels():
    """Build selected jobs and launch one MPrintPRO process per selected label type."""
    if not loaded_files:
        messagebox.showwarning(t("msg_no_files"), t("msg_select_folder_first"))
        return

    jobs = []
    use_r10 = settings.get("revision_selection", False)

    def add_revision_job(selected, display_name, src_key, old_mis, new_mis, direct=False):
        if selected and loaded_files.get(src_key):
            jobs.append((display_name, src_key, new_mis if use_r10 else old_mis, direct))

    if settings.get("legacy_selection", False):
        if var_groep.get() and loaded_files.get('groep'):
            jobs.append(("Groepscode", "groep", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Groepcode.mis", False))

        add_revision_job(var_onderdelen.get(), "Onderdelen", "onderdelen",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Onderdelen.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Onderdelen R10.mis")

        add_revision_job(var_onderdelen_lpc.get(), "Onderdelen LPC", "onderdelen",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Onderdelen_LPC.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Onderdelen_LPC.mis",
                         True)

        if var_onderdelen_lbl.get() and loaded_files.get('onderdelen'):
            jobs.append(("Onderdelen Label", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Onderdelen_VolgensLabelR02.mis", False))
        if var_onderdelen_tw.get() and loaded_files.get('onderdelen'):
            jobs.append(("Onderdelen Tech", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_OnderdelenR02.mis", False))

        add_revision_job(var_legends.get(), "Legends", "legends",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Legends.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Legends R10.mis")

        add_revision_job(var_klemmenstrook.get(), "Klemmenstrook", "klemmenstrook",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klemmenstrook.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klemmenstrook R10.mis")

        add_revision_job(var_klemmen.get(), "Klemmen", "klemmen",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klem.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klem R10.mis")

        add_revision_job(var_kab10.get(), "Kabels 0-10mm", "kabels",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 0-10mm.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 0-10mm R10.mis")

        add_revision_job(var_kab100.get(), "Kabels 10-100mm", "kabels",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 10-100 mm.mis",
                         r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 10-100 mm R10.mis")
    else:
        if var_cabinet_markers.get():
            if loaded_files.get('groep'):
                jobs.append(("Groepscode", "groep", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Groepcode.mis", False))

            add_revision_job(True, "Legends", "legends",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Legends.mis",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Legends R10.mis")

        if var_component_markers.get() and loaded_files.get('onderdelen'):
            jobs.append(("Onderdelen Tech", "onderdelen", r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_OnderdelenR02.mis", False))

        if var_terminal_markers.get():
            add_revision_job(True, "Klemmenstrook", "klemmenstrook",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klemmenstrook.mis",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klemmenstrook R10.mis")

            add_revision_job(True, "Klemmen", "klemmen",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klem.mis",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Klem R10.mis")

        if var_cable_markers.get():
            add_revision_job(True, "Kabels 0-10mm", "kabels",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 0-10mm.mis",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 0-10mm R10.mis")
            add_revision_job(True, "Kabels 10-100mm", "kabels",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 10-100 mm.mis",
                             r"C:\Users\werkplaats\projects\Eplan-Label\ImportScripts\Wolfs-TS_Labels_Kabels 10-100 mm R10.mis")

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


# ============================================================
# FILE DETECTION AND LOAD HELPERS
# ============================================================
REVISION_HEADER_PATTERN = re.compile(r'^\s*;{0,4}.*\bREVISIE\s+\d+\b', flags=re.IGNORECASE)


def is_revision_header_line(line):
    """Return True when the line looks like a revision-aware label header."""
    return bool(REVISION_HEADER_PATTERN.search(line.strip()))


def detect_revision_selection():
    """Return True for new format, False for old format, or None when detection fails."""
    inspected_any = False

    for file_path in loaded_files.values():
        if not file_path:
            print("Could not inspect revision format: missing file path.")
            return None
        if not os.path.exists(file_path):
            print(f"Could not inspect revision format, file missing: {file_path}")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                for line in fh:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    inspected_any = True
                    if is_revision_header_line(stripped):
                        return True
        except OSError as ex:
            print(f"Could not inspect revision format in {file_path}: {ex}")
            return None

    return False if inspected_any else None


def detect_files_from_candidates(candidates):
    """Classify TXT files based on filename keywords and update loaded_files."""
    global loaded_files
    loaded_files = {}

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

    detected_revision = detect_revision_selection()
    if detected_revision is not None:
        settings["revision_selection"] = detected_revision


def finish_project_load(project_display_name, status_text):
    """Finalize UI state after files were loaded."""
    global project_loaded
    update_loaded_indicators()
    detect_and_update_panels()

    Filename_label.config(text=f"Project: {project_display_name} ({len(loaded_files)} files)")
    status_var.set(status_text)
    project_loaded = True


# ============================================================
# MANUAL FILE/FOLDER LOAD
# ============================================================
def load_project_folder():
    """Load project by selecting one visible TXT file, then loading all TXT from that folder."""
    selected_file = filedialog.askopenfilename(
        title=t("msg_select_txt_for_folder"),
        filetypes=[
            ("Text files", "*.txt"),
            ("R0 text files", "*R0*.txt"),
            ("All files", "*.*"),
        ],
    )

    if not selected_file:
        return

    folder = os.path.dirname(selected_file)
    candidates = glob.glob(os.path.join(folder, "*R0*.txt"))
    if not candidates:
        candidates = glob.glob(os.path.join(folder, "*.txt"))

    detect_files_from_candidates(candidates)

    if len(loaded_files) == 0:
        messagebox.showwarning(t("msg_no_matching_txt_title"), t("msg_no_matching_txt"))

    project_name = os.path.basename(folder)
    finish_project_load(project_name, t("msg_folder_loaded").format(project_name=project_name))


# ============================================================
# LOAD PROJECT BY NUMBER (NEW FEATURE)
# ============================================================
def parse_revision_number(folder_name):
    """Return revision number from folder names like R1, R014, R123.

    If not a valid revision folder, returns None.
    """
    m = re.match(r'^R(\d+)$', folder_name.strip(), flags=re.IGNORECASE)
    if not m:
        return None
    return int(m.group(1))


def find_project_folder_by_number(main_folder, project_number):
    """Find first folder whose name starts with the project number."""
    try:
        entries = [
            os.path.join(main_folder, d)
            for d in os.listdir(main_folder)
            if os.path.isdir(os.path.join(main_folder, d))
        ]
    except Exception:
        return None

    proj_prefix = project_number.strip().upper()
    matches = [p for p in entries if os.path.basename(p).upper().startswith(proj_prefix)]
    matches.sort(key=lambda p: os.path.basename(p).upper())
    return matches[0] if matches else None


def find_latest_revision_folder(tekeningen_folder):
    """Find highest numeric R### folder using numeric comparison."""
    rev_candidates = []
    try:
        for d in os.listdir(tekeningen_folder):
            full = os.path.join(tekeningen_folder, d)
            if not os.path.isdir(full):
                continue
            rev_num = parse_revision_number(d)
            if rev_num is not None:
                rev_candidates.append((rev_num, d, full))
    except Exception:
        return None, None

    if not rev_candidates:
        return None, None

    # Numeric comparison exactly as requested.
    rev_candidates.sort(key=lambda x: x[0])
    latest_num, latest_name, latest_path = rev_candidates[-1]
    return latest_name, latest_path


def load_project_by_number():
    """Load TXT files by project number using:
    main folder -> <project startswith number> -> Tekeningen -> latest R### -> labels
    """
    main_folder = settings.get("main_project_folder", "").strip()
    if not main_folder or not os.path.isdir(main_folder):
        messagebox.showwarning(t("msg_settings_missing_title"), t("msg_settings_missing"))
        return

    project_number = simpledialog.askstring(
        t("msg_project_number_title"),
        t("msg_project_number_prompt"),
        parent=root
    )
    if project_number is None:
        return
    project_number = project_number.strip()
    if not project_number:
        return

    project_path = find_project_folder_by_number(main_folder, project_number)
    if not project_path:
        messagebox.showwarning(
            t("msg_project_not_found_title"),
            t("msg_project_not_found").format(project_number=project_number)
        )
        return

    tekeningen_path = os.path.join(project_path, "Tekeningen")
    if not os.path.isdir(tekeningen_path):
        messagebox.showwarning(
            t("msg_drawings_missing_title"),
            t("msg_drawings_missing").format(project_path=project_path)
        )
        return

    revision_name, revision_path = find_latest_revision_folder(tekeningen_path)
    if not revision_path:
        messagebox.showwarning(
            t("msg_revision_missing_title"),
            t("msg_revision_missing").format(drawings_path=tekeningen_path)
        )
        return

    labels_path = os.path.join(revision_path, "labels")
    if not os.path.isdir(labels_path):
        messagebox.showwarning(
            t("msg_labels_missing_title"),
            t("msg_labels_missing").format(revision_path=revision_path)
        )
        return

    # Collect txt files from labels folder.
    candidates = glob.glob(os.path.join(labels_path, "*R0*.txt"))
    if not candidates:
        candidates = glob.glob(os.path.join(labels_path, "*.txt"))

    detect_files_from_candidates(candidates)

    if len(loaded_files) == 0:
        messagebox.showwarning(t("msg_no_matching_txt_title"), t("msg_no_matching_txt"))

    project_display_name = os.path.basename(project_path)
    status_text = t("msg_loaded_from_project").format(project_number=project_number, revision_name=revision_name)
    finish_project_load(project_display_name, status_text)


# ============================================================
# LOAD PROJECT FOLDER INDICATORS
# ============================================================
def update_loaded_indicators():
    """Update colored status labels for each expected file type."""
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


# ============================================================
# LANGUAGE HANDLING
# ============================================================
def refresh_ui_texts():
    """Re-apply all visible texts after language changes."""
    root.title(t("app_title"))
    open_btn.config(text=t("load_btn"))
    load_project_btn.config(text=t("load_project_btn"))
    FilenameTitle_label.config(text=t("project_lbl"))
    action_btn.config(text=t("generate_btn"))
    right_frame.config(text=t("panels_section"))
    footer.config(text=t("footer"))
    lang_label_widget.config(text=t("lang_label"))

    lbl_kast_section.config(text=t("kast_section"))
    chk_cabinet_markers.config(text=t("cabinet_markers"))
    chk_component_markers.config(text=t("component_markers"))
    chk_terminal_markers.config(text=t("terminal_markers"))
    chk_cable_markers.config(text=t("cable_markers"))
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

    # Update settings menu labels as well.
    menubar.entryconfig(0, label=t("menu_settings"))
    settings_menu.entryconfig(0, label=t("menu_open_settings"))
    settings_menu.entryconfig(1, label=t("menu_manual_update"))
    settings_menu.entryconfig(2, label=t("menu_auto_update"))

    if not project_loaded:
        Filename_label.config(text=t("no_project"))
        status_var.set(t("status_ready"))

    update_wraps()


def apply_selection_mode_ui():
    """Show simplified or legacy label options based on settings."""
    use_legacy = settings.get("legacy_selection", False)
    if use_legacy:
        if not legacy_options_frame.winfo_manager():
            legacy_options_frame.pack(anchor="w", fill="x")
        if selection_mode_frame.winfo_manager():
            selection_mode_frame.pack_forget()
    else:
        if not selection_mode_frame.winfo_manager():
            selection_mode_frame.pack(anchor="w", fill="x")
        if legacy_options_frame.winfo_manager():
            legacy_options_frame.pack_forget()


def change_language(new_lang):
    """Set active language and refresh UI labels."""
    global current_lang
    current_lang = new_lang
    refresh_ui_texts()


def on_lang_change(event):
    """Combobox callback for language selection."""
    val = lang_combo.get()
    if val == "Nederlands":
        change_language("nl")
    elif val == "English":
        change_language("en")
    elif val == "Español":
        change_language("es")


# ============================================================
# RESPONSIVE HELPERS
# ============================================================
def update_wraps():
    """Adjust wrap length for long text in right panel when resizing."""
    if info_label is not None and right_frame is not None:
        wrap = max(260, right_frame.winfo_width() - 40)
        info_label.config(wraplength=wrap)


def on_resize(event):
    """Root resize event: refresh dynamic wraps."""
    if event.widget is root:
        update_wraps()


# ============================================================
# GUI
# ============================================================
root = tk.Tk()
root.geometry("1180x760")
root.minsize(980, 620)
root.wm_title(t("app_title"))

# Create top menu bar.
menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label=t("menu_open_settings"), command=open_settings_window)
settings_menu.add_command(label=t("menu_manual_update"), command=run_manual_update)
settings_menu.add_command(label=t("menu_auto_update"), command=run_auto_update)
menubar.add_cascade(label=t("menu_settings"), menu=settings_menu)
root.config(menu=menubar)

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
# Contains:
# - Manual TXT file load button
# - New "Load project" button based on settings + project number
# - Current project label
# - Language selector
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

load_project_btn = tk.Button(
    top_bar,
    text=t("load_project_btn"),
    command=load_project_by_number,
    bg="#1E88E5",
    fg="white",
    font=("calibre", 11, "bold"),
    padx=15,
    pady=6
)
load_project_btn.pack(side=tk.LEFT, padx=6)

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

selection_mode_frame = tk.Frame(left_frame)
selection_mode_frame.pack(anchor="w", fill="x")

var_cabinet_markers = tk.BooleanVar(value=True)
chk_cabinet_markers = ttk.Checkbutton(selection_mode_frame, text=t("cabinet_markers"), variable=var_cabinet_markers)
chk_cabinet_markers.pack(anchor="w")

var_component_markers = tk.BooleanVar(value=True)
chk_component_markers = ttk.Checkbutton(selection_mode_frame, text=t("component_markers"), variable=var_component_markers)
chk_component_markers.pack(anchor="w")

var_terminal_markers = tk.BooleanVar(value=True)
chk_terminal_markers = ttk.Checkbutton(selection_mode_frame, text=t("terminal_markers"), variable=var_terminal_markers)
chk_terminal_markers.pack(anchor="w")

var_cable_markers = tk.BooleanVar(value=True)
chk_cable_markers = ttk.Checkbutton(selection_mode_frame, text=t("cable_markers"), variable=var_cable_markers)
chk_cable_markers.pack(anchor="w")

legacy_options_frame = tk.Frame(left_frame)
legacy_options_frame.pack(anchor="w", fill="x")

var_groep = tk.BooleanVar(value=True)
chk_groep = ttk.Checkbutton(legacy_options_frame, text=t("groepscode"), variable=var_groep)
chk_groep.pack(anchor="w")

var_onderdelen = tk.BooleanVar(value=True)
chk_onderdelen = ttk.Checkbutton(legacy_options_frame, text=t("onderdelen_norm"), variable=var_onderdelen)
chk_onderdelen.pack(anchor="w")

var_onderdelen_lpc = tk.BooleanVar(value=False)
chk_onderdelen_lpc = ttk.Checkbutton(legacy_options_frame, text=t("onderdelen_lpc"), variable=var_onderdelen_lpc)
chk_onderdelen_lpc.pack(anchor="w")

var_onderdelen_lbl = tk.BooleanVar(value=False)
chk_onderdelen_lbl = ttk.Checkbutton(legacy_options_frame, text=t("onderdelen_label"), variable=var_onderdelen_lbl)
chk_onderdelen_lbl.pack(anchor="w")

var_onderdelen_tw = tk.BooleanVar(value=False)
chk_onderdelen_tw = ttk.Checkbutton(legacy_options_frame, text=t("onderdelen_tech"), variable=var_onderdelen_tw)
chk_onderdelen_tw.pack(anchor="w")

var_legends = tk.BooleanVar(value=True)
chk_legends = ttk.Checkbutton(legacy_options_frame, text=t("legends"), variable=var_legends)
chk_legends.pack(anchor="w")

lbl_klemmen_section = tk.Label(legacy_options_frame, text=t("klemmen_section"), font=('calibre', 10, 'bold'), fg="#2E86AB")
lbl_klemmen_section.pack(anchor="w", pady=(12, 2))

var_klemmenstrook = tk.BooleanVar(value=True)
chk_klemmenstrook = ttk.Checkbutton(legacy_options_frame, text=t("klemmenstrook"), variable=var_klemmenstrook)
chk_klemmenstrook.pack(anchor="w")

var_klemmen = tk.BooleanVar(value=True)
chk_klemmen = ttk.Checkbutton(legacy_options_frame, text=t("klemmen_los"), variable=var_klemmen)
chk_klemmen.pack(anchor="w")

lbl_kabels_section = tk.Label(legacy_options_frame, text=t("kabels_section"), font=('calibre', 10, 'bold'), fg="#2E86AB")
lbl_kabels_section.pack(anchor="w", pady=(12, 2))

var_kab10 = tk.BooleanVar(value=True)
chk_kab10 = ttk.Checkbutton(legacy_options_frame, text=t("kabels_0_10"), variable=var_kab10)
chk_kab10.pack(anchor="w")

var_kab100 = tk.BooleanVar(value=True)
chk_kab100 = ttk.Checkbutton(legacy_options_frame, text=t("kabels_10_100"), variable=var_kab100)
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

# Load settings and initialize wrapping after first draw.
load_settings_from_disk()
apply_selection_mode_ui()
root.after(100, update_wraps)

root.mainloop()
