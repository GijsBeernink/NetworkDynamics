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
    plt.show(block=False)


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


def compare_ranking_spotify_youtube(youtube_data, spotify_data):
    # Get all youtube titles and views and make it an ordinal list.
    youtube_titles = []
    youtube_views = []

    for snapshot in youtube_data[127]:                          # datapoint 127 is the data at 29-07-2016. Halfway our used YouTube dataset. Change 127 to -1 to take last datapoint.
        youtube_titles.append(snapshot.title)
        youtube_views.append(int(snapshot.views))
    youtube_ordinal = to_ordinal(youtube_views)

    # Sort youtube titles in ordinal order
    youtube_ordinal_titles = []
    for _ in range(len(youtube_ordinal)):
        youtube_ordinal_titles.append(0)

    pos = 0
    for i in youtube_ordinal:
        youtube_ordinal_titles[i-1] = youtube_titles[pos]
        pos += 1

    # Keep track of the original top 100 of spotify. These songs are in the youtube data as well.
    spotify_titles_orig = []
    for track in spotify_data[0]:
        spotify_titles_orig.append(track.title)

    # Ordinal titles are in the order as they appear in the last array of snapshots
    spotify_ordinal_titles = []
    for track in spotify_data[261]:                             # datapoint 261 is the data at 29-07-2016. Halfway our used YouTube dataset. Change 261 to -1 to take last datapoint.
        spotify_ordinal_titles.append(track.title)

    # Only get songs which were in the top100 at the beginning
    spotify_ordinal_titles_useful = []
    for i in range(len(spotify_ordinal_titles)):
        if spotify_ordinal_titles[i] in spotify_titles_orig:
            spotify_ordinal_titles_useful.append(spotify_ordinal_titles[i])
        else:
            spotify_ordinal_titles_useful.append("-")

    print_comparison(spotify_ordinal_titles_useful, youtube_ordinal_titles)


# Print the ordinal rankings of the youtube titles and spotify titles. It is necessary to provide the titles in ordinal ranking.
def print_comparison(youtube_ordinal_titles, spotify_ordinal_titles):
    print "Position | \t \t spotify title \t\t \t\t| \t  youtube title "

    for i in range(len(spotify_ordinal_titles)):
        if i+1 < 10:
            nr = str(0) + str(i+1)
        else:
            nr = i+1
        print nr, " \t | ", youtube_ordinal_titles[i], "\t\t\t\t | ", spotify_ordinal_titles[i]

spotify_data = util.read_spotify_data()
youtube_data = util.read_youtube_data()
song_views = get_song_views(youtube_data)
song_ratios = song_views_to_percentage(song_views)
plot_distribution(song_ratios)
compare_ranking_spotify_youtube(youtube_data, spotify_data)
plt.show() # to ensure the plots don't disappear right after the program finishes.


