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
from django.contrib import admin
import os
from django.db.models import Q

# --- Configuration: Virtual App Setup ---
class SingleFileAppConfig(AppConfig):
    """Defines the configuration for this single-file script as a Django app."""
    name = '__main__' 
    verbose_name = "Single File Project"
    default_auto_field = 'django.db.models.BigAutoField'

# --- Configuration: Django Settings ---
if not settings.configured:
    settings.configure(
        SECRET_KEY='django-insecure-single-file-project-key',
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
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        INSTALLED_APPS=[
            # Core Django services
            'django.contrib.admin',       
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            'django.contrib.messages',
            'django.contrib.staticfiles', 
            # Local App
            '__main__.SingleFileAppConfig',
        ],
        # Static file serving configuration
        STATIC_URL = '/static/',
    )
    django.setup()

# --- Model Imports ---
from django.contrib.auth.models import User 

# --- Model Definition: Item ---
class Item(models.Model):
    """Represents a simple data entry model for the application."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = '__main__'
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.name} ({self.email})"

# --- Admin Configuration ---
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin interface customization for the Item model."""
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

# --- Database Management Utilities ---
def initialize_database():
    """Bypasses migrations and uses the SchemaEditor to create the Item table."""
    with connection.schema_editor() as schema_editor:
        if Item._meta.db_table not in connection.introspection.table_names():
            print(f"ORM: Creating table for {Item.__name__}...")
            schema_editor.create_model(Item)

def create_initial_user():
    """Creates a default superuser (admin/admin) if no users exist."""
    if 'auth_user' in connection.introspection.table_names() and not User.objects.exists():
        print("Creating default superuser: admin/admin...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

# --- Forms and Templates ---
class ContactForm(Form):
    """Simple form for user input."""
    name = CharField(max_length=100)
    email = EmailField()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Django Single File Project</title>
<style>
    body { font-family: system-ui; padding: 20px; max-width: 600px; margin: auto; }
    .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
    form { background: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #ccc; }
    button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    .search-form input { padding: 10px; border: 1px solid #ccc; width: 80%; }
    .search-form button { width: 15%; margin-left: 5%; background: #6c757d; }
</style>
</head>
<body>
    <h1>Django Single File App</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Item</button>
    </form>
    <hr>
    
    <form method="get" class="search-form">
        <input type="text" name="q" placeholder="Search by name or email" value="{{ search_query }}">
        <button type="submit">Search</button>
    </form>
    
    <h2>Database Items {% if search_query %}(Filtered){% endif %}</h2>
    {% for item in items %}
        <div class="card">
            <strong>{{ item.name }}</strong><br>
            <span style="color: #666;">{{ item.email }}</span>
        </div>
    {% empty %}
        <p>No items in database yet. <a href="/admin/">Go to Admin</a>.</p>
    {% endfor %}
</body>
</html>
"""

# --- Views ---
def form_view(request):
    """Handles form submission, filtering, and displays existing data."""
    initialize_database()
    
    search_query = request.GET.get('q', '').strip()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Item.objects.create(**form.cleaned_data)
            form = ContactForm()
    else:
        form = ContactForm()
    
    # ORM Filtering Logic
    items = Item.objects.all()
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        )

    items = items.order_by('-created_at')
    
    template = Template(HTML_TEMPLATE)
    context = Context({
        'form': form,
        'items': items,
        'search_query': search_query,
        'csrf_token': get_token(request),
    })
    return HttpResponse(template.render(context))

# --- URL Routing (Static URLs are added in the execution block) ---
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", form_view, name="home"),
]

# --- Main Execution Block ---
if __name__ == "__main__":
    
    # Add static URL routing here, where settings.DEBUG is safe to access.
    if settings.DEBUG:
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
        urlpatterns += staticfiles_urlpatterns()

    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        print("Applying system migrations for Admin functionality...")
        execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
        create_initial_user()
    
    application = get_wsgi_application()
    execute_from_command_line(sys.argv)