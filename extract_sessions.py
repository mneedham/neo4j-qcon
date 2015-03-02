import csv
import requests
from bs4 import BeautifulSoup
from soupselect import select

import time
import datetime

schedule = open("schedule", 'r')
soup = BeautifulSoup(schedule.read())

with open("data/sessions.csv", 'w') as sessions_file:
    writer = csv.writer(sessions_file, delimiter=',')
    writer.writerow(["time", "title", "titleHref", "speaker", "speakerHref", "type"])

    for day in select(soup, "table.schedule-full"):
        track_rows = select(day, "tr.track-th")
        for track_row in track_rows:
            for track in select(track_row, "td.track"):
                print track
                title = select(track, "a.track-title")
                host = select(track, "a.track-host")
                print title, host

    for day in select(soup, "table.schedule-full"):
        keynotes = select(day, "tr.keynote-row")
        for keynote in keynotes:
            title = select(keynote, "a.keynote-title")[0].text
            title_href = select(keynote, "a.keynote-title")[0].get('href')
            speaker = select(keynote, "a.keynote-speaker")[0].text
            speaker_href = select(keynote, "a.keynote-speaker")[0].get("href")
            time =  select(keynote, "td.time")[0].text

            speaker = " ".join([part for part in speaker.split(" ") if part])
            row = [word.strip().encode("utf-8") for word in [time, title, title_href, speaker, speaker_href, "keynote"]]
            writer.writerow(row)

        presentation_rows = select(day, "tr.presentations-row")
        for presentation_row in presentation_rows:
            time =  select(presentation_row, "td.time")[0].text
            for talk in select(presentation_row, "td.presentation"):
                title = select(talk, "a.presentation-title")[0].text
                title_href = select(talk, "a.presentation-title")[0].get('href')
                potential_speaker = select(talk, "a.presentation-speaker")
                if potential_speaker:
                    speaker = select(talk, "a.presentation-speaker")[0].text
                    speaker_href = select(talk, "a.presentation-speaker")[0].get("href")
                else:
                    [x.extract() for x in select(talk, "span")]
                    [x.extract() for x in select(talk, "a")]
                    [x.extract() for x in select(talk, "br")]
                    speaker = talk.text.strip()
                    speaker_href = ""

                speaker = " ".join([part for part in speaker.split(" ") if part])
                row = [word.strip().encode("utf-8") for word in [time, title, title_href, speaker, speaker_href, "presentation"]]
                writer.writerow(row)
                # print time, title, title_href, speaker, speaker_href

# with open('data/import/episodes.csv', 'w') as episodes:
#     writer = csv.writer(episodes, delimiter=',')
#     writer.writerow(["NumberOverall", "NumberInSeason", "Episode", "Season", "DateAired", "Timestamp"])
#
#     for row in select(soup, 'tr'):
#         link_to_episode = select(row.contents[3], "a")
#         if len(link_to_episode) > 0:
#             number_overall = row.contents[1].text.strip()
#             number_in_season = row.contents[2].text.strip()
#             episode = link_to_episode[0].get("href").replace('"', '').strip()
#
#             date_aired = row.contents[4].text.strip()
#             timestamp = int(time.mktime(datetime.datetime.strptime(date_aired, "%B %d, %Y").timetuple()))
#
#             if number_overall == "216":
#                 number_overall = "180"
#                 number_in_season = "20"
#
#             if int(number_overall) < 23:
#                 season = 1
#             elif int(number_overall) < 45:
#                 season = 2
#             elif int(number_overall) < 65:
#                 season = 3
#             elif int(number_overall) < 89:
#                 season = 4
#             elif int(number_overall) < 113:
#                 season = 5
#             elif int(number_overall) < 137:
#                 season = 6
#             elif int(number_overall) < 161:
#                 season = 7
#             elif int(number_overall) < 185:
#                 season = 8
#             else:
#                 season = 9
#
#             writer.writerow([number_overall, number_in_season, episode, season, date_aired, timestamp])
