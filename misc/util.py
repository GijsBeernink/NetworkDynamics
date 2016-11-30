import json


class SongSnapshot:
    def __init__(self, name, views, likes, dislikes, comment_count):
        self.name = name
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comment_count = comment_count
