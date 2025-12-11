
# Single File Project 

This is a minimalist, single-file Django application (`project_file.py`) that demonstrates advanced framework features—such as Forms, CSRF protection, and Template rendering—without the overhead of a standard multi-directory Django project.

It serves as a lightweight template for rapid prototyping, micro-tools, or learning the core mechanics of Django internals.

## Features

  * **Zero Boilerplate:** No `manage.py`, `settings.py`, or `urls.py` files.
  * **Self-Contained Configuration:** All Django settings are configured inline.
  * **Built-in Forms:** Includes a functional contact form with server-side validation.
  * **Template Rendering:** Renders HTML directly from a string variable with full template tag support (`{% if %}`, `{{ variable }}`).
  * **Security:** Fully configured **CSRF protection** and Session middleware.

## Prerequisites

  * Python 3.8+
  * Django 3.0+ (Tested on Django 5.x)

## Installation & Usage

1.  **Clone or Copy:**
    Copy the code into a new file named `project_file.py`.

2.  **Install Django:**

    ```bash
    pip install django
    ```

3.  **Run the Application:**
    Execute the file directly using Python. It acts as its own management utility.

    ```bash
    python project_file.py runserver
    ```

4.  **Access the App:**
    Open your web browser and navigate to:
    `http://127.0.0.1:8000/`

## Code Structure

The file `project_file.py` is organized into 5 clear sections:

1.  **Settings:** Configures `DEBUG`, `SECRET_KEY`, `TEMPLATES`, and `MIDDLEWARE`.
2.  **Forms:** Defines a standard Django `ContactForm` class.
3.  **Templates:** Contains the `HTML_TEMPLATE` string with CSS and Django tags.
4.  **Views:** The `form_view` function handles GET/POST requests and validation logic.
5.  **Runner:** The `if __name__ == "__main__":` block initializes the WSGI app and command-line execution.

## Customization

  * **Change the Port:**
    ```bash
    python project_file.py runserver 8080
    ```
  * **Add Database Support:**
    Uncomment or add the `DATABASES` dictionary in the `settings.configure` block to use SQLite or PostgreSQL.

---