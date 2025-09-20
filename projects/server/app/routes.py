# app/routes.py
# Define route handlers here
routes = {}

def route(path):
    def decorator(func):
        routes[path] = func
        return func
    return decorator

@route('/')
def home():
    return b"<h1>Hello, World!</h1><a href='/about'>About</a> | <a href='/contact'>Contact</a> | <a href='/form'>Form</a>"

@route('/about')
def about():
    return b"<h1>About Page</h1><p>This is the About page.</p>"

@route('/contact')
def contact():
    return b"<h1>Contact</h1><p>Contact us at: contact@example.com</p>"

@route('/form')
def form():
    return b"""
        <h1>Form Example</h1>
        <form method='POST' action='/submit'>
            <input name='username' placeholder='Enter your name'>
            <input type='submit'>
        </form>
    """

@route('/submit')
def submit(post_data=None):
    import urllib.parse
    if post_data:
        parsed = urllib.parse.parse_qs(post_data)
        username = parsed.get('username', [''])[0]
        return f"<h1>Form submitted!</h1><p>Hello, {username}!</p>".encode()
    return b"<h1>Form submitted!</h1>"
