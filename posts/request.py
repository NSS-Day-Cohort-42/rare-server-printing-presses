from models.tags import Tag
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
            p.category_id,
            t.id tag_id,
            t.label tag_label
        FROM posts p
        JOIN post_tags pt ON p.id = pt.post_id
        JOIN tags t ON pt.tag_id = t.id
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Posts(row['id'], row['user_id'], row['title'],
                            row['content'], row['category_id'])

            tag = Tag("",row['tag_label'])

            post.tags = tag.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)

def create_post(new_posts):
        with sqlite3.connect("rare.db") as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO posts
                (user_id, title, content, category_id )
            VALUES
                (?, ?, ?, ?);
            """, (new_posts['user_id'], new_posts['title'], new_posts['content'], new_posts['category_id'], ))

            id = db_cursor.lastrowid

            new_posts['id'] = id


        return json.dumps(new_posts)

def get_single_post(id):
     with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.title,
            a.content,
            a.category_id
        FROM posts a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        post = Posts(data['id'], data['user_id'], data['title'],
                        data['content'], data['category_id'])

        return json.dumps(post.__dict__)

def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))