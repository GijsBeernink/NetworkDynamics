import numpy as np
import matplotlib.pyplot as plt
import misc.utils.util as util
import datetime


# Plots day vs like and day vs dislike of a single song.
def plot_song(nr, data):
    get_song = nr
    view_counts = []
    title = ""
    previous_day = -1
    for day in data:
        if previous_day == -1:
            previous_day = day[get_song].date - datetime.timedelta(days=1)
            title = day[get_song].title
            view_counts.append(day[get_song].views)

        elif day[get_song].date == previous_day + datetime.timedelta(days=1):
            view_counts.append(day[get_song].views)

        else:
            view_counts.append(0)

        while day[get_song].date > previous_day + datetime.timedelta(days=1):
            view_counts.append(0)
            previous_day += datetime.timedelta(days=1)

        previous_day = previous_day + datetime.timedelta(days=1)

    t = np.arange(0, len(view_counts), 1)
    plt.figure(title)
    plt.plot(t, view_counts, 'r')
    plt.ylabel("Views")
    plt.xlabel("Days since 21-03-2015")
    plt.show()


youtube_data = util.read_youtube_data()
for i in range(len(youtube_data[0])):
    plot_song(i, youtube_data)

