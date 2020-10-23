from models.categories import Categories
import sqlite3
import json

def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO categories
            (label)
        VALUES
            ( ? );
        """, (new_category ['label'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the category
        # dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_category['id'] = id


    return json.dumps(new_category)