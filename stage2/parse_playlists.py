import numpy as np
import json

dict_tracks_artists = {}
dict_tracks_names = {}
dict_artists_name = {}

def open_file(track_to_file): # './data/tracks.jsonl' './data/artists.jsonl'
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

def create_dics(tracks, artists):
    """
    create dics with tracks name and artists name
    """
    id = 0.0
    for track in tracks:
        dict_tracks_artists[id] = track["id_artist"]
        dict_tracks_names[id] = track["name"]
        id += 1

    for artist in artists:
        dict_artists_name[artist["id"]] = artist["name"]

def create_playlist(playlists_ids):
    """
    create list with merged artist and track name
    """
    playlists = []  # Create an empty list to store the playlists

    for playlist in playlists_ids:
        # print(playlist)
        playlists.append([dict_tracks_names[playlist], dict_artists_name[dict_tracks_artists[playlist]]])

    return playlists

def save_file(track, data, playlists): # ./results/playlists.txt
    """
    save list to file
    """
    with open(f'{track}', "w") as file:
        counter = 0
        file.write(f'Title; \t Artist\n')
        for playlist in playlists:
            if counter % data[1] == 0:
                file.write(f'\n\nPlaylist {int(counter / data[1] + 1)}: \n')
            for i in range(0, len(playlist), 2):
                file.write(playlist[i] + ";\t" + playlist[i+1])
            file.write("\n")
            counter += 1

def read_config():
    with open('./uploads/config.txt', 'r') as file:
        data = []
        while True:
            line = file.readline()
            if not line:
                break
            a = int(json.loads(line))
            data.append(a)
    return data

def main():
    tracks = open_file('./data/tracks.jsonl')
    artists = open_file('./data/artists.jsonl')
    create_dics(tracks, artists)
    playlists_ids = np.loadtxt('./results/playlists_ids.txt')
    playlists = create_playlist(playlists_ids)
    data = read_config()
    save_file('./results/playlists.txt', data, playlists)