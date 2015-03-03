import csv
import requests
from bs4 import BeautifulSoup
from soupselect import select

import sys

schedule = open("schedule", 'r')
soup = BeautifulSoup(schedule.read())
days = ["Wednesday", "Thursday", "Friday"]

with open("data/sessions.csv", 'w') as sessions_file:
    writer = csv.writer(sessions_file, delimiter=',')
    writer.writerow(["day", "time",
                     "talkTitle", "talkHref",
                     "speaker", "speakerHref",
                     "trackTitle", "trackHref",
                     "host", "hostHref",
                     "type", "room"])

    count = 0
    for day_number, day in enumerate(select(soup, "table.schedule-full")):
        # if count > 0:
        #     sys.exit()
        day_of_week = days[day_number]
        tracks = [{}, {}, {}, {}, {}, {}, {}]
        locations = ["", "", "", "", "", "", ""]

        rows = select(day, "tr")
        for row in rows:
            if "keynote-row" in row['class']:
                title = select(row, "a.keynote-title")[0].text
                title_href = select(row, "a.keynote-title")[0].get('href')
                speaker = select(row, "a.keynote-speaker")[0].text
                speaker_href = select(row, "a.keynote-speaker")[0].get("href")
                time =  select(row, "td.time")[0].text

                room_container = select(row, "td.keynote")[0]
                [x.extract() for x in select(room_container, "span")]
                [x.extract() for x in select(room_container, "a")]
                [x.extract() for x in select(room_container, "br")]
                [x.extract() for x in select(room_container, "img")]

                room = "".join([y.strip() for y in list(room_container.children)]).replace("by", "")
                speaker = " ".join([part for part in speaker.split(" ") if part])
                row = [word.strip().encode("utf-8") for word in [day_of_week, time, title, title_href, speaker, speaker_href, "", "", "", "", "keynote", room]]

                writer.writerow(row)
                continue

            if "track-th" in row['class']:
                for column, track in enumerate(select(row, "td.track")):
                    title = select(track, "a.track-title")
                    host = select(track, "a.track-host")
                    if title and host:
                        tracks[column] = {"title": title[0].text,
                                          "title_href": title[0].get("href"),
                                          "host": host[0].text,
                                          "host_href": host[0].get("href")}
                continue

            if "track-location-th" in row['class']:
                for column, location in enumerate(select(row, "td")):
                    potential_room = select(location, "span.track-location")
                    if potential_room:
                        room = potential_room[0].text
                        print column, room
                        locations[column-1] = room
                continue

            if "presentations-row" in row['class']:
                time =  select(row, "td.time")[0].text
                for column, talk in enumerate(select(row, "td.presentation")):
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

                    track_info = tracks[column]

                    row = [word.strip().encode("utf-8")
                           for word in
                           [day_of_week,time,
                            title, title_href,
                            speaker, speaker_href,
                            track_info['title'], track_info['title_href'],
                            track_info['host'], track_info['host_href'],
                            "presentation", locations[column]]]
                    writer.writerow(row)

        count +=1
