RFID_SONG_MAP = {
    "1234567890": "spotify:track:3ZEno9fORwMA1HPecdLi0R",
    "0987654321": "spotify:track:0y1QJc3SJVPKJ1OvFmFqe6"
}

def get_song_uri(rfid_code):
    return RFID_SONG_MAP.get(rfid_code, None)
