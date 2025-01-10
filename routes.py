from flask import render_template, request, redirect, flash
from forms import *
import os, requests
from configs import *
from models import *
from flask_login import current_user, login_user, logout_user


# artists = [
#     {"name": "Kendrick Lamar", "img": "ken.jpeg", "streams": '28,696,564 streams', "id": "2YZyLoL8N0Wb9xBt1NhZWg"},
#     {"name": "Taylor Swift", "img": "tay.jpeg", "streams": '26,920,804 streams', "id": 1},
#     {"name": "Tyler, The Creator", "img": "tyl.jpeg", "streams": '16,396,728 streams', "id": "4V8LLVI7PbaPR0K2TGSxFF"},
#     {"name": "Travis Scott", "img": "trav.jpeg", "streams": '14,195,759 streams', "id": 3},
#     {"name": "Kanye West", "img": "kan.jpeg", "streams": '13,450,622 streams', "id": 4}]
# albums = [{"image": "TPAB.png", "name": 'To Pimp A Butterfly'},
#           {"image": "TPAB.png", "name": "ammamamma"}]


@app.route('/')
def index():
    return render_template('about.html')


# @app.route('/artists')
# def artistlist():
#     token = get_spotify_token()
#     headers = {"Authorization": f"Bearer {token}"}
#
#     artists_url = 'https://api.spotify.com/v1/artists'
#     artists_response = requests.get(artists_url, headers=headers)
#     artists_data = artists_response.json()
#     print(artists_data)
#     artist_details = [
#         {"id": artist["id"], "name": artist["name"], "popularity": artist["popularity"]}
#         for artist in artists_data["artists"]
#     ]
#     return render_template('artists.html', artists=artist_details)

@app.route('/artists')
def artistlist():
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    playlist_id = "37i9dQZF1DX9lzz0FRAxgl"
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    playlist_response = requests.get(playlist_url, headers=headers)
    playlist_data = playlist_response.json()["item"]
    playlist_artists = [
        {"id": artist["id"], "name": artist["name"]}
        for artist in playlist_data["artists"]
    ]

    # if playlist_response.status_code == 200:
    #     playlist_data = playlist_response.json()
    #
    #     # Extract the artist IDs from the playlist
    #     artist_ids = []
    #     for item in playlist_data['items']:
    #         for artist in item['track']['artists']:
    #             artist_ids.append(artist['id'])
    #
    #     # Deduplicate the artist IDs (to avoid fetching the same artist multiple times)
    #     artist_ids = list(set(artist_ids))
    #
    #     # Now, fetch the details for each artist using the /v1/artists/{id} endpoint
    #     artists_url = f'https://api.spotify.com/v1/artists?ids={",".join(artist_ids)}'
    #     artists_response = requests.get(artists_url, headers=headers)
    #
    #     if artists_response.status_code == 200:
    #         artists_data = artists_response.json()
    #
    #         # Extract the artist details (id, name, popularity)
    #         artist_details = [
    #             {"id": artist["id"], "name": artist["name"], "popularity": artist["popularity"]}
    #             for artist in artists_data["artists"]
    #         ]
    #     else:
    #         artist_details = []
    #         print(f"Error fetching artist details: {artists_response.status_code}")
    #         print(artists_response.text)
    # else:
    #     artist_details = []
    #     print(f"Error fetching playlist tracks: {playlist_response.status_code}")
    #     print(playlist_response.text)

    return render_template('artists.html', artists=playlist_artists)


@app.route('/about')
def about():
    return render_template('about.html')


# @app.route("/add", methods=["GET", "POST"])
# def addproduct():
#     form = AddAlbumForm()
#     if request.method == "POST":
#         print('dada')
#         image = request.files['image']
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
#         name = form.name.data
#         album = {"image": image.filename, "name": name}
#         albums.append(album)
#         return redirect("/artists")
#     return render_template('add_album.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registered')
        return redirect("/login")
    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('logged in')
            return redirect("/")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("logged out")
    return redirect("/")


def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET), data=data)
    print(response.json()["access_token"])
    return response.json()["access_token"]


@app.route("/artist/<artist_id>")
def artist_page(artist_id):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    albums_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    albums_response = requests.get(albums_url, headers=headers)
    albums_data = albums_response.json()["items"]
    albums = albums_data[:8]

    top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    top_tracks_response = requests.get(top_tracks_url, headers=headers)
    top_tracks_data = top_tracks_response.json()["tracks"]
    top_tracks = top_tracks_data[:5]

    artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    artist_response = requests.get(artist_url, headers=headers)
    artist_data = artist_response.json()
    artist_name = artist_data["name"]

    # traks_in_album_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    # traks_in_album_response = requests.get(traks_in_album_url, headers=headers)
    # traks_in_album = traks_in_album_response.json()

    return render_template("artist.html", albums=albums, tracks=top_tracks, name=artist_name)


@app.route("/check_login")
def album_redirect():
    if current_user.is_authenticated:
        print("ok ok")
        return redirect("/album/<album_id>")
    else:
        print("not not")
        return redirect("/album_register")


@app.route("/album_register", methods=["GET", "POST"])
def album_register():
    form = AlbumRegisterForm()
    if request.method == "POST":
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registered')
        return redirect("/login")
    return render_template('album_register.html', form=form)


@app.route("/album_login", methods=["GET", "POST"])
def album_login():
    form = AlbumloginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('logged in')
            return redirect("/album/<album_id>")
    return render_template('album_login.html', form=form)


@app.route("/album/<album_id>")
def get_album_tracks(album_id):
    token = get_spotify_token()
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    album_url = f"https://api.spotify.com/v1/albums/{album_id}"
    album_response = requests.get(album_url, headers=headers)
    album_data = album_response.json()["images"]
    album_name = album_response.json()["name"]

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    tracks_data = response.json()["items"]
    tracks = [{"name": track["name"], "id": track["id"],
               "artists": ", ".join([artist["name"] for artist in track["artists"]])} for track in tracks_data]
    return render_template("album.html", tracks=tracks, album=album_data, album_name=album_name)
