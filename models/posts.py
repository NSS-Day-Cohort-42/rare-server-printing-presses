    
class Posts: 

    def __init__(self, id, user_id, title, content, category_id):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.category_id = category_id
        self.tags = None