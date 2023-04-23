from config import client_id, client_secret, username, redirect_uri, playlist_id
from image_to_text import image_to_text
from progress_bar import progress_bar

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


def main():
    # Shows the top tracks for a user

    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    # print(token)
    if token:
        print("\nAuthenticated :)\n")
        sp = spotipy.Spotify(auth=token)
    else:
        print("\nCouldn't authenticate !!")
        return

    tracks_artists = image_to_text()
    uris = get_track_uris(sp, tracks_artists)
    add_tracks(sp, uris)


def get_track_uris(sp, tracks_artists):
    uris = []
    total = len(tracks_artists)
    print("\nGetting track uris from spotify api")
    for progress, (track, artist) in enumerate(tracks_artists.items()):
        response = sp.search(q=f"track: {track}", type="track")
        uri = response["tracks"]["items"][0]["uri"]
        uris.append(uri)
        progress_bar(progress + 1, total)
    print("\nCompleted getting uris")
    return uris


def add_tracks(sp, uris):
    total = len(uris)
    print("\nAdding tracks to playlist")
    for progress, uri in enumerate(uris):
        try:
            sp.user_playlist_add_tracks(username, playlist_id, [uri], position=None)
        except Exception:
            print("Can't add a song")
            continue

        progress_bar(progress + 1, total)
    print("\nCompleted adding tracks")


if __name__ == "__main__":
    main()
