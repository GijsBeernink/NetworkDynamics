import misc.utils.util as util
import numpy as np
import matplotlib.pyplot as plt
import os

path, dirs, files = os.walk("../../data/youtube_top100").next()
file_count = len(files)
days_interval = 20

def get_song_views(data):
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
            tmp.append(ratio * 100)
            result[song] = tmp
    return result


# Plots distribution of the number of views of all songs over several days
def plot_distribution(songs):
    x = np.arange(0, file_count, days_interval)

#   Plot distribution of all songs
    plt.figure("Distribution of songs with " + str(days_interval) + " days interval")
    plt.ylabel("Percentage of views")
    plt.xlabel("Day")
    plt.ylim(0, 5.5)
    for song in songs:
        plt.plot(x, songs.get(song))
    plt.show(block=False)

#   Plot distribution of songs which rise
    plt.figure("Distribution of songs which rise (" + str(days_interval) + " days interval)")
    plt.ylabel("Percentage of views")
    plt.xlabel("Day")
    plt.ylim(0, 5.5)
    for song in songs:
        views = songs.get(song)
        if views[0] < views[-1]:
            plt.plot(x, views)
    plt.show(block=False)

    #   Plot distribution of songs which have a rich-get-richer trend
    plt.figure("Distribution of songs with rich-get-richer trend (" + str(days_interval) + " days interval)")
    plt.ylabel("Percentage of views")
    plt.xlabel("Day")
    plt.ylim(0, 5.5)
    line_in_plot = False
    for song in songs:
        views = songs.get(song)
        dv = np.gradient(views)
        if all(0 < x < y for x, y in zip(dv, dv[1:])):
            plt.plot(x, views)
            line_in_plot = True
    if not line_in_plot:
        plt.figtext(.5,.5,"No rich-get-richer trend in this data.")
    plt.show()

# youtube_data = util.read_youtube_data()
# song_views = get_song_views(youtube_data)
# song_ratios = song_views_to_percentage(song_views)
# plot_distribution(song_ratios)


#   Returns a measure of similarity between the two ordinal vectors
def distance(ordinal_1, ordinal_2):
    return sum([abs(ordinal_1[i] - ordinal_2[i]) for i in range(len(ordinal_1))])


#   Sum the distances between two lists of ordinal vectors
def total_distances(ordinals_1, ordinals_2):
    return sum([distance(ordinals_1[i], ordinals_2[i]) for i in range(len(ordinals_1))])


#   Convert a ranking vector to an ordinal vector
def to_ordinal(ranking):
    page_rank_tuple = sorted(([(i,j) for i,j in enumerate(ranking, 0)]), key = lambda x: x[1], reverse = True)
    ordinal_rank = [0 for _ in ranking]
    j = 1
    for t in page_rank_tuple:
        ordinal_rank[t[0]] = j
        j += 1
    return ordinal_rank

