import numpy as np
import json

def load_data(track1, track2, track3): # ./results/songs_stats.txt ./results/groups_similarity.txt ./results/songs_in_groups.txt
    """
    load data from previous calculation
    """
    songs_statistics = np.loadtxt(f'{track1}')
    groups_similarity = np.loadtxt(f'{track2}')
    songs_in_groups = np.loadtxt(f'{track3}')
    return songs_statistics, groups_similarity, songs_in_groups

def normalize_statistics(songs_statistics):
    """
    normalize values to space [0, 1]
    """
    min_vals = np.min(songs_statistics, axis=0)
    max_vals = np.max(songs_statistics, axis=0)
    return (songs_statistics - min_vals) / (max_vals - min_vals)

def apply_wages(songs_statistics):
    """
    apply wages to statistics
    """
    wage_vector = np.array((1, 2, 3))
    return np.sum(songs_statistics * wage_vector, axis=1)

def create_groups(songs_statistics, songs_in_groups):
    """
    create lists to easier works
    """
    songs_in_groups = np.column_stack((songs_in_groups, -songs_statistics))
    return np.column_stack((songs_in_groups, np.arange(len(songs_in_groups))))

def sort_groups(songs_in_groups):
    """
    sort by groups
    """
    sorted_indices = np.lexsort(songs_in_groups.T[::-1])
    return songs_in_groups[sorted_indices]

def create_dict(songs_in_groups):
    """
    create dict to group songs
    """
    dict_groups_songs = {}
    for song in songs_in_groups:
        if song[0] in dict_groups_songs:
            dict_groups_songs[song[0]].append(song[2])
        else:
            dict_groups_songs[song[0]] = [song[2]]
    return dict_groups_songs


def getSongFromAGroup(group_id, dict_groups_songs):
    """
    pick song from choosen group by normal distribution
    """
    group_size = len(dict_groups_songs[group_id]) - 1
    gauss_song_id = int(abs(np.random.normal(0, group_size/3)))
    song_id_in_group = min(gauss_song_id, group_size)
    return dict_groups_songs[group_id][song_id_in_group]


def create_playlists(number_of_playlist, playlist_size, dict_groups_songs, groups_similarity): # 30
    """
    create final playlists
    """
    playlists = np.array([])
    for _ in range(number_of_playlist):
        playlist = np.array([])
        random_group = np.random.choice(100)
        for _ in range(playlist_size):
            pick_gauss_neighbour = min(int(abs(np.random.normal(0, 15))), 29)
            #group from which we will pick a song
            song_id = getSongFromAGroup(groups_similarity[random_group][pick_gauss_neighbour], dict_groups_songs)
            playlist = np.append(playlist, np.array([song_id]))
        playlists = np.append(playlists, playlist)
    np.savetxt("./results/playlists_ids.txt", playlists)

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
    playlists_config = read_config()
    songs_statistics, groups_similarity, songs_in_groups = load_data('./results/songs_stats.txt', './results/groups_similarity.txt', './results/songs_in_groups.txt')
    songs_statistics = normalize_statistics(songs_statistics)
    songs_statistics = apply_wages(songs_statistics)
    songs_in_groups = create_groups(songs_statistics, songs_in_groups)
    songs_in_groups = sort_groups(songs_in_groups)
    dict_groups_songs = create_dict(songs_in_groups)
    create_playlists(playlists_config[0], playlists_config[1], dict_groups_songs, groups_similarity)