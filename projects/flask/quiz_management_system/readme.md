

# Flask Quiz Management System 

A professional, full-stack Quiz Engine built with **Flask** and **SQLAlchemy**. This system demonstrates role-based access control (RBAC), real-time state persistence, and automated grading.

## Core Functionalities

* **Role-Based Access Control (RBAC):** Distinct workflows for **Admins** (content creators) and **Students** (examinees).
* **Persistent Quiz Sessions:** Uses a "Sync-on-Click" mechanism to save progress; if a student refreshes or loses connection, they resume exactly where they left off.
* **Timed Examination Engine:** Server-side time enforcement prevents tampering with client-side timers.
* **Dynamic UI (SPA Lite):** Uses asynchronous `Fetch API` to load questions and submit answers without full page reloads.

---

## Project Structure

```text
quiz_system/
├── src/                    # All core Python logic goes here
│   ├── app.py              # Central Controller (Routes & API)
│   ├── models.py           # Data Architect (SQLAlchemy Models)
│   └── seed.py             # Data Injector (Setup Script)
├── static/                 # Assets served to the client
│   ├── js/
│   │   └── spa_engine.js   # Frontend Logic (DOM & Fetch)
│   └── css/
│       └── style.css       # [Add this] For custom styling
├── templates/              # HTML View Layer  
│   ├── admin_create.html     # Quiz creation interface
│   ├── admin_dashboard.html  # Admin dashboard
│   ├── admin_stats.html      # Quiz statistics report
│   ├── auth.html             # Login/Registration entry
│   ├── engine.html           # Active Quiz display
│   ├── gallery.html          # Quiz selection menu
│   └── register.html         # Public registration
├── instance/               # Flask-specific instance folder
│   └── quiz.db             # The SQLite Database
├── .gitignore              # Ignore file list
├── requirements.txt        # Dependencies
└── README.md               # Professional Documentation

```

---

## Database Architecture

The system uses a relational schema to handle complex many-to-many relationships between users, quizzes, and specific responses.

| Model | Responsibility | Key Fields |
| --- | --- | --- |
| **User** | Identity Management | `username`, `password_hash`, `role` |
| **Quiz** | Content Metadata | `time_limit`, `max_attempts`, `passing_score` |
| **Question** | Content Body | `text`, `points`, `quiz_id` (FK) |
| **Attempt** | Session Tracking | `start_time`, `status` (Started/Completed), `final_score` |
| **Response** | Data Persistence | `attempt_id`, `question_id`, `selected_option_id` |

---

## API Authentication

### Authentication API

* **`POST /login`**: Authenticates user credentials and establishes a secure, encrypted session cookie.
* **`POST /register`**: Persists a new user identity to the database using one-way password hashing for security.
* **`GET /logout`**: Terminates the active session and redirects the user to the entry portal.

### Student & Exam API

* **`GET /api/quiz/<id>/start`**: Validates eligibility and initializes a new attempt record with a server-side start timestamp.
* **`GET /api/quiz/<id>/questions`**: Fetches the specific question set and previously saved responses for a persistent testing experience.
* **`POST /api/sync`**: Persists every user selection to the database immediately to prevent data loss during network interruptions.
* **`POST /api/submit`**: Closes the attempt, performs server-side grading, and archives the final score.

### Administrative & Management API

* **`POST /admin/create-quiz`**: Transforms JSON configuration payloads into relational database entries for quizzes and questions.
* **`DELETE /admin/quiz/<id>`**: Executes a cascading deletion to remove a quiz and all associated student performance data.
* **`GET /admin/api/live-monitor`**: Provides a real-time snapshot of all currently active examination sessions across the system.
* **`GET /admin/api/stats/<quiz_id>`**: Aggregates raw attempt data into actionable insights like average scores and question difficulty metrics.

---

## Technical Implementation Details

- **Secure Server-Side Grading**: The system isolates grading logic within the backend, calculating scores via a relational join between `Response` and `Option` tables to prevent client-side data tampering.
- **Stateless Time Enforcement**: Remaining time is calculated dynamically as $$T_{remaining} = (Quiz_{limit} \times 60) - (T_{now} - T_{started\_at})$$, with the server rejecting any `POST` requests once the limit is exceeded.
- **Atomic Response Syncing**: Every selection triggers an asynchronous "Upsert" operation via the `/api/sync` endpoint, ensuring real-time data persistence and session recovery across network interruptions.
- **LAN-Optimized Deployment**: The application is configured to bind to `0.0.0.0`, enabling multi-device accessibility across a local subnet via the host’s primary IP address.

---

## Setup & Installation

1. **Clone and Install:**
```bash
pip install -r requirements.txt

```


2. **Initialize Data:**
```bash
python src/seed.py

```


3. **Run Application:**
```bash
python src/app.py

```
