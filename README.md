# Eplan Label Tool

A professional desktop application for automating label generation in electrical engineering projects. This tool simplifies the workflow for creating and managing labels for cabinets, components, terminals, and cables in EPLAN projects.

**Original Creator:** Wolfs-TS  
**Improved by:** Lira Sobrino Rodríguez

## Overview

The Eplan Label Tool provides a user-friendly graphical interface to streamline label generation for electrical designs. It integrates with MPrintPRO to automate the printing workflow, reducing manual effort and improving consistency across projects.

### Key Features

- **Multi-Language Support:** Full interface support for Dutch, English, and Spanish
- **Project Management:** Load projects by folder selection or project number
- **Intelligent File Detection:** Automatically identifies and classifies EPLAN text files
- **Panel Filtering:** Detect and filter specific panels/cabinets from source data
- **Automatic Data Cleaning:** Removes empty markers and blank lines automatically
- **Dual Selection Modes:** Toggle between simplified and legacy label selection interfaces
- **Persistent Settings:** Save and restore configuration preferences
- **Responsive UI:** Adaptive layout that adjusts to window resizing
- **Status Monitoring:** Real-time indicators showing loaded file types

## Supported Label Types

The tool supports generation for multiple label categories:

- **Cabinet & Component Labels:** Group codes, parts (normal/LPC/technical), legends
- **Terminal Labels:** Terminal strips, individual terminals
- **Cable Labels:** Cables 0-10mm, cables 10-100mm

### Selection Modes

1. **Simplified Mode** (Default)
   - Cabinet markers (group codes + legends)
   - Component markers (parts)
   - Terminal markers (strips + terminals)
   - Cable markers (all cable types)

2. **Legacy Mode**
   - Individual checkboxes for each label type
   - Fine-grained control over exact label generation options
   - Enable in Settings

## Getting Started

### Requirements

- Python 3.x
- Tkinter (usually included with Python)
- MPrintPRO (Weidmüller) installed for label printing
- EPLAN projects with standard folder structure

### Installation

1. Clone or download the repository
2. Ensure Python 3 is installed
3. Run the application:
   ```bash
   python3 main.py
   ```

### Project Structure

The tool expects projects organized as follows:

```
Main Project Folder/
└── ProjectNumber_Name/
    └── Tekeningen/
        └── R###/ (revision folder)
            └── labels/
                ├── GROEPSCODE_*.txt
                ├── ONDERDELEN_*.txt
                ├── KLEMMENSTROOK_*.txt
                ├── KLEMMEN_*.txt
                ├── KABELS_*.txt
                └── LEGENDS_*.txt
```

## Usage

### Basic Workflow

1. **Configure Settings** (First time only)
   - Open Settings menu
   - Set the main project folder path
   - Save configuration

2. **Load a Project**
   - Click "📁 Load project folder (TXT)" to manually select files, OR
   - Click "🔎 Load project" to load by project number
   - Files are automatically detected and classified

3. **Select Label Types**
   - Check boxes for desired label categories
   - Review detected panels on the right panel

4. **Filter Panels (Optional)**
   - Enable "Apply filter" checkbox
   - Select specific panels from the list
   - Selected panels will be included in export

5. **Generate Labels**
   - Click "▶ GENERATE SELECTED LABELS"
   - MPrintPRO processes will launch automatically
   - Confirmation dialog shows number of processes started

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Load project folder |
| `F5` | Detect/Refresh panels |
| `Enter` | Generate labels |

## Configuration

Settings are stored in `settings.json` next to `main.py`:

```json
{
  "main_project_folder": "/path/to/projects",
  "legacy_selection": false
}
```

- **main_project_folder:** Root directory containing all EPLAN projects
- **legacy_selection:** Enable/disable legacy UI mode

## Features in Detail

### Automatic Data Cleaning

The tool automatically filters:
- Empty lines
- Blank marker rows (lines containing only semicolons)
- Lines with minimal content

### Panel Detection

Panels are automatically extracted from the Groepscode file. The detector:
- Reads unique panel identifiers
- Filters entries by length (2-25 characters)
- Sorts alphabetically for easy browsing
- Selects all detected panels by default

### File Detection Logic

Files are classified by filename keywords:
- **GROEPSCODE:** Group code labels
- **ONDERDEEL:** Component labels
- **KLEMMENSTROOK:** Terminal strip labels
- **KLEMMEN:** Individual terminal labels
- **KABELS:** Cable labels
- **LEGENDS:** Legend labels

### MPrintPRO Integration

The tool supports two printing modes:
- **Standard Mode:** Opens MPrintPRO with import filter
- **Direct Print Mode:** Prints immediately without preview

## Status Indicators

Color-coded file status shows at the top of the window:
- 🟢 Green (✓): File found and loaded
- 🔴 Red (✗): File not found

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Main project folder missing" | Open Settings and configure the main project folder |
| "Project not found" | Verify project folder name starts with entered number |
| "No revision folders found" | Check Tekeningen folder contains R### subdirectories |
| "Labels folder missing" | Verify R### folder contains a labels subfolder |
| "No usable TXT files" | Ensure files follow EPLAN naming conventions |
| Empty filter results | Not all selected panels exist in source file |

## Supported File Formats

- **Input:** UTF-8 encoded text files (.txt) with semicolon-delimited data
- **Output:** Temporary filtered files in system TEMP directory
- **Filter Scripts:** .mis (MPrintPRO import scripts)

## License

Original tool by Wolfs-TS. Improvements and UI enhancements by Lira Sobrino Rodríguez.

## Support

For issues, questions, or suggestions, please refer to the repository issues section.
