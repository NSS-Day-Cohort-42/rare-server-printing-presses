from models.categories import Categories
import sqlite3
import json

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