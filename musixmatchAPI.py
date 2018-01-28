import requests

def getAPIkey():
    return 'c29c3abf374df843346ed1bccb20f2ec'

"""
HOW TO MAKE THIS FUNCTION?
by Hanifa Arrumaisha (25/01/2017)

*   URL didapet dari link https://playground.musixmatch.com/
*   pilih API yang pengen diambil
*   klik expand operations dari API yg mau dipake
*   value dari URL adalah value yang ada di request URL di kotak warna biru tapi cuma sampe sebelum tanda tanya, 
    misal, aslinya request URL nya isinya 
    https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=jsonp&callback=callback&q_track=jatuh%20hati&q_artist=raisa&apikey=c29c3abf374df843346ed1bccb20f2ec
    tapi yang kita pake cuma sampe sebelum tanda tanya, berarti yang diambil
    https://api.musixmatch.com/ws/1.1/matcher.lyrics.get
*   PARAMS ikutin yang diminta di expand operations, ada list parameter apa aja yg harus dikirim
*   SELALU SERTAKAN APIKEY DI PARAMETER MESKIPUN TIDAK TERDAPAT DI EXPAND OPERATIONS
*   terakhir, tinggal gunain function ini di index.py yaaa tapi aku belum nyoba
"""

def getLyricsWithArtist(artist):
    URL = 'https://api.musixmatch.com/ws/1.1/track.search' 
    PARAMS = {
        'apikey': getAPIkey(),
        'format':'json',
        'callback':'callback',
        'q_artist':artist
    }

    r = requests.get(url = URL, params=PARAMS)

    data = r.json()
    return data

def getLyricsWithTrackArtist(track,artist):
    URL = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get' 
    PARAMS = {
        'apikey': getAPIkey(),
        'format':'json',
        'callback':'callback',
        'q_track':track,
        'q_artist':artist
    }

    r = requests.get(url = URL, params=PARAMS)

    data = r.json()
    print(data)

# kalau mau coba
# getLyricsWithTrackArtist('jatuh hati','raisa')