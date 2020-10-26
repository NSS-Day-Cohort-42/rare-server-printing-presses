from models.posts import Posts
import sqlite3
import json


def get_all_posts():

    with sqlite3.connect("rare.db") as conn:


        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.title,
            p.content,
            p.category_id
        FROM posts p
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Posts(row['id'], row['user_id'], row['title'],
                            row['content'], row['category_id'])

            posts.append(post.__dict__)

    return json.dumps(posts)

def create_post(new_posts):
        with sqlite3.connect("rare.db") as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO posts
                ( user_id, title, content )
            VALUES
                ( ?, ?, ?, ?);
            """, (new_posts['user_id'], new_posts['title'],
                new_posts['content']))

            # The `lastrowid` property on the cursor will return
            # the primary key of the last thing that got added to
            # the database.
            id = db_cursor.lastrowid

            # Add the `id` property to the animal dictionary that
            # was sent by the client so that the client sees the
            # primary key in the response.
            new_posts['id'] = id


        return json.dumps(new_posts)