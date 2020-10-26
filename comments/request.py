from models.comments import Comments
import sqlite3
import json

def get_all_comments():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.user_id,
            c.post_id,
            c.subject,
            c.content
        FROM comments c
        """)

        # Initialize an empty list to hold all animal representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            user = Comments(row['id'], row['user_id'], row['post_id'], row['subject'], row['content'])

            users.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)

def add_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            ( user_id, post_id, subject, content )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_comment['user_id'], new_comment['post_id'],
              new_comment['subject'], new_comment['content']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id


    return json.dumps(new_comment)

def delete_comment(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))

def get_single_comment(id):
     with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.post_id,
            a.subject,
            a.content
        FROM comments a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        comment = Comments(data['id'], data['user_id'], data['post_id'],
                        data['subject'], data['content'])

        return json.dumps(comment.__dict__)

def update_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Comments
            SET
                user_id = ?,
                post_id = ?,
                subject = ?,
                content = ?
        WHERE id = ?
        """, (new_comment['user_id'], new_comment['post_id'],
                        new_comment['subject'], new_comment['content'], new_comment['id']))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True