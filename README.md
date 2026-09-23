# Bookky — Receipt Management & Expense Tracker

**Bookky** is a Python CLI-based receipt and expense management system for storing, organizing, filtering, and exporting transaction records for personal bookkeeping and small-business accounting.

The project is being developed progressively as I learn Python, with each phase introducing new functionality and concepts.

---

## Project Progress

### Phase One — Foundation

The first version focused on building the core receipt management system using Python data structures.

**Features:**

* Add receipts
* View all receipts
* View a single receipt
* Delete a single receipt
* Delete all receipts
* Custom receipt ID generation (`RN0001`, `RN0002`, etc.)
* In-memory storage using Python `lists` and `dicts`

> **Note:** Data from Phase One was only available while the application was running.

---

### Phase Two — Persistence, Filtering & Export

Phase Two upgraded Bookky from a temporary in-memory application into a **persistent and more flexible bookkeeping tool**.

#### Persistent Storage

* Receipt data is stored locally in `./data/receipts.json`.
* Added `load_receipts()` and `save_receipts()` functions for reading and writing receipt data.
* Receipt records remain available after closing and restarting the application.
* Uses Python's `json` and `os` modules for file and data management.

#### Viewing & Filtering

Receipts can now be filtered and viewed by:

* **Month & Year**
* **Year**
* **Business Name**

Bookky dynamically generates business-selection menus and uses Python's `datetime` module to process receipt dates.

#### Data Export

Bookky can export receipt records directly to the user's default `~/Downloads` folder.

Supported formats:

* **CSV**
* **JSON**

Exports can contain either the **complete receipt collection** or a **filtered selection**.

Export filenames include timestamps to prevent accidental overwriting:

```text
receipts_export_20260923_165324.csv
```

---

## Project Structure

```text
bookky/
├── data/
│   ├── messages.py          # Terminal messages and menu prompts
│   └── receipts.json        # Persistent receipt storage
│
├── utilities/
│   ├── choice_maker.py      # Input validation and selection helpers
│   └── receipt_helper.py    # Receipt management, filtering and export logic
│
├── main.py                  # CLI application entry point
└── README.md                # Project documentation
```

---

## Technologies & Concepts

* **Python**
* Lists & Dictionaries
* Functions & Modules
* File Handling
* JSON
* CSV
* `datetime`
* Input Validation
* Filtering & Data Processing

---

