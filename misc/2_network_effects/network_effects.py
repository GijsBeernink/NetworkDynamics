import numpy as np
import matplotlib.pyplot as plt
import misc.utils.util as util
import datetime

# Plots day vs like and day vs dislike of a single song.
def plot_song(nr, data):
    get_song = nr
    like_counts = []
    dislike_counts = []
    title = ""
    previous_day = -1
    for day in data:
        if previous_day == -1:
            previous_day = day[get_song].date - datetime.timedelta(days=1)
            title = day[get_song].title
            like_counts.append(day[get_song].likes)
            dislike_counts.append(day[get_song].dislikes)

        elif day[get_song].date == previous_day + datetime.timedelta(days=1):
            like_counts.append(day[get_song].likes)
            dislike_counts.append(day[get_song].dislikes)

        else:
            like_counts.append(0)
            dislike_counts.append(0)

        while day[get_song].date > previous_day + datetime.timedelta(days=1):
            like_counts.append(0)
            dislike_counts.append(0)
            previous_day += datetime.timedelta(days=1)

        previous_day = previous_day + datetime.timedelta(days=1)

    t = np.arange(0, len(like_counts), 1)
    plt.figure(title)
    plt.plot(t, like_counts, 'r', t, dislike_counts, 'b')
    plt.ylabel("Votes")
    plt.xlabel("Days since 21-03-2015")
    plt.show()


youtube_data = util.read_youtube_data()

