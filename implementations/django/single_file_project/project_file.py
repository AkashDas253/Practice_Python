import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.template import Template, Context
from django.middleware.csrf import get_token
from django.forms import Form, CharField, EmailField
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# --- 1. SETTINGS ---
if not settings.configured:
    settings.configure(
        SECRET_KEY='project-secret-key',
        ROOT_URLCONF=__name__,
        DEBUG=True,
        ALLOWED_HOSTS=['*'],
        # REQUIRED: Defines the engine for rendering templates
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
        # REQUIRED: Middleware for sessions and CSRF protection
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.sessions', 
        ],
    )

# --- 2. FORMS ---
class ContactForm(Form):
    """Simple validation form."""
    name = CharField(max_length=100)
    email = EmailField()

# --- 3. TEMPLATE ---
# HTML string with Django template tags
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Single Project</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; max-width: 600px; margin: 0 auto; }
        .success { color: #155724; background: #d4edda; padding: 1rem; border-radius: 5px; margin-bottom: 20px;}
        label { display: block; margin-top: 10px; font-weight: bold; }
        input { padding: 8px; width: 100%; box-sizing: border-box; margin-top: 5px; }
        button { margin-top: 15px; padding: 10px 20px; cursor: pointer; background: #007bff; color: white; border: none; }
        button:hover { background: #0056b3; }
        .errorlist { color: red; list-style: none; padding: 0; }
    </style>
</head>
<body>
    <h1>Single-File Form</h1>
    
    {% if message %}
        <div class="success">{{ message }}</div>
    {% endif %}

    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
        
        {{ form.as_p }}
        
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# --- 4. VIEW ---
def form_view(request):
    """Handles GET (show form) and POST (process data)."""
    message = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = f"Success! Data received for: {name}"
            form = ContactForm() # Clear form
    else:
        form = ContactForm()

    # Create Template object and Context
    template = Template(HTML_TEMPLATE)
    context = Context({
        'form': form,
        'message': message,
        'csrf_token': get_token(request), # Inject CSRF manually
    })
    
    return HttpResponse(template.render(context))

# --- 5. URLS & RUNNER ---
urlpatterns = [
    path("", form_view, name="home"),
]

if __name__ == "__main__":
    application = get_wsgi_application()
    execute_from_command_line(sys.argv)