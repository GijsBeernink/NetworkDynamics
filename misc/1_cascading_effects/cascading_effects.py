import numpy as np
import matplotlib.pyplot as plt
import misc.utils.util as util
import datetime

def get_data():
    return util.read_youtube_data()


# Change format of data from [[data_per_day]] to [total_snapshot_song_0, total_snapshot_song_1,...]
def reformat_data(data):
    new_data = []
    for j in range(len(data[0])):
        views = []
        likes = []
        dislikes = []
        commment_count = []
        date = []
        title = data[0][j].title
        for i in range(1, len(data)):
            if data[i - 1][j].title == data[i][j].title:
                views.append(data[i - 1][j].views)
                likes.append(data[i - 1][j].likes)
                dislikes.append(data[i - 1][j].dislikes)
                commment_count.append(data[i - 1][j].comment_count)
                date.append(data[i - 1][j].date)
            else:
                print ("Titles not equal!:\n\t", data[i - 1][j].title, "\n\t", data[i][j].title)
        new_data.append(util.SongSnapshot(title, views, likes, dislikes, commment_count))
    return new_data

def check_titles(data):
    try:
        for j in range(len(data[0])):
            for i in range(1,len(data)):
                if data[i-1][j].title != data[i][j].title:
                    print data[i-1][j].title , "\n", data[i][j].title
                    print data[i-1][j].date , "\n", data[i][j].date
                    print i, j
                    print "---------------------------------"
    except IndexError:
        print i,", ", j


def plot_song(nr, data):
    get_song = nr
    like_counts = []
    dislike_counts = []
    title = ""
    previous_day = -1
    for day in data:
        print previous_day
        print day[get_song].date
        print ""
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
            print "while: ", previous_day
            print "while: ", day[get_song].date
            print ""
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


def calculate_difference_with_previous(array):
    result = []
    for i in range(1, len(array)):
        incr = float(array[i]) - float(array[i-1])
        result.append(incr)
    return result

def calculate_ratio(a, b):
    result = []
    for i in range(len(a)):
        try:
            ratio = float(a[i]) / float((float(a[i]) + float(b[i])))
        except ZeroDivisionError:
            print a[i], ", ", b[i]
        result.append(ratio * 100)
    return result


data = get_data()
data_ref = reformat_data(data)

    # diff_likes = calculate_difference_with_previous(song.likes)
    # diff_dislikes = calculate_difference_with_previous(song.dislikes)

for i in range(len(data_ref)):
    ratio = calculate_ratio(data_ref[i].likes, data_ref[i].dislikes)

    if all(x<y for x, y in zip(ratio, ratio[1:])):
        x = np.arange(0, len(ratio), 1)
        plt.figure("Song: " + str(data_ref[i].title))
        plt.plot(x, ratio, 'r')
        plt.ylabel("ratio")
        plt.xlabel("days")
        plt.show()
