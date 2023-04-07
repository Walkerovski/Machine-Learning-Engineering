import json
import numpy as np
from datetime import datetime

tracks_stats = {

}
    
tracks_time = {

}
    
def open_file(track_to_file): # './data/sessions.jsonl' './data/tracks.jsonl'
    """
    open file and save it to list
    """
    with open(f'{track_to_file}', 'r') as file:
        data = []
        while True:
            line = file.readline()
            if not line:
                break
            a = json.loads(line)
            data.append(a)
    return data

def create_dics(tracks):
    """
    create dics to save stats
    """
    for line in tracks:
        tracks_time[line["id"]] = line["duration_ms"]
        tracks_stats[line["id"]]= {'like': 0, 'skip': 0, 'play' : 0, 'time': 0}


def add_time_to_dic(data):
    """
    calculate time of listening songs
    """
    prev_line = {}
    for line in data:
        if prev_line == {}:
            prev_line = line
        if line["event_type"] == "play" or line["event_type"] == "skip" or line["event_type"] == "like":
            tracks_stats[line["track_id"]][line["event_type"]] += 1
            actual = datetime.fromisoformat(line["timestamp"]).timestamp()
            if prev_line["track_id"] == line["track_id"] and line["event_type"] == "skip" and prev_line["session_id"]== line["session_id"]:
                duration = actual - datetime.fromisoformat(prev_line["timestamp"]).timestamp()
                tracks_stats[line["track_id"]]["time"] += duration
            elif prev_line["session_id"] != line["session_id"] and prev_line["event_type"] == "play":
                duration = tracks_time[line["track_id"]]
                tracks_stats[line["track_id"]]["time"] += (duration / 1000)
            prev_line = line


def create_final_song_stats():
    """
    calculate average listening time and prepare stats to save
    """
    songs_stats = np.empty((0, 3))
    for song_id, song in tracks_stats.items():
        avg_time = 0
        if song["play"] != 0:
            avg_time = (song["time"] * 1000) / (song["play"] * float(tracks_time[song_id]))
        data = np.array((song["play"], song["like"], avg_time))
        songs_stats = np.vstack((songs_stats, data))
    return songs_stats


def main():
    data = open_file('./uploads/sessions.jsonl')
    tracks = open_file('./uploads/tracks.jsonl')
    create_dics(tracks)
    add_time_to_dic(data)
    songs_stats = create_final_song_stats()
    decimal_formatter = dict(float=lambda x: format(x, '.10f'))
    np.savetxt("./results/songs_stats.txt", songs_stats)
