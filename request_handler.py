from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from users.request import check_if_valid, get_all_users
from comments.request import get_all_comments, add_comment, delete_comment, update_comment
class HandleRequests(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "login":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "comments":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_comments()}"

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        response = None

        if resource == "login":
            response = check_if_valid(post_body)
        
        if resource == "comments":
            response = add_comment(post_body)

        if resource == "posts":
            response = create_posts(post_body)

        self.wfile.write(f"{response}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_posts(id)
        
        elif resource == "comments":
            delete_comment(id)

        self.wfile.write("".encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "posts":
            update_posts(id, post_body)

        elif resource == "comments":
            update_comment(id, post_body)

        elif resource == "tags":
            update_tags(id, post_body)
        
        elif resource == "categories":
            update_categories(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def  main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()




if __name__ == "__main__":
    main()