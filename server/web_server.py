from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
from urllib.parse import urlparse, parse_qs
from search_embeddings import SearchEmbeddings

class StatusHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.embeddings = SearchEmbeddings()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            message = "Server is running!"
            self.wfile.write(message.encode())
        elif parsed_url.path == '/search':
            query_params = parse_qs(parsed_url.query)
            query = query_params.get('query', [''])[0]
            limit = int(query_params.get('limit', ['10'])[0])

            # TODO: implement search logic using limit parameters
            results = self.embeddings.search(query)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            message = json.dumps(results)
            self.wfile.write(message.encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    server_address = ('', 8000)
    httpd = HTTPServer(server_address, StatusHandler)
    logging.info('Server running on http://localhost:8000')
    httpd.serve_forever()
