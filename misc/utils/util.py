import json
import os
import dateutil.parser


class SongSnapshot:
    def __init__(self, title, views, likes, dislikes, comment_count, date):
        self.title = title
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comment_count = comment_count
        self.date = date

def get_snapshots(data, date):
    snapshots = []
    for i in range(len(data)):
        title = data[i]["snippet"]["title"]
        views = data[i]["statistics"]["viewCount"]
        likes = data[i]["statistics"]["likeCount"]
        dislikes = data[i]["statistics"]["dislikeCount"]
        comment_count = data[i]["statistics"]["commentCount"]
        snapshot = SongSnapshot(title, views, likes, dislikes, comment_count, date)
        snapshots.append(snapshot)
    return snapshots

def read_youtube_data():
    days = []
    for filename in os.listdir("../../data/youtube_top100"):
        data_file = open('../../data/youtube_top100/' + filename)
        data = json.load(data_file)
        snapshots = get_snapshots(data, filter_date(filename))
        days.append(snapshots)
    return days

def read_megahit_data():
    days = []
    for filename in os.listdir("../../data/radio3fm_megahit"):
        data_file = open('../../data/radio3fm_megahit/' + filename)
        data = json.load(data_file)
        snapshots = get_snapshots(data, filter_date(filename))
        days.append(snapshots)
    return days

def filter_date(filename):
    res = filename[0:8]
    return dateutil.parser.parse(res)

def print_nr_titles(data):
    i = 0;
    for snapshot in data[0]:
        print i , ": ", snapshot.title
        i += 1