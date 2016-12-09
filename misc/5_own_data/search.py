#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import random as rand


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = open('../API_KEY.txt', 'r').read()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def run(options):
    if options.barry != -1:
        barry(options)

    elif options.related != -1:
        find_related(options)

    else:
        youtube_search(options)

def find_related(options):
    search_response = youtube.search().list(
        part="id,snippet",
        maxResults=options.max_results,
        type="video",
        relatedToVideoId=options.related
    ).execute()
    recommendations = handle_response(search_response)
    print "Related:\n", "\n".join(recommendations), "\n"


def youtube_search(options):
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()
    videos = handle_response(search_response)
    print "Videos:\n", "\n".join(videos), "\n"


def handle_response(search_response):
    videos = dict()
    recommendations = dict()

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos[search_result["snippet"]["title"]] = search_result["id"]["videoId"]
        # elif search_result["id"]["kind"] == "youtube#channel":
        #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
        #                                  search_result["id"]["channelId"]))
        # elif search_result["id"]["kind"] == "youtube#playlist":
        #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
        #                                   search_result["id"]["playlistId"]))
        elif search_result["id"]["kind"] == "youtube#recommendation":
            recommendations[search_result["snippet"]["title"]] = search_result["id"]["videoId"]

    return videos, recommendations

# def handle_response(search_response):
#     videos = []
#     channels = []
#     playlists = []
#     recommendations = []
#
#     # Add each result to the appropriate list, and then display the lists of
#     # matching videos, channels, and playlists.
#     for search_result in search_response.get("items", []):
#         if search_result["id"]["kind"] == "youtube#video":
#             videos.append("%s (%s)" % (search_result["snippet"]["title"],
#                                        search_result["id"]["videoId"]))
#         elif search_result["id"]["kind"] == "youtube#channel":
#             channels.append("%s (%s)" % (search_result["snippet"]["title"],
#                                          search_result["id"]["channelId"]))
#         elif search_result["id"]["kind"] == "youtube#playlist":
#             playlists.append("%s (%s)" % (search_result["snippet"]["title"],
#                                           search_result["id"]["playlistId"]))
#         elif search_result["id"]["kind"] == "youtube#recommendation":
#             recommendations.append("%s (%s)" % (search_result["snippet"]["title"],
#                                                 search_result["id"]["videoId"]))
#
#     print "Videos:\n", "\n".join(videos), "\n"
#     print "Channels:\n", "\n".join(channels), "\n"
#     print "Playlists:\n", "\n".join(playlists), "\n"
#     print "Recommendations:\n", "\n".join(recommendations), "\n"


# Barry chooses a random video from the recommendations of a random video of the recommendations of another video etc... repeats until Barry found 100 videos.

def barry(options):
    videos_seen = []

    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()
    res = handle_response(search_response)
    videos = res[0]

    video_id = str(videos.get(videos.keys()[0]))
    videos_seen.append(video_id)
    print "Video chosen: ", videos.keys()[0]

    for i in range(100):

        search_response = youtube.search().list(
            part="id,snippet",
            maxResults=options.max_results,
            type="video",
            relatedToVideoId=video_id
        ).execute()
        res = handle_response(search_response)
        recommendations = res[0]

        next = rand.randint(0, len(recommendations) - 1)
        video_id = str(recommendations.get(recommendations.keys()[next]))
        print recommendations.keys()[next]

        while video_id in videos_seen:
            other = rand.randint(0, len(recommendations) - 1)
            video_id = str(recommendations.get(recommendations.keys()[other]))
            print "Other: ", recommendations.keys()[other]

        videos_seen.append(video_id)


    print videos_seen


    #
    # search_response = youtube.search().list(
    #     part="id,snippet",
    #     maxResults=options.max_results,
    #     type="video",
    #     relatedToVideoId=options.related
    # ).execute()
    # videos, recommendations = handle_response(search_response)
    # print "Related:\n", "\n".join(recommendations), "\n"






if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="vrouwkes")
    argparser.add_argument("--max-results", help="Max results", default=25)
    argparser.add_argument("--related", help="Related video's to this video ID",default=-1)
    argparser.add_argument("--barry", help="Search video from query and find" +
                                           " 100 recommendations of its recommendations zegmaar", default=-1)
    args = argparser.parse_args()

try:
    run(args)
except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

