import misc.utils.util as util
import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


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
    plt.xlabel(data[0][nr].title)
    plt.show()



h = [186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
     187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
     161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180]
h.sort()
hmean = np.mean(h)
hstd = np.std(h)
pdf = stats.norm.pdf(h, hmean, hstd)
plt.plot(h, pdf) # including h here is crucial
youtube_data = util.read_youtube_data()

