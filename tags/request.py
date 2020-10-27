from models.post_tags import Post_Tags
from models.tags import Tag
import sqlite3 
import json
from models import tags

def get_all_tags():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row["id"], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)

def create_new_tag(new_tag):

    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
        ( ? );
        """, (new_tag['label'], )
        )

        id = db_cursor.lastrowid

        new_tag['id'] = id

    return json.dumps(new_tag)

def get_posts_tags():
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id
        FROM post_tags pt
        """)

        post_tags = []
        dataset = db_cursor.fetchall()

        

        for row in dataset:
            pt = Post_Tags(row[0], row[1], row[2])

            post_tags.append(pt.__dict__)

    return json.dumps(post_tags)



