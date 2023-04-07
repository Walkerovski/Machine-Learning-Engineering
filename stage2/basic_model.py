import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

# normalize to space [0, 1]
normalize_dic = {
    "popularity" : 100,
    "duration_ms" : 1e6,
    "explicit" : 1,
    "release_date" : 100,
    "danceability" : 1,
    "energy" : 1,
    "key" : 12,
    "loudness" : 50,
    "speechiness" : 1,
    "acousticness" : 1,
    "instrumentalness" : 1,
    "liveness" : 1,
    "valence" : 1,
    "tempo" : 250
}

# wages of values
key_dict = {
    "popularity": 3,
    "duration_ms": 0.2,
    "explicit": 0.2,
    "release_date": 0.2,
    "danceability": 0.7,
    "energy": 0.7,
    "key": 0.4,
    "loudness": 0.6,
    "speechiness": 1.4,
    "acousticness": 0.7,
    "instrumentalness": 0.5,
    "liveness": 0.6,
    "valence": 0.7,
    "tempo": 0.7
}

def open_file(track_to_file): # './data/tracks.jsonl
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

def create_data(data):
    """
    preprocess data to algorithm
    """
    df = np.empty((0, 17))
    for line in data:
        newrow = []
        for value in line.values():
            newrow.append(value)
        df = np.vstack([df, newrow])
    df = np.delete(df, 0, axis=1)
    df = np.delete(df, 0, axis=1)
    df = np.delete(df, 3, axis=1)
    for date in range(len(df)):
        df[date][3] = int(df[date][3][:4])
    return df.astype(float)

def normalize_data():
    """
    create list to normalize data
    """
    normalizer = []
    for col in normalize_dic.values():
        normalizer.append(col)
    return normalizer

def create_wages():
    """
    create list to apply wages to data
    """
    wage = []
    for col in key_dict.values():
        wage.append(col)
    return wage

def k_means(k, df, normalizer, wage): # k = 100
    """
    solve data with KMEANS algorithm
    """
    df = df / normalizer * wage
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(df)
    np.savetxt("./results/songs_in_groups.txt", kmeans.labels_)
    return kmeans.cluster_centers_

def k_neighbours(k, cluster_centers): # k = 30
    """
    solve data with KNEIGHBOURS algorithm
    """
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(cluster_centers)
    _, indicates = knn.kneighbors(cluster_centers)
    np.savetxt("./results/groups_similarity.txt", indicates)


def main():
    data = open_file('./uploads/tracks.jsonl')
    df = create_data(data)
    normalizer = normalize_data()
    wage = create_wages()

    clusters = k_means(100, df, normalizer, wage)
    k_neighbours(30, clusters)