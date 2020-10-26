from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from tags.request import create_new_tag, get_all_tags
from users.request import check_if_valid, get_all_users
from comments.request import get_all_comments, add_comment
from posts.request import create_post, get_all_posts, update_post
from users.request import check_if_valid, get_all_users, create_user
from categories.request import create_category, get_all_categories
from comments.request import get_all_comments, add_comment, delete_comment, update_comment, get_single_comment
from posts.request import get_all_posts


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

            param = resource.split("?")[1]  
            resource = resource.split("?")[0]  
            pair = param.split("=")  
            key = pair[0]  
            value = pair[1] 

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
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"
                    
            elif resource == "tags":
                response = f"{get_all_tags()}"

            elif resource == "posts":
                if id is not None:
                    response = f"{get_single_posts()}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "categories":
                    response = f"{get_all_categories()}"

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

        if resource == "register":
            response = create_user(post_body)
        
        if resource == "posts":
            response = create_post(post_body)

        if resource == "categories":
            response = create_category(post_body)
        if resource == "tags":
            response = create_new_tag(post_body)

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
        success = False

        print("Edit about to happen")

        if resource == "posts":
            update_post(id, post_body)

        elif resource == "comments":
            success = update_comment(post_body)

        elif resource == "tags":
            update_tags(id, post_body)
        
        elif resource == "categories":
            update_categories(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def  main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()




if __name__ == "__main__":
    main()