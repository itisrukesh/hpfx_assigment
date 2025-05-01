# hpfx_assignment

A standalone python application that integrates with Gmail API and performs some rule based operations on emails.

# Gmail-API Rule Engine -- Mail Processing

The project scripts connects to the Gmail API, fetches emails, and applies user-defined rules to automate actions like labeling and marking as read.
It logs the entire process and maintains full traceability of rule applications in a local database.

Built with **Python**, the project is designed using **SOLID principles**, tested with **unit + integration tests** in test/ folder, and includes logging, environment configs, and a modular structure for long-term maintainability.

---

## Features

- Connects securely to Gmail API via OAuth2
- Fetches and stores email metadata in a local SQLite DB
- Loads rules from `rules.json` to match emails by fields (e.g., sender, subject)
- Supports match predicates: `Contains`, `Does Not Contain`, `Equals`.
- Processes rule actions: `mark_as_read`, `move_to_label:<label_name>` [Supports both predefined & customized GMAIL LABELS]
- Stores rule application history. (for rollbacks, traces of matched emails, rules)
- Modular code structure using Single Responsibility principle
- `.env`-driven config and `.logs/` for traceable logging

---

## 📁 Project Structure

```bash
    📁 hpfx_assignment/
    ├── main.py                    # Entry point for running the pipeline
    ├── auth.py                    # Handles Gmail authentication (OAuth2)
    ├── config.py                  # Loads and validates .env configuration
    ├── db.py                      # SQLite table creation, basic DB operations, inserts emails and rule history into the DB
    ├── fetchEmail.py              # Fetches emails via Gmail API and parses metadata
    ├── ruleEngine.py              # Core rule processing logic
    ├── rules.json                 # List of rules to apply to emails
    ├── logger.py                  # Central logger setup (console + .logs/app.log)
    ├── requirements.txt           # Python dependencies
    ├── .env                       # Environment variables (user-defined)
    ├── .gitignore                 # Git exclusions (credentials, tokens, logs, etc.)
    ├── .logs/
    │   └── date_app.log           # Automatically generated runtime logs
    └── tests/                     # Unit and integration tests
        ├── test_auth.py
        ├── test_rule_engine.py
        ├── test_integrationRuleEngine.py
        └── ...
```

---

## ⚙️ Setup Instructions

### 1. 📥 Clone & Install Requirements

```bash
git clone https://github.com/itisrukesh/hpfx_assigment.git
cd hpfx_assigment
python -m venv env
source env/bin/activate   # or env\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### 2. ⚙️ Setup Instructions

📄 Create a .env File

```bash
CREDSFILE="credentials.json" (your-credentials.json-filepath)
TOKENFILE="token.json" (your-token.json-filepath)
DEBUG="False"
PORTVAL=8080
SCOPESVAl="https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly"
DBFILEVAL="usermails.db"
EMAILSTABLEVAL="emails"
HISTORYTABLEVAL='processing_history'
```

### 3. 🧠 Sample Rule File (rules.json)

Similarly you can create your own rules.json with mentioned fields.

```bash
[
  {
    "rule_id": "Rid001",
    "description": "Ignore Promotions",
    "predicate": "All",
    "conditions": [
      {"field": "sender", "predicate": "Contains", "value": "noreply@"}
    ],
    "actions": ["mark_as_read", "move_to_label:PROMOTIONS"]
  }
]
```

### 4. 🔐 Set Up Gmail OAuth credentials.json

📌 This file is not included. You must generate your own.
Follow these steps:

```bash
-- Visit Google Cloud Console: [link](https://developers.google.com/workspace/gmail/api/guides)

-- Create or select a project

-- Enable Gmail API

-- Go to APIs & Services → Credentials

-- Click Create Credentials → OAuth Client ID

-- Choose Desktop App, give it a name

-- Download the file and rename it to credentials.json

-- Place it in your project root (next to main.py)
```

## 5. 📧 Run Script - Process Emails!

Once Completion of All setup now you can Run Scripts. In terminal: Use following command!

```bash
python main.py
```
