from flask import Flask, redirect, request, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rfid_handler import get_song_uri
from dotenv import load_dotenv
import os
import socket



load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'Spotify-Auth-Session'

# Spotify app credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

def get_local_ip():
    """Get the local IP address of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't matter if it's not reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# Automatically find the local IP address
local_ip = get_local_ip()
SPOTIPY_REDIRECT_URI = f'http://{local_ip}:8080/callback'

# Spotify scope
SCOPE = 'user-read-playback-state,user-modify-playback-state'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)

    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def token_required(f):
    def decorated_function(*args, **kwargs):
        token_info = session.get('token_info', None)
        if not token_info:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/play', methods=['POST'])
@token_required
def play():
    rfid_code = request.form.get('rfid')
    song_uri = get_song_uri(rfid_code)

    if not song_uri:
        return "RFID code not recognized", 400

    token_info = session.get('token_info')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.start_playback(uris=[song_uri])
    return f'Playing song with URI: {song_uri}'

@app.route('/rfid', methods=['POST'])
@token_required
def rfid():
    rfid_code = request.form.get('rfid')
    return play_song_from_rfid(rfid_code)

def play_song_from_rfid(rfid_code):
    song_uri = get_song_uri(rfid_code)

    if not song_uri:
        return "RFID code not recognized", 400

    token_info = session.get('token_info')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.start_playback(uris=[song_uri])
    return f'Playing song with URI: {song_uri}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
