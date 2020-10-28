from models.post_tags import Post_Tag
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

def get_post_tags_by_id(post_id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id,
            t.id tag_id,
            t.label
        FROM post_tags pt
        JOIN tags t ON t.id = pt.tag_id
        WHERE pt.post_id = ?
               """,(post_id, ))

        post_tags = []
        dataset = db_cursor.fetchall()

        

        for row in dataset:
            pt = Post_Tag(row[0], row[1], row[2])
            tag = Tag(row[3], row[4])

            pt.tags = tag.__dict__

            post_tags.append(pt.__dict__)

    return json.dumps(post_tags)
