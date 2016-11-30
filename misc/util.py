import json
import os
from pprint import pprint

class SongSnapshot:
    def __init__(self, name, views, likes, dislikes, comment_count):
        self.name = name
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comment_count = comment_count

def get_snapshots(data):
    snapshots = []
    for i in range(len(data)):
        title = data[i]["snippet"]["title"]
        views = data[i]["statistics"]["viewCount"]
        likes = data[i]["statistics"]["likeCount"]
        dislikes = data[i]["statistics"]["dislikeCount"]
        comment_count = data[i]["statistics"]["commentCount"]
        snapshot = SongSnapshot(title, views, likes, dislikes, comment_count)
        snapshots.append(snapshot)
    return snapshots

def read_youtube_data():
    days = []
    for filename in os.listdir("C:\Users\Gijs\PycharmProjects\NetworkDynamics\data\youtube_top100"):
        data_file = open('../data/youtube_top100/' + filename)
        data = json.load(data_file)
        snapshots = get_snapshots(data)
        days.append(snapshots)
    return days

