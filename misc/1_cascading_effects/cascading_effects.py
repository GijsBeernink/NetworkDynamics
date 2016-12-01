import numpy as np
import matplotlib.pyplot as plt
import misc.utils.util as util
import datetime
import pprint


data = util.read_youtube_data()

# try:
#     for j in range(len(data[0])):
#         for i in range(1,305):
#             if data[i-1][j].title != data[i][j].title:
#                 print data[i-1][j].title , "\n", data[i][j].title
#                 print data[i-1][j].date , "\n", data[i][j].date
#                 print i, j
#                 print "---------------------------------"
# except IndexError:
#     print i,", ", j


get_song = 0
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

fig = plt.figure(title)
plt.plot(t, like_counts, 'r', t, dislike_counts, 'b')
plt.ylabel("Votes")
plt.xlabel("Days since 09-11-2015")
plt.show()
