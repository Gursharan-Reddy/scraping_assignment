## 1. AI Tools Used
* **Assistant**: Google Gemini 
* **Role**: Supplementary coding reference and syntax check assistant

---

## 2. Purpose of AI Assistance
AI was used in a limited capacity for minor reference tasks during development, including:
* **Boilerplate & Syntax Checks**: Reviewing standard library patterns for `pathlib`, `logging`, and `csv` module configuration.
* **Regular Expressions**: Double-checking regex patterns for numeric price extraction (`£51.77` → `51.77`).
* **Test Structure**: Confirming standard test syntax for `pytest`.

All core architecture design, CSS selector inspection via DevTools, cleaning logic implementation, validation rules, and error-handling strategies were designed, written, and debugged independently.

---

## 3. Representative Prompts
* *"What is the standard regular expression pattern to extract a decimal price from a currency string in Python?"*
* *"Show the basic syntax structure for a parameterized pytest test function."*

---

## 4. Verification and Testing
* **Unit Testing**: Developed and executed the full test suite using `pytest tests/ -v`, verifying all 7 test cases independently.
* **Pipeline Execution**: Ran `python main.py` locally through all 50 book pages and 10 quote pages to validate live scraper behavior and pagination handling.
* **Data Reconciliation**: Manually verified the output numbers by cross-referencing `summary_report.json` against `final_dataset.csv` to ensure accurate row counts and reconciliation.