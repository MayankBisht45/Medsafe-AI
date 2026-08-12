# MedSafe AI: AI-Powered Healthcare Safety & Preventive Awareness Platform

MedSafe AI is an interactive, local-first healthcare safety and preventive awareness platform built with Python and Streamlit. The application helps users understand medicine interactions, extract structured details from prescriptions, and assess symptom risk levels through a unified, modular dashboard.

---

> **ETHICAL AI DISCLAIMER**  
> MedSafe AI is designed strictly as an educational and preventive awareness tool. It DOES NOT provide professional medical diagnosis, treatment, or clinical advice.

---

## Key Features

### 1. Scenario 1: Medicine Interaction Analysis
- **RapidFuzz Matching:** Resolves typos and brand names (e.g., "Aspirne" -> "Aspirin").
- **Rule Engine:** Flags drug-drug interactions against a local JSON database.
- **LLaMA 3 Guidance:** Connects via Ollama to generate plain-language explanations of potential side effects and safety risks.

### 2. Scenario 2: Prescription OCR & AI Structuring
- **Tesseract OCR Integration:** Extracts raw text from uploaded printed or written prescription images.
- **JSON Information Parsing:** LLaMA 3 parses unstructured OCR output into clean JSON format (Medication Name, Dosage, Frequency) rendered as a table.

### 3. Scenario 3: Symptom Guidance & Emergency Risk Assessment
- **Rule-Based Emergency Scoring:** Scans user symptoms for critical "red-flag" terms (e.g., chest pain, breathing difficulty) to output a 1-10 Emergency Risk Score.
- **AI Educational Support:** Generates non-definitive possible causes, comfort measures, and emergency warning signs.

---

## Architecture & Tech Stack

### System Flow

    [ Streamlit UI Shell ]
           |
           +-- Scenario 1: [ RapidFuzz ] ---> [ Local DB ] ---> [ Ollama / LLaMA 3 ]
           +-- Scenario 2: [ Tesseract OCR ] -----------------> [ Ollama / LLaMA 3 ]
           +-- Scenario 3: [ Rule Engine ] -------------------> [ Ollama / LLaMA 3 ]

### Technologies Used

| Category | Technology |
| :--- | :--- |
| Frontend | Streamlit |
| Backend Logic | Python 3.10+ |
| OCR Engine | Tesseract OCR & PyTesseract |
| String Matching | RapidFuzz |
| AI Engine | LLaMA 3 running locally via Ollama |
| Data Persistence | JSON-based local database |

---

## Quick Start & Installation

### 1. Install System Prerequisites
- Python 3.10 or higher installed.
- Tesseract OCR installed on your operating system (Ensure `pytesseract.tesseract_cmd` path is configured in `ocr_engine.py`).

### 2. Install & Setup Local LLaMA 3 Model (Ollama)
1. Download and install Ollama from [https://ollama.com](https://ollama.com)
2. Open your terminal or Command Prompt and run:

    ollama run llama3

   *This downloads and runs the LLaMA 3 model locally as a background service listening on port 11434.*

### 3. Setup Python Virtual Environment
Create the project folder and navigate into it:

    mkdir medsafe_ai
    cd medsafe_ai

Set up the virtual environment:

    python -m venv venv

Activate the virtual environment:
- **Windows (CMD):**

    venv\Scripts\activate

- **Windows (PowerShell):**

    .\venv\Scripts\Activate.ps1

- **macOS / Linux:**

    source venv/bin/activate

### 4. Install Python Dependencies

    pip install streamlit rapidfuzz pytesseract pillow ollama pandas

### 5. Run Application

    streamlit run app.py

Open your web browser and navigate to `http://localhost:8501`

---

## Project File Structure

    medsafe_ai/
    ├── app.py              # Main Streamlit UI application
    ├── matcher.py          # RapidFuzz logic & interaction detection
    ├── ocr_engine.py       # Tesseract OCR processing module
    ├── llm_engine.py       # Local Ollama / LLaMA 3 integration
    ├── README.md           # Project documentation
    └── data/
        └── medicines.json  # Local drug registry and interaction database