import pandas as pd
import matplotlib.pyplot as plt
import misc.utils.util as util

def plot(songs):
    print songs.keys()[0]
    print songs.get(songs.keys()[0])

    raw_data = songs
    # raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
    #             'pre_score': [4, 24, 31, 2, 3],
    #             'mid_score': [25, 94, 57, 62, 70],
    #             'post_score': [5, 43, 23, 23, 51]}
    # df = pd.DataFrame(raw_data, columns=['first_name', 'pre_score', 'mid_score', 'post_score'])
    df = pd.DataFrame(raw_data, columns = ['Song'].append(songs.keys()))

    print df

    #  TODO generate bars

    # # Create the general blog and the "subplots" i.e. the bars
    # f, ax1 = plt.subplots(1, figsize=(10,5))
    #
    # # Set the bar width
    # bar_width = 0.75
    #
    # # positions of the left bar-boundaries
    # bar_l = [i+1 for i in range(len(df['pre_score']))]
    #
    # # positions of the x-axis ticks (center of the bars as bar labels)
    # tick_pos = [i+(bar_width/2) for i in bar_l]
    #
    # # Create a bar plot, in position bar_1
    # ax1.bar(bar_l,
    #         # using the pre_score data
    #         df['pre_score'],
    #         # set the width
    #         width=bar_width,
    #         # with the label pre score
    #         label='Pre Score',
    #         # with alpha 0.5
    #         alpha=0.5,
    #         # with color
    #         color='#F4561D')
    #
    # # Create a bar plot, in position bar_1
    # ax1.bar(bar_l,
    #         # using the mid_score data
    #         df['mid_score'],
    #         # set the width
    #         width=bar_width,
    #         # with pre_score on the bottom
    #         bottom=df['pre_score'],
    #         # with the label mid score
    #         label='Mid Score',
    #         # with alpha 0.5
    #         alpha=0.5,
    #         # with color
    #         color='#F1911E')
    #
    # # Create a bar plot, in position bar_1
    # ax1.bar(bar_l,
    #         # using the post_score data
    #         df['post_score'],
    #         # set the width
    #         width=bar_width,
    #         # with pre_score and mid_score on the bottom
    #         bottom=[i+j for i,j in zip(df['pre_score'],df['mid_score'])],
    #         # with the label post score
    #         label='Post Score',
    #         # with alpha 0.5
    #         alpha=0.5,
    #         # with color
    #         color='#F1BD1A')
    #
    # # set the x ticks with names
    # plt.xticks(tick_pos, df['first_name'])
    #
    # # Set the label and legends
    # ax1.set_ylabel("Total Score")
    # ax1.set_xlabel("Test Subject")
    # plt.legend(loc='upper left')
    #
    # # Set a buffer around the edge
    # plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
    # plt.show()

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

youtube_data = util.read_youtube_data()

songs = get_song_views(20, youtube_data)
plot(songs)