import numpy as np
import matplotlib.pyplot as plt
import misc.utils.util as util
import datetime

# Songs to be investigated
to_investigate = [13, 23, 43, 53, 93]


# Plots day vs like and day vs dislike of a single song.
def plot_song(nr, data):
    view_counts = []
    title = ""
    previous_day = -1

    for day in data:
        if previous_day == -1:
            previous_day = day[nr].date - datetime.timedelta(days=1)
            title = day[nr].title
            view_counts.append(day[nr].views)

        elif day[nr].date == previous_day + datetime.timedelta(days=1):
            view_counts.append(day[nr].views)

        else:
            view_counts.append(0)

        while day[nr].date > previous_day + datetime.timedelta(days=1):
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

for nr in to_investigate:
    plot_song(nr, youtube_data)

