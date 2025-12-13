import sys
import django
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.template import Template, Context
from django.middleware.csrf import get_token
from django.forms import Form, CharField, EmailField
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line
from django.db import models, connection
from django.apps import AppConfig

# --- 1. SETTINGS & APP CONFIG ---
class SimpleAppConfig(AppConfig):
    name = '__main__'  # Tells Django this script is the "App"
    verbose_name = "Main App"
    default_auto_field = 'django.db.models.BigAutoField'

if not settings.configured:
    settings.configure(
        SECRET_KEY='django-insecure-single-file',
        ROOT_URLCONF=__name__,
        DEBUG=True,
        ALLOWED_HOSTS=['*'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': './mydatabase.sqlite3',
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
        ],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            '__main__.SimpleAppConfig',
        ],
    )
    django.setup()

# --- 2. THE DJANGO MODEL (ORM) ---
class Item(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = '__main__'

    def __str__(self):
        return f"{self.name} ({self.email})"

# --- 3. THE ORM TABLE CREATOR ---
def initialize_database():
    """
    Uses the Django ORM's SchemaEditor to create tables.
    This replaces the 'makemigrations' and 'migrate' commands.
    """
    with connection.schema_editor() as schema_editor:
        if Item._meta.db_table not in connection.introspection.table_names():
            print(f"ORM: Creating table for {Item.__name__}...")
            schema_editor.create_model(Item)

# --- 4. FORMS & VIEWS ---
class ContactForm(Form):
    name = CharField(max_length=100)
    email = EmailField()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Django ORM Single File</title>
<style>
    body { font-family: system-ui; padding: 20px; max-width: 600px; margin: auto; }
    .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
    form { background: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #ccc; }
    button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
</style>
</head>
<body>
    <h1>Django ORM (Single File)</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Item via ORM</button>
    </form>
    <hr>
    <h2>Database Items</h2>
    {% for item in items %}
        <div class="card">
            <strong>{{ item.name }}</strong><br>
            <span style="color: #666;">{{ item.email }}</span>
        </div>
    {% empty %}
        <p>No items in database yet.</p>
    {% endfor %}
</body>
</html>
"""

def form_view(request):
    # Ensure ORM tables exist
    initialize_database()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # --- USING THE ORM TO SAVE ---
            Item.objects.create(**form.cleaned_data)
            form = ContactForm()
    else:
        form = ContactForm()

    # --- USING THE ORM TO FETCH ---
    items = Item.objects.all().order_by('-created_at')
    
    template = Template(HTML_TEMPLATE)
    context = Context({
        'form': form,
        'items': items,
        'csrf_token': get_token(request),
    })
    return HttpResponse(template.render(context))

# --- 5. URLS & RUNNER ---
urlpatterns = [
    path("", form_view, name="home"),
]

if __name__ == "__main__":
    # 1. First, handle built-in Django migrations (sessions, auth)
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
    
    # 2. Run the server
    application = get_wsgi_application()
    execute_from_command_line(sys.argv)