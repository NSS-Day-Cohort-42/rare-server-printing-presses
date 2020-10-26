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

def create_post(posts):
    max_id = Posts[-1]["id"]

    new_id = max_id + 1

    posts["id"] = new_id

    Posts.append(posts)

    return posts