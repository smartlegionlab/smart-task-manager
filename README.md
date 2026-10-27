# Smart Task Manager <sup>v1.1.3</sup>

A modern desktop task management application built with Python and PyQt5, featuring an
intuitive dark theme interface, priority-based organization, and automatic data persistence.

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-task-manager)](https://github.com/smartlegionlab/smart-task-manager)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-task-manager)](https://github.com/smartlegionlab/smart-task-manager/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-task-manager)](https://github.com/smartlegionlab/smart-task-manager/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-task-manager?style=social)](https://github.com/smartlegionlab/smart-task-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-task-manager?style=social)](https://github.com/smartlegionlab/smart-task-manager/network/members)

---

## Overview

**Smart Task Manager** is a feature-rich desktop application designed to help you
efficiently organize and track your tasks. With a clean dark-themed interface,
priority management, due date tracking, and automatic saving, it's the perfect tool
for personal productivity.

---

## Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-task-manager/blob/master/DISCLAIMER.md)

---

## Features

### Task Management
- **Create tasks** with title, description, priority, and due date
- **Edit tasks** anytime with full detail modification
- **View task details** in a dedicated dialog
- **Delete tasks** individually or clear completed tasks in bulk
- **Double-click** a task row or press **Enter** to open task details

### Priority System
- **Three priority levels**: **High**, **Medium**, **Low**
- **Color-coded visual indicators** for quick identification

### Task Status
- **Toggle completion status** with one click or `Space`
- **Visual strikethrough** for completed tasks
- **Overdue task highlighting** (red text for overdue items)

### Data Management
- **Automatic saving** to `~/.todos.json`
- **Persistent storage** between sessions
- **JSON-based data format** for easy backup and migration
- **Statistics tracking** (total, completed, pending tasks)

### User Interface
- **Dark theme** with modern styling
- **Responsive table layout** with resizable columns
- **Context menu** for quick actions (right-click on tasks)
- **Task statistics** displayed in real-time
- **Menu bar** (File / Edit / View / Help) with keyboard shortcuts
- **Status bar** with live feedback
- **Compact single-row filters** (search + status + priority + due date + reset)

### Additional Features
- **Due date calendar picker** with visual date selection
- **Task descriptions** with word wrap
- **Overdue task notifications** (visual indicators)
- **Help documentation** built into the application
- **About dialog** with project information
- **Keyboard shortcuts dialog**
- **Confirmation dialogs** for destructive actions

---

## Installation

### Prerequisites
- Python 3.7 or higher
- PyQt5
- Git (only for the installer)
- curl (only for the installer)

### Option 1 - Run from Source (no system install)

```bash
git clone https://github.com/smartlegionlab/smart-task-manager.git
cd smart-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python task_manager.py
```

### Option 2 - Install System-Wide (recommended)

#### One-command install

```bash
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-task-manager/master/install.sh | bash
```

**What the installer does:**

1. Downloads the source code from GitHub.
2. Installs the application to `~/.local/share/smart-task-manager/`.
   No root, no sudo - everything lives inside your home directory.
3. Creates a dedicated Python virtual environment at
   `~/.local/share/smart-task-manager/venv/` and installs dependencies into it.
4. Registers the app in your desktop environment by creating
   `~/.local/share/applications/smart-task-manager.desktop`.
5. Refreshes the desktop database so the menu entry appears without a full
   re-login on most systems.

**Launch after install:**
- Application menu -> **Smart Task Manager**

**Desktop shortcut (opt-in):**

By default, no Desktop shortcut is created. This is intentional - on GNOME
(default on Ubuntu), desktop icons are hidden by default, which would make a
shortcut invisible and confusing.

To also create a Desktop shortcut during install, pass the
`STM_CREATE_DESKTOP_SHORTCUT=1` environment variable to **bash** - the second
command in the pipeline:

```bash
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-task-manager/master/install.sh | STM_CREATE_DESKTOP_SHORTCUT=1 bash
```

Or export it first, then run the normal installer:

```bash
export STM_CREATE_DESKTOP_SHORTCUT=1
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-task-manager/master/install.sh | bash
```

> **Note:** Writing `STM_CREATE_DESKTOP_SHORTCUT=1 curl ... | bash` does **not**
> work - in a shell pipeline, an environment variable prefix applies only to the
> command on the **left** side of the `|`. The variable never reaches `bash`,
> which is on the right side. Pass it to `bash` directly, or `export` it
> beforehand.

#### Alternative - install from a cloned repo

```bash
cd smart-task-manager
./install.sh
```

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-task-manager/master/uninstall.sh | bash
```

**What the uninstaller removes:**
- `~/.local/share/smart-task-manager/` - the application and its venv
- `~/.local/share/applications/smart-task-manager.desktop` - the menu entry
- `~/Desktop/smart-task-manager.desktop` - the Desktop shortcut (if present)

**What the uninstaller never touches:**
- `~/.todos.json` - your tasks. It is your data. Only you decide what to do with it.

If you want to remove your data as well, run after uninstall:

```bash
rm -f ~/.todos.json
```

### Installation Paths

| Item                       | Path                                                              |
|----------------------------|-------------------------------------------------------------------|
| Application files          | `~/.local/share/smart-task-manager/`                              |
| Virtual environment        | `~/.local/share/smart-task-manager/venv/`                         |
| Application menu entry     | `~/.local/share/applications/smart-task-manager.desktop`          |
| Desktop shortcut (opt-in)  | `~/Desktop/smart-task-manager.desktop`                            |
| User data (tasks)          | `~/.todos.json`                                                   |

---

## Usage Guide

### Creating a New Task
1. Click the **"+ Add Task"** button or use **File -> New Task** (`Ctrl+N`)
2. Fill in the task details:
   - **Title** (required): Brief description of the task
   - **Description** (optional): Detailed notes
   - **Priority**: Select from High, Medium, or Low
   - **Due Date**: Choose from the calendar picker
3. Click **"Create Task"**

### Managing Tasks
- **Toggle Completion**: Click the status button, or press `Space`
- **View Details**: Double-click the row, press `Enter`, or click "View"
- **Edit Task**: Click the "Edit" button, or press `Ctrl+E`
- **Delete Task**: Click the "Delete" button, or press `Delete`

### Quick Actions (Context Menu)
Right-click on any task in the table to access:
- Mark as Complete/Pending
- Edit Task
- View Details
- Delete Task

### Bulk Operations
- **Clear Completed Tasks**: Click "Clear Completed" or use **File -> Clear Completed** (`Ctrl+Shift+C`)
- **Exit Confirmation**: Application warns if unsaved tasks exist on exit

---

## Menu Bar

- **File**: Create Desktop Entry (`Ctrl+Shift+D`, Linux only), New Task (`Ctrl+N`), Clear Completed (`Ctrl+Shift+C`), Exit (`Ctrl+Q`)
- **Edit**: Edit Selected Task (`Ctrl+E`), Delete Selected Task (`Delete`), Toggle Completion (`Space`)
- **View**: Focus Search (`Ctrl+F`), Refresh (`F5`), Reset Filters (`Ctrl+R`)
- **Help**: Help (`F1`), Keyboard Shortcuts (`Ctrl+/`), About (`Ctrl+A`)

---

## Keyboard Shortcuts

| Shortcut         | Action                              |
|------------------|-------------------------------------|
| `Ctrl+N`         | New task                            |
| `Ctrl+Shift+D`   | Create desktop entry (Linux)        |
| `Ctrl+Shift+C`   | Clear completed tasks               |
| `Ctrl+Q`         | Exit application                    |
| `Ctrl+E`         | Edit selected task                  |
| `Delete`         | Delete selected task                |
| `Space`          | Toggle completion of selection      |
| `Enter`          | View details of selected task       |
| `Ctrl+F`         | Focus search box                    |
| `Ctrl+R`         | Reset filters                       |
| `F5`             | Refresh view                        |
| `F1`             | Open help                           |
| `Ctrl+/`         | Show keyboard shortcuts dialog      |
| `Ctrl+A`         | Open about dialog                   |

---

### Desktop Integration (Linux)

> **Note:** If you installed the app via `install.sh`, the application menu entry
> is already created automatically. The in-app option described below is useful
> when you run the app manually from a custom location, or when you want to add
> a Desktop shortcut on demand. It is also the recommended way for development:
> it creates a shortcut pointing to the **currently running instance** (your
> working copy), not to a copy under `~/.local/share/`.

**Creating Application Shortcuts:**

The application allows you to create desktop entries directly from the menu:

1. **Go to File -> Create Desktop Entry** (`Ctrl+Shift+D`)
2. **Choose locations:**
   - Application Menu (`~/.local/share/applications/`) - adds to system app menu
   - Desktop (`~/Desktop/`) - creates shortcut on desktop
3. **Click "Create Entry"**

**After creation:**
- **Application Menu**: log out and back in (or restart desktop) for the entry to appear
- **Desktop shortcut**: may show "Unsecured Application Launcher" warning
  - Right-click on shortcut -> "Allow Launching" or "Trust"
  - This is a one-time security confirmation

---

## Data Storage

### File Location
Tasks are automatically saved to:
```
~/.todos.json
```

### Data Format
```json
{
  "task-uuid-here": {
    "id": "uuid-string",
    "title": "Task Title",
    "description": "Task Description",
    "priority": 1,
    "completed": false,
    "created_at": "2025-12-05T10:30:00.000000",
    "due_date": "2025-12-10"
  }
}
```

### Backup & Migration
- Simply copy the `~/.todos.json` file to back up your tasks
- The JSON format is human-readable and editable

---

## Windows Standalone Executable

### Creating a Single-File *.exe

Build a standalone `smart_task_manager.exe` that runs without Python installation:

#### Step 1: Get the Project Files
1. **Download project ZIP:**
   - Go to: https://github.com/smartlegionlab/smart-task-manager-master
   - Click green "Code" button
   - Select "Download ZIP"
   - Extract to: `C:\smart-task-manager-master\`

#### Step 2: Install Python
1. Download Python installer from: https://python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"

#### Step 3: Open Command Prompt
1. Press `Win + R`
2. Type `cmd`, press Enter
3. Navigate to project folder:
   ```cmd
   cd C:\smart-task-manager-master
   ```

#### Step 4: Create Virtual Environment
```cmd
python -m venv venv
.\venv\Scripts\activate
```

#### Step 5: Install Dependencies
```cmd
pip install pyinstaller
pip install PyQt5==5.15.9
```

#### Step 6: Build Executable
```cmd
pyinstaller --onefile --windowed --name "smart_task_manager.exe" --additional-hooks-dir=. app.py
```

#### Step 7: Find and Use
**Location:** `C:\smart-task-manager-master\dist\smart_task_manager.exe`

---

## Technical Details

### Architecture
- **Model**: `Task` class representing individual tasks
- **Controller**: `TaskManager` handling data persistence and operations
- **View**: PyQt5-based GUI with dialog windows and table view

### Key Components
- **MainWindow**: Primary application interface with menu bar, filters, task table, status bar
- **TaskInputDialog**: Modal dialog for creating/editing tasks
- **TaskDisplayDialog**: Modal dialog for viewing task details
- **AboutDialog**: Project information dialog
- **HelpDialog**: Built-in help documentation
- **ShortcutsDialog**: Keyboard shortcuts reference
- **DesktopEntryDialog**: Linux desktop integration
- **Context Menu**: Right-click menu for quick task operations

### Dependencies
- **PyQt5**: GUI framework
- **Python Standard Library**: json, os, uuid, datetime, typing

---

## Screenshots

![Main Interface](https://github.com/smartlegionlab/smart-task-manager/raw/master/data/images/smart-task-manager.png)

---

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'PyQt5'"**
   ```bash
   pip install -r requirements.txt
   ```

2. **Application won't start**
   - Ensure Python 3.7+ is installed
   - Check file permissions on `~/.todos.json`

3. **Tasks not saving**
   - Verify write permissions in home directory
   - Check disk space availability

4. **UI elements look wrong**
   - Ensure all dependencies are installed
   - Try restarting the application

---

## License

This project is licensed under the **BSD 3-Clause License** - see the [LICENSE](https://github.com/smartlegionlab/smart-task-manager/blob/master/LICENSE) file for details.

---

## Author

**Alexander Suvorov**
- GitHub: [@smartlegionlab](https://github.com/smartlegionlab)
- Project: [Smart Task Manager](https://github.com/smartlegionlab/smart-task-manager)

---

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by modern task management applications

---

*"Organize your tasks, simplify your life."*

