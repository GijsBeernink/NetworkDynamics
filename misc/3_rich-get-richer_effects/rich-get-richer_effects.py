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


# # Plots distribution of the number of views of all songs over several days
# def plot_distribution(days_interval, data):
#
#
#
#     x = np.arange(0, file_count, days_interval)
#
#     plt.figure("Distribution of songs with" + str(days_interval) + " days interval")
#
#     for i in range(0,len(songs.values()[0])):
#
#         for song in songs:
#             if i == 0:
#                 plt.bar(x, float(songs.get(song.title))/float(totals[i]), 20, color='r')
#             else:
#                 plt.bar(x, float(songs.get(song.title))/float(totals[i]), 20, color='y', bottom=songs.get())
#
#
#     #
#     # plt.bar(x, songs.get(data[0][0].title), 20, color='r')
#     # plt.bar(x, songs.get(data[0][1].title), 20, color='y', bottom=songs.get(data[0][0].title))
#     plt.show()

youtube_data = util.read_youtube_data()
# plot_distribution(20, youtube_data)

# mu = 100
# sigma = 25
# n_bins = 50
# x = mu + sigma * np.random.randn(10000)
#
# n, bins, patches = plt.hist(x, n_bins, normed=1,
#                             histtype='step', cumulative=True)
#
# # Add a line showing the expected distribution.
# y = mlab.normpdf(bins, mu, sigma).cumsum()
# y /= y[-1]
# plt.plot(bins, y, 'k--', linewidth=1.5)
#
# # Overlay a reversed cumulative histogram.
# plt.hist(x, bins=bins, normed=1, histtype='step', cumulative=-1)
#
# plt.grid(True)
# plt.ylim(0, 1.05)
# plt.title('cumulative step')
#
# plt.show()