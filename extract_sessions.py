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
