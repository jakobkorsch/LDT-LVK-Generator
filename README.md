# LDT LVK Generator

Generate LVK (Light Distribution Curve) diagrams from **EULUMDAT (.ldt)** files using Python.

The application automatically reads photometric data from an LDT file and generates:

- PNG light distribution diagram
- PDF light distribution diagram
- Interactive Streamlit interface

---

## Features

- Read EULUMDAT (.ldt) files
- Automatic detection of C-planes and Gamma angles
- Automatic extraction of photometric values (cd/klm)
- Generate LVK diagrams
- Export as PNG
- Export as PDF
- Streamlit web interface

---

## Installation

Clone the repository:

```bash
git clone https://github.com/jakobkorsch/LDT-LVK-Generator.git
cd LDT-LVK-Generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the application

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## Usage

1. Upload an **LDT (EULUMDAT)** file.
2. Click **Generate LVK**.
3. Preview the generated light distribution diagram.
4. Download the result as PNG or PDF.

---

## Technologies

- Python
- Streamlit
- NumPy
- Matplotlib

---

## Project Structure

```
app.py
lvk_generator.py
requirements.txt
example_spotlight.ldt
README.md
```

---

## Example

The repository contains a sample LDT file for testing.

---

## License

MIT License
