from flask import Flask, render_template, request, redirect, Response
from stage2 import basic_model, listening_statistics, target_model, parse_playlists

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_artists():
    file = request.files['artists']  # Get the uploaded file
    file.save(f'uploads/artists.jsonl')  # Save the file to the desired location
    file = request.files['sessions']  # Get the uploaded file
    file.save(f'uploads/sessions.jsonl')  # Save the file to the desired location
    file = request.files['tracks']  # Get the uploaded file
    file.save(f'uploads/tracks.jsonl')  # Save the file to the desired location
    text = request.form['playlist_size']  # Get the uploaded file
    text += "\n"
    text += request.form['playlist_number']
    with open("./uploads/config.txt", "w") as file:
        file.write(text)  # Save the file to the desired location

    basic_model.main()
    listening_statistics.main()
    target_model.main()
    parse_playlists.main()
    with open("./results/playlists.txt", "r") as file:
        content = file.read()
    return render_template('playlist.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
