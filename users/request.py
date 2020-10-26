from models.users import Users
import sqlite3
import json


def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.email,
            u.name,
            u.password
        FROM users u
        """)

        # Initialize an empty list to hold all user representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            user = Users(row['id'], row['email'], row['name'], row['password'])

            users.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)


def check_if_valid(post_body):
    
    # {'password': 'password', 'email': 'mo@mo.com'}
    password = post_body['password']
    email = post_body['email']

    with sqlite3.connect("rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.email,
            u.name,
            u.password
        FROM users u
        WHERE u.email = ? AND u.password = ?
        """, (email, password, ))

        # Initialize an empty list to hold all user representations
        

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        user = Users(data['id'], data['email'], data['name'], data['password'])
        # Iterate list of data returned from database
        response_object = {'valid': True, 'id': user.id}
        
        return json.dumps(response_object)
    
def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO users
            (email, name, password)
        VALUES
            ( ?, ?, ?);
        """, (new_user['email'], new_user['name'], new_user['password'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the user dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_user['id'] = id


    return json.dumps(new_user)
