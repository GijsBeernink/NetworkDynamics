import json
import os
import dateutil.parser

'''
Paths
'''

youtube_data_path = "../../data/youtube_top100/"
radio3fm_data_path = "../../data/radio3fm_megahit/"
radio538data_path = "../../data/radio538_alarmschijf/"
spotify_data_path = "../../data/spotify_top100/"

'''
Data point object
'''


class SongSnapshot:
    def __init__(self, title, views, likes, dislikes, comment_count, date):
        self.title = title
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comment_count = comment_count
        self.date = date


class SpotifySnapshot:
    def __init__(self, title, position_in_top100, date):
        self.title = title
        self.position_in_top100 = position_in_top100
        self.date = date


'''
Queries
'''


def get_snapshots(data, date):
    snapshots = []
    for i in range(len(data)):
        title = data[i]["snippet"]["title"]
        views = data[i]["statistics"]["viewCount"]
        likes = data[i]["statistics"]["likeCount"]
        dislikes = data[i]["statistics"]["dislikeCount"]
        comment_count = data[i]["statistics"]["commentCount"]
        snapshots.append(SongSnapshot(title, views, likes, dislikes, comment_count, date))
    return snapshots


def read_data(path):
    result = []
    for filename in os.listdir(path):
        data_file = open(path + filename)
        data = json.load(data_file)
        snapshots = get_snapshots(data, filter_date(filename))
        result.append(snapshots)
    return result


def read_youtube_data():
    return read_data(youtube_data_path)


def read_megahit_data():
    return read_data(radio3fm_data_path)


def read_alarmschijf_data():
    return read_data(radio538data_path)


def read_spotify_data():
    result = []
    for filename in os.listdir(spotify_data_path):
        data_file = open(spotify_data_path + filename)
        data = json.load(data_file)
        snapshots = []
        position_in_top100 = 0  # zero is first place
        for track in data["tracks"]["items"]:
            title = str(track["track"]["artists"][0]["name"].encode('ascii', 'ignore')) + " - " + str(track["track"]["name"].encode('ascii', 'ignore'))          # only takes first artist
            date = filter_date(filename)
            snapshots.append(SpotifySnapshot(title, position_in_top100, date))
            position_in_top100 += 1
        result.append(snapshots)
    return result


def filter_date(filename):
    res = filename[0:8]
    return dateutil.parser.parse(res)


def print_nr_titles(data):
    i = 0
    for snapshot in data[0]:
        print i, ": ", snapshot.title
        i += 1
