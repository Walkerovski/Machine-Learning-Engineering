import matplotlib.pyplot as plt
import json

file = open('./data/tracks.jsonl', 'r')
df = []

while True:
    line = file.readline()
    if not line:
        break
    a = json.loads(line)
    df.append(a)

for attribute in {"instrumentalness"}:#df[0].keys():
    data = []

    for track in df:
        data.append(track[f'{attribute}'])

    # duration_ms without "waves" songs
    # for _ in data:
    #     if _ < 0.2:
    #         data.remove(_)
    plt.figure(figsize=(15, 10))
    plt.hist(data, bins=100)
    plt.xlabel(attribute)
    plt.ylabel("Frequency")
    plt.title(f'Distribution of {attribute}')
    plt.xticks(rotation=90)
    plt.savefig(f'./plots/{attribute}')

    file.close()
