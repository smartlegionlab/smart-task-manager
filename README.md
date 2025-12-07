# Smart Task Manager <sup>v1.1.1</sup>

A modern desktop task management application built with Python and PyQt5, featuring an 
intuitive dark theme interface, priority-based organization, and automatic data persistence.

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-task-manager)](https://github.com/smartlegionlab/smart-task-manager)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-task-manager)](https://github.com/smartlegionlab/smart-task-manager/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-task-manager)](https://github.com/smartlegionlab/smart-task-manager/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-task-manager?style=social)](https://github.com/smartlegionlab/smart-task-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-task-manager?style=social)](https://github.com/smartlegionlab/smart-task-manager/network/members)

---

## 📋 Overview

**Smart Task Manager** is a feature-rich desktop application designed to help you 
efficiently organize and track your tasks. With a clean dark-themed interface, 
priority management, due date tracking, and automatic saving, it's the perfect tool for personal productivity.

---

## ✨ Features

### 📝 Task Management
- **Create tasks** with title, description, priority, and due date
- **Edit tasks** anytime with full detail modification
- **View task details** in a dedicated dialog
- **Delete tasks** individually or clear completed tasks in bulk

### 🎯 Priority System
- **Three priority levels**: 🚨 High, ⚠️ Medium, 📋 Low
- **Color-coded visual indicators** for quick identification

### ✅ Task Status
- **Toggle completion status** with one click
- **Visual strikethrough** for completed tasks
- **Overdue task highlighting** (red text for overdue items)

### 📊 Data Management
- **Automatic saving** to `~/.todos.json`
- **Persistent storage** between sessions
- **JSON-based data format** for easy backup and migration
- **Statistics tracking** (total, completed, pending tasks)

### 🖥️ User Interface
- **Dark theme** with modern styling
- **Responsive table layout** with resizable columns
- **Context menu** for quick actions (right-click on tasks)
- **Task statistics** displayed in real-time

### 🎨 Additional Features
- **Due date calendar picker** with visual date selection
- **Task descriptions** with word wrap
- **Overdue task notifications** (visual indicators)
- **Help documentation** built into the application
- **Confirmation dialogs** for destructive actions

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- PyQt5

### Step-by-Step Installation

1. **Clone the repository**
```bash
git clone https://github.com/smartlegionlab/smart-task-manager.git
cd smart-task-manager
```

2. **Install required dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python task_manager.py
```

### Alternative: One-line Installation
```bash
git clone https://github.com/smartlegionlab/smart-task-manager.git && cd smart-task-manager && pip install PyQt5 && python task_manager.py
```

---

## 📖 Usage Guide

### Creating a New Task
1. Click the **"➕ Add Task"** button
2. Fill in the task details:
   - **Title** (required): Brief description of the task
   - **Description** (optional): Detailed notes
   - **Priority**: Select from High, Medium, or Low
   - **Due Date**: Choose from the calendar picker
3. Click **"Create Task"**

### Managing Tasks
- **Toggle Completion**: Click the status button (⏳/✅)
- **View Details**: Click the "👁 View" button
- **Edit Task**: Click the "✏️ Edit" button
- **Delete Task**: Click the "🗑️" button

### Quick Actions (Context Menu)
Right-click on any task in the table to access:
- Mark as Complete/Pending
- Edit Task
- View Details
- Delete Task

### Bulk Operations
- **Clear Completed Tasks**: Click "🗑️ Clear Completed" to remove all completed tasks
- **Exit Confirmation**: Application warns if unsaved tasks exist on exit

---

## 🗂️ Data Storage

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

## 📦 Windows Standalone Executable

### Creating a Single-File *.exe

Build a standalone `smart_task_manager.exe` that runs without Python installation:

#### Step 1: Get the Project Files
1. **Download project ZIP:**
   - Go to: https://github.com/smartlegionlab/smart-task-manager
   - Click green "Code" button
   - Select "Download ZIP"
   - Extract to: `C:\smart-task-manager\`

2. **Or clone with git (if installed):**
   ```cmd
   git clone https://github.com/smartlegionlab/smart-task-manager.git
   cd smart-task-manager
   ```

#### Step 2: Install Python
1. Download Python installer from: https://python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check ✅ "Add Python to PATH"
4. Click "Install Now"

#### Step 3: Open Command Prompt
1. Press `Win + R`
2. Type `cmd`, press Enter
3. Navigate to project folder:
   ```cmd
   cd C:\smart-task-manager
   ```

#### Step 4: Create Virtual Environment
```cmd
# Create virtual environment
python -m venv venv

# Activate it (IMPORTANT!)
.\venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### Step 5: Install Dependencies
```cmd
# Install PyInstaller in virtual environment
pip install pyinstaller
pip install PyQt5==5.15.9
```

#### Step 6: Build Executable
```cmd
# Build single .exe file

pyinstaller --onefile --windowed --name "smart_task_manager.exe --additional-hooks-dir=. app.py

# Wait for build to complete (1-2 minutes)
```

#### Step 7: Find and Use
**Location:** `C:\smart-task-manager\dist\smart_task_manager.exe`

**Create desktop shortcut:**
1. Open `C:\smart-task-manager\dist\` folder
2. Right-click `smart_task_manager.exe`
3. Select "Create shortcut"
4. Drag shortcut to desktop
5. Rename shortcut to "Smart Task Manager"
6. Double-click to start


**What you get:**
- Single file: `smart_task_manager.exe` (~50MB)
- No Python required to run
- Works on any Windows 10/11 PC
- Can be copied to USB drive

---

## 🛠️ Technical Details

### Architecture
- **Model**: `Task` class representing individual tasks
- **Controller**: `TaskManager` handling data persistence and operations
- **View**: PyQt5-based GUI with dialog windows and table view

### Key Components
- **MainWindow**: Primary application interface with task table
- **TaskInputDialog**: Modal dialog for creating/editing tasks
- **TaskDisplayDialog**: Modal dialog for viewing task details
- **Context Menu**: Right-click menu for quick task operations

### Dependencies
- **PyQt5**: GUI framework
- **Python Standard Library**: json, os, uuid, datetime, typing

---

## 🎨 Screenshots

![Main Interface](https://github.com/smartlegionlab/smart-task-manager/raw/master/data/images/smart-task-manager.png)

---

## 🔧 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'PyQt5'"**
   ```bash
   pip install PyQt5
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

## 📄 License

This project is licensed under the **BSD 3-Clause License** - see the [LICENSE](LICENSE) file for details.

```text

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

```

---

## 👤 Author

**Alexander Suvorov**
- GitHub: [@smartlegionlab](https://github.com/smartlegionlab)
- Project: [Smart Task Manager](https://github.com/smartlegionlab/smart-task-manager)

---

## 🌟 Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by modern task management applications

---

*"Organize your tasks, simplify your life."*
