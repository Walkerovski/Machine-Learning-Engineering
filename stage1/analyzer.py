import json


### ARTISTS

# Otwarcie pliku do odczytu.
plik_odczyt = open('data/artists.jsonl', 'r')
# Odczyt zawartości pliku
dic = {

}

while True:
    caly_tekst = plik_odczyt.readline()
    if not caly_tekst:
        break
    a = json.loads(caly_tekst)
    if a["id"] in dic:
        dic[a["id"]] += 1
    else:
        dic[a["id"]] = 1

    for _ in a:
        if a[_] == "null":
            print("Error")

for _ in dic:
    if dic[_] > 1:
        print(_) 
plik_odczyt.close()

print("ARTISTS OK\n")


### SESSIONS
# Otwarcie pliku do odczytu.
plik_odczyt = open('data/sessions.jsonl', 'r')
# Odczyt zawartości pliku
dic = {

}

while True:
    caly_tekst = plik_odczyt.readline()
    if not caly_tekst:
        break
    a = json.loads(caly_tekst)
    for _ in a:
        if a[_] == None and "advertisment" != a["event_type"]:
            print("Error")

plik_odczyt.close()

print("SESSIONS OK\n")

### TRACKS
# Otwarcie pliku do odczytu.
plik_odczyt = open('data/tracks.jsonl', 'r')
# Odczyt zawartości pliku
dic = {

}

while True:
    caly_tekst = plik_odczyt.readline()
    if not caly_tekst:
        break
    a = json.loads(caly_tekst)
    if a["id"] in dic:
        dic[a["id"]] += 1
    else:
        dic[a["id"]] = 1

    for _ in a:
        if a[_] == "null":
            print("Error")

for _ in dic:
    if dic[_] > 1:
        print(_) 
plik_odczyt.close()

print("TRACKS OK\n")

### USERS
plik_odczyt = open('data/users.jsonl', 'r')
dic = {

}

while True:
    caly_tekst = plik_odczyt.readline()
    if not caly_tekst:
        break
    a = json.loads(caly_tekst)
    if a["user_id"] in dic:
        dic[a["user_id"]] += 1
    else:
        dic[a["user_id"]] = 1

    for _ in a:
        if a[_] == "null":
            print("Error")
            
for _ in dic:
    if dic[_] > 1:
        print(_) 
plik_odczyt.close()

print("USERS OK\n")