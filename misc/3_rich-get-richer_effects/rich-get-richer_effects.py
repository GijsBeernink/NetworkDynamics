import misc.utils.util as util
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
import os

path, dirs, files = os.walk("../../data/youtube_top100").next()
file_count = len(files)


def get_song_views(days_interval, data):
    songs = dict()
    datapoints = 0
    for song in data[0]:
        songs[song.title] = []

    for day in range(len(data)):
        if day % days_interval == 0:
            datapoints += 1

            for song in data[day]:
                temp = songs.get(song.title)
                views = int(song.views)
                temp.append(views)
                songs[song.title] = temp
    return songs

# {title: [views]} to {title: [percentage of views}
def song_views_to_percentage(songs):
    result = dict()

    for song in songs:
        result[song] = []

    for i in range(0, len(songs.get(songs.keys()[0]))):
        total_views = 0
        for song in songs:
            songviews = songs.get(song)[i]
            total_views += songviews

        for song in songs:
            songviews = songs.get(song)[i]
            ratio = float(songviews) / float(total_views)
            tmp = result.get(song)
            tmp.append(ratio)
            result[song] = tmp
    return result


# Plots distribution of the number of views of all songs over several days
def plot_distribution(days_interval, songs):

    x = np.arange(0, file_count/days_interval + 1, 1)

    plt.figure("Distribution of songs with " + str(days_interval) + " days interval")

    for song in songs:
        # print song, ": ", songs.get(song)
        plt.plot(x, songs.get(song))

    plt.show()

days_interval = 50

youtube_data = util.read_youtube_data()
song_views = get_song_views(days_interval, youtube_data)
song_ratios = song_views_to_percentage(song_views)
plot_distribution(days_interval,song_ratios)