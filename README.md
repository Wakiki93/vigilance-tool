# API Breaking Change Risk Vigilance Tool

A Python tool that compares two OpenAPI specifications, identifies changes, and scores the risk of those changes on a 1-10 scale.

**✨ Now with a Web UI!** Perfect for product managers and non-technical users.

## Installation

1.  **Clone the repository** or download the source.
2.  **Install dependencies**:
    ```bash
    git clone https://github.com/Wakiki93/vigilance-tool.git
cd vigilance-tool
pip install -r requirements.txt

    ```

2.  **One-Click Setup & Demo (Windows)**:
    *   Double-click `run_demo.bat`.
    *   This will install dependencies and run a sample test automatically.

3.  **One-Click Setup & Demo (Linux/Mac)**:
    *   Run `bash run_demo.sh` in your terminal.

4.  **Manual Install**:
    ```bash
    pip install -r requirements.txt
    ```

## Testing & QA

Run the automated test suite (Unit Tests + Linting):

```bash
python src/qa.py
```

## Usage

### 🌐 Web Interface (Recommended for Product Managers)

The easiest way to use the tool is through the web interface:

1. **Start the web server:**
   ```bash
   python web_app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

3. **Upload and analyze:**
   - Upload your old specification file
   - Upload your new specification file
   - Click "Analyze Changes"
   - View your risk assessment with a beautiful, easy-to-understand interface!

The web UI provides:
- 📊 Visual risk score display
- 📋 Clear, actionable recommendations
- 🔄 Detailed list of all detected changes
- 📱 Mobile-friendly responsive design
- ✨ No technical knowledge required!

### 💻 Command Line Interface (For Developers)

Run the tool from the command line by providing the paths to the "old" (base) and "new" (head) OpenAPI specification files (YAML or JSON).

```bash
python -m src.main --old path/to/old_spec.yaml --new path/to/new_spec.yaml
```

### Options

*   `--old`: Path to the original OpenAPI specification file (Required).
*   `--new`: Path to the new OpenAPI specification file (Required).
*   `--output`: (Optional) Path to save the report (e.g., `report.txt`). If omitted, prints to console.

## Interpreting the Score

*   **1-3 (Low Risk)**: Routine changes (e.g., adding optional fields). Safe to merge.
*   **4-6 (Medium Risk)**: Requires careful review (e.g., deprecations).
*   **7-10 (High Risk)**: Critical changes (e.g., removing endpoints). Requires multiple reviewers and rigorous testing.
