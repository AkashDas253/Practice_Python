# run.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from app.routes import routes

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = routes.get(self.path)
        if handler:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(handler())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        handler = routes.get(self.path)
        if handler:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            response = handler(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Serving on http://localhost:8000")
    server.serve_forever()
