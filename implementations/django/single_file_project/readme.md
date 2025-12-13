# Single File Django Project 

This is a minimalist, single-file Django application (`project_file.py`) that demonstrates **advanced framework features** and **full persistence** without the boilerplate of a standard multi-directory Django project.

It serves as a lightweight template for rapid prototyping, micro-tools, or a deep dive into the core mechanics of Django internals.

## Features

* **Zero Boilerplate:** No separate `manage.py`, `settings.py`, `urls.py`, or `models.py` files.
* **Self-Contained Configuration:** All Django settings, including `INSTALLED_APPS` and `MIDDLEWARE`, are configured inline.
* **Database Persistence (ORM):** Includes a functional `Item` model, managed by the Django ORM and an SQLite database file (`mydatabase.sqlite3`).
* **Full Admin Interface:** Access the standard Django Admin at `/admin/`, complete with correct static file styling.
    * **Default Superuser:** `admin` / `admin` (created automatically on first run).
* **Forms & Views:** Includes a data submission form (`ContactForm`) and powerful search functionality.
* **Dynamic Filtering:** Implements model-based search on the homepage using Django's `Q` objects.
* **Template Rendering:** Renders HTML directly from a string variable (`HTML_TEMPLATE`) with full template tag support.
* **Security:** Fully configured **CSRF protection**, Session, and Authentication middleware.

## Prerequisites

* Python 3.8+
* Django 4.0+ (Tested on Django 5.x)

## Installation & Usage

1.  **Clone or Copy:**
    Copy the provided code into a new file named `project_file.py`.

2.  **Install Django:**

    ```bash
    pip install django
    ```

3.  **Run the Application:**
    Execute the file directly using Python. It handles system migrations and creates the superuser automatically.

    ```bash
    python project_file.py runserver
    ```

4.  **Access the App:**
    | Location | Description |
    | :--- | :--- |
    | `http://127.0.0.1:8000/` | Main data submission form and filtered list. |
    | `http://127.0.0.1:8000/admin/` | Administration interface (Login: `admin` / `admin`). |

## Key Implementation Details

The core challenge in this single-file setup is ensuring all Django components are initialized in the correct order.

* **Bootstrapping:** The `settings.configure()` and `django.setup()` calls must execute before any app models or modules (like `User` or `staticfiles_urlpatterns`) are imported or accessed.
* **Static Files:** Static serving for the Admin panel is enabled by conditionally appending `staticfiles_urlpatterns()` to the `urlpatterns` list inside the `if __name__ == "__main__":` block.
* **Database:** A simple `initialize_database()` utility uses the `connection.schema_editor` to create the custom `Item` table without relying on Django's multi-step migration process.

## Customization

* **Change the Port:**
    ```bash
    python project_file.py runserver 8080
    ```
* **Create a Custom User:**
    Modify the `create_initial_user()` function to change the default username, password, or email address.

---